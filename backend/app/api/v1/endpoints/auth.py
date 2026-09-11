from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.audit.audit_logger import audit_logger, SecurityEventType
from backend.app.auth.dependencies import authenticate_user, get_current_user
from backend.app.auth.jwt import create_access_token
from backend.app.auth.models import LoginRequest, Token, User
from backend.app.core.config import settings
from backend.app.security.rate_limit import RateLimiter

router = APIRouter()

@router.post(
    "/auth/login",
    response_model=Token,
    summary="Authenticate officer and issue JWT access token",
    dependencies=[Depends(RateLimiter(times=15, seconds=60))]
)
async def login(req: LoginRequest):
    """
    Authenticates a law enforcement officer using Argon2 password verification
    and generates a cryptographically signed JWT token with role claims.
    """
    user = authenticate_user(req.username, req.password)
    if not user:
        audit_logger.log(
            event_type=SecurityEventType.LOGIN_FAILED,
            operation="USER_LOGIN",
            status="FAILED",
            details={"username": req.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_payload = {
        "sub": user.user_id,
        "username": user.username,
        "role": user.role.value,
        "badge": user.badge_number
    }
    access_token = create_access_token(token_payload)

    audit_logger.log(
        event_type=SecurityEventType.LOGIN_SUCCESS,
        operation="USER_LOGIN",
        status="SUCCESS",
        user_id=user.user_id,
        role=user.role.value,
        details={"username": user.username, "badge": user.badge_number}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.user_id,
        username=user.username,
        role=user.role
    )

@router.get(
    "/auth/me",
    response_model=User,
    summary="Get current authenticated user profile and case clearances"
)
async def get_me(current_user: User = Depends(get_current_user)):
    """Returns the authenticated officer's profile, role, and authorized case IDs."""
    return current_user
