from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class CustodyTransferEvent(BaseModel):
    transfer_index: int
    transferred_by: str
    transferred_by_badge: str
    transferred_to: str
    transferred_to_badge: str
    transfer_timestamp: str
    purpose: str
    custody_status: str

class ChainOfCustodyRecord(BaseModel):
    chain_of_custody_id: str
    evidence_id: str
    case_id: str
    collection_officer: str
    collection_officer_badge: str
    collection_timestamp: str
    collection_location: str
    transfer_events: List[CustodyTransferEvent] = Field(default_factory=list)
    storage_location: str
    examination_location: str
    evidence_status: str
    original_hash: str
    current_hash: str
    hash_algorithm: str = "SHA-256"
    integrity_status: str
    bsa_section_63_compliant: bool = True
    report_id: str

class DNAEvidenceRecord(BaseModel):
    evidence_id: str
    case_id: str
    sample_id: str
    sample_type: str
    biological_material: str
    collection_location: str
    collection_timestamp: str
    collection_method: str
    dna_profile_id: str
    str_profile_metadata: Dict[str, Any] = Field(default_factory=dict)
    candidate_entity: Optional[str] = None
    comparison_result: str
    match_confidence: float
    laboratory_id: str
    analyst_id: str
    report_id: str
    examination_date: str
    status: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    integrity_hash: str
    chain_of_custody_id: str

class FingerprintEvidenceRecord(BaseModel):
    evidence_id: str
    fingerprint_id: str
    case_id: str
    surface_or_object: str
    collection_location: str
    collection_timestamp: str
    print_quality: str
    print_type: str
    candidate_entity: Optional[str] = None
    similarity_score: float
    comparison_result: str
    examiner_info: str
    report_id: str
    status: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    integrity_hash: str
    chain_of_custody_id: str

class DigitalForensicRecord(BaseModel):
    evidence_id: str
    device_id: str
    imei: Optional[str] = None
    sim_identifier: Optional[str] = None
    artifact_id: str
    artifact_type: str
    application_source: str
    recovered_data_type: str
    timestamp: str
    location_gps: Optional[Dict[str, Any]] = None
    associated_phone: Optional[str] = None
    associated_entity: Optional[str] = None
    file_metadata: Optional[Dict[str, Any]] = None
    file_hash: Optional[str] = None
    extraction_method: str
    extraction_date: str
    forensic_tool: str
    analyst: str
    report_id: str
    confidence: float
    status: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    integrity_hash: str

class CCTVVideoForensicRecord(BaseModel):
    evidence_id: str
    cctv_event_id: str
    camera_id: str
    case_id: str
    timestamp: str
    location: str
    detected_person: Optional[str] = None
    candidate_entity: Optional[str] = None
    person_similarity_score: Optional[float] = None
    detected_vehicle: Optional[str] = None
    vehicle_similarity_score: Optional[float] = None
    partial_plate: Optional[str] = None
    clothing_attributes: Optional[str] = None
    movement_direction: Optional[str] = None
    entry_exit_info: Optional[str] = None
    frame_reference: str
    analyst_or_system: str
    comparison_result: str
    confidence: float
    report_id: str
    integrity_hash: str
    provenance: Dict[str, Any] = Field(default_factory=dict)

class TraceEvidenceRecord(BaseModel):
    evidence_id: str
    case_id: str
    trace_type: str
    sample_id: str
    collection_location: str
    collection_timestamp: str
    material_characteristics: str
    comparison_candidate: str
    comparison_result: str
    similarity_confidence: float
    laboratory: str
    analyst: str
    report_id: str
    status: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    integrity_hash: str
    chain_of_custody_id: str

class ImpressionEvidenceRecord(BaseModel):
    evidence_id: str
    impression_id: str
    case_id: str
    impression_type: str
    scene_location: str
    timestamp: str
    pattern_characteristics: str
    size_dimensions: str
    tread_characteristics: str
    candidate_vehicle_or_person: Optional[str] = None
    comparison_result: str
    similarity_score: float
    confidence: float
    analyst: str
    report_id: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    integrity_hash: str
    chain_of_custody_id: str

class BallisticsToolmarkRecord(BaseModel):
    evidence_id: str
    case_id: str
    item_id: str
    evidence_type: str
    tool_or_weapon_type: str
    markings: str
    pattern_characteristics: str
    recovered_location: str
    candidate_tool: str
    comparison_result: str
    similarity_confidence: float
    laboratory: str
    analyst: str
    report_id: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    integrity_hash: str
    chain_of_custody_id: str

class CaseForensicsOverview(BaseModel):
    case_id: str
    total_forensic_records: int
    categories_present: List[str]
    dna_evidence: List[DNAEvidenceRecord] = Field(default_factory=list)
    fingerprint_evidence: List[FingerprintEvidenceRecord] = Field(default_factory=list)
    digital_forensics: List[DigitalForensicRecord] = Field(default_factory=list)
    cctv_video_forensics: List[CCTVVideoForensicRecord] = Field(default_factory=list)
    trace_evidence: List[TraceEvidenceRecord] = Field(default_factory=list)
    impression_evidence: List[ImpressionEvidenceRecord] = Field(default_factory=list)
    ballistics_toolmarks: List[BallisticsToolmarkRecord] = Field(default_factory=list)
    chain_of_custody: List[ChainOfCustodyRecord] = Field(default_factory=list)
