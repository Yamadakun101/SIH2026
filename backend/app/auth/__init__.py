"""KavachNet Authentication & Authorization Package"""
from backend.app.auth.models import Role, User, Token, LoginRequest
from backend.app.auth.password import hash_password, verify_password
from backend.app.auth.jwt import create_access_token, decode_access_token
from backend.app.auth.dependencies import (
    get_current_user, require_role, require_case_access
)

__all__ = [
    "Role",
    "User",
    "Token",
    "LoginRequest",
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "require_role",
    "require_case_access"
]
