# backend/app/services/log_rotation.py
import os
import json
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
from app.logging_config import get_logger

logger = get_logger("services.log_rotation")

class LogRotationService:
    def __init__(self, log_dir: str = "/tmp/partle-logs", max_age_days: int = 30, max_size_mb: int = 100):
        self.log_dir = Path(log_dir)
        self.max_age = timedelta(days=max_age_days)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Log files
        self.frontend_logs = self.log_dir / "frontend.jsonl"
        self.metrics_logs = self.log_dir / "metrics.jsonl"
        self.error_logs = self.log_dir / "errors.jsonl"
    
    def store_frontend_log(self, log_entry: Dict[str, Any]) -> None:
        """Store frontend log entry to file"""
        try:
            log_line = json.dumps(log_entry, default=str) + '\n'
            
            # Rotate if file is too large
            if self.frontend_logs.exists() and self.frontend_logs.stat().st_size > self.max_size_bytes:
                self._rotate_file(self.frontend_logs)
            
            # Append log entry
            with open(self.frontend_logs, 'a', encoding='utf-8') as f:
                f.write(log_line)
                
        except Exception as e:
            logger.error("Failed to store frontend log", error=str(e))
    
    def store_metric(self, metric: Dict[str, Any]) -> None:
        """Store performance metric to file"""
        try:
            metric_line = json.dumps(metric, default=str) + '\n'
            
            # Rotate if file is too large
            if self.metrics_logs.exists() and self.metrics_logs.stat().st_size > self.max_size_bytes:
                self._rotate_file(self.metrics_logs)
            
            # Append metric
            with open(self.metrics_logs, 'a', encoding='utf-8') as f:
                f.write(metric_line)
                
        except Exception as e:
            logger.error("Failed to store metric", error=str(e))
    
    def store_error_log(self, error_entry: Dict[str, Any]) -> None:
        """Store error log separately for quick access"""
        try:
            error_line = json.dumps(error_entry, default=str) + '\n'
            
            # Rotate if file is too large
            if self.error_logs.exists() and self.error_logs.stat().st_size > self.max_size_bytes:
                self._rotate_file(self.error_logs)
            
            # Append error
            with open(self.error_logs, 'a', encoding='utf-8') as f:
                f.write(error_line)
                
        except Exception as e:
            logger.error("Failed to store error log", error=str(e))
    
    def _rotate_file(self, file_path: Path) -> None:
        """Rotate a log file by compressing and archiving it"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archived_name = f"{file_path.stem}_{timestamp}.gz"
            archived_path = file_path.parent / archived_name
            
            # Compress and archive
            with open(file_path, 'rb') as f_in:
                with gzip.open(archived_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original file
            file_path.unlink()
            
            logger.info(f"Rotated log file", 
                       original=str(file_path), 
                       archived=str(archived_path))
            
        except Exception as e:
            logger.error("Failed to rotate log file", 
                        file=str(file_path), 
                        error=str(e))
    
    def cleanup_old_logs(self) -> None:
        """Remove old compressed log files"""
        try:
            cutoff_time = datetime.now() - self.max_age
            removed_count = 0
            
            for log_file in self.log_dir.glob("*.gz"):
                try:
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_time < cutoff_time:
                        log_file.unlink()
                        removed_count += 1
                except Exception as e:
                    logger.warning("Failed to check/remove old log", 
                                 file=str(log_file), 
                                 error=str(e))
            
            if removed_count > 0:
                logger.info(f"Cleaned up old logs", removed_files=removed_count)
                
        except Exception as e:
            logger.error("Failed to cleanup old logs", error=str(e))
    
    def get_recent_errors(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent error logs for debugging"""
        try:
            if not self.error_logs.exists():
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_errors = []
            
            with open(self.error_logs, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        error_entry = json.loads(line.strip())
                        # Parse timestamp and filter
                        if 'timestamp' in error_entry:
                            log_time = datetime.fromisoformat(error_entry['timestamp'].replace('Z', '+00:00'))
                            if log_time.replace(tzinfo=None) > cutoff_time:
                                recent_errors.append(error_entry)
                    except (json.JSONDecodeError, ValueError):
                        continue
            
            return recent_errors[-100:]  # Last 100 errors
            
        except Exception as e:
            logger.error("Failed to get recent errors", error=str(e))
            return []
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Get statistics about stored logs"""
        try:
            stats = {}
            
            for log_file, name in [(self.frontend_logs, 'frontend'), 
                                 (self.metrics_logs, 'metrics'), 
                                 (self.error_logs, 'errors')]:
                if log_file.exists():
                    stat = log_file.stat()
                    stats[name] = {
                        'size_mb': round(stat.st_size / (1024 * 1024), 2),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'lines': self._count_lines(log_file)
                    }
                else:
                    stats[name] = {'size_mb': 0, 'modified': None, 'lines': 0}
            
            # Count archived files
            archived_count = len(list(self.log_dir.glob("*.gz")))
            stats['archived_files'] = archived_count
            
            return stats
            
        except Exception as e:
            logger.error("Failed to get log stats", error=str(e))
            return {}
    
    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file efficiently"""
        try:
            with open(file_path, 'rb') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0


# Global instance
log_rotation_service = LogRotationService()