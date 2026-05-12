"""Test AI client with skill system integration."""

import asyncio
from ai_client import AIClient


async def test_skill_integration():
    """Test skill system integration with AI client."""
    print("=" * 80)
    print("Testing AI Client with Skill System")
    print("=" * 80)
    print()
    
    client = AIClient()
    
    # Test 1: Generate with skill (NEW way)
    print("Test 1: Generate with skill system (NEW)")
    print("-" * 80)
    
    params = {
        'product_name': 'Wireless Bluetooth Earbuds',
        'category': 'Electronics',
        'features': 'noise cancellation, 24h battery, waterproof IPX7',
        'target_audience': 'young professionals',
        'tone': 'professional',
        'language': 'English'
    }
    
    result = await client.generate_with_skill('product-description', params)
    
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Model: {result.get('model')}")
        print(f"Backend: {result.get('backend')}")
        print(f"Skill: {result.get('skill')}")
        print()
        print("Content:")
        content = result['content']
        print(f"  Headline: {content.get('headline')}")
        print(f"  Bullets: {len(content.get('bullets', []))} items")
        for i, bullet in enumerate(content.get('bullets', []), 1):
            print(f"    {i}. {bullet}")
        print(f"  Description: {content.get('description')[:100]}...")
        print(f"  SEO Keywords: {', '.join(content.get('seo_keywords', []))}")
        print()
        print("Quality Report:")
        quality = result['quality_report']
        print(f"  Score: {quality['score']}/100")
        print(f"  Passed: {'✓' if quality['passed'] else '❌'}")
        print(f"  Checks: {sum(1 for v in quality['checks'].values() if v)}/{len(quality['checks'])} passed")
        if quality['issues']:
            print(f"  Issues:")
            for issue in quality['issues']:
                print(f"    - {issue}")
        if quality['suggestions']:
            print(f"  Suggestions:")
            for suggestion in quality['suggestions']:
                print(f"    - {suggestion}")
    else:
        print(f"Error: {result.get('error')}")
    print()
    
    # Test 2: Generate with old API (backward compatibility)
    print("Test 2: Generate with old API (backward compatibility)")
    print("-" * 80)
    
    result = await client.generate(
        content_type='product_description',
        product_name='Wireless Bluetooth Earbuds',
        category='Electronics',
        features='noise cancellation, 24h battery, waterproof IPX7',
        target_audience='young professionals',
        tone='professional',
        language='English'
    )
    
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Model: {result.get('model')}")
        print(f"Content Type: {result.get('content_type')}")
        print(f"Has Quality Report: {'quality_report' in result}")
        if 'quality_report' in result:
            print(f"Quality Score: {result['quality_report']['score']}/100")
    else:
        print(f"Error: {result.get('error')}")
    print()
    
    # Test 3: Custom user config
    print("Test 3: Custom user configuration")
    print("-" * 80)
    
    user_config = {
        'tone': 'casual',
        'max_headline_words': 12,
        'min_bullets': 4,
        'quality_threshold': 85
    }
    
    result = await client.generate_with_skill(
        'product-description',
        params,
        user_config=user_config
    )
    
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Custom config applied:")
        print(f"  Tone: casual")
        print(f"  Quality threshold: 85")
        print(f"Quality Score: {result['quality_report']['score']}/100")
        print(f"Passed threshold: {'✓' if result['quality_report']['passed'] else '❌'}")
    print()
    
    print("=" * 80)
    print("✓ All tests completed!")
    print("=" * 80)


if __name__ == '__main__':
    asyncio.run(test_skill_integration())
