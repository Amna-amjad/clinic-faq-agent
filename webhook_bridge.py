"""Meta WhatsApp test webhook bridge for clinics — stdlib only.

This is the missing piece between WhatsApp and the clinic FAQ agent:

    WhatsApp message -> POST /webhook -> faq_agent.answer()
                     -> POST to Meta Graph API -> WhatsApp reply

It does NOT change the agent. The same answer() function that powers
the terminal demo powers WhatsApp replies, with the same rules:
answer only from the chosen clinic's own pages, name the source,
or say "not found" and offer a human. No diagnosis, no medicine
recommendation, ever.

Multi-clinic routing (v1, test mode):
  Meta's payload includes metadata.phone_number_id for the number
  that received the message. If that id matches
  BRIGHT_SMILE_PHONE_NUMBER_ID or GREEN_VALLEY_PHONE_NUMBER_ID,
  the answer comes from that clinic. Otherwise it defaults to
  Bright Smile. Start with ONE test number (Bright Smile) — that
  is the normal Meta test setup, and it is all you need to prove
  the live flow.

Calendar (v1, test mode):
  The bridge attaches a seeded, in-memory calendar, so a live
  question like "What slots are available?" shows only free slots
  for that clinic, automatically. Booking via WhatsApp is NOT in
  v1: a patient message does not create a booking. Booking still
  needs owner confirmation, via run_booking.py / the owner view
  (a later step). Do not promise live WhatsApp booking from this
  bridge.

Setup (see META_TEST_SETUP.md for the full walkthrough):
  1. Copy .env.example to .env in this same folder (next to
     webhook_bridge.py, NOT inside the faq_agent folder) and fill
     in your TEST values only. The bridge loads that .env file
     itself at startup, so you do not need to set variables by
     hand in the terminal. Never commit .env, and never paste a
     token into chat or code.
  2. Run:  python webhook_bridge.py
  3. Expose it publicly while testing, e.g. with ngrok:
         ngrok http 8000
  4. In Meta's WhatsApp Configuration, set the callback URL to
     <your-public-url>/webhook and the verify token to the same
     value as META_VERIFY_TOKEN, then subscribe to "messages".

Environment variables (all read at startup, none hard-coded):
  WHATSAPP_PHONE_NUMBER_ID  - long numeric ID from Meta API Setup
  WHATSAPP_ACCESS_TOKEN     - TEST token only (temporary, ~24h)
  META_VERIFY_TOKEN         - any random string you choose
  BRIGHT_SMILE_PHONE_NUMBER_ID - optional, for routing
  GREEN_VALLEY_PHONE_NUMBER_ID - optional, for routing
  PORT                      - default 8000
  WHATSAPP_DRY_RUN          - set to "1" to log replies instead of
                              calling Meta. Use this for local tests
                              with no Meta credentials at all.

Usage:
    python webhook_bridge.py
    python webhook_bridge.py --port 8000 --dry-run

Health check:  GET /  -> "ok"
Verification:  GET /webhook?hub.mode=subscribe
                   &hub.verify_token=<your token>
                   &hub.challenge=<challenge>
               -> returns the challenge, only if the token matches.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# Allow running from the repo root: faq_agent lives next to this file.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_dotenv() -> None:
    """Load a .env file next to this file into os.environ, if present.

    Stdlib only, no python-dotenv needed. Only sets variables that
    are not already set in the real environment, so a real terminal
    variable always wins over .env. Lines starting with # and blank
    lines are ignored; values may be quoted with " or '.
    The file must sit next to webhook_bridge.py, in the main
    project folder — NOT inside the faq_agent folder.
    """
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    try:
        with open(dotenv_path, encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except FileNotFoundError:
        pass


load_dotenv()

from faq_agent.agent import answer  # noqa: E402
from faq_agent.calendar import Calendar, seeded_calendar  # noqa: E402
from faq_agent.clinics import DEFAULT_CLINIC_ID  # noqa: E402

GRAPH_API_VERSION = "v23.0"

# One shared seeded calendar for the test bridge. In-memory, so it
# re-seeds on restart — fine for a test, not for production bookings.
CALENDAR = seeded_calendar()


def resolve_clinic_id(phone_number_id: str | None) -> str:
    """Map a Meta phone_number_id to a clinic id, or the default."""
    if phone_number_id:
        if phone_number_id == os.environ.get("BRIGHT_SMILE_PHONE_NUMBER_ID"):
            return "bright-smile"
        if phone_number_id == os.environ.get("GREEN_VALLEY_PHONE_NUMBER_ID"):
            return "green-valley"
    return DEFAULT_CLINIC_ID


def answer_for_clinic(text: str, clinic_id: str, calendar: Calendar | None = None) -> str:
    """Answer one message for one clinic, using its pages + calendar."""
    cal = calendar if calendar is not None else CALENDAR
    return answer(text, clinic=clinic_id, calendar=cal).text


def verify_challenge(query: dict, expected_token: str) -> str | None:
    """Return the hub.challenge if mode and token match, else None."""
    mode = query.get("hub.mode", [""])[0]
    token = query.get("hub.verify_token", [""])[0]
    challenge = query.get("hub.challenge", [""])[0]
    if mode == "subscribe" and token and token == expected_token and challenge:
        return challenge
    return None


def parse_incoming(payload: dict) -> list[tuple[str, str, str | None]]:
    """Extract (sender_number, text, phone_number_id) from a Meta payload.

    Only text messages are returned. Non-text messages (images, audio,
    stickers, ...) are ignored by design in v1. Malformed payloads
    return [] instead of raising, so the webhook can still answer
    Meta with 200.
    """
    found: list[tuple[str, str, str | None]] = []
    try:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                phone_number_id = (value.get("metadata", {}) or {}).get("phone_number_id")
                for message in value.get("messages", []):
                    if message.get("type") != "text":
                        continue
                    sender = message.get("from", "")
                    text = (message.get("text", {}) or {}).get("body", "")
                    if sender and text:
                        found.append((sender, text, phone_number_id))
    except (AttributeError, TypeError):
        return []
    return found


def build_reply_payload(to: str, body: str) -> dict:
    """Build the Meta Graph API payload for one text reply."""
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": body},
    }


def send_reply(
    to: str,
    body: str,
    dry_run: bool = False,
    phone_number_id: str | None = None,
) -> dict:
    """Send one WhatsApp reply via Meta, or log it in dry-run mode.

    In dry-run mode (or when credentials are missing), nothing is
    sent and the would-be payload is returned for inspection.
    """
    payload = build_reply_payload(to, body)
    send_from = phone_number_id or os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
    token = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
    if dry_run or not send_from or not token:
        print(f"[dry-run] Would send to {to}: {body!r}", flush=True)
        return {"dry_run": True, "payload": payload}

    url = (
        f"https://graph.facebook.com/{GRAPH_API_VERSION}/"
        f"{send_from}/messages"
    )
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"[error] Meta API {exc.code}: {detail}", file=sys.stderr)
        return {"error": exc.code, "detail": detail}
    except Exception as exc:  # network errors, timeouts
        print(f"[error] Could not reach Meta API: {exc}", file=sys.stderr)
        return {"error": str(exc)}


class WhatsAppHandler(BaseHTTPRequestHandler):
    dry_run = False

    def log_message(self, *args):  # keep logs readable, not noisy
        sys.stderr.write("%s - %s\n" % (self.address_string(), args[0] % args[1:]))

    def _send_text(self, status: int, body: str, content_type: str = "text/plain"):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802 - BaseHTTPRequestHandler naming
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_text(200, "ok")
            return
        if parsed.path == "/webhook":
            expected = os.environ.get("META_VERIFY_TOKEN", "")
            challenge = verify_challenge(parse_qs(parsed.query), expected)
            if challenge is not None:
                self._send_text(200, challenge)
            else:
                self._send_text(403, "verification failed")
            return
        self._send_text(404, "not found")

    def do_POST(self):  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/webhook":
            self._send_text(404, "not found")
            return
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            payload = {}
        # Always answer 200 for a webhook POST, even for a message
        # we cannot parse — Meta retries non-200 responses.
        for sender, text, phone_number_id in parse_incoming(payload):
            clinic_id = resolve_clinic_id(phone_number_id)
            reply_text = answer_for_clinic(text, clinic_id)
            print(f"[incoming] {sender} -> {clinic_id}: {text!r}", flush=True)
            print(f"[reply] {reply_text!r}", flush=True)
            send_reply(sender, reply_text, dry_run=self.dry_run,
                       phone_number_id=phone_number_id)
        self._send_text(200, "ok")


def main() -> None:
    parser = argparse.ArgumentParser(description="Meta WhatsApp test webhook bridge for clinics.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    parser.add_argument("--dry-run", action="store_true", help="Log replies instead of calling Meta")
    args = parser.parse_args()

    dry_run = args.dry_run or os.environ.get("WHATSAPP_DRY_RUN", "") == "1"
    WhatsAppHandler.dry_run = dry_run
    server = HTTPServer(("0.0.0.0", args.port), WhatsAppHandler)
    mode = "DRY-RUN (no Meta calls)" if dry_run else "LIVE (Meta Graph API)"
    print(f"Clinic WhatsApp webhook bridge listening on :{args.port} — {mode}")
    print("Health check: GET /  |  Webhook: /webhook")
    print("Default clinic: Bright Smile. Routing: metadata.phone_number_id -> clinic.")
    if not dry_run and not os.environ.get("WHATSAPP_ACCESS_TOKEN"):
        print("Warning: WHATSAPP_ACCESS_TOKEN is not set — replies will be dry-run logged.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    main()
