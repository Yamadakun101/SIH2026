from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from backend.app.audit.audit_logger import audit_logger, AuditEvent
from backend.app.auth.dependencies import require_role
from backend.app.auth.models import Role, User

router = APIRouter()

@router.get(
    "/audit/security",
    response_model=List[AuditEvent],
    summary="Retrieve security and external access audit trail (Supervisor/Admin only)"
)
async def get_security_audit_logs(
    limit: int = Query(50, ge=1, le=500),
    case_id: Optional[str] = Query(None, description="Filter audit logs by case ID"),
    current_user: User = Depends(require_role(Role.SUPERVISOR, Role.ADMIN))
):
    """
    Returns immutable audit logs recording logins, external API accesses,
    challenge handshakes, and tamper-verification events.
    """
    return audit_logger.get_events(limit=limit, case_id=case_id)
