"""Clinic registry: the multi-clinic part of the SaaS demo.

One engine, many clinics. A clinic is just an id, a name, and its
own pages. Adding a new clinic means adding one pages file and one
entry here — the answering engine in agent.py does not change.

Both clinics here are fictional, for the demo only.
"""

from __future__ import annotations

from dataclasses import dataclass

from .green_valley_pages import PAGES as GREEN_VALLEY_PAGES
from .pages import PAGES as BRIGHT_SMILE_PAGES
from .pages import Page


@dataclass(frozen=True)
class Clinic:
    id: str
    name: str
    pages: list[Page]


CLINICS: dict[str, Clinic] = {
    "bright-smile": Clinic(
        id="bright-smile",
        name="Bright Smile Dental Clinic",
        pages=BRIGHT_SMILE_PAGES,
    ),
    "green-valley": Clinic(
        id="green-valley",
        name="Green Valley Dental Clinic",
        pages=GREEN_VALLEY_PAGES,
    ),
}

DEFAULT_CLINIC_ID = "bright-smile"


def get_clinic(clinic: Clinic | str | None) -> Clinic:
    """Resolve a clinic id, clinic name, Clinic object, or None (default).

    Raises ValueError for an unknown id/name, so a message is never
    silently answered from the wrong clinic's pages.
    """
    if clinic is None:
        return CLINICS[DEFAULT_CLINIC_ID]
    if isinstance(clinic, Clinic):
        return clinic
    key = clinic.strip().lower()
    if key in CLINICS:
        return CLINICS[key]
    for candidate in CLINICS.values():
        if candidate.name.lower() == key:
            return candidate
    known = ", ".join(sorted(CLINICS))
    raise ValueError(f"Unknown clinic: {clinic!r}. Known clinics: {known}")


def list_clinics() -> list[Clinic]:
    return list(CLINICS.values())
