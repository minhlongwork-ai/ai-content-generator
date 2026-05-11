"""Quick test for 9router integration."""
import asyncio, json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from ai_client import AIClient

async def test():
    client = AIClient()
    print("Testing 9router + Kiro...")
    
    # Test 1: Simple call
    try:
        result = await client._call_9router('Say hi in one word', 'kr/claude-sonnet-4.5')
        print(f"Test 1 OK: {result}")
    except Exception as e:
        print(f"Test 1 FAIL: {e}")
    
    # Test 2: Full generate
    try:
        result = await client.generate(
            'product_description',
            product_name='Test Product',
            category='Test',
            features='Feature 1, Feature 2',
            target_audience='Everyone',
            language='English',
            tone='professional'
        )
        print(f"Test 2 OK: {json.dumps(result, indent=2)[:500]}")
    except Exception as e:
        print(f"Test 2 FAIL: {e}")

asyncio.run(test())
