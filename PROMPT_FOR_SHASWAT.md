# Prompt for Shaswat (Frontend & UI/UX Lead)

Copy and paste the prompt below into Shaswat's Antigravity chat window:

---

```markdown
You are Shaswat, the Frontend & UI/UX Lead for the KavachNet project (SIH 2026, Problem Statement #26189 — AI-Powered Criminal Network Analysis System).

### 1. Current Project State & What Has Already Been Done for You
Anish (Data & Backend Lead) has completed all backend APIs, data models, and synthetic datasets on branch `anish-backend`:
- **Cytoscape-Ready Static Dataset**: `data/dl-2026-0412.json` is completely formatted for Cytoscape.js (`elements: { nodes: [{ data: { ... } }], edges: [{ data: { ... } }] }`). You can import this JSON directly into React for an offline prototype without needing any running database.
- **FastAPI REST API**: If you prefer live HTTP requests, the backend is fully operational at `http://localhost:8000/api/v1` with CORS pre-configured for Vite (`http://localhost:5173`, `5174`, `3000`).
- **API Payloads**: All 8 contract endpoints defined in `docs/API_CONTRACT.md` are live:
  - `GET /api/v1/states`: State-level case counts and map coordinates.
  - `GET /api/v1/cases?state=DL`: Case cards and incident metadata.
  - `GET /api/v1/cases/DL-2026-0412/graph`: Cytoscape nodes and edges with centrality metrics.
  - `GET /api/v1/cases/DL-2026-0412/timeline`: Chronological multi-source event list.
  - `GET /api/v1/cases/DL-2026-0412/entities/{id}`: Detailed entity profile and provenance hash.
  - `POST /api/v1/cases/DL-2026-0412/query`: AI assistant natural language query endpoint.
  - `GET /api/v1/cases/DL-2026-0412/provenance/verify`: Section 63 BSA 2023 evidence custody verification.

### 2. Git & Working Rules
- Your designated branch is `shaswat-frontend`.
- Before beginning, sync or merge the latest work from `origin/anish-backend` into `shaswat-frontend`:
  ```bash
  git checkout shaswat-frontend
  git merge origin/anish-backend
  ```
- Your workspace is exclusively inside `frontend/`. Do NOT touch `backend/`, `data/`, `ai/`, or `blockchain/`.
- Do NOT commit directly to `main`.
- Terminology Rule: All UI copy must read as investigative intelligence (e.g., "Investigative Lead", "Possible Central Network Entity", "Confidence: 94%"). Never display legal verdicts like "Guilty" or "Criminal Confirmed".

### 3. Your Scope of Work (Shaswat's Deliverables)
Please build the frontend application in `frontend/` using **React + Vite** with a sleek, cinematic dark command-center aesthetic (`#0a0f1d`, `#111c38`, `#1e293b`, cyan/indigo accents):

#### Task 1: Project Initialization (`frontend/`)
- Initialize React + Vite project in `frontend/`.
- Install dependencies: `lucide-react`, `cytoscape`, `cytoscape-fcose` (or D3.js).
- Configure CSS / styling with modern typography (Inter / Outfit) and glassmorphism styling.

#### Task 2: India Map & State Selection Landing Screen
- Interactive India Map (SVG / Canvas) or state selector.
- Clicking **Delhi (DL)** opens active cases list showing Case `DL-2026-0412` (*"Missing Woman — Suspected Trafficking Network"*).
- Clicking the case opens the Case Workspace.

#### Task 3: Interactive Cytoscape.js Knowledge Graph Canvas
- Render the nodes and edges from `data/dl-2026-0412.json` (or `GET /api/v1/cases/DL-2026-0412/graph`).
- Distinct node visual styling by type:
  - 👤 **Person**: Priya (Victim/Search), Rakesh Kumar (Central Entity, large node, alert glow), Vikram Singh (Driver).
  - 📱 **Phone**: Burner SIMs, Victim handset.
  - 🚗 **Vehicle**: White Swift Dzire (`DL 01 AB 9921`).
  - 📍 **Location**: ISBT Kashmere Gate, Singhu Border Toll.
  - 🏦 **Bank Account**: Mule Account ••4091.
- Node size scaled by `centrality_score` (e.g. Rakesh Kumar score 0.94 is largest).
- Edge labels displaying interaction type and confidence pill (`94%`).

#### Task 4: Entity Inspector Slide-over Panel
- Clicking any node or edge opens the Inspector Panel on the right.
- Displays: entity label, aliases, centrality score, risk level, confidence explanation, chronological supporting records, and SHA-256 digital custody seal.

#### Task 5: Interactive Timeline Playback Bar
- Scrubbable multi-source event timeline (CDR pings, ATM cash withdrawal, ANPR toll pass at Singhu Border).
- Filtering by category (Telecom, Banking, CCTV, FIR).

#### Task 6: AI Investigative Assistant Drawer & BSA 2023 Certificate Modal
- Floating chat drawer with pre-canned query chips:
  - *"What connects Rakesh Kumar to the vehicle sighted at Singhu Border?"*
  - *"Show timeline of Priya's phone before power off"*
- Structured response cards with cited entities, cited sources, and clickable action buttons.
- BSA 2023 Section 63 Modal displaying digital chain-of-custody verification, Merkle root, and court-admissible certificate summary.

Please inspect `docs/API_CONTRACT.md`, `docs/DATA_SCHEMA.md`, and `data/dl-2026-0412.json`, then initialize `frontend/` and execute Tasks 1 through 6.
```
