from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db.postgres_models import (
    Base, CaseModel, RawEvidenceModel, TimelineEventModel, AuditBlockModel
)

def test_sqlalchemy_schema_creation_and_crud():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Insert Case
    case = CaseModel(
        case_id="DL-2026-0412",
        title="Missing Woman — Suspected Trafficking Network",
        state_code="DL",
        state_name="Delhi",
        incident_date=datetime(2026, 9, 2, 22, 30, tzinfo=timezone.utc),
        lead_agency="Special Cell / Crime Branch, Delhi Police",
        fir_number="FIR-412/2026/PS-KashmereGate",
        total_entities_identified=18,
        total_evidence_records=84,
        summary="Suspected syndicate involving transport hubs and burner phones."
    )
    session.add(case)
    session.commit()

    # 2. Insert Raw Evidence Record linked to Case
    raw_rec = RawEvidenceModel(
        record_id="REC-CDR-0902-88",
        case_id="DL-2026-0412",
        source_type="CDR",
        ingested_by_badge="DL-INV-301",
        raw_content={"duration": 142},
        sha256_hash="a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
    )
    session.add(raw_rec)
    session.commit()

    # 3. Query back
    fetched_case = session.query(CaseModel).filter_by(case_id="DL-2026-0412").first()
    assert fetched_case is not None
    assert fetched_case.title == "Missing Woman — Suspected Trafficking Network"
    assert len(fetched_case.raw_records) == 1
    assert fetched_case.raw_records[0].record_id == "REC-CDR-0902-88"

    session.close()
