# AGENT_SANJAY.md — Technical Lead & Core AI/Graph/Provenance Architecture

> **Role**: Sanjay (Technical Lead — Core, AI, Graph Logic, Provenance & Integration)  
> **Repository Clearance**: Full Access across all directories (`ai/`, `graph/`, `blockchain/`, `backend/`, `frontend/`, `data/`, `tests/`)  
> **Primary Branches**: `sanjay-core` (feature development), `main` (merges)

---

## 1. Responsibilities & Scope

As Technical Lead, Sanjay is responsible for the overall technical coherence, core algorithms, evidence integrity guarantees, and end-to-end integration:

1. **System Architecture & Data Flow**: Ensure all components (Ingestion → AI/NER → Knowledge Graph → Provenance Hash-chain → REST API → Interactive Frontend) adhere to [ARCHITECTURE.md](file:///docs/ARCHITECTURE.md).
2. **AI & Entity Resolution (`ai/`)**:
   - Multi-source entity extraction from raw unstructured text (FIRs, police logs, transcripts) using spaCy / Transformers / IndicNER concepts.
   - Entity disambiguation & fuzzy resolution (e.g., matching aliases, phone number formatting, vehicle plate normalization).
   - Confidence scoring algorithms for associations and extracted relationships.
3. **Graph Analytics & Intelligence Engine (`graph/`)**:
   - Graph modeling (Entities as Nodes, Interactions as Edges).
   - Centrality metrics computation (Betweenness, Degree, PageRank) to surface "Possible Central Network Entities" / key network facilitators.
   - Community detection (Louvain / Label Propagation) to uncover isolated syndicates.
   - Shortest-path and suspicious flow pathfinding between victims, suspects, and bank accounts.
4. **Evidence Provenance & BSA 2023 Section 63 (`blockchain/`)**:
   - SHA-256 Merkle hash-chain implementation for tamper-evident digital evidence custody.
   - Cryptographic timestamping and immutable audit log generation.
   - Certificate of Evidence Integrity generation complying with Indian evidentiary standards (**Bharatiya Sakshya Adhiniyam, 2023 - Section 63**).
5. **Integration & API Bridge**:
   - Connecting Anish's backend data & endpoints (`backend/`, `data/`) with Shaswat's frontend visualization (`frontend/`).
   - Maintaining mock datasets and test fixtures for Phase 1 local execution.

---

## 2. Core Operational Principles

1. **Lead Generation, Never Verdicts**:
   - All AI summaries and graph scores must use investigative terminology: *"Investigative Lead"*, *"High Centrality Node"*, *"Suggested Association (Confidence: 91%)"*.
   - Never output legal verdicts or words like *"Guilty"* or *"Convicted Criminal"*.
2. **Synthetic Data Integrity**:
   - Ensure all demo datasets strictly use fictional entities (Canonical case `DL-2026-0412`: Priya, Rakesh Kumar, Vikram Singh, etc.).
3. **Cross-Component Review**:
   - Before modifying any shared API or data schema, verify with [API_CONTRACT.md](file:///docs/API_CONTRACT.md) and [DATA_SCHEMA.md](file:///docs/DATA_SCHEMA.md) to ensure Shaswat and Anish are not blocked.

---

## 3. Directory Layout Owned / Supervised

```
SIH2026/
├── ai/
│   ├── ner_extractor.py          # Entity & relation extraction pipeline
│   ├── entity_resolution.py      # Disambiguation & cross-source linking
│   └── assistant_engine.py       # Rule-based / NLP investigative assistant
├── graph/
│   ├── graph_builder.py          # NetworkX / Neo4j graph generator
│   ├── centrality_analytics.py   # PageRank, Betweenness centrality
│   └── syndicate_clustering.py   # Community detection
├── blockchain/
│   ├── hash_chain.py             # SHA-256 Merkle chain implementation
│   ├── custody_ledger.py         # Evidence custody logger
│   └── bsa_certificate.py        # Section 63 compliance generator
└── tests/
    ├── test_graph_analytics.py
    ├── test_entity_resolution.py
    └── test_hash_chain.py
```

---

## 4. Immediate Phase 1 Directives

- [x] Establish repository baseline and shared team documentation.
- [ ] Create Python prototype / standalone JSON mock graph for canonical case `DL-2026-0412`.
- [ ] Validate mock graph schema with Shaswat's React Cytoscape.js component.
- [ ] Implement local evidence hash-chain verification logic for the frontend inspector.
