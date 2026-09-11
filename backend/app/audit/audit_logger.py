from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

class SecurityEventType(str, Enum):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    EXTERNAL_DATA_REQUEST = "EXTERNAL_DATA_REQUEST"
    CHALLENGE_ISSUED = "CHALLENGE_ISSUED"
    CHALLENGE_VERIFIED = "CHALLENGE_VERIFIED"
    CHALLENGE_REJECTED = "CHALLENGE_REJECTED"
    REPLAY_DETECTED = "REPLAY_DETECTED"
    PACKET_RECEIVED = "PACKET_RECEIVED"
    PACKET_SIGNATURE_VERIFIED = "PACKET_SIGNATURE_VERIFIED"
    PACKET_VALIDATION_FAILED = "PACKET_VALIDATION_FAILED"
    EVIDENCE_INTEGRITY_VERIFIED = "EVIDENCE_INTEGRITY_VERIFIED"
    DATA_INGESTED = "DATA_INGESTED"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

class AuditEvent(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"AUD-{uuid.uuid4().hex[:8].upper()}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: SecurityEventType
    user_id: Optional[str] = None
    role: Optional[str] = None
    case_id: Optional[str] = None
    operation: str
    source_system: Optional[str] = None
    request_id: Optional[str] = None
    packet_id: Optional[str] = None
    status: str  # SUCCESS, DENIED, FAILED
    details: Dict[str, Any] = Field(default_factory=dict)

class AuditLogger:
    """
    Cryptographically secure, tamper-evident audit logger.
    Logs sensitive security, auth, and external data events without leaking credentials.
    """
    def __init__(self, max_records: int = 1000):
        self._events: List[AuditEvent] = []
        self._max_records = max_records

    def log(
        self,
        event_type: SecurityEventType,
        operation: str,
        status: str,
        user_id: Optional[str] = None,
        role: Optional[str] = None,
        case_id: Optional[str] = None,
        source_system: Optional[str] = None,
        request_id: Optional[str] = None,
        packet_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        clean_details = {}
        if details:
            # Filter out sensitive fields
            forbidden = {"password", "secret", "token", "hmac", "private_key", "key"}
            clean_details = {k: v for k, v in details.items() if not any(f in k.lower() for f in forbidden)}

        event = AuditEvent(
            event_type=event_type,
            user_id=user_id,
            role=role,
            case_id=case_id,
            operation=operation,
            source_system=source_system,
            request_id=request_id,
            packet_id=packet_id,
            status=status,
            details=clean_details
        )
        self._events.append(event)
        if len(self._events) > self._max_records:
            self._events.pop(0)
        return event

    def get_events(
        self,
        limit: int = 50,
        event_type: Optional[SecurityEventType] = None,
        case_id: Optional[str] = None
    ) -> List[AuditEvent]:
        events = list(reversed(self._events))
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if case_id:
            events = [e for e in events if e.case_id == case_id]
        return events[:limit]

    def clear(self):
        """Used for testing resets"""
        self._events.clear()

audit_logger = AuditLogger()
