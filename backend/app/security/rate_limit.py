from collections import defaultdict
from datetime import datetime, timezone
import time
from typing import Dict, List
from fastapi import HTTPException, Request, status
from backend.app.audit.audit_logger import audit_logger, SecurityEventType

class InMemoryRateLimiter:
    """Sliding-window in-memory rate limiter protecting endpoints against abusive bursts."""
    def __init__(self):
        # key -> list of timestamp floats
        self._requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str, max_requests: int = 60, window_seconds: int = 60) -> bool:
        now = time.time()
        cutoff = now - window_seconds
        
        # Clean older timestamps
        self._requests[key] = [ts for ts in self._requests[key] if ts > cutoff]
        
        if len(self._requests[key]) >= max_requests:
            return False
        
        self._requests[key].append(now)
        return True

    def reset(self):
        self._requests.clear()

rate_limiter = InMemoryRateLimiter()

class RateLimiter:
    """FastAPI dependency for endpoint rate limiting."""
    def __init__(self, times: int = 60, seconds: int = 60):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        key = f"{client_ip}:{path}"

        if not rate_limiter.is_allowed(key, max_requests=self.times, window_seconds=self.seconds):
            audit_logger.log(
                event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
                operation=f"HTTP {request.method} {path}",
                status="DENIED",
                details={"client_ip": client_ip, "limit": self.times, "window": self.seconds}
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait before retrying."
            )
