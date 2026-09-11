from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Role(str, Enum):
    INVESTIGATOR = "INVESTIGATOR"
    SUPERVISOR = "SUPERVISOR"
    ADMIN = "ADMIN"

class User(BaseModel):
    user_id: str
    username: str
    badge_number: str
    role: Role
    assigned_cases: List[str] = Field(default_factory=list)
    is_active: bool = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    username: str
    role: Role

class TokenPayload(BaseModel):
    sub: str
    username: str
    role: Role
    badge: str
    exp: int

class LoginRequest(BaseModel):
    username: str
    password: str
