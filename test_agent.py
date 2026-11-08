"""Tests for the clinic WhatsApp FAQ agent. Run with: python test_agent.py"""

import unittest

from faq_agent.agent import answer


class TestClinicFaqAgent(unittest.TestCase):
    def test_greeting(self):
        self.assertIn("Bright Smile", answer("Hi").text)

    def test_straightforward_hours(self):
        reply = answer("What time do you open on Saturday?")
        self.assertTrue(reply.found)
        self.assertIn("9:00", reply.text)
        self.assertEqual(reply.source_title, "Opening hours")

    def test_differently_worded_fee(self):
        reply = answer("How much does a checkup cost?")
        self.assertTrue(reply.found)
        self.assertIn("Rs 1,500", reply.text)
        self.assertEqual(reply.source_title, "Consultation fees and prices")

    def test_appointment(self):
        reply = answer("How do I book an appointment?")
        self.assertTrue(reply.found)
        self.assertEqual(reply.source_title, "Appointments")
        self.assertIn("4 hours", reply.text)

    def test_first_visit(self):
        reply = answer("What should I bring for my first visit?")
        self.assertTrue(reply.found)
        self.assertEqual(reply.source_title, "First visit")
        self.assertIn("15 minutes early", reply.text)

    def test_emergency_points_to_clinic(self):
        reply = answer("I have severe tooth pain and swelling, what should I do?")
        self.assertTrue(reply.found)
        self.assertEqual(reply.source_title, "Emergencies and aftercare")
        self.assertIn("contact the clinic right away", reply.text)

    def test_medical_advice_is_not_answered(self):
        reply = answer("What medicine should I take for tooth pain?")
        self.assertFalse(reply.found)
        self.assertIn("can't recommend medicine", reply.text)
        self.assertIn("clinic staff", reply.text)
        self.assertIsNone(reply.source_title)

    def test_fever_medicine_is_not_answered(self):
        # Regression test for the live-test bug found 8 Nov 2026:
        # "I have a fever, what medicine should I take?" was answered
        # from the First Visit page, because the old refusal rule
        # required a medicine word AND a pain word together, and
        # fever is not a pain word. It must refuse, like any
        # medicine question, and name no source page.
        reply = answer("I have a fever, what medicine should I take?")
        self.assertFalse(reply.found)
        self.assertIn("can't recommend medicine", reply.text)
        self.assertIn("clinic staff", reply.text)
        self.assertIsNone(reply.source_title)

    def test_fever_without_medicine_is_not_answered(self):
        # A symptom on its own is also a personal health question,
        # not a FAQ lookup — it must not fall through to page
        # matching (First Visit won on "what should I" before).
        reply = answer("I have a fever, what should I do?")
        self.assertFalse(reply.found)
        self.assertIn("can't recommend medicine", reply.text)
        self.assertIn("clinic staff", reply.text)
        self.assertIsNone(reply.source_title)

    def test_not_found_is_honest(self):
        reply = answer("Do you offer home visits?")
        self.assertFalse(reply.found)
        self.assertIn("couldn't find", reply.text)
        self.assertIsNone(reply.source_title)

    def test_answers_name_a_source(self):
        for question in (
            "What time do you open on Sunday?",
            "Where are you located?",
            "Do you offer teeth whitening?",
        ):
            reply = answer(question)
            self.assertTrue(reply.found, question)
            self.assertIn("Source:", reply.text, question)


if __name__ == "__main__":
    unittest.main(verbosity=2)
