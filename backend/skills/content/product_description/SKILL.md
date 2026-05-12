---
name: product-description
description: Generate compelling e-commerce product descriptions with headlines, bullet points, and SEO optimization
version: 1.0.0
category: e-commerce
author: AI Content Generator
tags: [product, description, seo, e-commerce]
---

# Product Description Skill

## Overview

Generate high-converting product descriptions for e-commerce platforms. This skill creates:
- Catchy headlines (max 15 words)
- 3-5 benefit-focused bullet points
- Persuasive closing paragraph
- SEO keywords

## When to use this skill

✓ Creating product listings for Shopee, Lazada, Amazon
✓ Writing product pages for websites
✓ Generating multiple variations for A/B testing
✓ Optimizing existing descriptions for SEO

## Not ideal for

✗ Service descriptions (use service-description skill)
✗ Long-form content (use blog-post skill)
✗ Technical specifications (use spec-sheet skill)

## Required Inputs

1. **product_name** (string): Product name
2. **category** (string): Product category (e.g., "Electronics", "Fashion")
3. **features** (string): Key features, comma-separated

## Optional Inputs

1. **target_audience** (string): Who is this for? (default: "general")
2. **tone** (string): professional | casual | luxury | playful (default: "professional")
3. **language** (string): Output language (default: "English")

## Output Format

```json
{
  "headline": "Catchy headline under 15 words",
  "bullets": [
    "Benefit-focused bullet point 1",
    "Benefit-focused bullet point 2",
    "Benefit-focused bullet point 3"
  ],
  "description": "Persuasive closing paragraph (2-3 sentences)",
  "seo_keywords": [
    "keyword 1",
    "keyword 2",
    "keyword 3"
  ]
}
```

## Quality Checks

- ✓ Headline length < 15 words
- ✓ 3-5 bullet points
- ✓ Each bullet < 20 words
- ✓ Description 2-3 sentences
- ✓ 3-5 SEO keywords
- ✓ No duplicate keywords
- ✓ Benefits > Features ratio

## Configuration

Default config:
```yaml
tone: professional
language: English
target_audience: general
max_headline_words: 15
min_bullets: 3
max_bullets: 5
max_bullet_words: 20
min_description_sentences: 2
max_description_sentences: 3
min_seo_keywords: 3
max_seo_keywords: 5
quality_threshold: 70
```

## Examples

### Example 1: Electronics

Input:
```json
{
  "product_name": "Wireless Bluetooth Earbuds",
  "category": "Electronics",
  "features": "noise cancellation, 24h battery, waterproof IPX7",
  "target_audience": "young professionals",
  "tone": "professional"
}
```

Output:
```json
{
  "headline": "Premium Wireless Earbuds — Crystal Clear Sound, All Day Battery",
  "bullets": [
    "Active noise cancellation blocks distractions for focused listening",
    "24-hour battery life keeps you connected through your busiest days",
    "IPX7 waterproof rating survives workouts and unexpected rain",
    "Ergonomic design ensures comfortable wear during long commutes",
    "One-touch pairing connects instantly to all your devices"
  ],
  "description": "Elevate your audio experience with earbuds designed for the modern professional. Whether you're taking calls, enjoying music, or blocking out the world, these earbuds deliver premium performance that lasts all day.",
  "seo_keywords": [
    "wireless bluetooth earbuds",
    "noise cancelling earbuds",
    "waterproof earbuds IPX7",
    "24 hour battery earbuds",
    "best earbuds for professionals"
  ]
}
```

### Example 2: Fashion

Input:
```json
{
  "product_name": "Summer Floral Dress",
  "category": "Women's Fashion",
  "features": "breathable cotton, adjustable straps, pockets",
  "target_audience": "women 25-40",
  "tone": "casual"
}
```

Output:
```json
{
  "headline": "Breezy Summer Dress — Effortless Style Meets All-Day Comfort",
  "bullets": [
    "Soft, breathable cotton keeps you cool on hot summer days",
    "Adjustable straps let you find your perfect fit",
    "Hidden pockets hold your phone and essentials (yes, really!)",
    "Flattering floral print works for brunch, beach, or date night",
    "Machine washable — easy care for busy lifestyles"
  ],
  "description": "Your new go-to dress for everything summer throws at you. Dress it up with heels or keep it casual with sandals — either way, you'll look amazing and feel even better.",
  "seo_keywords": [
    "summer floral dress",
    "cotton dress with pockets",
    "adjustable strap dress",
    "casual summer dress women",
    "breathable summer dress"
  ]
}
```

## Best Practices

1. **Focus on benefits, not features**
   - ✗ "Has 24-hour battery"
   - ✓ "24-hour battery keeps you connected through your busiest days"

2. **Use power words**
   - Premium, Effortless, Instant, Proven, Guaranteed, Exclusive

3. **Address pain points**
   - Identify what frustrates customers and show how product solves it

4. **Create urgency (when appropriate)**
   - Limited stock, Seasonal, Trending, Best-seller

5. **SEO keywords should be natural**
   - Don't stuff keywords
   - Use long-tail keywords (3-5 words)
   - Include product name + key feature

## Customization

Users can override defaults:

```python
# Custom config for luxury products
config = {
    'tone': 'luxury',
    'max_headline_words': 12,
    'min_bullets': 4,
    'quality_threshold': 85
}
```

## References

- [SEO Best Practices](./references/seo-best-practices.md)
- [Copywriting Formulas](./references/copywriting-formulas.md)

## Templates

- [default.txt](./templates/default.txt) - Standard product description
- [luxury.txt](./templates/luxury.txt) - High-end products
- [tech.txt](./templates/tech.txt) - Technical products
