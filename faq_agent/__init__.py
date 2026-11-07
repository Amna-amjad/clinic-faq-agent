"""Clinic WhatsApp FAQ Agent — multi-clinic + calendar, simulated WhatsApp chat, no API key needed."""

from .agent import Answer, answer
from .calendar import BOOKED, FREE, PENDING, Booking, Calendar, Slot, seeded_calendar
from .clinics import CLINICS, Clinic, get_clinic, list_clinics

__all__ = [
    "Answer", "answer",
    "CLINICS", "Clinic", "get_clinic", "list_clinics",
    "BOOKED", "FREE", "PENDING", "Booking", "Calendar", "Slot", "seeded_calendar",
]
__version__ = "3.0.0"
