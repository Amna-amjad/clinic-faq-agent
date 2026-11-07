"""Clinic WhatsApp FAQ agent: short, sourced answers — or an honest 'not found'.

Rules, kept deliberately simple (same engine as the bakery demo):
  1. Answer ONLY from the chosen clinic's own pages (see clinics.py).
     The clinic is a parameter, not hardcoded — that is what makes
     this multi-clinic instead of single-clinic.
  2. Name the source page in every answer.
  3. Keep it WhatsApp-short: at most 2 sentences from the source.
  4. If no page matches, do NOT invent an answer. Say so and offer
     a human handoff instead.
  5. Never send anything, take payment, or book anything in v1.
     The agent only answers and drafts; a human approves the rest.
  6. Clinic safety rule: never diagnose, recommend medicine, or
     advise treatment. Personal health questions go to clinic staff,
     and emergency questions point to contacting the clinic promptly.

How matching works (no LLM, no API key, standard library only):
  - The question is lower-cased, split into words, and expanded with
    a small synonym map (cost -> price, ...).
  - Each page is scored by how many of those words appear in its
    keywords or its text. The best page wins; ties go to the page
    with the best-matching sentence.
  - The best 1–2 sentences from that page become the answer.
  - A score of 0 means 'not found' — by design, not by accident.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .clinics import Clinic, get_clinic
from .pages import Page

_STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for",
    "with", "is", "are", "was", "were", "do", "does", "did", "can",
    "you", "your", "i", "me", "my", "we", "it", "its", "at", "by",
    "what", "when", "where", "which", "how", "please", "hi", "hello",
    "hey", "there", "this", "that", "if", "so",
}

_SYNONYMS = {
    "cost": {"price", "prices"},
    "costs": {"price", "prices"},
    "expensive": {"price", "prices"},
    "cheap": {"price", "prices"},
    "close": {"closing", "hours"},
    "closed": {"closing", "hours"},
    "open": {"opening", "hours"},
    "timings": {"hours"},
    "timing": {"hours"},
    "charges": {"price", "prices", "fee", "fees"},
    "fee": {"fees", "price", "prices"},
    "book": {"appointment", "booking"},
    "appointment": {"booking"},
    "slot": {"appointment"},
    "slots": {"slot", "appointment", "appointments"},
    "allergic": {"allergy"},
    "checkup": {"consultation"},
    "checkups": {"consultation"},
    "located": {"location", "address"},
    "hurt": {"pain"},
    "hurts": {"pain"},
    "ache": {"pain"},
    "aching": {"pain"},
}

_GREETINGS = {"hi", "hello", "hey", "salam", "assalam", "aoa", "good morning", "good afternoon", "good evening"}
_HANDOFF_WORDS = {"human", "person", "manager", "staff", "someone", "receptionist"}
_MEDICINE_WORDS = {
    "medicine", "medicines", "medication", "medications",
    "tablet", "tablets", "painkiller", "painkillers",
    "antibiotic", "antibiotics", "prescribe", "prescription",
}
_PAIN_WORDS = {"pain", "ache", "tooth", "teeth", "swelling", "swollen", "hurt", "hurts"}
# Symptoms / personal health complaints. A question naming one of these is
# a personal health question, not a FAQ lookup — even without the word
# "medicine". This is what the old check missed: "fever" is not in
# _PAIN_WORDS, so "I have a fever, what medicine should I take?" fell
# through to page matching and matched First Visit on "take / should".
# Deliberately NOT including tooth/teeth, pressure, allergy, asthma or
# diabetes here: those can be legitimate service questions for a clinic
# ("do you clean teeth?", "do you check blood pressure?"), and the
# original code only used them together with a medicine word.
_SYMPTOM_WORDS = {
    "fever", "temperature", "cough", "cold", "flu", "headache", "migraine",
    "nausea", "vomiting", "vomit", "diarrhoea", "diarrhea", "rash",
    "infection", "sore", "dizziness", "dizzy", "bleeding", "injury",
    "wound", "burn", "fracture", "broken", "sick", "ill", "unwell",
    "symptom", "symptoms",
}
_TREATMENT_WORDS = {
    "diagnose", "diagnosis", "treatment", "treat", "treats", "cure",
    "cures", "dose", "dosage",
}


@dataclass
class Answer:
    text: str
    source_title: str | None
    found: bool


def _words(text: str) -> set[str]:
    words = set(re.findall(r"[a-z0-9]+", text.lower()))
    expanded = set(words)
    for word in words:
        expanded.update(_SYNONYMS.get(word, set()))
    return {w for w in expanded if w not in _STOPWORDS and len(w) > 1}


def _page_words(page: Page) -> set[str]:
    text_words = set(re.findall(r"[a-z0-9]+", page.text.lower()))
    return set(page.keywords) | text_words


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _best_page(
    question_words: set[str], pages: list[Page]
) -> tuple[Page | None, int]:
    best: Page | None = None
    best_score = 0
    for page in pages:
        score = len(question_words & _page_words(page))
        if score > best_score:
            best, best_score = page, score
    return best, best_score


def _best_sentences(page: Page, question_words: set[str], count: int = 2) -> list[str]:
    scored: list[tuple[int, str]] = []
    for sentence in _split_sentences(page.text):
        sentence_words = set(re.findall(r"[a-z0-9]+", sentence.lower()))
        scored.append((len(question_words & sentence_words), sentence))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [sentence for score, sentence in scored if score > 0][:count] or [
        _split_sentences(page.text)[0]
    ]


def answer(
    question: str,
    clinic: Clinic | str | None = None,
    calendar=None,
) -> Answer:
    """Answer one customer message, WhatsApp-style.

    clinic may be a Clinic object, a clinic id like "green-valley",
    a clinic name, or None for the default clinic (Bright Smile).
    An unknown clinic raises ValueError instead of answering from
    the wrong clinic's pages.

    calendar, if given, is a Calendar from calendar.py. When a
    patient asks for available slots and a calendar is attached,
    the answer comes from that clinic's live calendar — only free
    slots — not from a FAQ page. Without a calendar, slot questions
    fall back to the Appointments FAQ page, as before.
    """
    chosen = get_clinic(clinic)
    clinic_name = chosen.name
    pages = chosen.pages
    raw = question.strip()
    lowered = raw.lower().strip(" .!?")

    if lowered in _GREETINGS or lowered in {"hi there", "hello there"}:
        return Answer(
            text=(
                f"Hi! This is {clinic_name}. "
                "Ask me about hours, fees, services, appointments, "
                "location, first visits, or emergencies."
            ),
            source_title=None,
            found=True,
        )

    question_words = _words(raw)

    # Medical advice is never answered from the pages: hand it to staff.
    # This check runs BEFORE any page matching, and it triggers on ANY
    # medicine word, symptom, or treatment word on its own.
    # Old bug: it required medicine AND pain together, so "fever" (not a
    # pain word) + "medicine" did not trigger it, and the question fell
    # through to page scoring, where First Visit won on "take / should".
    # Pain words on their own are NOT a trigger here, on purpose:
    # tooth/teeth can be service questions ("do you clean teeth?").
    if (question_words & _MEDICINE_WORDS
            or question_words & _SYMPTOM_WORDS
            or question_words & _TREATMENT_WORDS):
        return Answer(
            text=(
                "I can't recommend medicine or diagnose a problem. "
                "I'll pass this to clinic staff — please leave your name "
                "and what it's about, and someone will reply."
            ),
            source_title=None,
            found=False,
        )

    # A request for a human always wins over a guessed answer.
    if (question_words & _HANDOFF_WORDS and len(question_words) <= 4) or \
            "talk to" in raw.lower() or "speak to" in raw.lower():
        return Answer(
            text=(
                f"Of course — I'll pass this to a human at {clinic_name}. "
                "Please leave your name and what it's about, "
                "and someone will reply."
            ),
            source_title=None,
            found=True,
        )

    # Live calendar answer: available slots, per clinic, automatically.
    if calendar is not None and \
            (question_words & {"available", "free"}) and \
            (question_words & {"slot", "slots", "appointment", "appointments"}):
        return Answer(
            text=calendar.available_text(chosen.id),
            source_title="Calendar",
            found=True,
        )

    page, score = _best_page(question_words, pages)
    if page is None or score == 0:
        return Answer(
            text=(
                f"Sorry, I couldn't find that in {clinic_name}'s pages. "
                "I can pass this to a human — just say the word."
            ),
            source_title=None,
            found=False,
        )

    sentences = _best_sentences(page, question_words)
    text = " ".join(sentences)

    return Answer(
        text=f"{text}\nSource: {page.title}",
        source_title=page.title,
        found=True,
    )
