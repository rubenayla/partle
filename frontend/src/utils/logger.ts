/**
 * Frontend logging utility for Partle
 * Provides structured logging with error tracking and performance monitoring
 */

interface LogEntry {
  timestamp: string;
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  context?: Record<string, any>;
  stack?: string;
  url?: string;
  userAgent?: string;
  userId?: string;
}

interface PerformanceMetric {
  name: string;
  duration: number;
  timestamp: string;
  details?: Record<string, any>;
}

class Logger {
  private apiUrl: string;
  private userId?: string;
  private sessionId: string;
  
  constructor() {
    this.apiUrl = import.meta.env.VITE_API_BASE || 'https://partle.rubenayla.xyz';
    this.sessionId = this.generateSessionId();
    this.setupErrorHandlers();
  }
  
  private generateSessionId(): string {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }
  
  private setupErrorHandlers(): void {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.error('Global JavaScript error', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        stack: event.error?.stack,
      });
    });
    
    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      this.error('Unhandled promise rejection', {
        reason: event.reason?.toString(),
        stack: event.reason?.stack,
      });
    });
    
    // Resource loading errors
    window.addEventListener('error', (event) => {
      if (event.target !== window) {
        this.error('Resource loading error', {
          tagName: (event.target as any)?.tagName,
          source: (event.target as any)?.src || (event.target as any)?.href,
        });
      }
    }, true);
  }
  
  setUserId(userId: string): void {
    this.userId = userId;
  }
  
  debug(message: string, context?: Record<string, any>): void {
    this.log('debug', message, context);
  }
  
  info(message: string, context?: Record<string, any>): void {
    this.log('info', message, context);
  }
  
  warn(message: string, context?: Record<string, any>): void {
    this.log('warn', message, context);
  }
  
  error(message: string, context?: Record<string, any>): void {
    this.log('error', message, context);
  }
  
  private log(level: LogEntry['level'], message: string, context?: Record<string, any>): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context,
      url: window.location.href,
      userAgent: navigator.userAgent,
      userId: this.userId,
    };
    
    // Console output for development
    if (import.meta.env.DEV) {
      console[level](message, context);
    }
    
    // Send to backend in production or if level is error/warn
    if (!import.meta.env.DEV || level === 'error' || level === 'warn') {
      this.sendToBackend(entry);
    }
    
    // Store locally for debugging
    this.storeLocally(entry);
  }
  
  private async sendToBackend(entry: LogEntry): Promise<void> {
    // TODO: Enable when backend /api/v1/logs endpoint is implemented
    // Temporarily disabled to prevent 404 errors
    if (import.meta.env.DEV) {
      console.debug('Logger: Would send to backend:', entry);
      return;
    }
    
    try {
      await fetch(`${this.apiUrl}/v1/logs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...entry,
          sessionId: this.sessionId,
          source: 'frontend',
        }),
      });
    } catch (error) {
      // Silently fail in production to avoid console spam
      if (import.meta.env.DEV) {
        console.error('Failed to send log to backend:', error);
      }
    }
  }
  
  private storeLocally(entry: LogEntry): void {
    try {
      const logs = JSON.parse(localStorage.getItem('partle_logs') || '[]');
      logs.push(entry);
      
      // Keep only last 100 logs
      if (logs.length > 100) {
        logs.splice(0, logs.length - 100);
      }
      
      localStorage.setItem('partle_logs', JSON.stringify(logs));
    } catch (error) {
      console.error('Failed to store log locally:', error);
    }
  }
  
  // Performance monitoring
  trackPerformance(name: string, startTime: number, details?: Record<string, any>): void {
    const duration = performance.now() - startTime;
    const metric: PerformanceMetric = {
      name,
      duration,
      timestamp: new Date().toISOString(),
      details,
    };
    
    this.info(`Performance: ${name}`, {
      duration_ms: duration,
      ...details,
    });
    
    // Send critical performance metrics
    if (duration > 1000 || name.includes('error')) {
      this.sendPerformanceMetric(metric);
    }
  }
  
  private async sendPerformanceMetric(metric: PerformanceMetric): Promise<void> {
    // TODO: Enable when backend /api/v1/metrics endpoint is implemented
    // Temporarily disabled to prevent 404 errors
    if (import.meta.env.DEV) {
      console.debug('Logger: Would send performance metric:', metric);
      return;
    }
    
    try {
      await fetch(`${this.apiUrl}/v1/metrics`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...metric,
          sessionId: this.sessionId,
          userId: this.userId,
        }),
      });
    } catch (error) {
      // Silently fail in production to avoid console spam
      if (import.meta.env.DEV) {
        console.error('Failed to send performance metric:', error);
      }
    }
  }
  
  // API request logging
  logApiCall(method: string, url: string, status: number, duration: number, error?: any): void {
    const level = status >= 400 ? 'error' : status >= 300 ? 'warn' : 'info';
    
    this.log(level, `API ${method} ${url}`, {
      http_method: method,
      url,
      status_code: status,
      duration_ms: duration,
      error: error?.message,
    });
  }
  
  // User action tracking
  trackUserAction(action: string, details?: Record<string, any>): void {
    this.info(`User action: ${action}`, {
      action,
      ...details,
    });
  }
  
  // Get logs for debugging
  getLocalLogs(): LogEntry[] {
    try {
      return JSON.parse(localStorage.getItem('partle_logs') || '[]');
    } catch {
      return [];
    }
  }
  
  // Clear local logs
  clearLocalLogs(): void {
    localStorage.removeItem('partle_logs');
  }
}

// Export singleton instance
export const logger = new Logger();

// Export types
export type { LogEntry, PerformanceMetric };