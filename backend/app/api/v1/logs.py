# backend/app/api/v1/logs.py
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import json

from app.logging_config import get_logger
from app.services.log_rotation import log_rotation_service

router = APIRouter()
logger = get_logger("api.logs")


class FrontendLogEntry(BaseModel):
    timestamp: str
    level: str = Field(..., pattern="^(debug|info|warn|error)$")
    message: str
    context: Optional[Dict[str, Any]] = None
    stack: Optional[str] = None
    url: Optional[str] = None
    userAgent: Optional[str] = None
    userId: Optional[str] = None
    sessionId: Optional[str] = None
    source: str = Field(default="frontend")


class FrontendMetric(BaseModel):
    name: str
    duration: float
    timestamp: str
    details: Optional[Dict[str, Any]] = None
    sessionId: Optional[str] = None
    userId: Optional[str] = None


@router.post("/", status_code=201)
async def receive_frontend_log(log_entry: FrontendLogEntry, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    
    # Convert frontend log level to our structured logging
    log_context = {
        "source": "frontend",
        "session_id": log_entry.sessionId,
        "user_id": log_entry.userId,
        "client_ip": client_ip,
        "url": log_entry.url,
        "user_agent": log_entry.userAgent,
        "frontend_timestamp": log_entry.timestamp,
    }
    
    # Add any additional context from the frontend
    if log_entry.context:
        log_context.update(log_entry.context)
    
    # Add stack trace for errors
    if log_entry.stack:
        log_context["stack_trace"] = log_entry.stack
    
    # Log using our structured logger
    if log_entry.level == "debug":
        logger.debug(f"Frontend: {log_entry.message}", **log_context)
    elif log_entry.level == "info":
        logger.info(f"Frontend: {log_entry.message}", **log_context)
    elif log_entry.level == "warn":
        logger.warning(f"Frontend: {log_entry.message}", **log_context)
    elif log_entry.level == "error":
        logger.error(f"Frontend: {log_entry.message}", **log_context)
    
    # Store to file system for aggregation
    full_log_entry = {
        **log_entry.model_dump(),
        "client_ip": client_ip,
        "received_at": datetime.now().isoformat()
    }
    
    log_rotation_service.store_frontend_log(full_log_entry)
    
    # Store errors separately for quick access
    if log_entry.level == "error":
        log_rotation_service.store_error_log(full_log_entry)
    
    return {"status": "logged"}


@router.post("/metrics", status_code=201)
async def receive_frontend_metric(metric: FrontendMetric, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    
    metric_context = {
        "source": "frontend_metrics",
        "session_id": metric.sessionId,
        "user_id": metric.userId,
        "client_ip": client_ip,
        "metric_name": metric.name,
        "duration_ms": metric.duration,
        "frontend_timestamp": metric.timestamp,
    }
    
    # Add any additional details
    if metric.details:
        metric_context.update(metric.details)
    
    # Log performance metrics
    if metric.duration > 1000:  # Slow operations
        logger.warning(f"Frontend slow operation: {metric.name}", **metric_context)
    else:
        logger.info(f"Frontend metric: {metric.name}", **metric_context)
    
    # Store metric to file system
    full_metric = {
        **metric.model_dump(),
        "client_ip": client_ip,
        "received_at": datetime.now().isoformat()
    }
    
    log_rotation_service.store_metric(full_metric)
    
    return {"status": "recorded"}


@router.get("/health")
async def logs_health():
    return {"status": "ok", "service": "frontend-logs"}


@router.get("/stats")
async def get_log_stats():
    """Get statistics about stored logs"""
    stats = log_rotation_service.get_log_stats()
    return {"status": "ok", "stats": stats}


@router.get("/errors/recent")
async def get_recent_errors(hours: int = 24):
    """Get recent error logs for debugging"""
    errors = log_rotation_service.get_recent_errors(hours)
    return {"status": "ok", "errors": errors, "count": len(errors)}


@router.post("/cleanup")
async def cleanup_old_logs():
    """Manually trigger cleanup of old log files"""
    log_rotation_service.cleanup_old_logs()
    return {"status": "cleanup_triggered"}