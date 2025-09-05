#!/usr/bin/env python3
"""
Quick test script for password reset email
Run this and enter your email address to test the email system
"""
import os
from app.auth.utils import send_reset_email, create_reset_token
from types import SimpleNamespace

def main():
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check if required environment variables are set
    if not os.environ.get("CLOUDFLARE_WORKER_URL"):
        print("❌ Missing CLOUDFLARE_WORKER_URL in environment")
        return
    if not os.environ.get("CLOUDFLARE_WORKER_API_KEY"):
        print("❌ Missing CLOUDFLARE_WORKER_API_KEY in environment")
        return
    if not os.environ.get("SECRET_KEY"):
        print("❌ Missing SECRET_KEY in environment")
        return
    
    print("🔍 QUICK EMAIL TEST")
    print("==================")
    
    your_email = input("Enter your email address: ").strip()
    if not your_email:
        print("❌ No email provided")
        return
    
    print(f"\n📧 Testing email to: {your_email}")
    
    try:
        # Create a mock user and token
        user = SimpleNamespace(email=your_email)
        token = create_reset_token(user)
        
        print(f"🔑 Generated token: {token[:30]}...")
        
        # Send the email
        send_reset_email(your_email, token)
        
        print(f"✅ Email sent successfully to {your_email}!")
        print(f"📨 Check your inbox (and spam folder)")
        print(f"🔗 Reset URL would be: https://partle.rubenayla.xyz/reset-password?token={token}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()