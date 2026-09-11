# AGENT_ANISH.md — Data Engineering & Backend API Architecture

> **Role**: Anish (Data & Backend Lead)  
> **Repository Clearance**: `data/`, `backend/`, database schemas, and data ingestion pipelines  
> **Primary Branch**: `anish-backend`

---

## 1. Responsibilities & Scope

Anish is responsible for multi-source synthetic data modeling, realistic log generation, ingestion pipelines (ETL), relational & graph databases, and high-performance REST APIs:

1. **Synthetic Data Generation (`data/`)**:
   - Fabricate realistic, multi-source synthetic crime logs for canonical case `DL-2026-0412` (*"Missing Woman — Suspected Trafficking Network"*, Delhi).
   - Generate realistic data records across 6 investigative sources:
     - 📜 **FIR Records**: Incident reports, complainant statements, witness statements.
     - 📞 **Call Detail Records (CDRs)**: Originating & terminating numbers, IMEI/IMSI, cell tower IDs, call duration, timestamp.
     - 💳 **Banking / UPI / Hawala Records**: P2P transfers, merchant payments, rapid cash withdrawals.
     - 📹 **CCTV & ANPR Logs**: License plate sightings, timestamped junction passes.
     - 🏨 **Hotel / Lodge Registers**: Check-in logs, guest name, contact provided.
     - 🔬 **Forensic & Cyber Reports**: Device extraction summaries, deleted message traces.
2. **Data Normalization & Ingestion Engine (`backend/ingestion/`)**:
   - Clean and normalize heterogeneous data streams.
   - Extract raw entities into the canonical schema defined in [DATA_SCHEMA.md](file:///docs/DATA_SCHEMA.md).
   - Attach unique `record_id`, `source_type`, `ingestion_timestamp`, and `sha256_hash` to every raw record.
3. **Database Architecture**:
   - **PostgreSQL**: Stores relational metadata, raw evidentiary logs, audit trails, and user sessions.
   - **Neo4j**: Stores the active knowledge graph (Nodes, Edges, Properties, Centrality weights).
4. **Backend REST APIs (`backend/api/`)**:
   - Implement FastAPI backend strictly adhering to [API_CONTRACT.md](file:///docs/API_CONTRACT.md).
   - Serve graph query payloads optimized for Cytoscape.js (`nodes`, `edges`, `metrics`).
   - Deliver timeline event streams and deep entity inspection endpoints.
5. **Phase 1 Static Data Asset**:
   - Provide the standalone, fully validated JSON data asset `data/dl-2026-0412.json` so Shaswat and Sanjay can run the prototype immediately without database dependencies.

---

## 2. Technical Stack & Tools

- **Language**: Python 3.10+
- **Framework**: FastAPI + Uvicorn
- **Data Processing**: Pandas, Pydantic v2, Faker (configured for Indian names/addresses/phones)
- **Databases**:
  - PostgreSQL (via SQLAlchemy / asyncpg)
  - Neo4j Community Edition (via `neo4j-python-driver`)
- **API Spec**: OpenAPI 3.0 / Swagger

---

## 3. Directory Layout (`backend/` & `data/`)

```
SIH2026/
├── data/
│   ├── raw/                  # Simulated raw inputs (firs/, cdrs/, cctv/, bank/)
│   ├── generators/           # Python Faker scripts to generate case data
│   └── dl-2026-0412.json     # Canonical synthesized case JSON
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── api/              # Route controllers (/cases, /graph, /timeline, etc.)
│   │   ├── core/             # Config, security, database connectors
│   │   ├── models/           # SQLAlchemy & Pydantic models
│   │   ├── ingestion/        # Multi-source parsers (FIR, CDR, Bank, CCTV)
│   │   └── services/         # Graph query service, Evidence hash service
│   ├── requirements.txt
│   └── Dockerfile
└── tests/
    └── test_api_endpoints.py
```

---

## 4. Phase 1 Implementation Checklist

- [x] Create `data/dl-2026-0412.json` containing the complete synthetic network for Priya, Rakesh Kumar, Vikram, and associate nodes.
- [x] Validate that all nodes and edges have proper IDs, source records, and confidence scores matching [DATA_SCHEMA.md](file:///docs/DATA_SCHEMA.md).
- [x] Scaffold the basic FastAPI project structure in `backend/`.
- [x] Implement mock endpoints matching [API_CONTRACT.md](file:///docs/API_CONTRACT.md).
