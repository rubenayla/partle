#!/usr/bin/env python3
"""Test password reset email functionality - automated version"""

import os
import sys
import logging
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from parent directory first
parent_env = Path(__file__).parent.parent / '.env'
if parent_env.exists():
    logger.info(f"Loading environment from parent: {parent_env}")
    from dotenv import load_dotenv
    load_dotenv(parent_env)

# Import after env is loaded
from app.auth.utils import create_reset_token, send_reset_email
from app.db.session import SessionLocal
from app.db.models import User

def test_password_reset(test_email="test@example.com"):
    """Test the password reset email flow"""
    
    # Check environment variables
    worker_url = os.environ.get("CLOUDFLARE_WORKER_URL")
    worker_api_key = os.environ.get("CLOUDFLARE_WORKER_API_KEY")
    
    logger.info("Environment check:")
    logger.info(f"  CLOUDFLARE_WORKER_URL: {'✓ Set' if worker_url else '✗ Missing'}")
    logger.info(f"  CLOUDFLARE_WORKER_API_KEY: {'✓ Set' if worker_api_key else '✗ Missing'}")
    
    if not worker_url or not worker_api_key:
        logger.error("Missing required environment variables!")
        return False
    
    # Get a test user
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=test_email).first()
        if not user:
            logger.info(f"Creating test user: {test_email}")
            from app.auth.utils import hash_password
            user = User(email=test_email, password_hash=hash_password("test123"))
            db.add(user)
            db.commit()
            logger.info(f"Created user: {test_email}")
        
        logger.info(f"Testing with user: {user.email}")
        
        # Create reset token
        token = create_reset_token(user)
        logger.info(f"Created reset token: {token[:30]}...")
        
        # Send email
        logger.info("Sending password reset email...")
        try:
            send_reset_email(user.email, token)
            logger.info("✓ Email sent successfully!")
            logger.info(f"Check inbox for: {user.email}")
            
            # Show the reset URL for debugging
            frontend_url = "http://localhost:3000"
            reset_url = f"{frontend_url}/reset-password?token={token}"
            logger.info(f"Reset URL would be: {reset_url[:80]}...")
            
            return True
        except Exception as e:
            logger.error(f"✗ Failed to send email: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    finally:
        db.close()

if __name__ == "__main__":
    # Use a real email if provided as argument
    test_email = sys.argv[1] if len(sys.argv) > 1 else "test@example.com"
    success = test_password_reset(test_email)
    sys.exit(0 if success else 1)