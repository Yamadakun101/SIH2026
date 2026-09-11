# KavachNet — SIH 2026, PS #26189
**AI-Powered Criminal Network Analysis System**

Ministry of Home Affairs → National Crime Records Bureau (NCRB), Women Safety Division
Category: Software · Theme: Blockchain & Cybersecurity

> Turn fragmented, multi-source crime data into a living, tamper-evident knowledge graph — AI to find the hidden connections, blockchain to preserve evidence integrity so it can survive a courtroom.

**Read this file before writing any code.** If you're an AI coding agent (Antigravity, Claude Code, etc.), this is your entry point — read it in full, then read your agent-specific file (`AGENT_SANJAY.md`, `AGENT_SHASWAT.md`, or `AGENT_ANISH.md`) before touching anything.

---

## 1. What this system is

An investigative intelligence tool that ingests fragmented crime data (FIRs, CDRs, financial records, CCTV, vehicle records, social intel, forensic reports), extracts entities and relationships with AI/NLP, builds a knowledge graph, runs graph analytics to surface key players and suspicious patterns, reconstructs timelines, and hashes every piece of evidence to a tamper-evident ledger so the chain of custody holds up in court under **Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63**.

## 2. Core principle — read this twice

This is an **investigative lead-generation system, not a verdict machine.** It surfaces relationships, patterns, anomalies, and timelines for a human investigator to check — it never declares guilt.

- ✅ "Investigative Lead", "Possible Central Network Entity", "Association Confidence: 94%", "AI-generated observation"
- ❌ "Criminal: Yes", "Guilty", or anything that reads as a legal conclusion

This applies everywhere: UI copy, code comments, commit messages, AI-generated summaries, and the pitch deck. It's not just an ethics call — it's also what makes this system legally and practically defensible.

## 3. Data rules

- **All prototype/demo data is synthetic and fabricated. Never use real personal data, and never model a real identifiable person** — including real unsolved-case victims. (Real cases are referenced only in the *pitch deck's* research section as public-record background, never as data the system ingests or "solves.")
- Never discard raw values during ingestion — always keep the original alongside the normalized value, with source, record ID, and confidence (see `docs/DATA_SCHEMA.md`, once added).

## 4. Current phase — build this first

**Phase 1: a local, standalone prototype. No backend yet.**

```
India Map → Select State → See Cases → Select Case → Case Workspace
  → Interactive Network Graph → Click Entity
  → Details / Explanation / Source / Confidence / Date / Location
  → Timeline → Mini AI Assistant
```

- Data: local JSON/JS, fabricated to look realistic.
- Stack: React/Vite (or plain HTML/CSS/JS) + an SVG/Canvas or graph-viz library.
- AI assistant: a local rule-based/mock assistant reading the synthetic dataset — **no external AI API needed for Phase 1.**

**Do NOT build yet:** PostgreSQL, Neo4j, blockchain, authentication, the real ML pipeline, or production ingestion/scraping. The goal of Phase 1 is one working, demoable product story — not infrastructure.

Full phase order (2 through 10 — repo foundation, synthetic data generators, real ingestion, AI/NER, Neo4j, FastAPI, connecting the frontend to real APIs, the hash-chain, final demo polish) is documented in the master project doc — ask Sanjay for it if it's not yet copied into `docs/`.

## 5. Canonical demo scenario

**Case `DL-2026-0412` — "Missing Woman — Suspected Trafficking Network," Delhi.**
Fictional entities: **Priya** (missing person), **Rakesh Kumar** (fictional subject / possible central network entity), plus supporting phones, vehicles, accounts, locations, and associates. Use these names consistently across the frontend, the AI assistant's example responses, and synthetic data generators, so demo data lines up everywhere.

*(There's a second scenario, "Peter & Pedro," from earlier pitch-deck research — that one is for the PPT/pitch narrative only, not the coded prototype. Don't mix the two in the codebase.)*

## 6. Team & ownership

Three people code. Everyone else owns the pitch deck, research, and delivery.

| Person | Owns |
|---|---|
| **Sanjay** — Core + AI + Integration (Technical Lead) | Architecture, AI/NLP, entity resolution, knowledge-graph logic, blockchain/provenance, investigation logic, integration, testing, final technical calls. Has access to everything. |
| **Shaswat** — Frontend + UI/UX | React app, India map, case list, graph visualization, node interaction, timeline UI, AI assistant UI, evidence/provenance screens, navigation. Owns `frontend/`. |
| **Anish** — Data + Backend | Synthetic data generation, ingestion/ETL, PostgreSQL, Neo4j, backend APIs, database architecture. Owns `data/` and `backend/`. |

**Shared contract files (`docs/API_CONTRACT.md`, `docs/DATA_SCHEMA.md`) should never be silently changed** — see §8.

## 7. Repo structure (target shape — build it out as phases require it)

```
SIH2026/
├── README.md                  ← this file
├── AGENT_SANJAY.md
├── AGENT_SHASWAT.md
├── AGENT_ANISH.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_CONTRACT.md
│   ├── DATA_SCHEMA.md
│   └── DEVELOPMENT_RULES.md
├── backend/
├── frontend/
├── ai/
├── data/
├── graph/
├── blockchain/
└── tests/
```

## 8. Working rules — everyone, every session

1. Synthetic data only. No real personal data, ever.
2. Never declare guilt — see §2.
3. Preserve provenance on every ingested record.
4. Always show/explain confidence scores — no black-box matches.
5. Never silently break the API contract (`docs/API_CONTRACT.md`).
6. Read the architecture doc before making a cross-component change.
7. Keep code modular; prefer working vertical slices over building each layer in isolation.
8. Test after every change.
9. Don't over-engineer the MVP — build what the current phase needs, not the full future architecture.
10. Shaswat's agent: frontend only, use documented APIs, never invent endpoints, don't touch backend.
11. Anish's agent: data/backend only, follow the API contract, don't silently break frontend assumptions.
12. Sanjay's agent: may touch anything, but checks cross-component impact first.
13. Major API/schema/architecture changes must be explicit and communicated to the whole team, not just committed quietly.
14. The final UI must be usable by an investigator with zero technical training.

## 9. Git workflow

```
main
├── sanjay-core
├── shaswat-frontend
└── anish-backend
```
```
branch → code → test → commit → push → Pull Request → review → merge
```
Git handles code sync. It does **not** handle architecture compatibility — that's what `docs/API_CONTRACT.md` is for. Keep it current.

## 10. Tech stack (target — see §4 for what Phase 1 actually needs)

Python + FastAPI · Pandas · spaCy / HuggingFace Transformers · IndicNER (AI4Bharat) · PostgreSQL · Neo4j + Graph Data Science · React · Cytoscape.js / D3.js · Docker · Git/GitHub · a Python hash-chain now, Hyperledger Fabric as the cited production direction.

## 11. Success criteria

A teammate should understand the product with zero technical explanation: open it → see India and active cases → pick a state → pick a case → see connected entities → click one → understand why it's connected, when/where it happened, and how confident the system is → read an AI-generated summary → ask the assistant a follow-up question → understand this is a synthetic preview of a system that will run on real ingestion, real AI, a real graph, and real evidence provenance.

**Build one investigation experience, not a pile of technologies.** The demo should make a judge think: *"I have fragmented information from many sources — this cleans it, connects it, explains it, and keeps a provable record of how it got there."*
