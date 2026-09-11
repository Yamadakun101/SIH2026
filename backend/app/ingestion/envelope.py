import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

def compute_sha256(content: Any) -> str:
    """Computes a deterministic SHA-256 hash over dictionary or string content."""
    if isinstance(content, dict) or isinstance(content, list):
        serialized = json.dumps(content, sort_keys=True, separators=(',', ':'), default=str)
    elif isinstance(content, str):
        serialized = content
    else:
        serialized = str(content)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def create_envelope(
    source_type: str,
    raw_content: Dict[str, Any],
    badge_id: str = "DL-INV-301",
    record_id: Optional[str] = None,
    block_height: int = 1,
    previous_hash: str = "0000000000000000000000000000000000000000000000000000000000000000"
) -> Dict[str, Any]:
    """
    Wraps raw evidentiary content in canonical envelope preserving digital chain-of-custody
    under Section 63 of Bharatiya Sakshya Adhiniyam (BSA) 2023.
    """
    if not record_id:
        timestamp_prefix = datetime.now(timezone.utc).strftime("%Y%m%d")
        record_id = f"REC-{source_type}-{timestamp_prefix}-{uuid.uuid4().hex[:6].upper()}"

    ingested_at = datetime.now(timezone.utc).isoformat()
    record_hash = compute_sha256(raw_content)

    return {
        "record_id": record_id,
        "source_type": source_type,
        "ingested_at": ingested_at,
        "ingested_by_badge": badge_id,
        "raw_content": raw_content,
        "provenance": {
            "sha256_hash": record_hash,
            "block_height": block_height,
            "previous_hash": previous_hash
        }
    }

def verify_envelope(envelope: Dict[str, Any]) -> bool:
    """Verifies that the raw_content matches the recorded SHA-256 provenance hash."""
    expected_hash = envelope.get("provenance", {}).get("sha256_hash")
    if not expected_hash:
        return False
    actual_hash = compute_sha256(envelope.get("raw_content", {}))
    return expected_hash == actual_hash
