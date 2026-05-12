"""auth.py — Simple JWT-based authentication + user management."""
import os
import time
import hashlib
import secrets
from typing import Optional
from pathlib import Path
import json

import jwt
import bcrypt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(32))
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24 * 30  # 30 days

# Simple file-based user store (swap to DB in production)
USERS_FILE = Path("output/users.json")


def _load_users() -> dict:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return {}


def _save_users(users: dict):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, indent=2))


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_user(email: str, password: str, name: str = "") -> dict:
    users = _load_users()
    if email in users:
        raise ValueError("Email already registered")

    user_id = hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()[:16]
    user = {
        "id": user_id,
        "email": email,
        "name": name or email.split("@")[0],
        "password_hash": hash_password(password),
        "plan": "free",
        "role": "user",
        "created_at": time.time(),
        "generations_today": 0,
        "generations_total": 0,
        "last_generation_date": "",
        "stripe_customer_id": None,
    }
    users[email] = user
    _save_users(users)
    return user


def authenticate_user(email: str, password: str) -> Optional[dict]:
    users = _load_users()
    user = users.get(email)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user


def get_user_by_id(user_id: str) -> Optional[dict]:
    users = _load_users()
    for user in users.values():
        if user["id"] == user_id:
            return user
    return None


def get_user_by_email(email: str) -> Optional[dict]:
    users = _load_users()
    return users.get(email)


def create_token(user: dict) -> str:
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "plan": user.get("plan", "free"),
        "role": user.get("role", "user"),
        "exp": time.time() + JWT_EXPIRY_HOURS * 3600,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def upgrade_user_plan(email: str, plan: str, stripe_customer_id: str = None):
    users = _load_users()
    if email in users:
        users[email]["plan"] = plan
        if stripe_customer_id:
            users[email]["stripe_customer_id"] = stripe_customer_id
        _save_users(users)


def increment_generation(email: str):
    users = _load_users()
    if email in users:
        today = time.strftime("%Y-%m-%d")
        if users[email]["last_generation_date"] != today:
            users[email]["generations_today"] = 0
            users[email]["last_generation_date"] = today
        users[email]["generations_today"] += 1
        users[email]["generations_total"] += 1
        _save_users(users)


def get_generation_stats(email: str) -> dict:
    users = _load_users()
    user = users.get(email, {})
    today = time.strftime("%Y-%m-%d")
    if user.get("last_generation_date") != today:
        return {"today": 0, "total": user.get("generations_total", 0), "remaining": 5}
    today_count = user.get("generations_today", 0)
    plan = user.get("plan", "free")
    limit = float("inf") if plan in ("pro", "business") else 5
    return {
        "today": today_count,
        "total": user.get("generations_total", 0),
        "remaining": max(0, limit - today_count),
        "plan": plan,
    }
