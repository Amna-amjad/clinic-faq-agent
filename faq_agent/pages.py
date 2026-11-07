"""The clinic's own pages — the ONLY sources this agent may answer from.

This is a fictional clinic set, created for the SaaS demo.
No real clinic is represented. Prices are fictional, in Rs.

To use this agent for a real clinic, replace these 7 pages with that
clinic's own pages/documents and keep everything else the same.

Safety rule built into the pages: this agent gives information only.
It does not diagnose, recommend medicine, or advise treatment.
For pain, swelling, bleeding, or any personal health question, the
pages direct the customer to clinic staff promptly.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    title: str
    text: str
    keywords: frozenset


PAGES: list[Page] = [
    Page(
        title="Opening hours",
        text=(
            "Open Monday–Friday 9:00–18:00, Saturday 9:00–14:00. "
            "Closed on Sundays and public holidays. "
            "Walk-ins are seen only if a slot is free; appointments are preferred."
        ),
        keywords=frozenset(
            {
                "open", "opening", "close", "closing", "hours", "time",
                "saturday", "sunday", "monday", "friday", "holiday",
                "holidays", "when", "walk", "walk-in", "walk-ins",
            }
        ),
    ),
    Page(
        title="Consultation fees and prices",
        text=(
            "Consultation Rs 1,500. Dental cleaning Rs 5,000. "
            "Filling Rs 4,000–8,000 depending on the tooth. "
            "Extraction Rs 6,000 and up. "
            "These are starting prices; the final price is confirmed after a checkup."
        ),
        keywords=frozenset(
            {
                "price", "prices", "cost", "much", "fee", "fees",
                "consultation", "consult", "checkup", "cleaning",
                "filling", "extraction", "charge", "charges",
            }
        ),
    ),
    Page(
        title="Services",
        text=(
            "Services offered: checkups, dental cleaning, fillings, "
            "extractions, braces consultations, and teeth whitening. "
            "This list describes services only; it is not advice about "
            "which treatment is right for any person."
        ),
        keywords=frozenset(
            {
                "service", "services", "treatment", "treatments",
                "braces", "whitening", "cleaning", "filling",
                "extraction", "checkup",
            }
        ),
    ),
    Page(
        title="Appointments",
        text=(
            "Book by WhatsApp or phone with your name, phone number, "
            "and preferred date and time. "
            "Please reschedule or cancel at least 4 hours before your appointment. "
            "If you are more than 15 minutes late, your slot may be given to another patient."
        ),
        keywords=frozenset(
            {
                "appointment", "appointments", "book", "booking",
                "schedule", "reschedule", "cancel", "cancellation",
                "slot", "late", "visit", "date", "time",
            }
        ),
    ),
    Page(
        title="Location and contact",
        text=(
            "Bright Smile Dental Clinic, Ground Floor, 12 Rose Street. "
            "Contact the clinic by WhatsApp or phone through the number "
            "shown on the clinic profile. "
            "Parking is available on the street outside the clinic."
        ),
        keywords=frozenset(
            {
                "location", "address", "where", "contact", "phone",
                "number", "reach", "find", "parking", "street", "located",
            }
        ),
    ),
    Page(
        title="First visit",
        text=(
            "For a first visit, please arrive 15 minutes early. "
            "Bring your ID, a list of medicines you take, and any previous "
            "dental reports or X-rays you already have. "
            "You will fill in a short registration form at reception."
        ),
        keywords=frozenset(
            {
                "first", "visit", "bring", "arrive", "early",
                "id", "report", "reports", "x-ray", "x-rays",
                "form", "registration", "reception", "new", "patient",
            }
        ),
    ),
    Page(
        title="Emergencies and aftercare",
        text=(
            "For severe pain, swelling, bleeding, or a broken tooth, "
            "contact the clinic right away so staff can advise you promptly. "
            "This agent does not diagnose or recommend medicine. "
            "After treatment, follow only the written instructions given by the clinic."
        ),
        keywords=frozenset(
            {
                "emergency", "emergencies", "urgent", "severe",
                "pain", "swelling", "bleeding", "broken", "tooth",
                "aftercare", "after", "treatment", "hurt", "hurts",
                "ache", "swollen",
            }
        ),
    ),
]
