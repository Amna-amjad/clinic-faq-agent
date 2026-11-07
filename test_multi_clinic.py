"""Multi-clinic tests. Run with: python test_multi_clinic.py

The point of these tests: one engine, two clinics, no cross-talk.
The same question must get each clinic's own correct answer, and
never the other clinic's answer.
"""

import unittest

from faq_agent.agent import answer
from faq_agent.clinics import CLINICS, get_clinic, list_clinics


class TestMultiClinic(unittest.TestCase):
    def test_two_clinics_registered(self):
        self.assertEqual(len(list_clinics()), 2)
        self.assertIn("bright-smile", CLINICS)
        self.assertIn("green-valley", CLINICS)

    def test_default_is_still_bright_smile(self):
        reply = answer("What time do you open on Saturday?")
        self.assertIn("9:00–14:00", reply.text)
        reply_by_name = answer("Hi", clinic="Bright Smile Dental Clinic")
        self.assertIn("Bright Smile", reply_by_name.text)

    def test_same_hours_question_different_answers(self):
        bright = answer("What time do you open on Saturday?", clinic="bright-smile")
        green = answer("What time do you open on Saturday?", clinic="green-valley")
        self.assertIn("9:00–14:00", bright.text)
        self.assertNotIn("10:00–16:00", bright.text)
        self.assertIn("10:00–16:00", green.text)
        self.assertNotIn("9:00–14:00", green.text)

    def test_same_fee_question_different_answers(self):
        bright = answer("How much does a checkup cost?", clinic="bright-smile")
        green = answer("How much does a checkup cost?", clinic="green-valley")
        self.assertIn("Rs 1,500", bright.text)
        self.assertNotIn("Rs 2,000", bright.text)
        self.assertIn("Rs 2,000", green.text)
        self.assertNotIn("Rs 1,500", green.text)

    def test_same_appointment_question_different_rules(self):
        bright = answer("How do I book an appointment?", clinic="bright-smile")
        green = answer("How do I book an appointment?", clinic="green-valley")
        self.assertIn("4 hours", bright.text)
        self.assertIn("24 hours", green.text)

    def test_greeting_names_the_right_clinic(self):
        self.assertIn("Green Valley", answer("Hi", clinic="green-valley").text)
        self.assertIn("Bright Smile", answer("Hi", clinic="bright-smile").text)

    def test_not_found_names_the_right_clinic(self):
        reply = answer("Do you offer home visits?", clinic="green-valley")
        self.assertFalse(reply.found)
        self.assertIn("Green Valley", reply.text)

    def test_medical_guard_works_for_both_clinics(self):
        for clinic_id in ("bright-smile", "green-valley"):
            reply = answer("What medicine should I take for tooth pain?", clinic=clinic_id)
            self.assertFalse(reply.found)
            self.assertIn("can't recommend medicine", reply.text)

    def test_unknown_clinic_is_never_answered(self):
        with self.assertRaises(ValueError):
            answer("What time do you open?", clinic="not-a-clinic")
        with self.assertRaises(ValueError):
            get_clinic("not-a-clinic")


if __name__ == "__main__":
    unittest.main(verbosity=2)
