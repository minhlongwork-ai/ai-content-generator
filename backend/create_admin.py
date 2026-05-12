"""create_admin.py — Create admin account. Run on Render: python backend/create_admin.py"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
import time
import hashlib
import bcrypt
from pathlib import Path

USERS_FILE = Path("output/users.json")

ADMIN_EMAIL = "admin@aicontentgen.com"
ADMIN_PASSWORD = "admin123456"
ADMIN_NAME = "Admin"

def create_admin():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if USERS_FILE.exists():
        users = json.loads(USERS_FILE.read_text())
    else:
        users = {}
    
    if ADMIN_EMAIL in users:
        users[ADMIN_EMAIL]["role"] = "admin"
        users[ADMIN_EMAIL]["plan"] = "business"
        USERS_FILE.write_text(json.dumps(users, indent=2))
        print(f"✅ Admin account updated: {ADMIN_EMAIL}")
        return
    
    user_id = hashlib.sha256(f"{ADMIN_EMAIL}{time.time()}".encode()).hexdigest()[:16]
    password_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
    
    users[ADMIN_EMAIL] = {
        "id": user_id,
        "email": ADMIN_EMAIL,
        "name": ADMIN_NAME,
        "password_hash": password_hash,
        "plan": "business",
        "role": "admin",
        "created_at": time.time(),
        "generations_today": 0,
        "generations_total": 0,
        "last_generation_date": "",
        "stripe_customer_id": None,
    }
    
    USERS_FILE.write_text(json.dumps(users, indent=2))
    print(f"✅ Admin account created!")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print(f"   Role: admin")
    print(f"   Plan: business")

if __name__ == "__main__":
    create_admin()
