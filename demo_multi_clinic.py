"""Scripted multi-clinic demo: the same questions, two clinics.

    python demo_multi_clinic.py [--out multi_demo_transcript.md]

Proves one engine serves many clinics: each answer comes only from
that clinic's own pages, with different hours, fees, and booking rules.
"""

from __future__ import annotations

import argparse

from faq_agent.agent import answer
from faq_agent.clinics import list_clinics

DEMO_MESSAGES = [
    "Hi",
    "What time do you open on Saturday?",
    "How much does a checkup cost?",
    "How do I book an appointment?",
]


def run_demo() -> list[str]:
    lines = ["Multi-clinic WhatsApp FAQ demo (simulated chat)", ""]
    for clinic in list_clinics():
        lines.append(f"--- {clinic.name} ({clinic.id}) ---")
        lines.append("")
        for message in DEMO_MESSAGES:
            reply = answer(message, clinic=clinic.id)
            lines.append(f"Customer: {message}")
            lines.append(f"Clinic: {reply.text}")
            lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the scripted multi-clinic demo.")
    parser.add_argument("--out", default=None, help="Also write the transcript to this file")
    args = parser.parse_args()

    lines = run_demo()
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("# Multi-clinic WhatsApp FAQ demo transcript (simulated chat)\n\n")
            fh.write(
                "Fictional clinics: Bright Smile Dental Clinic and "
                "Green Valley Dental Clinic. No real messages were sent.\n\n"
            )
            fh.write("```\n")
            fh.write(text)
            fh.write("\n```\n")
        print(f"[done] Transcript written to {args.out}")


if __name__ == "__main__":
    main()
