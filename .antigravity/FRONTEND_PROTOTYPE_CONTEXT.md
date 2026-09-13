# SIH 2026 — Criminal Network Analysis System
## Antigravity Prototype Context

### 1. Purpose

We are building a small LOCAL PROTOTYPE for the SIH 2026 problem statement PS #26189:
**AI-Powered Criminal Network Analysis System**

This is a prototype/demo only. All data must be synthetic/fabricated. Do not use real personal data.

The goal of this prototype is to demonstrate the user experience and the core idea before building the full backend.

### 2. Prototype goal

Create a very simple, clean, light-themed investigator dashboard with this flow:

India Map
→ Select a state/region
→ See cases
→ Select a case
→ See an interactive criminal/entity network
→ Click nodes
→ Inspect details, source, dates, locations, match confidence and explanation
→ View a simple timeline
→ Ask a small case-aware AI-style chatbot questions

The prototype should feel like a professional investigation tool, NOT a cyberpunk/hacker dashboard.

### 3. Visual direction

Use a LIGHT UI.

Principles:
- Very easy to understand and navigate
- Spacious layout
- Clear typography
- Minimal colours
- Use colour mainly for risk/status:
  - Red = high risk / urgent
  - Orange = medium
  - Green = low
  - Blue = resolved/informational
- Avoid excessive animations
- Avoid visual clutter
- Avoid tiny unreadable graph labels
- Avoid unnecessary technical terminology

Reference style:
- Modern professional investigation software
- Map-first workflow
- Clean graph/network visualization
- Simple cards and side panels
- Similar conceptual interaction to tools such as DataWalk, but much simpler and easier to use

### 4. Opening screen

The first screen should NOT immediately show the criminal network.

It should open on an INDIA MAP.

Show synthetic case markers/dots across India.

Example:
- Red markers = high-risk cases
- Orange = medium
- Green = low
- Blue = closed/resolved

A small summary area may show:
- Active cases
- High-risk cases
- Cases under monitoring
- Closed cases

Clicking a state should show the synthetic cases in that state.

### 5. Case selection

Create a small fabricated case list.

Use one primary demonstration case:

Case ID:
**DL-2026-0412**

Title:
**Missing Woman — Suspected Trafficking Network**

Location:
Delhi

Status:
Investigation Ongoing

Risk:
High

Important:
This is fictional demonstration data.

Selecting the case opens the case workspace.

### 6. Case workspace

The case page should have simple tabs or sections:

- Overview
- Network Graph
- Timeline
- Evidence
- AI Analysis

The prototype does not need fully separate pages if that makes development unnecessarily complicated.

### 7. Network graph

This is the central visual feature.

Create an interactive spider-web/entity network.

The PRIMARY PERSON should be visually central.

Example synthetic network:

                Location
                    |
                  Phone
                    |
CCTV -------- Person -------- Vehicle
                    |
                  Bank
                    |
                   FIR
                    |
                Associate

Use additional connected entities so the graph feels like a real network.

Suggested entity types:
- Person
- Phone
- Vehicle
- Bank Account
- Location
- CCTV Event
- FIR / Case
- Organization
- Transaction

Use simple icons or labels.

Lines represent relationships.

Example relationships:
- USES
- CALLED
- OWNS
- SEEN_AT
- TRANSFERRED_TO
- ASSOCIATED_WITH
- MENTIONED_IN

### 8. Clickable nodes

Every major node should be clickable.

When clicked, open a side panel/modal containing:

1. What is this?
2. Stored details
3. Associated entity/person
4. Why is it connected?
5. Match/association confidence
6. Dates
7. Locations
8. Source
9. Short AI explanation

Example:

PHONE NUMBER

+91 98765 43210

Type:
CDR

Associated Person:
Rakesh Kumar

Association Confidence:
94%

Why connected:
- Same subscriber record
- Appears in multiple CDR records
- Temporal overlap with case
- Location overlap

Recent activity:
12 Aug 2026, 18:20
12 Aug 2026, 17:54

Source:
Synthetic CDR Record CDR-00142

### 9. Primary person panel

Use fictional person:
**Rakesh Kumar**

Do NOT label the person as legally guilty.

Use wording such as:
- Possible central network entity
- Investigative lead
- Association confidence
- Potential suspect/subject only where appropriate

Example AI summary:

"Multiple independent synthetic records connect this person to phone numbers, vehicles, financial accounts, locations and previous case records."

Show:
- Network size
- Connected phones
- Vehicles
- Accounts
- Locations
- FIRs
- CCTV events
- AI association confidence

### 10. Timeline

Create a simple chronological timeline.

Example:

16:30 — New associate identified
17:15 — ₹50,000 transaction
18:20 — Phone call with unknown number
18:42 — CCTV sighting

Timeline should be visually simple and readable.

### 11. AI Assistant

Add a SMALL chatbot panel.

It should be case-aware using the local synthetic dataset.

No real external AI API is required for this prototype.

Implement a lightweight rule-based/mock assistant if necessary.

Example user questions:

"What connects Rakesh to this case?"
"How many people are connected to him?"
"Why is this phone number linked?"
"What happened before the disappearance?"
"Show the strongest connection."

Responses should use the synthetic data already in the prototype.

Example response:

"Rakesh Kumar is connected through three synthetic evidence paths: a phone number appearing in the victim's CDR, a vehicle appearing in CCTV records, and a financial transaction occurring shortly before the incident. Association confidence: 91%."

Always distinguish:
- data-backed observation
- AI/investigative lead
- legal conclusion

Never claim the system proves guilt.

### 12. Data

For this prototype, DO NOT build PostgreSQL, Neo4j or blockchain yet.

Use a small local JavaScript/JSON dataset.

Keep the data clearly separated so it can later be replaced by APIs/database data.

Example structure:

data/
  cases.json
  entities.json
  relationships.json
  timeline.json
  evidence.json

If keeping the prototype even smaller, a single local data file is acceptable.

Use around 15–30 entities and enough relationships to make the graph interesting.

### 13. Future architecture

The prototype is only the UI/UX demonstration.

The eventual architecture is:

Raw fragmented/synthetic data
→ Data ingestion
→ Cleaning / parsing / OCR where necessary
→ Normalization
→ Validation
→ Canonical structured data
→ NLP / NER
→ Relation extraction
→ Entity resolution
→ Confidence scoring
→ Neo4j knowledge graph
→ Graph analytics
→ Investigator UI
→ Evidence provenance / blockchain audit layer

The eventual system will simulate fragmented sources such as:
- CCTNS/FIR data
- CDR/telecom data
- Bank/financial transactions
- CCTV observations
- VAHAN/vehicle records
- Identity/address records
- Social intelligence
- Forensic records
- Case diary/evidence records

### 14. Technology for prototype

Prefer the simplest setup that works locally.

Recommended:
- HTML/CSS/JavaScript OR React if already convenient
- SVG/Canvas/network graph library if useful
- Local JSON data

Do NOT install a large technology stack just for the prototype.

The prototype must run locally on the laptop.

### 15. Coding behaviour for Antigravity

Before writing code:
1. Inspect the existing project directory.
2. Read this file completely.
3. Keep the prototype small.
4. Do not add unnecessary dependencies.
5. Do not build the full SIH backend yet.
6. Do not use real personal/government data.
7. Keep synthetic data obvious and fictional.
8. Keep components modular enough to extend later.
9. Make the UI functional, not just a static mockup.
10. Test the application locally after implementation.
11. Fix errors before declaring completion.

### 16. Important future team architecture

There will eventually be three developers:

Sanjay:
- Core architecture
- AI/NLP
- entity resolution
- investigation logic
- integration
- can modify any part of the project

Shashvat:
- Frontend
- UI/UX
- graph visualization
- dashboard
- timeline
- interaction design

Anish:
- Data
- synthetic data generation
- ingestion/ETL
- cleaning/normalization
- PostgreSQL
- Neo4j
- backend APIs

The full project will later use API contracts and Git branches so the three developers can work independently.

### 17. Prototype success criteria

The prototype is successful if a teammate can open it and understand this story without explanation:

1. I am an investigator.
2. I see India and active cases.
3. I choose a case.
4. I see the entities connected to the case.
5. I click a person/phone/vehicle/account/location.
6. I understand why the entity is connected.
7. I can see when/where the activity happened.
8. I can see an AI-generated investigative summary.
9. I can ask the small assistant a question.
10. I understand that the final system will eventually replace the local synthetic data with a proper ingestion + AI + graph + provenance backend.

### 18. First task

BUILD ONLY THIS PROTOTYPE.

Do not attempt to implement the complete SIH system.

After implementation:
- run it locally
- verify navigation
- verify graph interaction
- verify node details
- verify timeline
- verify chatbot interaction
- verify responsive layout
- report exactly how to run it locally
