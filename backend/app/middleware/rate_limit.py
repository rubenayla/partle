"""
Rate limiting middleware for public API endpoints
"""
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time
from typing import Dict, Tuple

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter for API endpoints"""
    
    def __init__(self, app, calls: int = 100, period: int = 3600):
        super().__init__(app)
        self.calls = calls  # Max calls per period
        self.period = period  # Period in seconds (default: 1 hour)
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Only apply rate limiting to public API endpoints
        if not request.url.path.startswith("/v1/public/"):
            return await call_next(request)
        
        # Get client identifier (API key from auth header or IP)
        client_id = self._get_client_id(request)
        current_time = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] 
            if current_time - req_time < self.period
        ]
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.calls:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.calls} requests per {self.period} seconds."
            )
        
        # Add current request
        self.requests[client_id].append(current_time)
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = max(0, self.calls - len(self.requests[client_id]))
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.period))
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting"""
        # Try to get API key from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return f"api_key:{auth_header[7:10]}..."  # Use first 3 chars of key
        
        # Fallback to IP address
        client_ip = request.headers.get("X-Forwarded-For", request.client.host if request.client else "unknown")
        return f"ip:{client_ip}"