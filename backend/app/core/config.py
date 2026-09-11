from pathlib import Path
from typing import List
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "KavachNet"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Allow local frontend ports (Vite default is 5173, fallback 3000, 5174)
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DATA_PATH: Path = BASE_DIR / "data" / "dl-2026-0412.json"

settings = Settings()
