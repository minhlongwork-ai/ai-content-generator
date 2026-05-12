"""Test the skill system."""

import asyncio
from skills.skill_loader import load_skill, list_skills


async def test_product_description_skill():
    """Test product description skill."""
    print("=" * 80)
    print("Testing Product Description Skill")
    print("=" * 80)
    
    # Load skill
    skill = load_skill('product-description')
    
    if not skill:
        print("❌ Failed to load skill")
        return
    
    print("✓ Skill loaded successfully")
    print(f"  Name: {skill.get_skill_metadata()['name']}")
    print(f"  Version: {skill.get_skill_metadata()['version']}")
    print()
    
    # Test input validation
    print("Testing input validation...")
    
    # Invalid input (missing fields)
    is_valid, error = skill.validate_input({})
    print(f"  Empty input: {'✓ Rejected' if not is_valid else '❌ Accepted'}")
    if error:
        print(f"    Error: {error}")
    
    # Valid input
    valid_params = {
        'product_name': 'Wireless Bluetooth Earbuds',
        'category': 'Electronics',
        'features': 'noise cancellation, 24h battery, waterproof IPX7',
        'target_audience': 'young professionals',
        'tone': 'professional'
    }
    
    is_valid, error = skill.validate_input(valid_params)
    print(f"  Valid input: {'✓ Accepted' if is_valid else '❌ Rejected'}")
    print()
    
    # Test prompt building
    print("Testing prompt generation...")
    prompt = skill.build_prompt(valid_params)
    print(f"  Prompt length: {len(prompt)} characters")
    print(f"  First 200 chars: {prompt[:200]}...")
    print()
    
    # Test quality checking
    print("Testing quality checks...")
    
    # Mock good content
    good_content = {
        'headline': 'Premium Wireless Earbuds — Crystal Clear Sound',
        'bullets': [
            'Active noise cancellation blocks distractions',
            '24-hour battery life keeps you connected',
            'IPX7 waterproof rating survives workouts'
        ],
        'description': 'Elevate your audio experience with earbuds designed for the modern professional. Whether you\'re taking calls or enjoying music, these earbuds deliver premium performance.',
        'seo_keywords': [
            'wireless bluetooth earbuds',
            'noise cancelling earbuds',
            'waterproof earbuds IPX7'
        ]
    }
    
    quality = skill.check_quality(good_content)
    print(f"  Quality score: {quality['score']}/100")
    print(f"  Passed: {'✓' if quality['passed'] else '❌'}")
    print(f"  Checks passed: {sum(1 for v in quality['checks'].values() if v)}/{len(quality['checks'])}")
    
    if quality['issues']:
        print(f"  Issues:")
        for issue in quality['issues']:
            print(f"    - {issue}")
    
    if quality['suggestions']:
        print(f"  Suggestions:")
        for suggestion in quality['suggestions']:
            print(f"    - {suggestion}")
    print()
    
    # Test with bad content
    print("Testing with bad content...")
    bad_content = {
        'headline': 'This is a very very very very very very very long headline that exceeds the maximum word limit',
        'bullets': ['Only one bullet'],
        'description': 'Too short.',
        'seo_keywords': ['keyword1', 'keyword1']  # Duplicate
    }
    
    quality = skill.check_quality(bad_content)
    print(f"  Quality score: {quality['score']}/100")
    print(f"  Passed: {'✓' if quality['passed'] else '❌'}")
    print(f"  Issues found: {len(quality['issues'])}")
    for issue in quality['issues']:
        print(f"    - {issue}")
    print()


async def test_list_skills():
    """Test listing all skills."""
    print("=" * 80)
    print("Listing All Skills")
    print("=" * 80)
    
    skills = list_skills()
    print(f"Found {len(skills)} skill(s):")
    print()
    
    for skill_meta in skills:
        print(f"  • {skill_meta['name']} v{skill_meta['version']}")
        print(f"    {skill_meta['description']}")
        print(f"    Category: {skill_meta['category']}")
        print(f"    Required inputs: {', '.join(skill_meta['required_inputs'])}")
        print()


async def main():
    """Run all tests."""
    await test_list_skills()
    await test_product_description_skill()
    
    print("=" * 80)
    print("✓ All tests completed!")
    print("=" * 80)


if __name__ == '__main__':
    asyncio.run(main())
