"""Scripted calendar demo: available slots, request, owner confirms.

    python booking_demo.py [--out booking_demo_transcript.md]

Proves, step by step:
  1. Available slots are shown automatically, per clinic.
  2. A patient request holds a slot (pending) — it stops showing as free.
  3. Owner confirmation books it — it stays gone.
  4. Another patient cannot take the same slot afterwards.
  5. The other clinic's slots are untouched.
"""

from __future__ import annotations

import argparse

from faq_agent.agent import answer
from faq_agent.calendar import seeded_calendar


def run_demo() -> list[str]:
    cal = seeded_calendar()
    lines = ["Calendar booking demo (simulated, fictional clinics)", ""]
    lines.append("Step 1 — Patient asks Bright Smile what slots are available:")
    lines.append(answer("What slots are available?", clinic="bright-smile", calendar=cal).text)
    lines.append("")

    slot = cal.available("bright-smile")[0]
    lines.append(f"Step 2 — Patient Ali requests slot {slot.id} ({slot.label()}):")
    booking = cal.request("bright-smile", slot.id, "Ali")
    lines.append(f"Booking {booking.id} created, status: {booking.status} (waiting for owner).")
    lines.append("")
    lines.append("Step 3 — Available slots now (the requested slot is held, not free):")
    lines.append(answer("What slots are available?", clinic="bright-smile", calendar=cal).text)
    lines.append("")

    lines.append("Step 4 — Owner confirms:")
    confirmed = cal.confirm(booking.id)
    lines.append(f"Booking {confirmed.id} status: {confirmed.status}.")
    lines.append("")
    lines.append("Step 5 — Available slots after owner confirmation (slot stays gone):")
    lines.append(answer("What slots are available?", clinic="bright-smile", calendar=cal).text)
    lines.append("")

    lines.append("Step 6 — Another patient, Sara, tries the same slot:")
    try:
        cal.request("bright-smile", slot.id, "Sara")
        lines.append("ERROR: second booking should not have succeeded.")
    except ValueError as exc:
        lines.append(f"Refused, as it should be: {exc}")
    lines.append("")

    lines.append("Step 7 — Green Valley slots are untouched:")
    lines.append(answer("What slots are available?", clinic="green-valley", calendar=cal).text)
    lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the scripted calendar demo.")
    parser.add_argument("--out", default=None, help="Also write the transcript to this file")
    args = parser.parse_args()

    lines = run_demo()
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("# Calendar booking demo transcript (simulated)\n\n")
            fh.write(
                "Fictional clinics: Bright Smile Dental Clinic and "
                "Green Valley Dental Clinic. No real bookings were made.\n\n"
            )
            fh.write("```\n")
            fh.write(text)
            fh.write("\n```\n")
        print(f"[done] Transcript written to {args.out}")


if __name__ == "__main__":
    main()
