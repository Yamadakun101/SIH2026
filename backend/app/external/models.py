from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class PacketIntegrity(BaseModel):
    algorithm: str = "SHA-256"
    hash: str

class PacketSignature(BaseModel):
    algorithm: str = "Ed25519"
    public_key_hex: str
    value: str

class SecureDataPacket(BaseModel):
    packet_id: str
    request_id: str
    source_system: str
    schema_version: str = "1.0"
    created_at: str
    data: Dict[str, Any]
    integrity: PacketIntegrity
    signature: PacketSignature

class ExternalFetchRequest(BaseModel):
    provider_type: str = Field(..., description="Provider type: CDR, VEHICLE, BANKING, CCTV")
    resource_id: str = Field(..., description="Specific resource key e.g. VEHICLE:DL-01-AB-9921")
    case_id: str = Field(..., description="Target case ID e.g. DL-2026-0412")

class ExternalFetchResponse(BaseModel):
    status: str
    packet_id: str
    request_id: str
    source_system: str
    verified_integrity: bool
    verified_signature: bool
    provenance_record_id: str
    data: Dict[str, Any]
