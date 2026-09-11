# KavachNet — Backend / Frontend API Contract

> **Version**: 1.0.0 (Phase 1 Baseline)  
> **Base URL**: `/api/v1`  
> **Status**: Fixed. Do NOT make breaking changes to these payloads without team consensus.

---

## 1. Endpoints Overview

| Method | Path | Description |
|---|---|---|
| `GET` | `/states` | List of states with active case statistics |
| `GET` | `/cases?state={state_code}` | List cases for a given state |
| `GET` | `/cases/{case_id}` | Overview metadata & summary for a single case |
| `GET` | `/cases/{case_id}/graph` | Cytoscape-formatted nodes and edges with metrics |
| `GET` | `/cases/{case_id}/timeline` | Chronological multi-source event sequence |
| `GET` | `/cases/{case_id}/entities/{entity_id}` | Detailed profile & provenance of a specific node |
| `POST` | `/cases/{case_id}/query` | AI investigative assistant query endpoint |
| `GET` | `/cases/{case_id}/provenance/verify` | BSA 2023 Sec 63 digital chain-of-custody verification |

---

## 2. Detailed Schemas & Payloads

### 2.1 `GET /api/v1/states`
**Response (200 OK)**:
```json
[
  {
    "state_code": "DL",
    "state_name": "Delhi",
    "active_cases_count": 4,
    "high_risk_alerts": 2,
    "lat": 28.6139,
    "lng": 77.2090
  },
  {
    "state_code": "MH",
    "state_name": "Maharashtra",
    "active_cases_count": 7,
    "high_risk_alerts": 1,
    "lat": 19.7515,
    "lng": 75.7139
  }
]
```

---

### 2.2 `GET /api/v1/cases?state=DL`
**Response (200 OK)**:
```json
[
  {
    "case_id": "DL-2026-0412",
    "title": "Missing Woman — Suspected Trafficking Network",
    "state_code": "DL",
    "status": "ACTIVE_INVESTIGATION",
    "priority": "CRITICAL",
    "incident_date": "2026-09-02T22:30:00Z",
    "lead_agency": "Special Cell / Crime Branch, Delhi Police",
    "fir_number": "FIR-412/2026/PS-KashmereGate",
    "total_entities_identified": 18,
    "total_evidence_records": 84,
    "summary": "Suspected interstate syndicate involving transport hubs, burner phones, and rapid mule account transactions."
  }
]
```

---

### 2.3 `GET /api/v1/cases/{case_id}/graph`
Returns elements structured directly for **Cytoscape.js**.

**Response (200 OK)**:
```json
{
  "case_id": "DL-2026-0412",
  "elements": {
    "nodes": [
      {
        "data": {
          "id": "person-priya",
          "label": "Priya",
          "type": "PERSON",
          "sub_role": "SUBJECT_OF_SEARCH",
          "centrality_score": 0.42,
          "risk_level": "HIGH",
          "evidence_count": 14,
          "status": "UNRESOLVED_LOCATION",
          "icon": "user-x"
        }
      },
      {
        "data": {
          "id": "person-rakesh",
          "label": "Rakesh Kumar",
          "type": "PERSON",
          "sub_role": "POSSIBLE_CENTRAL_NETWORK_ENTITY",
          "centrality_score": 0.94,
          "risk_level": "CRITICAL",
          "evidence_count": 38,
          "status": "PERSON_OF_INTEREST",
          "icon": "user-alert"
        }
      },
      {
        "data": {
          "id": "phone-98710xxxxx",
          "label": "+91 98710 44219",
          "type": "PHONE",
          "sub_role": "BURNER_SIM",
          "centrality_score": 0.78,
          "evidence_count": 22,
          "icon": "phone-call"
        }
      },
      {
        "data": {
          "id": "vehicle-dl01-9921",
          "label": "DL 01 AB 9921",
          "type": "VEHICLE",
          "sub_role": "SIGHTED_CONVEYANCE",
          "centrality_score": 0.55,
          "evidence_count": 8,
          "icon": "car"
        }
      }
    ],
    "edges": [
      {
        "data": {
          "id": "edge-call-01",
          "source": "person-rakesh",
          "target": "phone-98710xxxxx",
          "label": "SUBSCRIBER_OF",
          "confidence": 0.98,
          "interaction_count": 1,
          "category": "TELECOM"
        }
      },
      {
        "data": {
          "id": "edge-call-02",
          "source": "phone-98710xxxxx",
          "target": "person-priya",
          "label": "FREQUENT_CALLS [14x]",
          "confidence": 0.91,
          "interaction_count": 14,
          "category": "TELECOM"
        }
      }
    ]
  }
}
```

---

### 2.4 `GET /api/v1/cases/{case_id}/timeline`
**Response (200 OK)**:
```json
[
  {
    "event_id": "evt-001",
    "timestamp": "2026-09-02T21:45:00Z",
    "title": "Last Known Mobile Signal",
    "category": "TELECOM",
    "source_record_id": "CDR-REC-9018",
    "location": "ISBT Kashmere Gate, Tower #482",
    "involved_entities": ["person-priya", "phone-98710xxxxx"],
    "description": "Outbound call lasting 142 seconds before mobile tower disconnect.",
    "confidence": 0.95
  },
  {
    "event_id": "evt-002",
    "timestamp": "2026-09-02T22:15:00Z",
    "title": "Vehicle Sighted at Toll Plaza",
    "category": "CCTV_ANPR",
    "source_record_id": "ANPR-LOG-3301",
    "location": "Singhu Border Toll, Lane 4",
    "involved_entities": ["vehicle-dl01-9921", "person-rakesh"],
    "description": "ANPR camera captured vehicle heading north at Singhu Border.",
    "confidence": 0.92
  }
]
```

---

### 2.5 `POST /api/v1/cases/{case_id}/query`
**Request Body**:
```json
{
  "query": "What connects Rakesh Kumar to the vehicle sighted at Singhu Border?"
}
```

**Response (200 OK)**:
```json
{
  "query": "What connects Rakesh Kumar to the vehicle sighted at Singhu Border?",
  "answer": "Rakesh Kumar is connected to vehicle DL 01 AB 9921 through Fastag billing records registered to his associated mobile (+91 98710 44219) and matching ANPR toll camera logs at Singhu Border at 22:15 on 02-Sep-2026.",
  "confidence": 0.94,
  "cited_entities": ["person-rakesh", "vehicle-dl01-9921", "phone-98710xxxxx"],
  "cited_sources": ["ANPR-LOG-3301", "FASTAG-TX-8812"],
  "suggested_actions": [
    "Highlight path between Rakesh Kumar and Vehicle DL 01 AB 9921",
    "Inspect Singhu Border CCTV timeline segment"
  ]
}
```

---

### 2.6 `GET /api/v1/cases/{case_id}/provenance/verify`
**Response (200 OK)**:
```json
{
  "case_id": "DL-2026-0412",
  "status": "VERIFIED_INTACT",
  "bsa_section_63_compliant": true,
  "total_evidence_blocks": 84,
  "genesis_timestamp": "2026-09-02T23:00:00Z",
  "latest_block_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "merkle_root": "8f4e2c1b9a8d7e6f5c4b3a210987654321fedcba0987654321abcdef01234567",
  "audit_trail": [
    {
      "block_index": 1,
      "record_id": "FIR-412/2026",
      "sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
      "timestamp": "2026-09-02T23:05:12Z",
      "officer_badge": "DP-SI-4921",
      "status": "VALID"
    }
  ]
}
```
