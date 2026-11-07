"""Tests for the clinic Meta webhook bridge. Run with: python test_webhook.py

No Meta credentials or network calls are needed: the send test uses
dry-run mode, and the parsing tests use sample Meta payloads.
"""

import os
import unittest

os.environ.setdefault("WHATSAPP_DRY_RUN", "1")
os.environ["BRIGHT_SMILE_PHONE_NUMBER_ID"] = "111111"
os.environ["GREEN_VALLEY_PHONE_NUMBER_ID"] = "222222"

from webhook_bridge import (  # noqa: E402
    answer_for_clinic,
    build_reply_payload,
    parse_incoming,
    resolve_clinic_id,
    send_reply,
    verify_challenge,
)

SAMPLE_PAYLOAD = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "metadata": {"phone_number_id": "222222"},
                        "messages": [
                            {
                                "from": "1234567890",
                                "type": "text",
                                "text": {"body": "What time do you open on Saturday?"},
                            },
                            {
                                "from": "1234567890",
                                "type": "image",
                                "image": {"id": "abc"},
                            },
                        ],
                    }
                }
            ]
        }
    ],
}


class TestClinicWebhookBridge(unittest.TestCase):
    def test_verify_challenge_ok(self):
        query = {
            "hub.mode": ["subscribe"],
            "hub.verify_token": ["secret-token"],
            "hub.challenge": ["12345"],
        }
        self.assertEqual(verify_challenge(query, "secret-token"), "12345")

    def test_verify_challenge_wrong_token(self):
        query = {
            "hub.mode": ["subscribe"],
            "hub.verify_token": ["wrong"],
            "hub.challenge": ["12345"],
        }
        self.assertIsNone(verify_challenge(query, "secret-token"))

    def test_parse_text_only_with_metadata(self):
        messages = parse_incoming(SAMPLE_PAYLOAD)
        # The image message is ignored; only the text message counts,
        # and its phone_number_id is carried for clinic routing.
        self.assertEqual(
            messages,
            [("1234567890", "What time do you open on Saturday?", "222222")],
        )

    def test_parse_malformed_payload(self):
        self.assertEqual(parse_incoming({}), [])
        self.assertEqual(parse_incoming({"entry": "not-a-list"}), [])

    def test_routing_by_phone_number_id(self):
        self.assertEqual(resolve_clinic_id("222222"), "green-valley")
        self.assertEqual(resolve_clinic_id("111111"), "bright-smile")
        self.assertEqual(resolve_clinic_id("999999"), "bright-smile")
        self.assertEqual(resolve_clinic_id(None), "bright-smile")

    def test_reply_payload_shape(self):
        payload = build_reply_payload("1234567890", "Hello")
        self.assertEqual(payload["messaging_product"], "whatsapp")
        self.assertEqual(payload["to"], "1234567890")
        self.assertEqual(payload["type"], "text")
        self.assertEqual(payload["text"]["body"], "Hello")

    def test_dry_run_send_does_not_call_meta(self):
        result = send_reply("1234567890", "Hello", dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["payload"]["to"], "1234567890")

    def test_live_faq_answer_via_bridge(self):
        # Same Saturday question, routed to Green Valley, must give
        # Green Valley's hours, not Bright Smile's.
        text = answer_for_clinic(
            "What time do you open on Saturday?", "green-valley"
        )
        self.assertIn("10:00–16:00", text)
        self.assertNotIn("9:00–14:00", text)

    def test_live_calendar_slots_via_bridge(self):
        text = answer_for_clinic(
            "What slots are available?", "bright-smile"
        )
        self.assertIn("BS1", text)
        self.assertNotIn("GV1", text)

    def test_live_not_found_via_bridge(self):
        text = answer_for_clinic("Do you offer home visits?", "bright-smile")
        self.assertIn("couldn't find", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
