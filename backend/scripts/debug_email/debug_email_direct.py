#!/usr/bin/env python3
"""Direct test of Cloudflare Worker email endpoint"""

import os
import sys
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    logger.info(f"Loading environment from: {env_path}")
    load_dotenv(env_path)

def test_direct_email():
    """Test direct call to Cloudflare Worker"""
    
    worker_url = os.environ.get("CLOUDFLARE_WORKER_URL")
    worker_api_key = os.environ.get("CLOUDFLARE_WORKER_API_KEY")
    
    logger.info("Configuration:")
    logger.info(f"  Worker URL: {worker_url}")
    logger.info(f"  API Key: {worker_api_key[:10]}..." if worker_api_key else "  API Key: Missing")
    
    if not worker_url or not worker_api_key:
        logger.error("Missing configuration!")
        return False
    
    # Test payload
    payload = {
        "to_email": "test@example.com",
        "token": "test-token-12345",
        "api_key": worker_api_key
    }
    
    logger.info(f"Sending POST to: {worker_url}")
    logger.info(f"Payload keys: {list(payload.keys())}")
    
    try:
        response = requests.post(
            worker_url,
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Body: {response.text}")
        
        if response.status_code == 401:
            logger.error("Authentication failed - API key mismatch")
            logger.info("The API key in your .env file doesn't match the one configured in Cloudflare Worker")
            logger.info("To fix this:")
            logger.info("1. Go to Cloudflare Workers dashboard")
            logger.info("2. Find the 'partle-email-sender' worker")
            logger.info("3. Check the API_KEY environment variable")
            logger.info("4. Update CLOUDFLARE_WORKER_API_KEY in .env to match")
            return False
            
        return response.status_code == 200
        
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_email()
    sys.exit(0 if success else 1)