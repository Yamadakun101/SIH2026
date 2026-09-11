from typing import Callable, Dict, List, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from backend.app.auth.jwt import decode_access_token
from backend.app.auth.models import Role, User, UserInDB
from backend.app.auth.password import hash_password, verify_password

security_bearer = HTTPBearer(auto_error=False)

# Seed mock law enforcement officers for SIH prototype
# Passwords hashed with Argon2
_USERS_DB: Dict[str, UserInDB] = {
    "investigator": UserInDB(
        user_id="USR-INV-001",
        username="investigator",
        badge_number="DL-INV-301",
        role=Role.INVESTIGATOR,
        assigned_cases=["DL-2026-0412"],
        is_active=True,
        hashed_password=hash_password("Investigator@2026")
    ),
    "supervisor": UserInDB(
        user_id="USR-SUP-001",
        username="supervisor",
        badge_number="DL-SUP-101",
        role=Role.SUPERVISOR,
        assigned_cases=["DL-2026-0412", "DL-2026-0418"],
        is_active=True,
        hashed_password=hash_password("Supervisor@2026")
    ),
    "admin": UserInDB(
        user_id="USR-ADM-001",
        username="admin",
        badge_number="DL-HQ-001",
        role=Role.ADMIN,
        assigned_cases=["*"],
        is_active=True,
        hashed_password=hash_password("Admin@2026")
    )
}

def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticates username and password against the secure Argon2 store."""
    user = _USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return User(**user.model_dump(exclude={"hashed_password"}))

def get_user_by_username(username: str) -> Optional[User]:
    user = _USERS_DB.get(username)
    if user:
        return User(**user.model_dump(exclude={"hashed_password"}))
    return None

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer)
) -> User:
    """Dependency verifying JWT token from Authorization: Bearer <token>."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    username = payload.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_username(username)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_role(*allowed_roles: Role) -> Callable:
    """Dependency factory enforcing Role-Based Access Control (RBAC)."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles and current_user.role != Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: insufficient role permissions"
            )
        return current_user
    return role_checker

def verify_case_authorization(user: User, case_id: str) -> bool:
    """Checks if the user is authorized to view/modify the specified case."""
    if user.role == Role.ADMIN or "*" in user.assigned_cases:
        return True
    return case_id.upper() in [c.upper() for c in user.assigned_cases]

def require_case_access(case_id: str) -> Callable:
    """Dependency factory checking if current user is authorized for case_id."""
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if not verify_case_authorization(current_user, case_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: user is not cleared for case '{case_id}'"
            )
        return current_user
    return checker
