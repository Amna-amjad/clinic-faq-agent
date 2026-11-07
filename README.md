# Clinic WhatsApp FAQ Agent — SaaS demo, clinics and dental clinics

**Problem:** Clinic customers ask the same short questions on
WhatsApp — hours, fees, services, appointments, location, first
visits — and the front desk answers them over and over.

**Solution:** The same small agent as the bakery demo, with clinic
pages instead: it answers only from the clinic's own pages, names
its source, keeps answers WhatsApp-short, and says "not found"
instead of inventing an answer — then offers a human handoff.

This is the first niche demo for the SaaS version of the WhatsApp
FAQ agent: clinics and dental clinics, chosen 2026-10-30, instead
of bakeries/restaurants. The bakery demo is untouched in
`~/workspace/whatsapp-faq-agent/`; this is a separate clinic demo
in `~/workspace/clinic-faq-agent/`.

## The simple formula (this is the whole agent)

- **One job:** answer a customer question from the clinic's pages.
- **Rules:** answer only from those pages, name the source, keep it
  to at most 2 sentences, never invent, never send/book/pay in v1.
- **Tool:** keyword + synonym matching over the supplied pages.
  No LLM, no API key, standard library only.
- **Check:** every answer either names a source page, or says
  "not found" and offers a human.

## Clinic safety rule (important)

This agent gives information only. It does **not** diagnose,
recommend medicine, or advise treatment.

- A question like "What medicine should I take for tooth pain?"
  is refused as a medical answer and passed to clinic staff.
- A question about severe pain, swelling, bleeding, or a broken
  tooth is answered from the Emergencies page: contact the clinic
  right away so staff can advise promptly.

## The fictional clinics (now multi-clinic)

Two fictional clinics, so the demo can be compared directly and
no real clinic is represented:

- **Bright Smile Dental Clinic** (`bright-smile`) — its 7 pages
  are in `faq_agent/pages.py`: opening hours, consultation fees
  and prices, services, appointments, location and contact, first
  visit, emergencies and aftercare. Prices are fictional, in Rs.
- **Green Valley Dental Clinic** (`green-valley`) — its 7 pages
  are in `faq_agent/green_valley_pages.py`, with deliberately
  different hours, fees, and booking rule.

The registry in `faq_agent/clinics.py` is the whole multi-clinic
idea: a clinic is just an id, a name, and its own pages. The
engine in `agent.py` takes the clinic as a parameter, so an
unknown clinic raises an error instead of being answered from
the wrong clinic's pages.

To add a real clinic, add one pages file and one entry in
`clinics.py` — the answering engine does not change.

## Run it

No dependencies. Python 3.10+ only.

Interactive simulated chat (default: Bright Smile, or pass a clinic id):

```bash
python run_chat.py
python run_chat.py green-valley
```

Scripted single-clinic demo:

```bash
python demo_chat.py --out demo_transcript.md
```

Scripted multi-clinic demo (same questions, both clinics):

```bash
python demo_multi_clinic.py --out multi_demo_transcript.md
```

Calendar booking demo (available slots, request, owner confirms):

```bash
python booking_demo.py --out booking_demo_transcript.md
python run_booking.py
```

Tests (38 tests, all passing: 9 single-clinic + 9 multi-clinic + 10 calendar + 10 webhook):

```bash
python test_agent.py
python test_multi_clinic.py
python test_calendar.py
python test_webhook.py
```

## Calendar and owner confirmation

One calendar per clinic, attached to the app in
`faq_agent/calendar.py`. A slot is free, pending, or booked:

- Patient asks "What slots are available?" — the agent answers
  from that clinic's live calendar, showing only free slots,
  automatically. Without a calendar attached, it falls back to
  the Appointments FAQ page.
- Patient picks a slot — a pending booking is created and the
  slot is held, so it stops showing as free to anyone else.
- Owner confirms — the booking is confirmed and the slot stays
  gone. Owner rejects — the slot becomes free again. Owner
  cancels a confirmed booking — the slot becomes free again.
- Nothing is auto-booked. A patient request alone never books.

Try it interactively: `python run_booking.py`, then
`slots`, `request BS1 Ali`, `confirm B1`, `slots` again.

Limitation, stated honestly: this demo calendar is in-memory,
so restarting the demo re-seeds it. A production version would
store bookings in a database and, later, sync with the owner's
Google Calendar. The free / pending / booked statuses and the
owner-confirmation rule would stay the same.

## What the demo proves

| Customer message | Agent does |
|---|---|
| "What time do you open on Saturday?" | Answers 9:00–14:00, source: Opening hours |
| "How much does a checkup cost?" | Answers Rs 1,500, source: Consultation fees and prices |
| "How do I book an appointment?" | Answers from Appointments, including the 4-hour reschedule rule |
| "What should I bring for my first visit?" | Answers from First visit, including arriving 15 minutes early |
| "I have severe tooth pain and swelling, what should I do?" | Answers from Emergencies and aftercare: contact the clinic right away |
| "What medicine should I take for tooth pain?" | Refuses to recommend medicine, passes to clinic staff — no invented answer |
| "Do you offer home visits?" | Says "couldn't find that in Bright Smile's pages" and offers a human |

See the full transcript in `demo_transcript.md`.

## Meta test webhook bridge (ready, not yet connected)

`webhook_bridge.py` is the bridge to Meta's official WhatsApp
test number — stdlib only, dry-run mode, routed by clinic, with
the seeded calendar attached so live slot questions work. It is
verified in dry-run (health check, verification ok / wrong token
403, Bright Smile slots, Green Valley Saturday hours). It is
**not yet connected to a Meta test number**: no Meta app, tokens,
or credentials have been created or stored. Follow
`META_TEST_SETUP.md` to connect it — start with Bright Smile on
one test number, and test from your own allowlisted number.

Important: the bridge answers FAQ and slot questions only. A
WhatsApp message does not book a slot; booking still needs owner
confirmation. And never connect it through a bot on a personal
WhatsApp number — that is the unofficial route that can get a
number banned. The official WhatsApp Business Platform only.

## Limitations (stated honestly)

- v1 matching is keyword-based, not an LLM. It handles reworded
  questions well when the words overlap with a page, and it will
  miss questions phrased in a completely different way — in that
  case it says "not found", which is the safe failure.
- It is only as good as the supplied pages. It cannot answer what
  the clinic has not written down.
- It does not book, take payment, or send messages in v1. A human
  approves anything beyond an answer.

## What the multi-clinic demo proves

| Same question | Bright Smile answers | Green Valley answers |
|---|---|---|
| "What time do you open on Saturday?" | 9:00–14:00 | 10:00–16:00 |
| "How much does a checkup cost?" | Rs 1,500 | Rs 2,000 |
| "How do I book an appointment?" | Reschedule at least 4 hours before | Reschedule at least 24 hours before |

See the full transcript in `multi_demo_transcript.md`.

## Next step toward SaaS

Multi-clinic answering, calendar booking with owner
confirmation, and the Meta test webhook bridge are done. The
steps after this are: actually connecting the bridge to a Meta
test number (see `META_TEST_SETUP.md`), a simple owner view for
editing FAQs and confirming bookings, and persistent booking
storage / Google Calendar sync.
