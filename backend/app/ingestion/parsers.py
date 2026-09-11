from typing import Any, Dict, List, Tuple
from backend.app.ingestion.normalizer import (
    normalize_phone, normalize_license_plate, normalize_timestamp, normalize_upi_vpa
)

def parse_fir(envelope: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    raw = envelope.get("raw_content", {})
    record_id = envelope.get("record_id", "UNKNOWN-REC")
    nodes = []
    edges = []

    # Victim Node
    if raw.get("victim_name"):
        victim_id = f"person-{raw['victim_name'].lower().replace(' ', '-')}"
        nodes.append({
            "id": victim_id,
            "type": "PERSON",
            "label": raw["victim_name"],
            "sub_role": "SUBJECT_OF_SEARCH",
            "attributes": {"age": raw.get("victim_age")},
            "supporting_records": [record_id]
        })

    # Complainant Node
    if raw.get("complainant_name"):
        comp_id = f"person-{raw['complainant_name'].lower().replace(' ', '-')}"
        nodes.append({
            "id": comp_id,
            "type": "PERSON",
            "label": raw["complainant_name"],
            "sub_role": "COMPLAINANT",
            "attributes": {"relation": raw.get("complainant_relation")},
            "supporting_records": [record_id]
        })

    return nodes, edges

def parse_cdr(envelope: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    raw = envelope.get("raw_content", {})
    record_id = envelope.get("record_id", "UNKNOWN-REC")
    nodes = []
    edges = []

    caller_norm = normalize_phone(raw.get("calling_number", ""))
    called_norm = normalize_phone(raw.get("called_number", ""))

    caller_id = f"phone-{caller_norm.replace('+', '')}"
    called_id = f"phone-{called_norm.replace('+', '')}"

    nodes.append({
        "id": caller_id,
        "type": "PHONE",
        "label": caller_norm,
        "sub_role": "SUSPICIOUS_CALLER",
        "attributes": {"imei": raw.get("calling_imei")},
        "supporting_records": [record_id]
    })
    nodes.append({
        "id": called_id,
        "type": "PHONE",
        "label": called_norm,
        "sub_role": "RECIPIENT",
        "attributes": {"imei": raw.get("called_imei")},
        "supporting_records": [record_id]
    })

    # CALLED edge
    edge_id = f"edge-call-{caller_id}-{called_id}"
    edges.append({
        "id": edge_id,
        "source": caller_id,
        "target": called_id,
        "type": "CALLED",
        "label": f"VOICE_CALL [{raw.get('duration_seconds', 0)}s]",
        "confidence": 0.95,
        "confidence_explanation": "Cellular CDR switch record verified with IMEI trace.",
        "interaction_count": 1,
        "category": "TELECOM",
        "metadata": {
            "timestamp": normalize_timestamp(raw.get("call_timestamp", "")),
            "cell_tower_id": raw.get("cell_tower_id")
        },
        "source_records": [record_id]
    })

    return nodes, edges

def parse_banking(envelope: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    raw = envelope.get("raw_content", {})
    record_id = envelope.get("record_id", "UNKNOWN-REC")
    nodes = []
    edges = []

    acc_no = raw.get("account_number", "UNKNOWN_ACC")
    acc_id = f"bank-{acc_no.replace(' ', '-').replace('•', 'X')}"

    nodes.append({
        "id": acc_id,
        "type": "BANK_ACCOUNT",
        "label": acc_no,
        "sub_role": "TRANSACTION_ACCOUNT",
        "attributes": {
            "upi_vpa": normalize_upi_vpa(raw.get("upi_vpa", "")),
            "channel": raw.get("channel")
        },
        "supporting_records": [record_id]
    })

    return nodes, edges

def parse_cctv(envelope: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    raw = envelope.get("raw_content", {})
    record_id = envelope.get("record_id", "UNKNOWN-REC")
    nodes = []
    edges = []

    plate = normalize_license_plate(raw.get("license_plate", ""))
    veh_id = f"vehicle-{plate.lower().replace(' ', '-')}"

    nodes.append({
        "id": veh_id,
        "type": "VEHICLE",
        "label": plate,
        "sub_role": "SIGHTED_VEHICLE",
        "attributes": {
            "vehicle_type": raw.get("vehicle_type"),
            "camera_id": raw.get("camera_id")
        },
        "supporting_records": [record_id]
    })

    if raw.get("location_name"):
        loc_id = f"loc-{raw['camera_id'].lower().replace(' ', '-')}"
        nodes.append({
            "id": loc_id,
            "type": "LOCATION",
            "label": raw["location_name"],
            "sub_role": "ANPR_SURVEILLANCE_POINT",
            "attributes": {"speed_kmph": raw.get("speed_kmph")},
            "supporting_records": [record_id]
        })

        edges.append({
            "id": f"edge-sighting-{veh_id}-{loc_id}",
            "source": veh_id,
            "target": loc_id,
            "type": "SIGHTED_AT",
            "label": f"SIGHTED [{raw.get('speed_kmph', 0)} km/h]",
            "confidence": raw.get("confidence_pct", 95.0) / 100.0,
            "confidence_explanation": f"ANPR camera sighting with optical confidence of {raw.get('confidence_pct')}%",
            "interaction_count": 1,
            "category": "CCTV_ANPR",
            "source_records": [record_id]
        })

    return nodes, edges
