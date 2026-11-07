"""Interactive calendar demo: try the owner-confirmation flow yourself.

    python run_booking.py [bright-smile|green-valley]

Commands (type them at the prompt):
  slots                  — show free slots for this clinic
  request <slot> <name>  — patient requests a slot (becomes pending)
  confirm <booking>      — owner confirms a pending booking
  reject <booking>       — owner rejects a pending booking
  cancel <booking>       — owner cancels a confirmed booking
  quit                   — stop

Example:
  slots
  request BS1 Ali
  confirm B1
  slots

This is a local demo — it does not send anything on WhatsApp, and
its calendar resets when you restart it. A production version
would store bookings in a database.
"""

import sys

from faq_agent.calendar import seeded_calendar
from faq_agent.clinics import get_clinic

CAL = seeded_calendar()


def main() -> None:
    clinic_id = sys.argv[1] if len(sys.argv) > 1 else "bright-smile"
    try:
        clinic = get_clinic(clinic_id)
    except ValueError as exc:
        print(exc)
        return
    print(f"{clinic.name} — calendar booking demo (simulated)")
    print("Commands: slots | request <slot> <name> | confirm <booking> | reject <booking> | cancel <booking> | quit\n")
    while True:
        try:
            raw = input("Booking: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()
        if cmd in {"quit", "exit", "bye"}:
            print("Bye!")
            break
        try:
            if cmd == "slots":
                print(CAL.available_text(clinic.id))
            elif cmd == "request" and len(parts) >= 3:
                booking = CAL.request(clinic.id, parts[1], " ".join(parts[2:]))
                print(f"Pending booking {booking.id} for slot {booking.slot_id} — waiting for owner confirmation.")
            elif cmd == "confirm" and len(parts) == 2:
                booking = CAL.confirm(parts[1])
                print(f"Booking {booking.id} confirmed. Slot {booking.slot_id} is now booked.")
            elif cmd == "reject" and len(parts) == 2:
                booking = CAL.reject(parts[1])
                print(f"Booking {booking.id} rejected. Slot {booking.slot_id} is free again.")
            elif cmd == "cancel" and len(parts) == 2:
                booking = CAL.cancel(parts[1])
                print(f"Booking {booking.id} cancelled. Slot {booking.slot_id} is free again.")
            else:
                print("Unknown command. Try: slots, request BS1 Ali, confirm B1, reject B1, cancel B1, quit")
        except ValueError as exc:
            print(f"Could not do that: {exc}")
        print()


if __name__ == "__main__":
    main()
