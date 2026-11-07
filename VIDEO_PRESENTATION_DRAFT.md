# Video Presentation Draft — Clinic WhatsApp FAQ Agent

**Status:** Draft only. Not recorded yet. Edit this before you record.
**Suggested length:** About 5 minutes. A 2-minute cut is at the end.
**Important, say this honestly in the video:** This is a simulated
chat demo with fictional clinics. It is not live on WhatsApp yet,
it does not book appointments by itself, and it does not give
medical advice.

---

## Slide / screen plan

1. Title: Clinic WhatsApp FAQ Agent — one agent, many clinics
2. The problem: same questions, again and again
3. The solution: short answers, only from the clinic's own pages
4. Live demo 1: Bright Smile Dental Clinic
5. Live demo 2: the multi-clinic proof — same question, different answers
6. Safety: no diagnosis, no medicine, human handoff
7. How this becomes a SaaS + what is next

---

## Full script — read this aloud, slowly

### 1. Opening — 20 seconds

[Show: title slide]

> "Hi, this is my project: a WhatsApp FAQ agent for clinics and
> dental clinics. It is the first step toward a small SaaS product:
> one system that can serve many clinics."

### 2. The problem — 30 seconds

[Show: problem slide — a phone with repeated WhatsApp questions]

> "Clinic receptionists get the same questions every day on
> WhatsApp. What time do you open? How much is a checkup? How do
> I book an appointment? What should I bring for my first visit?
> Answering these one by one takes time, and patients wait."

### 3. The solution — 45 seconds

[Show: solution slide — 3 rules]

> "My agent answers only from the clinic's own pages. It keeps
> the answer short, it names the source page, and if it does not
> know, it says so honestly and offers a human instead of
> inventing an answer. It never books, charges, or sends anything
> on its own. A human approves anything beyond an answer."

> "Each clinic has 7 pages: opening hours, fees and prices,
> services, appointments, location and contact, first visit,
> and emergencies and aftercare."

### 4. Live demo 1: Bright Smile — 60 seconds

[Show: terminal / simulated chat. Type each question slowly and
let the answer stay on screen for a few seconds.]

> "This is a fictional clinic, Bright Smile Dental Clinic.
> Let me ask it three questions a real patient would ask."

Customer: "What time do you open on Saturday?"
Clinic: "Open Monday–Friday 9:00–18:00, Saturday 9:00–14:00.
Source: Opening hours"

Customer: "How much does a checkup cost?"
Clinic: "These are starting prices; the final price is confirmed
after a checkup. Consultation Rs 1,500.
Source: Consultation fees and prices"

Customer: "How do I book an appointment?"
Clinic: "Book by WhatsApp or phone with your name, phone number,
and preferred date and time. Please reschedule or cancel at
least 4 hours before your appointment.
Source: Appointments"

> "Short, sourced, and only from Bright Smile's own pages."

### 5. Live demo 2: the multi-clinic proof — 60 seconds

[Show: comparison — same question, two clinics, side by side]

> "This is the important part. This is not one clinic's chatbot.
> It is one engine for many clinics. Watch what happens when I
> ask the same question to a second fictional clinic,
> Green Valley Dental Clinic."

Customer, to both clinics: "What time do you open on Saturday?"
- Bright Smile: "Saturday 9:00–14:00"
- Green Valley: "Saturday 10:00–16:00"

Customer, to both clinics: "How much does a checkup cost?"
- Bright Smile: "Consultation Rs 1,500"
- Green Valley: "Consultation Rs 2,000"

> "Same engine, same question, different correct answer — because
> each clinic has its own pages. Adding a new clinic means adding
> its pages, not rewriting the agent. And if a clinic is unknown,
> the agent refuses to answer instead of answering from the
> wrong clinic's pages."

### 6. Safety — 30 seconds

[Show: safety slide]

> "For clinics, safety matters more than clever answers. The
> agent never diagnoses and never recommends medicine."

Customer: "What medicine should I take for tooth pain?"
Clinic: "I can't recommend medicine or diagnose a problem.
I'll pass this to clinic staff — please leave your name and
what it's about, and someone will reply."

> "For severe pain or swelling, it points the patient to contact
> the clinic right away, so staff can advise promptly."

### 7. How this becomes a SaaS, and what is next — 40 seconds

[Show: SaaS slide — one server, many clinics, monthly service]

> "As a SaaS, the clinic does not buy code. It uses a running
> service on its own official WhatsApp business number, and pays
> monthly. The clinic gets its own pages, its own answers, and
> later, a simple owner view to edit FAQs and see the questions
> patients asked that had no answer yet."

> "What is done so far: a single-clinic demo, then a multi-clinic
> version, with 18 tests passing. What is next: connect a Meta
> test number through the official WhatsApp Business Cloud API,
> then build that owner view. It is not live on WhatsApp yet,
> and that is the honest next step."

> "One more thing about booking, so it is clear: the FAQ version
> answers booking questions and collects requests. The calendar
> version attaches a calendar to the app, shows available slots
> automatically, and updates the slots only when the owner
> confirms — it does not book without owner approval."

> "Thank you. That is the clinic WhatsApp FAQ agent: short,
> sourced answers, one engine, many clinics."

---

## 2-minute cut — if you have less time

Keep only these parts, in this order:

1. Problem, in one sentence: clinics answer the same WhatsApp
   questions every day.
2. One Bright Smile demo: Saturday hours and checkup price.
3. Multi-clinic proof: same Saturday question, Bright Smile
   9:00–14:00 versus Green Valley 10:00–16:00.
4. Safety, in one sentence: no diagnosis, no medicine, human
   handoff.
5. Closing, in one sentence: one engine, many clinics, monthly
   service, Meta test connection is next.

---

## Recording tips

- Record your screen for the demo parts, not just slides. The
  demo is the proof.
- Pause for 2–3 seconds after each agent answer, so viewers can
  read it.
- Say "fictional clinic" out loud. Do not present Bright Smile
  or Green Valley as real clinics.
- Do not say it is live on WhatsApp, books appointments, or
  gives medical advice — it does none of those.
- If you make a mistake while typing a demo question, keep
  going. A small mistake looks more real than a perfect take.

---

## Facts used in this draft (all verified in the demo)

- Bright Smile: Saturday 9:00–14:00, checkup Rs 1,500,
  reschedule at least 4 hours before.
- Green Valley: Saturday 10:00–16:00, checkup Rs 2,000,
  reschedule at least 24 hours before.
- Tests: 28 passing in total — 9 single-clinic, 9 multi-clinic,
  10 calendar.
- Calendar demo: per-clinic calendar, free / pending / booked
  slots, owner confirms to book, owner rejects or cancels to
  free a slot again. Demo calendar is in-memory and re-seeds
  on restart.
- Stack: Python, standard library only, no API key, no LLM.
- Status: simulated chat only, not live on WhatsApp, not pushed
  to GitHub yet.
