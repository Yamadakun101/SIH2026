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
   ├── Interactive D3 Entity / Nexus Graph (Drag, Zoom, Filter, Click)
   ├── Entity Inspection Drawer (Stored details, confidence %, why connected, sources, AI explanation)
   ├── Chronological Timeline (Multi-source telecom, CCTV, FastTag, and banking events)
   ├── Evidence Provenance Log (Multi-agency audit trail ready for blockchain)
   └── Case-Aware AI Reasoning Assistant (Interactive Q&A on synthetic knowledge graph)
```

---

### How to Run Locally

You can run this prototype using Python's built-in HTTP server or Node.js:

#### Option 1: Using Python
```bash
python -m http.server 8000
```
Then open [http://localhost:8000](http://localhost:8000) in your browser.

#### Option 2: Using Node.js (npx)
```bash
npx serve -l 8000 .
```
Then open [http://localhost:8000](http://localhost:8000) in your browser.

#### Option 3: Direct File Opening
You can also directly double-click `index.html` to open it in Google Chrome, Microsoft Edge, or Mozilla Firefox.

---

### File Structure
```
SIH2026-Prototype/
├── index.html          # Main application structure and views
├── css/
│   └── style.css       # Clean light-themed design system (DataWalk-inspired)
├── js/
│   ├── data.js         # Synthetic dataset (cases, entities, links, timeline, AI rules)
│   ├── map.js          # Interactive SVG India Map with state pins & case selectors
│   ├── graph.js        # Interactive D3.js Force-Directed Entity Network Graph
│   ├── timeline.js     # Chronological multi-sensor event stream
│   ├── assistant.js    # Case-aware AI reasoning assistant
│   └── app.js          # Application coordinator & state controller
├── README.md           # Documentation and run instructions
└── SIH2026_ANTIGRAVITY_PROTOTYPE_CONTEXT.md
```
