# PROMPT_FOR_SHASWAT.md — Frontend Integration Handoff

> **Role**: Shaswat (Frontend & UI/UX Lead)  
> **Repository Clearance**: `frontend/`, UI assets, styling, and visual components  
> **Primary Branch**: `shaswat-frontend`  
> **Live API URL**: `http://localhost:8000/api/v1`

---

## 1. Project State & What Has Been Done
Anish and Sanjay have completed and committed the entire backend, data layer, AI engine, graph analytics, digital evidence provenance system, and forensic database expansion:
- **Live REST API**: The FastAPI backend is fully operational at `http://localhost:8000/api/v1` and adheres strictly to `docs/API_CONTRACT.md`.
- **Reference Prototype Included**: Complete React + Vite command center in `frontend/` with India Map, Cytoscape network graph, chronological timeline, entity inspector drawer, AI assistant drawer, and BSA 2023 Section 63 certificate modal.

---

## 2. API Endpoints Available
- `GET /api/v1/states`: State-level case counts and map coordinates.
- `GET /api/v1/cases?state=DL`: Case cards and incident metadata.
- `GET /api/v1/cases/DL-2026-0412/graph`: Cytoscape nodes and edges with centrality metrics.
- `GET /api/v1/cases/DL-2026-0412/timeline`: Chronological multi-source event list.
- `GET /api/v1/cases/DL-2026-0412/entities/{id}`: Detailed entity profile and provenance hash.
- `POST /api/v1/cases/DL-2026-0412/query`: AI assistant natural language query endpoint.
- `GET /api/v1/cases/DL-2026-0412/provenance/verify`: Section 63 BSA 2023 evidence custody verification.
- `GET /api/v1/cases/DL-2026-0412/forensics/overview`: 8-discipline forensic overview and chain of custody.
