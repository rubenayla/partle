#!/usr/bin/env python3
"""
Enhanced debugging script for password reset email functionality
Run with: poetry run python test_email_debug.py
"""
import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, '/home/rubenayla/repos/partle/backend')

# Load environment variables from root .env
root_env = Path(__file__).parent.parent / '.env'
load_dotenv(root_env)

from app.auth.utils import create_reset_token, verify_reset_token
from app.db.models import User

def test_cloudflare_worker_directly():
    """Test Cloudflare Worker API directly"""
    print("\n" + "="*60)
    print("TESTING CLOUDFLARE WORKER DIRECTLY")
    print("="*60)
    
    worker_url = os.environ.get("CLOUDFLARE_WORKER_URL")
    worker_api_key = os.environ.get("CLOUDFLARE_WORKER_API_KEY")
    
    print(f"Worker URL: {worker_url}")
    print(f"API Key: {worker_api_key[:10]}..." if worker_api_key else "API Key: NOT SET")
    
    # Test payload
    test_payload = {
        "to_email": "test@example.com",
        "token": "test-token-debug-123",
        "api_key": worker_api_key
    }
    
    print(f"\nSending test payload:")
    print(json.dumps({**test_payload, "api_key": test_payload["api_key"][:10] + "..."}, indent=2))
    
    try:
        response = requests.post(
            worker_url, 
            json=test_payload,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Worker responded successfully!")
        else:
            print(f"❌ Worker returned error status: {response.status_code}")
            
        return response.status_code == 200
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 10 seconds")
        return False
    except Exception as e:
        print(f"❌ Exception occurred: {type(e).__name__}: {e}")
        return False

def test_token_generation():
    """Test token generation and verification"""
    print("\n" + "="*60)
    print("TESTING TOKEN GENERATION")
    print("="*60)
    
    # Create a mock user object
    class MockUser:
        def __init__(self, email):
            self.email = email
    
    test_email = "user@example.com"
    mock_user = MockUser(test_email)
    
    print(f"Creating token for: {test_email}")
    token = create_reset_token(mock_user)
    print(f"Generated token: {token[:50]}..." if len(token) > 50 else f"Generated token: {token}")
    
    # Verify the token
    print("\nVerifying token...")
    verified_email = verify_reset_token(token)
    
    if verified_email == test_email:
        print(f"✅ Token verified successfully! Email: {verified_email}")
        return True
    else:
        print(f"❌ Token verification failed! Expected: {test_email}, Got: {verified_email}")
        return False

def test_email_with_real_address(email_address):
    """Test sending to a real email address"""
    print("\n" + "="*60)
    print(f"TESTING WITH REAL EMAIL: {email_address}")
    print("="*60)
    
    worker_url = os.environ.get("CLOUDFLARE_WORKER_URL")
    worker_api_key = os.environ.get("CLOUDFLARE_WORKER_API_KEY")
    
    # Create a real token
    class MockUser:
        def __init__(self, email):
            self.email = email
    
    mock_user = MockUser(email_address)
    real_token = create_reset_token(mock_user)
    
    payload = {
        "to_email": email_address,
        "token": real_token,
        "api_key": worker_api_key
    }
    
    print(f"Sending real email to: {email_address}")
    print(f"Token (first 50 chars): {real_token[:50]}...")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    try:
        response = requests.post(
            worker_url,
            json=payload,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Email sent successfully to {email_address}!")
            print("📧 Check your inbox (and spam folder) for the reset email")
            
            # Generate the reset link that should be in the email
            frontend_url = "https://partle.rubenayla.xyz"  # or localhost:3000 for local testing
            reset_link = f"{frontend_url}/reset-password?token={real_token}"
            print(f"\nThe reset link in the email should be:")
            print(f"{reset_link}")
            return True
        else:
            print(f"❌ Failed to send email. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {type(e).__name__}: {e}")
        return False

def test_full_flow():
    """Test the complete email reset flow"""
    print("\n" + "="*60)
    print("RUNNING COMPLETE EMAIL RESET FLOW TEST")
    print("="*60)
    
    # Use the actual send_reset_email function
    from app.auth.utils import send_reset_email
    
    test_email = "debug-test@example.com"
    test_token = "debug-test-token-" + datetime.now().strftime("%Y%m%d%H%M%S")
    
    print(f"Testing send_reset_email function")
    print(f"Email: {test_email}")
    print(f"Token: {test_token}")
    
    try:
        send_reset_email(test_email, test_token)
        print("✅ send_reset_email completed without errors")
        return True
    except Exception as e:
        print(f"❌ send_reset_email failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n🔍 PASSWORD RESET EMAIL DEBUGGING TOOL")
    print("=" * 60)
    
    # Check environment variables
    print("\n📋 Environment Check:")
    env_vars = {
        "CLOUDFLARE_WORKER_URL": os.environ.get("CLOUDFLARE_WORKER_URL"),
        "CLOUDFLARE_WORKER_API_KEY": os.environ.get("CLOUDFLARE_WORKER_API_KEY"),
        "SECRET_KEY": os.environ.get("SECRET_KEY")
    }
    
    for key, value in env_vars.items():
        if value:
            if "KEY" in key:
                print(f"✅ {key}: {value[:10]}...")
            else:
                print(f"✅ {key}: {value}")
        else:
            print(f"❌ {key}: NOT SET")
    
    # Run tests
    results = []
    
    # Test 1: Token generation
    results.append(("Token Generation", test_token_generation()))
    
    # Test 2: Cloudflare Worker
    results.append(("Cloudflare Worker", test_cloudflare_worker_directly()))
    
    # Test 3: Full flow with mock email
    results.append(("Full Flow (Mock)", test_full_flow()))
    
    # Test 4: Real email (optional)
    print("\n" + "="*60)
    user_email = input("Enter your email to test real delivery (or press Enter to skip): ").strip()
    if user_email and "@" in user_email:
        results.append(("Real Email Delivery", test_email_with_real_address(user_email)))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Recommendations
    print("\n📝 Troubleshooting Tips:")
    if not all(r[1] for r in results):
        print("1. Check if the Cloudflare Worker is deployed and running")
        print("2. Verify the API key matches what's configured in Cloudflare")
        print("3. Check Cloudflare Worker logs for any errors")
        print("4. Ensure the worker has email sending capabilities configured")
        print("5. Check spam/junk folders for test emails")
        print("6. Verify the email template in the Cloudflare Worker")
    else:
        print("All tests passed! The email system appears to be working correctly.")

if __name__ == "__main__":
    main()