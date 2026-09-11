# PROMPT_FOR_SHASWAT.md — Frontend Integration Handoff

> **Role**: Shaswat (Frontend & UI/UX Lead)  
> **Repository Clearance**: `frontend/`, UI assets, styling, and visual components  
> **Primary Branch**: `shaswat-frontend`  
> **Live API URL**: `http://localhost:8001/api/v1`

---

## 1. Project State & What Has Been Done
Anish and Sanjay have completed and committed the entire backend, data layer, AI engine, graph analytics, and digital evidence provenance system to GitHub:
- **Git Branch**: Sanjay has pushed all core deliverables to the `sanjay-core` branch on `https://github.com/Yamadakun101/SIH2026.git`.
- **Live REST API**: The FastAPI backend is fully operational and adheres strictly to `docs/API_CONTRACT.md`. All 29/29 automated tests pass.
- **Reference Prototype Included**: Sanjay's official prototype design and source code are located in `frontend/` (`frontend/index.html`, `frontend/css/style.css`, `frontend/js/`).

---

## 2. Design System & Visual Requirements
- ⚠️ **Strict Visual Guideline**: **DO NOT use a dark command-center theme.**
- Strictly adhere to **Sanjay's existing prototype UI design, color palette, and light professional law-enforcement layout** (`#ffffff`, `#f8fafc`, `#e2e8f0`, `#0f172a`, `#2563eb`, `#dc2626`).
- Reference: `frontend/index.html` and `frontend/css/style.css`.

---

## 3. Shaswat's Scope of Work

Please wire the `frontend/` application to fetch live data from the FastAPI backend at `http://localhost:8001/api/v1`:

1. **National Case Map (`frontend/js/map.js` or React component)**:
   - Fetch live state statistics from `GET /api/v1/states`.
   - Clicking **Delhi (DL)** opens Case `DL-2026-0412`.

2. **Network Graph Canvas (`frontend/js/graph.js` or React component)**:
   - Fetch live Cytoscape/D3 graph payload from `GET /api/v1/cases/{case_id}/graph`.
   - Node sizes scaled dynamically by computed `centrality_score` (highlighting Rakesh Kumar as key facilitator).
   - Distinct icons for **Person**, **Phone**, **Vehicle**, **Bank Account**, **Location**.
   - Clicking any node opens the **Inspector Panel**.

3. **Entity Inspector Panel (`frontend/js/app.js`)**:
   - Slide-over card fetching details from `GET /api/v1/cases/{case_id}/entities/{entity_id}`.
   - Shows extracted confidence score, connected links, source records, and SHA-256 digital stamp.

4. **Multi-Source Chronological Timeline (`frontend/js/timeline.js`)**:
   - Fetch event feed from `GET /api/v1/cases/{case_id}/timeline`.
   - Filter by source (Telecom, Banking, Surveillance, FIR).

5. **AI Investigative Assistant Chat (`frontend/js/assistant.js`)**:
   - Connect chat input to `POST /api/v1/cases/{case_id}/query`.
   - Display AI answers with highlighted citations and suggested investigative actions.

6. **BSA 2023 Section 63 Evidence Certificate Modal**:
   - Fetch verification payload from `GET /api/v1/cases/{case_id}/provenance/verify`.
   - Display court-admissible certificate with unbroken Merkle hash chain and certifying officer badge.

---

## 4. Getting Started (Git Commands)
```bash
git checkout shaswat-frontend
git merge origin/sanjay-core
```
Backend is running at `http://localhost:8001`. Swagger documentation: `http://localhost:8001/docs`.
