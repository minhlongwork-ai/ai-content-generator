"""create_admin.py — Create admin account. Run: python create_admin.py"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from auth import create_user, get_user_by_email, _load_users, _save_users

ADMIN_EMAIL = "admin@aicontentgen.com"
ADMIN_PASSWORD = "admin123456"
ADMIN_NAME = "Admin"

def create_admin():
    """Create admin account if not exists."""
    existing = get_user_by_email(ADMIN_EMAIL)
    if existing:
        # Update role to admin
        users = _load_users()
        users[ADMIN_EMAIL]["role"] = "admin"
        users[ADMIN_EMAIL]["plan"] = "business"
        _save_users(users)
        print(f"✅ Admin account updated: {ADMIN_EMAIL}")
        print(f"   Role: admin")
        print(f"   Plan: business")
        return
    
    try:
        user = create_user(ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME)
        # Set role to admin
        users = _load_users()
        users[ADMIN_EMAIL]["role"] = "admin"
        users[ADMIN_EMAIL]["plan"] = "business"
        _save_users(users)
        print(f"✅ Admin account created!")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   Role: admin")
        print(f"   Plan: business")
    except ValueError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_admin()
