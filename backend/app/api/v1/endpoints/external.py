from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.audit.audit_logger import audit_logger, SecurityEventType
from backend.app.auth.dependencies import get_current_user, verify_case_authorization
from backend.app.auth.models import User
from backend.app.external.models import ExternalFetchRequest, ExternalFetchResponse
from backend.app.external.secure_client import secure_external_client
from backend.app.security.rate_limit import RateLimiter

router = APIRouter()

OFFICIAL_PROVIDERS = [
    {
        "provider_id": "DOT_OFFICIAL_CDR_GATEWAY",
        "provider_type": "CDR",
        "name": "Department of Telecommunications CDR Gateway",
        "description": "Authorized cellular subscriber records, tower triangulations, and IMEI traces",
        "auth_protocol": "HMAC-SHA256 Challenge-Response (Nonce-Based)"
    },
    {
        "provider_id": "VAHAN_NATIONAL_REGISTRY",
        "provider_type": "VEHICLE",
        "name": "MoRTH VAHAN National Vehicle Registry",
        "description": "National vehicle ownership, chassis numbers, Fastag IDs, and registration metadata",
        "auth_protocol": "HMAC-SHA256 Challenge-Response (Nonce-Based)"
    },
    {
        "provider_id": "FIU_FINANCIAL_INTELLIGENCE",
        "provider_type": "BANKING",
        "name": "Financial Intelligence Unit (FIU-IND)",
        "description": "Suspicious financial transactions, rapid ATM withdrawals, and mule account telemetry",
        "auth_protocol": "HMAC-SHA256 Challenge-Response (Nonce-Based)"
    },
    {
        "provider_id": "NHAI_TOLL_SURVEILLANCE",
        "provider_type": "CCTV_ANPR",
        "name": "NHAI National Highway Surveillance & ANPR",
        "description": "Highway toll plaza ANPR optical camera logs, lane telemetry, and junction sightings",
        "auth_protocol": "HMAC-SHA256 Challenge-Response (Nonce-Based)"
    }
]

@router.get(
    "/external/providers",
    response_model=List[Dict[str, Any]],
    summary="List available official data providers and security protocols"
)
async def list_providers():
    """Returns directory of authorized external official integration systems."""
    return OFFICIAL_PROVIDERS

@router.post(
    "/external/fetch",
    response_model=ExternalFetchResponse,
    summary="Securely fetch, verify, and ingest external data via cryptographic challenge-response",
    dependencies=[Depends(RateLimiter(times=30, seconds=60))]
)
async def fetch_external_data(
    req: ExternalFetchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Executes the zero-trust external data integration pipeline:
    1. Validates investigator case clearance.
    2. Requests single-use cryptographic nonce challenge.
    3. Computes HMAC-SHA-256 proof.
    4. Fetches and validates Ed25519 digitally signed packet.
    5. Verifies SHA-256 evidence integrity.
    6. Preserves raw provenance and auto-ingests into case knowledge graph.
    """
    # Authorization: Verify investigator has access to this case
    if not verify_case_authorization(current_user, req.case_id):
        audit_logger.log(
            event_type=SecurityEventType.UNAUTHORIZED_ACCESS,
            operation="EXTERNAL_DATA_FETCH",
            status="DENIED",
            user_id=current_user.user_id,
            role=current_user.role.value,
            case_id=req.case_id,
            details={"resource_id": req.resource_id, "reason": "User not cleared for case"}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: you are not authorized to request external intelligence for this case"
        )

    try:
        response = secure_external_client.fetch_verified_external_data(
            resource_id=req.resource_id,
            provider_type=req.provider_type,
            case_id=req.case_id,
            user_badge=current_user.badge_number,
            user_id=current_user.user_id
        )
        return response
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"External provider error: {str(e)}")
