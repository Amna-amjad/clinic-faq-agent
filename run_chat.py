"""Simulated WhatsApp chat with a clinic's FAQ agent.

    python run_chat.py [bright-smile|green-valley]

Type a customer message, get a short, sourced answer back.
Type 'quit' to stop. This is a local demo — it does not send
anything on WhatsApp. Connecting to the official WhatsApp
Business Platform is a separate, later step.
"""

import sys

from faq_agent.agent import answer
from faq_agent.clinics import get_clinic


def main() -> None:
    clinic_id = sys.argv[1] if len(sys.argv) > 1 else "bright-smile"
    try:
        clinic = get_clinic(clinic_id)
    except ValueError as exc:
        print(exc)
        return
    print(f"{clinic.name} — WhatsApp FAQ demo (simulated chat)")
    print("Type 'quit' to stop.\n")
    while True:
        try:
            message = input("Customer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if message.lower() in {"quit", "exit", "bye"}:
            print(f"Clinic: Thanks for messaging {clinic.name}!")
            break
        if not message:
            continue
        reply = answer(message, clinic=clinic.id)
        print(f"Clinic: {reply.text}\n")


if __name__ == "__main__":
    main()
