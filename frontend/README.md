# CRIMENET-AI — Criminal Network Analysis System
## SIH 2026 Problem Statement PS #26189 — Local Interactive Prototype

A lightweight, clean, light-themed investigator dashboard for multi-modal criminal intelligence, entity resolution, and network graph analysis.

> **Note:** All data used in this prototype is strictly synthetic and fabricated for demonstration purposes.

---

### Core Investigator Workflow
```
National India Map
   │
   ▼ Select State (e.g. Delhi NCR)
Regional Case List
   │
   ▼ Select Case (DL-2026-0412)
Case Intelligence Workspace
   ├── Interactive D3 / Cytoscape Entity Network Graph (Drag, Zoom, Filter, Click)
   ├── Entity Inspection Drawer (Stored details, match %, why connected, sources, AI explanation)
   ├── Chronological Timeline (Multi-source telecom, CCTV, FastTag, and banking events)
   ├── Evidence Provenance Log (BSA 2023 Section 63 Merkle Audit Trail)
   └── Case-Aware AI Reasoning Assistant (Interactive Q&A on synthetic knowledge graph)
```

---

### How to Run Locally

You can run this prototype using Vite or any local HTTP server:

```bash
cd frontend
npm install
npm run dev
```
Then open [http://localhost:5173](http://localhost:5173) in your browser.
