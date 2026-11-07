"""Pages for the second fictional clinic in the multi-clinic demo.

Green Valley Dental Clinic is fictional, like Bright Smile.
Its hours, fees, and booking rule are deliberately different from
Bright Smile's, so the multi-clinic test can prove the same question
gets a different correct answer for each clinic.

Prices are fictional, in Rs. Safety rule is the same as Bright
Smile's: information only, no diagnosis, no medicine recommendation.
"""

from __future__ import annotations

from .pages import Page

PAGES: list[Page] = [
    Page(
        title="Opening hours",
        text=(
            "Open Monday–Friday 10:00–19:00, Saturday 10:00–16:00. "
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
            "Consultation Rs 2,000. Dental cleaning Rs 6,000. "
            "Filling Rs 5,000–9,000 depending on the tooth. "
            "Extraction Rs 7,000 and up. "
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
            "extractions, braces consultations, teeth whitening, "
            "and children's checkups. "
            "This list describes services only; it is not advice about "
            "which treatment is right for any person."
        ),
        keywords=frozenset(
            {
                "service", "services", "treatment", "treatments",
                "braces", "whitening", "cleaning", "filling",
                "extraction", "checkup", "children", "child",
            }
        ),
    ),
    Page(
        title="Appointments",
        text=(
            "Book by WhatsApp or phone with your name, phone number, "
            "and preferred date and time. "
            "Please reschedule or cancel at least 24 hours before your appointment. "
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
            "Green Valley Dental Clinic, Ground Floor, 45 Hill Road. "
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
            "For a first visit, please arrive 20 minutes early. "
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
