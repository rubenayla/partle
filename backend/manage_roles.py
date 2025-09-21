#!/usr/bin/env python3
"""Script to manage user roles in Partle database."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv(override=True)

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import User, UserRole
from sqlalchemy.exc import OperationalError


def list_users(db: Session):
    """List all users and their roles."""
    try:
        users = db.query(User).all()
        print("\n=== User List ===")
        print(f"{'ID':<5} {'Email':<40} {'Username':<20} {'Role':<10}")
        print("-" * 75)
        for user in users:
            role = getattr(user, 'role', 'N/A')
            if role != 'N/A':
                role = role.value if hasattr(role, 'value') else role
            username = user.username or 'N/A'
            print(f"{user.id:<5} {user.email:<40} {username:<20} {role:<10}")
        print()
    except Exception as e:
        print(f"Error listing users: {e}")


def set_user_role(db: Session, email: str, role: str):
    """Set a user's role."""
    try:
        # Validate role
        if role not in ['user', 'admin', 'moderator']:
            print(f"Invalid role: {role}")
            print("Valid roles are: user, admin, moderator")
            return

        # Find user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User with email '{email}' not found")
            return

        # Check if role field exists
        if not hasattr(user, 'role'):
            print("Warning: Role field doesn't exist yet. Please run migration first:")
            print("  uv run alembic upgrade head")
            return

        # Set role
        user.role = UserRole[role]
        db.commit()
        print(f"✓ Successfully set {email} as {role}")

    except Exception as e:
        db.rollback()
        print(f"Error setting role: {e}")


def main():
    """Main CLI interface."""
    print("Partle Role Management Tool")
    print("===========================")

    # Check if migration has been run
    db = SessionLocal()
    try:
        test_user = db.query(User).first()
        if test_user and not hasattr(test_user, 'role'):
            print("\n⚠️  Warning: Role field not found in database!")
            print("Please run the migration first on the server:")
            print("  ssh deploy@91.98.68.236")
            print("  cd /srv/partle/backend")
            print("  uv run alembic upgrade head")
            print()
    except OperationalError as e:
        print(f"\n❌ Database connection error: {e}")
        print("Make sure DATABASE_URL is set correctly in .env")
        db.close()
        return

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python manage_roles.py list                    - List all users and their roles")
        print("  python manage_roles.py set <email> <role>      - Set user's role")
        print("  python manage_roles.py promote <email>         - Promote user to admin")
        print("\nExamples:")
        print("  python manage_roles.py list")
        print("  python manage_roles.py set user@example.com admin")
        print("  python manage_roles.py promote ruben.jimenezmejias@gmail.com")
        db.close()
        return

    command = sys.argv[1].lower()

    if command == "list":
        list_users(db)
    elif command == "set" and len(sys.argv) == 4:
        email = sys.argv[2]
        role = sys.argv[3].lower()
        set_user_role(db, email, role)
    elif command == "promote" and len(sys.argv) == 3:
        email = sys.argv[2]
        set_user_role(db, email, "admin")
    else:
        print(f"Invalid command: {' '.join(sys.argv[1:])}")
        print("Run 'python manage_roles.py' for usage information")

    db.close()


if __name__ == "__main__":
    main()