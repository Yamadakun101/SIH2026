import pytest
from fastapi import FastAPI, Depends, Request
from fastapi.testclient import TestClient
from backend.app.security.rate_limit import InMemoryRateLimiter, RateLimiter, rate_limiter

def test_in_memory_rate_limiter_window():
    limiter = InMemoryRateLimiter()
    key = "test-user-ip:test-path"
    
    # Allow 3 requests
    assert limiter.is_allowed(key, max_requests=3, window_seconds=10) is True
    assert limiter.is_allowed(key, max_requests=3, window_seconds=10) is True
    assert limiter.is_allowed(key, max_requests=3, window_seconds=10) is True
    
    # 4th request must be rejected
    assert limiter.is_allowed(key, max_requests=3, window_seconds=10) is False
    
    # Reset clears tracking
    limiter.reset()
    assert limiter.is_allowed(key, max_requests=3, window_seconds=10) is True

def test_rate_limiter_dependency_429():
    app = FastAPI()
    limiter_instance = InMemoryRateLimiter()

    # Create a custom route with a low rate limit
    class TestRateLimiter(RateLimiter):
        async def __call__(self, request: Request):
            client_ip = request.client.host if request.client else "unknown"
            key = f"{client_ip}:{request.url.path}"
            if not limiter_instance.is_allowed(key, max_requests=2, window_seconds=60):
                from fastapi import HTTPException, status
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    @app.get("/rate-limited-endpoint", dependencies=[Depends(TestRateLimiter(times=2, seconds=60))])
    def limited_route():
        return {"status": "success"}

    client = TestClient(app)
    
    # First 2 requests succeed
    res1 = client.get("/rate-limited-endpoint")
    assert res1.status_code == 200
    
    res2 = client.get("/rate-limited-endpoint")
    assert res2.status_code == 200
    
    # 3rd request should fail with 429
    res3 = client.get("/rate-limited-endpoint")
    assert res3.status_code == 429
    assert "Rate limit exceeded" in res3.text
