# KavachNet — Canonical Data & Entity Schema

> **Document**: `docs/DATA_SCHEMA.md`  
> **Status**: Standard Reference for Ingestion, AI/NER, Graph Storage, and Frontend Renderers

---

## 1. Raw Ingestion Record Schema

Every raw data file (FIR, CDR, Bank record, CCTV log) ingested into the system must be wrapped in a standardized raw envelope to preserve provenance:

```json
{
  "record_id": "REC-CDR-20260902-8819",
  "source_type": "CDR",
  "ingested_at": "2026-09-02T23:10:00Z",
  "ingested_by_badge": "DL-INV-301",
  "raw_content": {
    "calling_number": "+919871044219",
    "called_number": "+919811200341",
    "call_timestamp": "2026-09-02T21:45:00Z",
    "duration_sec": 142,
    "cell_tower_id": "TOW-DEL-KASHMERE-482",
    "imei": "864201049281720"
  },
  "provenance": {
    "sha256_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
    "block_height": 14,
    "previous_hash": "c89b910123...4fa"
  }
}
```

---

## 2. Entity Schema (Nodes)

Entities extracted by the NLP/NER engine are normalized into the following standard categories:

| Entity Type | Required Fields | Optional / Context Fields |
|---|---|---|
| `PERSON` | `id`, `label` (Full Name), `aliases` | `dob`, `gender`, `sub_role`, `risk_level` |
| `PHONE` | `id`, `phone_number` | `imsi`, `imei`, `carrier`, `is_burner_suspected` |
| `VEHICLE` | `id`, `license_plate` | `vehicle_make`, `color`, `chassis_no`, `registered_owner` |
| `BANK_ACCOUNT` | `id`, `account_no` | `ifsc`, `bank_name`, `upi_vpa`, `account_holder` |
| `LOCATION` | `id`, `location_name` | `lat`, `lng`, `district`, `state`, `geofence_type` |
| `ORGANIZATION` | `id`, `org_name` | `registration_no`, `org_type` (Shell, Trust, Travel Agency) |

### Entity JSON Structure:
```json
{
  "id": "person-rakesh-kumar",
  "type": "PERSON",
  "label": "Rakesh Kumar",
  "aliases": ["Raka", "RK"],
  "sub_role": "POSSIBLE_CENTRAL_NETWORK_ENTITY",
  "attributes": {
    "known_locations": ["Majnu Ka Tilla", "Kashmere Gate"],
    "flagged_flags": ["Interstate Movement", "Multiple SIM Switches"]
  },
  "metrics": {
    "centrality_score": 0.94,
    "degree": 12,
    "betweenness": 0.88,
    "cluster_id": "syndicate-north-01"
  },
  "supporting_records": [
    "REC-FIR-2026-412",
    "REC-CDR-20260902-8819",
    "REC-BANK-20260902-0041"
  ]
}
```

---

## 3. Relationship Schema (Edges)

Edges represent connections established through evidence. Every edge must explicitly reference its origin source and an explainable confidence value.

| Relationship Type | Source Node | Target Node | Key Attributes |
|---|---|---|---|
| `CALLED` / `MESSAGED` | `PHONE` | `PHONE` | `call_count`, `total_duration`, `time_range` |
| `SUBSCRIBER_OF` | `PERSON` | `PHONE` | `kyc_verified`, `sim_activation_date` |
| `TRANSFERRED_FUNDS` | `BANK_ACCOUNT` | `BANK_ACCOUNT` | `amount_inr`, `tx_hash`, `timestamp`, `channel` (UPI/NEFT) |
| `ACCOUNT_HOLDER` | `PERSON` | `BANK_ACCOUNT` | `confidence`, `branch` |
| `SIGHTED_WITH` | `PERSON` / `VEHICLE`| `LOCATION` / `PERSON` | `timestamp`, `cctv_camera_id`, `anpr_lane` |
| `ASSOCIATE_OF` | `PERSON` | `PERSON` | `association_type`, `inferred_by_ai` (true/false) |

### Edge JSON Structure:
```json
{
  "id": "rel-call-rakesh-priya",
  "source": "person-rakesh-kumar",
  "target": "person-priya",
  "type": "CALLED",
  "label": "FREQUENT_CALLS [14x]",
  "confidence": 0.94,
  "confidence_explanation": "14 direct cellular interactions recorded within 4 hours before disappearance; matching cell tower footprint.",
  "metadata": {
    "interaction_count": 14,
    "first_seen": "2026-09-02T18:10:00Z",
    "last_seen": "2026-09-02T21:45:00Z"
  },
  "source_records": ["REC-CDR-20260902-8819"]
}
```

---

## 4. Timeline Event Schema

```json
{
  "event_id": "evt-20260902-01",
  "case_id": "DL-2026-0412",
  "timestamp": "2026-09-02T21:45:00Z",
  "title": "Last Cellular Activity Detected",
  "category": "TELECOM",
  "severity": "CRITICAL",
  "entities": ["person-priya", "phone-98710xxxxx"],
  "location": {
    "name": "ISBT Kashmere Gate",
    "lat": 28.6672,
    "lng": 77.2285
  },
  "summary": "Victim's primary phone switched off immediately after a 142s call with burner SIM.",
  "source_record_id": "REC-CDR-20260902-8819",
  "sha256_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
}
```

---

## 5. Blockchain / Evidence Provenance Block Schema

```json
{
  "block_index": 14,
  "timestamp": "2026-09-02T23:10:05Z",
  "record_id": "REC-CDR-20260902-8819",
  "record_sha256": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
  "previous_block_hash": "c89b910123ef...4fa",
  "current_block_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "officer_digital_signature": "SIG-ED25519-89a1f2b4c6e8",
  "custody_action": "INGESTION_LOCK"
}
```
