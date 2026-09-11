from pathlib import Path
from backend.app.ingestion.envelope import create_envelope, verify_envelope
from backend.app.ingestion.engine import IngestionEngine
from backend.app.ingestion.normalizer import (
    normalize_phone, normalize_license_plate, normalize_timestamp, normalize_upi_vpa
)

def test_normalization_functions():
    assert normalize_phone("9871044219") == "+919871044219"
    assert normalize_phone("+91 98710 44219") == "+919871044219"
    assert normalize_phone("09871044219") == "+919871044219"

    assert normalize_license_plate("dl01ab9921") == "DL 01 AB 9921"
    assert normalize_license_plate("DL-01-AB-9921") == "DL 01 AB 9921"

    assert normalize_timestamp("2026-09-02T22:30:00Z") == "2026-09-02T22:30:00Z"
    assert normalize_upi_vpa("  RkEnterprises@OkHdfc  ") == "rkenterprises@okhdfc"

def test_envelope_tamper_evident_seal():
    raw_sample = {"caller": "+919871044219", "receiver": "+919811200341", "duration": 142}
    env = create_envelope(source_type="CDR", raw_content=raw_sample, badge_id="DP-INV-301")
    
    # Genuine envelope should verify
    assert verify_envelope(env) is True

    # Tampered envelope (modified duration) should fail verification
    tampered_env = dict(env)
    tampered_env["raw_content"] = {"caller": "+919871044219", "receiver": "+919811200341", "duration": 999}
    assert verify_envelope(tampered_env) is False

def test_ingestion_engine_batch():
    engine = IngestionEngine()
    raw_dir = Path("data/raw")
    stats = engine.ingest_directory(raw_dir)

    assert stats["records_processed"] >= 30
    assert stats["tamper_check_failures"] == 0
    assert stats["unique_nodes_extracted"] >= 10
    assert stats["unique_edges_extracted"] >= 4
