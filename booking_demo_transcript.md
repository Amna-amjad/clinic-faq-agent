# Calendar booking demo transcript (simulated)

Fictional clinics: Bright Smile Dental Clinic and Green Valley Dental Clinic. No real bookings were made.

```
Calendar booking demo (simulated, fictional clinics)

Step 1 — Patient asks Bright Smile what slots are available:
Free slots at Bright Smile Dental Clinic:
- BS1: 2026-11-02 09:00
- BS2: 2026-11-02 10:00
- BS3: 2026-11-02 11:00
- BS4: 2026-11-03 09:00
- BS5: 2026-11-03 10:00

Step 2 — Patient Ali requests slot BS1 (2026-11-02 09:00):
Booking B1 created, status: pending (waiting for owner).

Step 3 — Available slots now (the requested slot is held, not free):
Free slots at Bright Smile Dental Clinic:
- BS2: 2026-11-02 10:00
- BS3: 2026-11-02 11:00
- BS4: 2026-11-03 09:00
- BS5: 2026-11-03 10:00

Step 4 — Owner confirms:
Booking B1 status: confirmed.

Step 5 — Available slots after owner confirmation (slot stays gone):
Free slots at Bright Smile Dental Clinic:
- BS2: 2026-11-02 10:00
- BS3: 2026-11-02 11:00
- BS4: 2026-11-03 09:00
- BS5: 2026-11-03 10:00

Step 6 — Another patient, Sara, tries the same slot:
Refused, as it should be: Slot 2026-11-02 09:00 at Bright Smile Dental Clinic is not free (status: booked).

Step 7 — Green Valley slots are untouched:
Free slots at Green Valley Dental Clinic:
- GV1: 2026-11-02 10:00
- GV2: 2026-11-02 11:00
- GV3: 2026-11-02 12:00
- GV4: 2026-11-03 10:00
- GV5: 2026-11-03 11:00

```
