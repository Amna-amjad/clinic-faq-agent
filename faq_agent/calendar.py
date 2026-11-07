"""Per-clinic calendar: the booking part of the clinic SaaS demo.

This is the owner's calendar, attached to the app — one calendar
per clinic, not one shared list. A slot has exactly one status:

  free     — shown to patients as available
  pending  — a patient asked for it, waiting for owner confirmation.
             It is held, so it is NOT shown as available to anyone else.
  booked   — the owner confirmed it. It never shows as available again
             unless the owner cancels it, which frees it again.

Flow, in order (owner confirmation is the step that updates the calendar):
  1. Patient asks what slots are available -> only free slots are shown.
  2. Patient picks a slot -> a pending booking is created, slot -> pending.
  3. Owner confirms -> booking confirmed, slot -> booked.
     Owner rejects  -> booking rejected, slot -> free again.
  4. Owner cancels a confirmed booking -> slot -> free again.

Nothing is auto-booked. A patient request alone never books a slot.
No LLM, no API key, standard library only. This demo calendar is
in-memory: restarting the demo re-seeds it. A production version
would store this in a database and, later, sync it with the owner's
Google Calendar — the statuses and the owner-confirmation rule
would stay exactly the same.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .clinics import get_clinic

FREE = "free"
PENDING = "pending"
BOOKED = "booked"


@dataclass
class Slot:
    id: str
    clinic_id: str
    date: str  # YYYY-MM-DD, fictional demo dates
    time: str  # HH:MM, 24-hour
    status: str = FREE
    patient_name: str | None = None

    def label(self) -> str:
        return f"{self.date} {self.time}"


@dataclass
class Booking:
    id: str
    clinic_id: str
    slot_id: str
    patient_name: str
    status: str = PENDING


@dataclass
class Calendar:
    slots: dict[str, Slot] = field(default_factory=dict)
    bookings: dict[str, Booking] = field(default_factory=dict)
    _next_booking: int = 1

    def add_slot(self, clinic_id: str, date: str, time: str) -> Slot:
        clinic = get_clinic(clinic_id)
        prefix = "BS" if clinic.id == "bright-smile" else "GV"
        slot_id = f"{prefix}{len([s for s in self.slots.values() if s.clinic_id == clinic.id]) + 1}"
        slot = Slot(id=slot_id, clinic_id=clinic.id, date=date, time=time)
        self.slots[slot.id] = slot
        return slot

    def available(self, clinic_id: str, date: str | None = None) -> list[Slot]:
        clinic = get_clinic(clinic_id)
        slots = [
            s for s in self.slots.values()
            if s.clinic_id == clinic.id and s.status == FREE
        ]
        if date is not None:
            slots = [s for s in slots if s.date == date]
        return sorted(slots, key=lambda s: (s.date, s.time))

    def available_text(self, clinic_id: str, date: str | None = None) -> str:
        clinic = get_clinic(clinic_id)
        slots = self.available(clinic.id, date=date)
        if not slots:
            return f"No free slots at {clinic.name}."
        lines = [f"Free slots at {clinic.name}:"]
        lines += [f"- {slot.id}: {slot.label()}" for slot in slots]
        return "\n".join(lines)

    def request(self, clinic_id: str, slot_id: str, patient_name: str) -> Booking:
        clinic = get_clinic(clinic_id)
        slot = self.slots.get(slot_id)
        if slot is None or slot.clinic_id != clinic.id:
            raise ValueError(f"Slot {slot_id!r} does not exist for {clinic.name}.")
        if slot.status != FREE:
            raise ValueError(
                f"Slot {slot.label()} at {clinic.name} is not free "
                f"(status: {slot.status})."
            )
        booking_id = f"B{self._next_booking}"
        self._next_booking += 1
        booking = Booking(
            id=booking_id, clinic_id=clinic.id, slot_id=slot.id,
            patient_name=patient_name.strip(),
        )
        self.bookings[booking.id] = booking
        slot.status = PENDING
        slot.patient_name = booking.patient_name
        return booking

    def confirm(self, booking_id: str) -> Booking:
        booking = self.bookings.get(booking_id)
        if booking is None:
            raise ValueError(f"Unknown booking: {booking_id!r}.")
        if booking.status != PENDING:
            raise ValueError(
                f"Booking {booking_id} cannot be confirmed (status: {booking.status})."
            )
        booking.status = "confirmed"
        self.slots[booking.slot_id].status = BOOKED
        return booking

    def reject(self, booking_id: str) -> Booking:
        booking = self.bookings.get(booking_id)
        if booking is None:
            raise ValueError(f"Unknown booking: {booking_id!r}.")
        if booking.status != PENDING:
            raise ValueError(
                f"Booking {booking_id} cannot be rejected (status: {booking.status})."
            )
        booking.status = "rejected"
        slot = self.slots[booking.slot_id]
        slot.status = FREE
        slot.patient_name = None
        return booking

    def cancel(self, booking_id: str) -> Booking:
        booking = self.bookings.get(booking_id)
        if booking is None:
            raise ValueError(f"Unknown booking: {booking_id!r}.")
        if booking.status != "confirmed":
            raise ValueError(
                f"Booking {booking_id} cannot be cancelled (status: {booking.status})."
            )
        booking.status = "cancelled"
        slot = self.slots[booking.slot_id]
        slot.status = FREE
        slot.patient_name = None
        return booking


def seeded_calendar() -> Calendar:
    """Fresh demo calendar with fictional slots for both clinics."""
    calendar = Calendar()
    # Bright Smile: Monday 2026-11-02 and Tuesday 2026-11-03
    for date, time in (
        ("2026-11-02", "09:00"), ("2026-11-02", "10:00"), ("2026-11-02", "11:00"),
        ("2026-11-03", "09:00"), ("2026-11-03", "10:00"),
    ):
        calendar.add_slot("bright-smile", date, time)
    # Green Valley: different times, so clinics stay distinct
    for date, time in (
        ("2026-11-02", "10:00"), ("2026-11-02", "11:00"), ("2026-11-02", "12:00"),
        ("2026-11-03", "10:00"), ("2026-11-03", "11:00"),
    ):
        calendar.add_slot("green-valley", date, time)
    return calendar
