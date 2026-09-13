# AGENT_SHASWAT.md — Frontend Lead & UI/UX Architecture

> **Role**: Shaswat (Frontend & UI/UX Lead)  
> **Repository Clearance**: `frontend/`, UI assets, styling, and visual components  
> **Primary Branch**: `shaswat-frontend`

---

## 1. Responsibilities & Scope

Shaswat owns the entire user-facing experience of **KavachNet**. The goal is a clean, cinematic, dark-themed investigative interface usable by law enforcement officers with zero technical background:

1. **Interactive National & State Selection**:
   - High-fidelity interactive India Map (SVG / GeoJSON / Canvas).
   - State-level case breakdown (e.g., Delhi, Maharashtra, Uttar Pradesh) with active case counts and risk indicators.
2. **Case Workspace & Navigation**:
   - Case Selector & Case Header displaying metadata (Case ID: `DL-2026-0412`, Incident Date, Lead Officer, Status, FIR Reference).
   - Multi-tab investigative navigation: **Graph View**, **Timeline View**, **Evidence Matrix / BSA 2023 Audit**, **AI Assistant Drawer**.
3. **Interactive Knowledge Graph Visualization**:
   - Graph engine powered by **Cytoscape.js** or **D3.js**.
   - Custom node types with distinct icons and colors:
     - 👤 **Person** (Suspect / Victim / Associate)
     - 📱 **Phone / SIM** (IMEI, CDR record)
     - 🚗 **Vehicle** (Registration, Toll sighting)
     - 🏦 **Bank Account / Wallet** (Transaction node)
     - 📍 **Location / Geofence** (CCTV sighting / Cell Tower)
     - 🏢 **Organization / Shell Entity**
   - Node sizing scaled by **Centrality Score** (e.g., highlighting key hub entities).
   - Edge labels showing relationship type (e.g., `CALLED [42x]`, `TRANSFERRED ₹2.5L`, `SIGHTED_WITH`) and confidence pill (e.g., `94%`).
4. **Entity Inspector Panel (Slide-over / Modal)**:
   - Deep-dive card triggered when clicking any node or edge.
   - Breakdown of:
     - Entity details & aliases.
     - Extracted confidence score & reasoning ("Why is this node flagged?").
     - Chronological source logs (FIR excerpt, CDR record, Bank statement).
     - Cryptographic SHA-256 evidence stamp.
5. **Interactive Timeline & Playback**:
   - Scrubbable event timeline showing the progression of events leading up to and following the incident.
   - Filter events by source type (Call, Transaction, Sighting, FIR).
6. **AI Investigative Assistant UI**:
   - Conversational floating drawer/sidebar.
   - Pre-canned investigative query chips (e.g., *"Who was in contact with Priya between 10 PM and 2 AM?"*, *"Identify all common financial nodes connected to Rakesh"*).
   - Structured responses with highlighted citations and direct jump-to-node buttons.
7. **BSA 2023 Section 63 Digital Evidence Certificate Modal**:
   - Tamper-evident certificate viewer showing hash verification status, digital signatures, and exportable PDF/Printable court-ready summary.

---

## 2. Technical Stack & Standards

- **Framework**: React (Vite) + TypeScript / JavaScript.
- **Styling**: Modern Vanilla CSS / Tailwind CSS / CSS Modules with a curated dark command-center aesthetic (`#0a0f1d`, `#111c38`, `#1e293b`, cyan/indigo accents).
- **Graph Visualization**: Cytoscape.js (`cytoscape-fcose` or `cose-bilkent` layout) or D3 force simulation.
- **Icons**: Lucide React / Feather Icons.
- **State Management**: React Context or lightweight Zustand.

---

## 3. Directory Layout (`frontend/`)

```
frontend/
├── src/
│   ├── assets/               # Maps, logos, icons
│   ├── components/
│   │   ├── Map/              # India Map & State Case Selectors
│   │   ├── Graph/            # Cytoscape Graph Canvas & Node Controllers
│   │   ├── Inspector/        # Node/Edge Deep Dive & Provenance Cards
│   │   ├── Timeline/         # Chronological Playback Bar
│   │   ├── Assistant/        # AI Investigative Chat Drawer
│   │   └── Certificate/      # BSA 2023 Section 63 Audit Modal
│   ├── data/                 # Phase 1 mock data (DL-2026-0412.json)
│   ├── services/             # API client adhering to docs/API_CONTRACT.md
│   ├── styles/               # Global theme & typography
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
└── vite.config.js
```

---

## 4. Phase 1 Implementation Checklist

- [ ] Initialize React + Vite project in `frontend/`.
- [ ] Implement Phase 1 mock dataset matching [DATA_SCHEMA.md](file:///docs/DATA_SCHEMA.md).
- [ ] Build the landing screen: India Map → Select State (Delhi) → Select Case (`DL-2026-0412`).
- [ ] Render interactive Cytoscape.js network graph for Case `DL-2026-0412`.
- [ ] Connect click events on nodes/edges to the Inspector Panel.
- [ ] Implement local rule-based AI Assistant chat interface.
