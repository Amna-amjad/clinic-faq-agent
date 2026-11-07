# Meta test number setup — clinic FAQ agent

Goal: prove the clinic agent live on WhatsApp, on Meta's **free
test number**, before any real clinic or real number is involved.
No tokens are stored in this repo. Never paste a token into chat,
code, or a screenshot.

## What this bridge does — and does not do

Does:
- Receives a WhatsApp text message via Meta's webhook.
- Answers it from that clinic's own pages, naming the source.
- Shows only free calendar slots when asked "What slots are
  available?", for that clinic.
- Refuses medicine/diagnosis questions and passes them to staff.

Does NOT do (v1):
- Book a slot from a WhatsApp message. A patient message never
  creates a booking. Owner confirmation still happens in
  `run_booking.py` / the owner view (a later step).
- Send messages, take payment, or use a personal WhatsApp number.

## 1. What you need first

- A Meta developer account (free), at developers.facebook.com.
- This project on your computer, with Python 3.10+.
- ngrok (free) for exposing your local bridge while testing, or
  any always-on server you already have. The bridge itself is
  stdlib-only, no pip install needed.

## 2. Create the Meta test setup

1. In Meta for Developers, create an app (type: Other, or follow
   Meta's current WhatsApp setup flow) and add the **WhatsApp**
   product.
2. Open **WhatsApp > API Setup**. Meta gives you:
   - a **test phone number** (it looks like a US number, e.g.
     1 555 xxx xxxx — this is a test number, not a real clinic
     number),
   - a **Phone number ID** (long numeric id),
   - a **temporary access token** (valid about 24 hours).
3. In **Step 5: Add a recipient phone number**, add **your own
   personal WhatsApp number** and confirm the code Meta sends
   you by SMS/WhatsApp. The test number can only message numbers
   on this allowlist (up to 5). This is why you test with your
   own number first.

## 3. Run the bridge locally

Copy the example env file and fill in test values only:

```bash
cp .env.example .env
```

Edit `.env` (never commit it — it is in `.gitignore`):

```text
WHATSAPP_PHONE_NUMBER_ID=<the test Phone number ID from step 2>
WHATSAPP_ACCESS_TOKEN=<the temporary test token from step 2>
META_VERIFY_TOKEN=<choose any random string, e.g. clinic-test-2026>
BRIGHT_SMILE_PHONE_NUMBER_ID=<same as WHATSAPP_PHONE_NUMBER_ID, for routing>
PORT=8000
```

Start with **Bright Smile only**. That is the normal test: one
test number, one clinic. Green Valley routing is already in the
code for when a second test number exists, but you do not need
it to prove the live flow.

Run it:

```bash
python webhook_bridge.py
```

In a second terminal, expose it:

```bash
ngrok http 8000
```

ngrok gives you a public URL like `https://xxxx.ngrok-free.app`.
Keep both terminals running while you test. If ngrok restarts,
its URL changes and you must update Meta (step 4) again.

## 4. Tell Meta where your bridge is

In **WhatsApp > Configuration > Webhook**:

1. **Callback URL:** `<your ngrok URL>/webhook`
   (for example `https://xxxx.ngrok-free.app/webhook`)
2. **Verify token:** exactly the `META_VERIFY_TOKEN` you put in
   `.env` (for example `clinic-test-2026`).
3. Click **Verify and save**. Meta calls your bridge with a
   challenge; the bridge returns it only if the token matches,
   otherwise it answers 403.
4. Under **Webhook fields**, subscribe to **messages**.

If verification fails, check in order: the bridge is running,
ngrok is running, the callback URL ends in `/webhook`, and the
verify token matches `.env` exactly (no extra spaces).

## 5. Test it live

From your allowlisted personal number, send WhatsApp messages
**to the Meta test number** (not to your own number):

- "What time do you open on Saturday?"
  -> Bright Smile: 9:00–14:00, Source: Opening hours
- "How much does a checkup cost?"
  -> Rs 1,500, Source: Consultation fees and prices
- "What slots are available?"
  -> Free slots BS1–BS5, from the seeded calendar
- "What medicine should I take for tooth pain?"
  -> Refused as a medical answer, passed to clinic staff
- "Do you offer home visits?"
  -> "couldn't find that in Bright Smile's pages", human offered

Watch the bridge terminal: every incoming message and reply is
logged there, in dry-run style, even in live mode.

## 6. When the test token expires

The temporary token lasts about 24 hours. When replies stop,
go back to **WhatsApp > API Setup**, copy the new temporary
token into `.env`, restart the bridge, and test again. For a
longer-lived setup you later create a system user with a
permanent token — that is a production step, not a test step,
and it is not needed here.

## Troubleshooting

- **Meta cannot verify:** see step 4 checks above.
- **No reply arrives:** check the recipient number is on the
  allowlist (step 2.3), the bridge terminal shows the incoming
  message, and the token has not expired.
- **Wrong clinic answers:** check
  `BRIGHT_SMILE_PHONE_NUMBER_ID` in `.env` matches the test
  number's Phone number ID. Unmatched numbers default to
  Bright Smile by design, so they never answer from the wrong
  clinic silently — they answer as the default clinic.
- **Slots look old after restart:** the demo calendar is
  in-memory and re-seeds on restart. That is expected in the
  test bridge; production needs a database.

## Files

- `webhook_bridge.py` — the bridge (stdlib only).
- `test_webhook.py` — 10 tests, no Meta account needed.
- `.env.example` — placeholders only, copy to `.env`.
- `.gitignore` — keeps `.env` and `__pycache__` out of git.
