"""Scripted demo for the clinic FAQ agent, printed as a WhatsApp chat.

    python demo_chat.py [--out demo_transcript.md]
"""

from __future__ import annotations

import argparse

from faq_agent.agent import answer

DEMO_MESSAGES = [
    "Hi",
    "What time do you open on Saturday?",
    "How much does a checkup cost?",
    "How do I book an appointment?",
    "What should I bring for my first visit?",
    "I have severe tooth pain and swelling, what should I do?",
    "What medicine should I take for tooth pain?",
    "Do you offer home visits?",
]


def run_demo() -> list[str]:
    lines = ["Bright Smile Dental Clinic — WhatsApp FAQ demo (simulated chat)", ""]
    for message in DEMO_MESSAGES:
        reply = answer(message)
        lines.append(f"Customer: {message}")
        lines.append(f"Clinic: {reply.text}")
        lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the scripted WhatsApp demo.")
    parser.add_argument("--out", default=None, help="Also write the transcript to this file")
    args = parser.parse_args()

    lines = run_demo()
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("# WhatsApp FAQ demo transcript (simulated chat)\n\n")
            fh.write("Fictional clinic: Bright Smile Dental Clinic. No real messages were sent.\n\n")
            fh.write("```\n")
            fh.write(text)
            fh.write("\n```\n")
        print(f"[done] Transcript written to {args.out}")


if __name__ == "__main__":
    main()
