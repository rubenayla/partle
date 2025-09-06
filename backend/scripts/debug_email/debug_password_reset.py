#!/usr/bin/env python3
"""Test password reset email functionality"""

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

# Load environment variables
from dotenv import load_dotenv
env_path = backend_dir / '.env'
if env_path.exists():
    logger.info(f"Loading environment from: {env_path}")
    load_dotenv(env_path)
else:
    logger.warning(f"No .env file found at: {env_path}")

# Import after env is loaded
from app.auth.utils import create_reset_token, send_reset_email
from app.db.session import SessionLocal
from app.db.models import User

def test_password_reset():
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
        # Find or create a test user
        test_email = input("Enter email address to test with: ").strip()
        if not test_email:
            logger.error("No email provided")
            return False
            
        user = db.query(User).filter_by(email=test_email).first()
        if not user:
            logger.info(f"User {test_email} not found in database")
            create_new = input("Create this user? (y/n): ").strip().lower()
            if create_new == 'y':
                from app.auth.utils import hash_password
                user = User(email=test_email, password_hash=hash_password("test123"))
                db.add(user)
                db.commit()
                logger.info(f"Created user: {test_email}")
            else:
                return False
        
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
            return True
        except Exception as e:
            logger.error(f"✗ Failed to send email: {e}")
            return False
            
    finally:
        db.close()

if __name__ == "__main__":
    success = test_password_reset()
    sys.exit(0 if success else 1)