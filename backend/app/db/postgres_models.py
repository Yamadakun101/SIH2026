from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Text, JSON, ForeignKey, Boolean
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CaseModel(Base):
    __tablename__ = "cases"

    case_id = Column(String(64), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    state_code = Column(String(10), index=True, nullable=False)
    state_name = Column(String(100), nullable=False)
    status = Column(String(50), default="ACTIVE_INVESTIGATION")
    priority = Column(String(20), default="CRITICAL")
    incident_date = Column(DateTime, nullable=False)
    lead_agency = Column(String(255))
    fir_number = Column(String(100), unique=True, index=True)
    total_entities_identified = Column(Integer, default=0)
    total_evidence_records = Column(Integer, default=0)
    summary = Column(Text)
    bsa_section_63_verified = Column(Boolean, default=True)
    merkle_root = Column(String(64))

    # Relationships
    raw_records = relationship("RawEvidenceModel", back_populates="case", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEventModel", back_populates="case", cascade="all, delete-orphan")
    audit_blocks = relationship("AuditBlockModel", back_populates="case", cascade="all, delete-orphan")

class RawEvidenceModel(Base):
    __tablename__ = "raw_evidence_records"

    record_id = Column(String(64), primary_key=True, index=True)
    case_id = Column(String(64), ForeignKey("cases.case_id"), index=True, nullable=False)
    source_type = Column(String(30), index=True, nullable=False)  # FIR, CDR, BANK, CCTV_ANPR, HOTEL, FORENSIC
    ingested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ingested_by_badge = Column(String(50), nullable=False)
    raw_content = Column(JSON, nullable=False)
    sha256_hash = Column(String(64), index=True, nullable=False)
    block_height = Column(Integer, default=1)
    previous_hash = Column(String(64))

    case = relationship("CaseModel", back_populates="raw_records")

class TimelineEventModel(Base):
    __tablename__ = "timeline_events"

    event_id = Column(String(64), primary_key=True, index=True)
    case_id = Column(String(64), ForeignKey("cases.case_id"), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), index=True, nullable=False)
    source_record_id = Column(String(64))
    location = Column(String(255))
    involved_entities = Column(JSON, default=list)
    description = Column(Text)
    confidence = Column(Float, default=1.0)

    case = relationship("CaseModel", back_populates="timeline_events")

class AuditBlockModel(Base):
    __tablename__ = "audit_blocks"

    block_index = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(64), ForeignKey("cases.case_id"), index=True, nullable=False)
    record_id = Column(String(64), nullable=False)
    sha256 = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    officer_badge = Column(String(50), nullable=False)
    status = Column(String(20), default="VALID")

    case = relationship("CaseModel", back_populates="audit_blocks")
