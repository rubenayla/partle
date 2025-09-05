#!/usr/bin/env python3
"""
Quick test script for password reset email
Run this and enter your email address to test the email system
"""
import os
from app.auth.utils import send_reset_email, create_reset_token
from types import SimpleNamespace

def main():
    # Set environment variables if needed
    os.environ.setdefault("CLOUDFLARE_WORKER_URL", "https://partle-email-sender.ruben-jimenezmejias.workers.dev/")
    os.environ.setdefault("CLOUDFLARE_WORKER_API_KEY", "HXkIE9h3Lc4VfAzBBNHroeWioRmvgx_Gqb0jjK_EcXn")
    os.environ.setdefault("SECRET_KEY", "YzSWf51IvcYpQ2lznF6lCjhjdl2MVuF0Mo0aB6hFPCc")
    
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