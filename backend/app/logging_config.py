"""
Structured logging configuration for Partle backend
"""

import logging
import structlog
import sys
from datetime import datetime
from typing import Any, Dict

def configure_logging() -> None:
    """Configure structured logging for the application"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # Add custom processor for request tracking
            add_request_id,
            # JSON renderer for structured output
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

def add_request_id(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add request ID to log entries if available"""
    # This would be populated by middleware
    request_id = getattr(logger, '_request_id', None)
    if request_id:
        event_dict['request_id'] = request_id
    return event_dict

def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)

class LoggingMiddleware:
    """FastAPI middleware for request logging"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("api.requests")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        import uuid
        request_id = str(uuid.uuid4())[:8]
        
        # Start timing
        start_time = datetime.now()
        
        # Log request start
        method = scope.get("method", "")
        path = scope.get("path", "")
        
        self.logger.info(
            "Request started",
            request_id=request_id,
            method=method,
            path=path,
            client_ip=scope.get("client", ["unknown"])[0] if scope.get("client") else "unknown"
        )
        
        # Add request ID to logger context
        bound_logger = self.logger.bind(request_id=request_id)
        bound_logger._request_id = request_id
        
        async def send_with_logging(message):
            if message["type"] == "http.response.start":
                # Calculate duration
                duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                status_code = message.get("status", 0)
                
                # Log response
                bound_logger.info(
                    "Request completed",
                    status_code=status_code,
                    duration_ms=round(duration_ms, 2),
                    method=method,
                    path=path
                )
            
            await send(message)
        
        await self.app(scope, receive, send_with_logging)