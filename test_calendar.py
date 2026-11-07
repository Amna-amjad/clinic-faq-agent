"""Calendar + owner-confirmation tests. Run with: python test_calendar.py

The rule under test: a slot is only booked when the owner confirms.
A patient request alone holds it (pending, not shown as free);
owner confirmation books it (gone from free slots for good, until
an owner cancellation frees it again).
"""

import unittest

from faq_agent.agent import answer
from faq_agent.calendar import seeded_calendar


class TestCalendar(unittest.TestCase):
    def test_seeded_slots_are_per_clinic(self):
        cal = seeded_calendar()
        bright = cal.available("bright-smile")
        green = cal.available("green-valley")
        self.assertEqual(len(bright), 5)
        self.assertEqual(len(green), 5)
        self.assertTrue(all(s.clinic_id == "bright-smile" for s in bright))
        self.assertTrue(all(s.clinic_id == "green-valley" for s in green))

    def test_agent_shows_only_free_slots_for_the_right_clinic(self):
        cal = seeded_calendar()
        bright = answer("What slots are available?", clinic="bright-smile", calendar=cal)
        green = answer("What slots are available?", clinic="green-valley", calendar=cal)
        self.assertEqual(bright.source_title, "Calendar")
        self.assertIn("BS1", bright.text)
        self.assertNotIn("GV1", bright.text)
        self.assertIn("GV1", green.text)
        self.assertNotIn("BS1", green.text)

    def test_agent_without_calendar_falls_back_to_faq(self):
        reply = answer("What slots are available?", clinic="bright-smile")
        self.assertEqual(reply.source_title, "Appointments")

    def test_request_holds_slot_so_it_is_not_shown_as_free(self):
        cal = seeded_calendar()
        slot_id = cal.available("bright-smile")[0].id
        booking = cal.request("bright-smile", slot_id, "Ali")
        self.assertEqual(booking.status, "pending")
        self.assertNotIn(slot_id, [s.id for s in cal.available("bright-smile")])

    def test_owner_confirm_books_slot_and_it_stays_gone(self):
        cal = seeded_calendar()
        slot_id = cal.available("bright-smile")[0].id
        booking = cal.request("bright-smile", slot_id, "Ali")
        confirmed = cal.confirm(booking.id)
        self.assertEqual(confirmed.status, "confirmed")
        self.assertNotIn(slot_id, [s.id for s in cal.available("bright-smile")])
        # A second patient cannot take the same slot.
        with self.assertRaises(ValueError):
            cal.request("bright-smile", slot_id, "Sara")

    def test_owner_reject_frees_slot_again(self):
        cal = seeded_calendar()
        slot_id = cal.available("bright-smile")[0].id
        booking = cal.request("bright-smile", slot_id, "Ali")
        cal.reject(booking.id)
        self.assertIn(slot_id, [s.id for s in cal.available("bright-smile")])

    def test_owner_cancel_frees_confirmed_slot(self):
        cal = seeded_calendar()
        slot_id = cal.available("bright-smile")[0].id
        booking = cal.request("bright-smile", slot_id, "Ali")
        cal.confirm(booking.id)
        cal.cancel(booking.id)
        self.assertIn(slot_id, [s.id for s in cal.available("bright-smile")])

    def test_requesting_a_pending_slot_fails(self):
        cal = seeded_calendar()
        slot_id = cal.available("bright-smile")[0].id
        cal.request("bright-smile", slot_id, "Ali")
        with self.assertRaises(ValueError):
            cal.request("bright-smile", slot_id, "Sara")

    def test_slot_from_another_clinic_cannot_be_booked(self):
        cal = seeded_calendar()
        green_slot = cal.available("green-valley")[0].id
        with self.assertRaises(ValueError):
            cal.request("bright-smile", green_slot, "Ali")

    def test_unknown_clinic_and_booking_fail_loudly(self):
        cal = seeded_calendar()
        with self.assertRaises(ValueError):
            cal.available("not-a-clinic")
        with self.assertRaises(ValueError):
            cal.confirm("B999")


if __name__ == "__main__":
    unittest.main(verbosity=2)
