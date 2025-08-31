# backend/app/services/log_cleanup_task.py
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.log_rotation import log_rotation_service
from app.logging_config import get_logger

logger = get_logger("services.log_cleanup")

class LogCleanupScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    def start(self):
        """Start the log cleanup scheduler"""
        try:
            # Run cleanup daily at 2 AM
            self.scheduler.add_job(
                self._cleanup_task,
                'cron',
                hour=2,
                minute=0,
                id='daily_log_cleanup',
                replace_existing=True
            )
            
            # Run log rotation check every hour
            self.scheduler.add_job(
                self._rotation_check,
                'interval',
                hours=1,
                id='hourly_rotation_check',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info("Log cleanup scheduler started")
            
        except Exception as e:
            logger.error("Failed to start log cleanup scheduler", error=str(e))
    
    def stop(self):
        """Stop the log cleanup scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Log cleanup scheduler stopped")
        except Exception as e:
            logger.error("Failed to stop log cleanup scheduler", error=str(e))
    
    async def _cleanup_task(self):
        """Cleanup old log files"""
        try:
            logger.info("Starting scheduled log cleanup")
            log_rotation_service.cleanup_old_logs()
            logger.info("Scheduled log cleanup completed")
        except Exception as e:
            logger.error("Scheduled log cleanup failed", error=str(e))
    
    async def _rotation_check(self):
        """Check if any log files need rotation"""
        try:
            stats = log_rotation_service.get_log_stats()
            
            # Log stats for monitoring
            for log_type, stat in stats.items():
                if isinstance(stat, dict) and stat.get('size_mb', 0) > 50:  # Warning at 50MB
                    logger.warning(f"Large log file detected", 
                                 log_type=log_type, 
                                 size_mb=stat['size_mb'])
                    
        except Exception as e:
            logger.error("Log rotation check failed", error=str(e))

# Global instance
log_cleanup_scheduler = LogCleanupScheduler()