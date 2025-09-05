import os
from fastapi import APIRouter

router = APIRouter()


@router.get('/health/')
def health_check():
    # Check required environment variables
    required_vars = {
        'DATABASE_URL': bool(os.getenv('DATABASE_URL')),
        'SECRET_KEY': bool(os.getenv('SECRET_KEY') or os.getenv('JWT_SECRET_KEY')),
        'CLOUDFLARE_WORKER_URL': bool(os.getenv('CLOUDFLARE_WORKER_URL')),
        'CLOUDFLARE_WORKER_API_KEY': bool(os.getenv('CLOUDFLARE_WORKER_API_KEY'))
    }
    
    all_set = all(required_vars.values())
    
    return {
        'status': 'ok' if all_set else 'degraded',
        'environment': required_vars,
        'warnings': [] if all_set else ['Missing environment variables: ' + ', '.join(k for k, v in required_vars.items() if not v)]
    }

