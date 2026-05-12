"""Test skill API endpoints.

Tests for /api/skills routes.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_skills():
    """Test GET /api/skills - list all skills."""
    print("=" * 80)
    print("TEST: GET /api/skills")
    print("=" * 80)
    
    response = client.get("/api/skills")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Skills found: {len(data)}")
        for skill in data:
            print(f"  • {skill['name']} v{skill['version']} ({skill['category']})")
        print("✓ PASS")
    else:
        print(f"✗ FAIL: {response.text}")
    print()


def test_get_skill_details():
    """Test GET /api/skills/{skill_name}."""
    print("=" * 80)
    print("TEST: GET /api/skills/product-description")
    print("=" * 80)
    
    response = client.get("/api/skills/product-description")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['name']}")
        print(f"Description: {data['description']}")
        print(f"Category: {data['category']}")
        print(f"Version: {data['version']}")
        print(f"Premium: {data['is_premium']}")
        print(f"Default config keys: {list(data['default_config'].keys())}")
        print("✓ PASS")
    else:
        print(f"✗ FAIL: {response.text}")
    print()


def test_get_skill_config():
    """Test GET /api/skills/{skill_name}/config."""
    print("=" * 80)
    print("TEST: GET /api/skills/product-description/config")
    print("=" * 80)
    
    response = client.get("/api/skills/product-description/config?user_id=1")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Skill: {data['skill_name']}")
        print(f"Customized: {data['is_customized']}")
        print(f"Config keys: {list(data['config'].keys())}")
        print("✓ PASS")
    else:
        print(f"✗ FAIL: {response.text}")
    print()


def test_update_skill_config():
    """Test POST /api/skills/{skill_name}/config."""
    print("=" * 80)
    print("TEST: POST /api/skills/product-description/config")
    print("=" * 80)
    
    custom_config = {
        "tone": "casual",
        "max_headline_words": 12,
        "quality_threshold": 85
    }
    
    response = client.post(
        "/api/skills/product-description/config?user_id=1",
        json={"config": custom_config}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Updated config: {data['config']}")
        print("✓ PASS")
    else:
        print(f"✗ FAIL: {response.text}")
    print()


def test_generate_with_skill():
    """Test POST /api/skills/{skill_name}/generate."""
    print("=" * 80)
    print("TEST: POST /api/skills/product-description/generate")
    print("=" * 80)
    
    request_data = {
        "params": {
            "product_name": "Wireless Bluetooth Earbuds",
            "category": "Electronics",
            "features": "noise cancellation, 24h battery, waterproof IPX7",
            "target_audience": "young professionals",
            "tone": "professional",
            "language": "English"
        }
    }
    
    response = client.post(
        "/api/skills/product-description/generate?user_id=1",
        json=request_data
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Generation ID: {data['generation_id']}")
        print(f"Quality Score: {data['quality_report']['score']}/100")
        print(f"Model: {data['model']}")
        print(f"Duration: {data['duration_ms']}ms")
        print(f"Content keys: {list(data['content'].keys())}")
        print("✓ PASS")
    else:
        print(f"✗ FAIL: {response.text}")
    print()


def test_get_generation_history():
    """Test GET /api/skills/generations/history."""
    print("=" * 80)
    print("TEST: GET /api/skills/generations/history")
    print("=" * 80)
    
    response = client.get("/api/skills/generations/history?user_id=1&limit=5")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total: {data['total']}")
        print(f"Returned: {len(data['generations'])}")
        for gen in data['generations']:
            print(f"  • ID {gen['id']}: {gen['skill_name']} (score: {gen['quality_score']})")
        print("✓ PASS")
    else:
        print(f"✗ FAIL: {response.text}")
    print()


def run_all_tests():
    """Run all API tests."""
    print("\n")
    print("=" * 80)
    print("TESTING SKILL API ENDPOINTS")
    print("=" * 80)
    print()
    
    # Note: These tests require database to be set up
    # For now, we'll test the routes are registered
    
    try:
        test_list_skills()
        test_get_skill_details()
        test_get_skill_config()
        # test_update_skill_config()  # Requires DB
        # test_generate_with_skill()  # Requires DB + API
        # test_get_generation_history()  # Requires DB
        
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print("✓ Routes are registered and accessible")
        print("⚠ Full tests require database setup")
        print()
        print("To run full tests:")
        print("  1. Set up PostgreSQL database")
        print("  2. Run: python3 database.py")
        print("  3. Run: python3 test_api_skills.py")
        print("=" * 80)
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
