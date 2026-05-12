"""admin.py — Admin middleware and helpers."""
from fastapi import HTTPException, Request
from auth import verify_token, get_user_by_id, _load_users, _save_users


async def require_admin(authorization: str = None) -> dict:
    """Verify token and require admin role. Returns user dict."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user


def get_all_users() -> list:
    """Get all users (for admin)."""
    users = _load_users()
    result = []
    for email, user in users.items():
        result.append({
            "id": user["id"],
            "email": user["email"],
            "name": user.get("name", ""),
            "plan": user.get("plan", "free"),
            "role": user.get("role", "user"),
            "generations_today": user.get("generations_today", 0),
            "generations_total": user.get("generations_total", 0),
            "created_at": user.get("created_at", 0),
            "last_generation_date": user.get("last_generation_date", ""),
        })
    # Sort by created_at descending
    result.sort(key=lambda x: x.get("created_at", 0), reverse=True)
    return result


def get_admin_stats() -> dict:
    """Get platform-wide stats (for admin dashboard)."""
    users = _load_users()
    total_users = len(users)
    total_generations = sum(u.get("generations_total", 0) for u in users.values())
    
    plan_counts = {"free": 0, "pro": 0, "business": 0}
    for u in users.values():
        plan = u.get("plan", "free")
        if plan in plan_counts:
            plan_counts[plan] += 1
    
    # Today's generations
    import time
    today = time.strftime("%Y-%m-%d")
    today_generations = sum(
        u.get("generations_today", 0) 
        for u in users.values() 
        if u.get("last_generation_date") == today
    )
    
    # Recent users (last 7 days)
    week_ago = time.time() - 7 * 24 * 3600
    new_users_week = sum(1 for u in users.values() if u.get("created_at", 0) > week_ago)
    
    return {
        "total_users": total_users,
        "total_generations": total_generations,
        "today_generations": today_generations,
        "new_users_week": new_users_week,
        "plan_distribution": plan_counts,
    }


def set_user_role(email: str, role: str) -> bool:
    """Set user role (user/admin)."""
    if role not in ("user", "admin"):
        return False
    users = _load_users()
    if email not in users:
        return False
    users[email]["role"] = role
    _save_users(users)
    return True


def set_user_plan(email: str, plan: str) -> bool:
    """Set user plan (free/pro/business)."""
    if plan not in ("free", "pro", "business"):
        return False
    users = _load_users()
    if email not in users:
        return False
    users[email]["plan"] = plan
    _save_users(users)
    return True


def delete_user(email: str) -> bool:
    """Delete a user."""
    users = _load_users()
    if email not in users:
        return False
    del users[email]
    _save_users(users)
    return True
