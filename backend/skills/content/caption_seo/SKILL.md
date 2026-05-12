---
name: caption-seo
description: Generate SEO-optimized titles, captions, and hashtags for e-commerce product listings
version: 1.0.0
category: e-commerce
author: AI Content Generator
tags: [seo, caption, title, hashtags, social-media]
---

# Caption SEO Skill

## Overview

Generate SEO-optimized titles and captions for product listings on e-commerce platforms and social media. This skill creates:
- SEO-optimized title (max 80 characters)
- Short caption/description (max 160 characters)
- 5 relevant hashtags
- 3 long-tail SEO keywords

## When to use this skill

✓ Creating product listings for Shopee, Lazada, Amazon
✓ Optimizing existing product titles for search
✓ Writing social media captions (Instagram, Facebook, TikTok)
✓ Generating hashtags for product posts
✓ SEO optimization for product pages

## Not ideal for

✗ Long-form product descriptions (use product-description skill)
✗ Ad copy (use ad-copy skill)
✗ Blog posts (use blog-post skill)

## Required Inputs

1. **product_name** (string): Product name
2. **category** (string): Product category
3. **features** (string): Key features, comma-separated

## Optional Inputs

1. **platform** (string): shopee | lazada | amazon | instagram | facebook | tiktok (default: "shopee")
2. **language** (string): Output language (default: "English")

## Output Format

```json
{
  "seo_title": "SEO-optimized title under 80 characters",
  "caption": "Short description under 160 characters",
  "hashtags": [
    "#hashtag1",
    "#hashtag2",
    "#hashtag3",
    "#hashtag4",
    "#hashtag5"
  ],
  "seo_keywords": [
    "long-tail keyword 1",
    "long-tail keyword 2",
    "long-tail keyword 3"
  ]
}
```

## Quality Checks

- ✓ SEO title length ≤ 80 characters
- ✓ Caption length ≤ 160 characters
- ✓ Exactly 5 hashtags
- ✓ Hashtags start with #
- ✓ 3 SEO keywords
- ✓ No duplicate keywords
- ✓ Title contains product name
- ✓ Keywords are long-tail (3+ words)

## Configuration

Default config:
```yaml
platform: shopee
language: English
max_title_length: 80
max_caption_length: 160
num_hashtags: 5
num_seo_keywords: 3
min_keyword_words: 3
quality_threshold: 70
```

## Examples

### Example 1: Shopee Electronics

Input:
```json
{
  "product_name": "Wireless Bluetooth Earbuds",
  "category": "Electronics",
  "features": "noise cancellation, 24h battery, waterproof IPX7",
  "platform": "shopee",
  "language": "English"
}
```

Output:
```json
{
  "seo_title": "Wireless Bluetooth Earbuds Noise Cancelling 24H Battery Waterproof IPX7",
  "caption": "Premium wireless earbuds with active noise cancellation, all-day battery life, and waterproof design. Perfect for work, gym, and travel.",
  "hashtags": [
    "#WirelessEarbuds",
    "#BluetoothEarbuds",
    "#NoiseCancelling",
    "#WaterproofEarbuds",
    "#TechGadgets"
  ],
  "seo_keywords": [
    "wireless bluetooth earbuds noise cancelling",
    "waterproof earbuds 24 hour battery",
    "best wireless earbuds for sports"
  ]
}
```

### Example 2: Instagram Fashion

Input:
```json
{
  "product_name": "Summer Floral Dress",
  "category": "Women's Fashion",
  "features": "breathable cotton, adjustable straps, pockets",
  "platform": "instagram",
  "language": "English"
}
```

Output:
```json
{
  "seo_title": "Summer Floral Dress Cotton Breathable Adjustable Straps with Pockets",
  "caption": "Your new favorite summer dress! Soft cotton, adjustable fit, and yes—it has pockets! Perfect for brunch, beach days, or date nights. 🌸☀️",
  "hashtags": [
    "#SummerDress",
    "#FloralDress",
    "#DressWithPockets",
    "#SummerFashion",
    "#OOTD"
  ],
  "seo_keywords": [
    "summer floral dress with pockets",
    "breathable cotton dress adjustable straps",
    "casual summer dress women"
  ]
}
```

### Example 3: Vietnamese (Shopee)

Input:
```json
{
  "product_name": "Tai nghe Bluetooth không dây",
  "category": "Điện tử",
  "features": "chống ồn, pin 24h, chống nước IPX7",
  "platform": "shopee",
  "language": "Vietnamese"
}
```

Output:
```json
{
  "seo_title": "Tai Nghe Bluetooth Không Dây Chống Ồn Pin 24H Chống Nước IPX7",
  "caption": "Tai nghe Bluetooth cao cấp với chống ồn chủ động, pin 24 giờ, chống nước IPX7. Hoàn hảo cho công việc, tập gym và du lịch.",
  "hashtags": [
    "#TaiNgheBluetooth",
    "#TaiNgheKhongDay",
    "#ChongOn",
    "#ChongNuoc",
    "#CongNghe"
  ],
  "seo_keywords": [
    "tai nghe bluetooth không dây chống ồn",
    "tai nghe chống nước pin 24 giờ",
    "tai nghe bluetooth tốt nhất"
  ]
}
```

## Best Practices

### SEO Title Optimization

1. **Front-load important keywords**
   - ✓ "Wireless Bluetooth Earbuds Noise Cancelling 24H Battery"
   - ✗ "Amazing Earbuds That Are Wireless and Have Bluetooth"

2. **Include key specs**
   - Size, color, material, capacity
   - "iPhone 15 Case Silicone Shockproof Clear"

3. **Use separators wisely**
   - Pipe: | (formal, e-commerce)
   - Dash: - (casual, blogs)
   - Space: (Shopee, Lazada)

4. **Platform-specific**
   - Shopee: All caps for emphasis "TAI NGHE BLUETOOTH"
   - Amazon: Title case "Wireless Bluetooth Earbuds"
   - Instagram: Casual, emoji-friendly

### Caption Writing

1. **Hook in first 50 characters**
   - Mobile users see truncated text
   - Make it count!

2. **Include benefits, not just features**
   - ✗ "Has 24-hour battery"
   - ✓ "Never worry about charging during your workday"

3. **Add urgency (when appropriate)**
   - "Limited stock"
   - "Flash sale today"
   - "New arrival"

4. **Use emojis strategically**
   - Instagram/TikTok: Yes (🔥💯✨)
   - Shopee/Lazada: Sparingly
   - Amazon: No

### Hashtag Strategy

1. **Mix popularity levels**
   - 1-2 mega hashtags (1M+ posts): #Fashion #Tech
   - 2-3 medium hashtags (100K-1M): #WirelessEarbuds
   - 1-2 niche hashtags (10K-100K): #NoiseCancellingEarbuds

2. **Platform-specific**
   - Instagram: 5-10 hashtags
   - TikTok: 3-5 hashtags
   - Facebook: 1-3 hashtags
   - Shopee/Lazada: Not used

3. **Avoid banned hashtags**
   - Check platform guidelines
   - Avoid spammy hashtags

4. **Use branded hashtags**
   - Your brand name
   - Campaign hashtags
   - Product line hashtags

### SEO Keywords

1. **Long-tail is better**
   - ✗ "earbuds"
   - ✓ "wireless bluetooth earbuds noise cancelling"

2. **Include modifiers**
   - Best, Top, Cheap, Premium
   - 2026, New, Latest
   - For [audience]: "for sports", "for work"

3. **Local SEO**
   - Add location: "tai nghe bluetooth Hà Nội"
   - Add language: "wireless earbuds Philippines"

## Platform-Specific Guidelines

### Shopee
- Title: 80 chars max
- Use ALL CAPS for key words
- Include price range if competitive
- Add "Freeship" if applicable

### Lazada
- Title: 255 chars max (but keep under 80 for mobile)
- Include brand name
- Add "Official Store" if applicable

### Amazon
- Title: 200 chars max (but keep under 80 for mobile)
- Follow category guidelines
- Include size, color, quantity

### Instagram
- Caption: 2,200 chars max (but keep under 160 for preview)
- Use line breaks for readability
- Emojis encouraged
- 5-10 hashtags

### TikTok
- Caption: 150 chars max
- 3-5 hashtags
- Trending hashtags boost visibility

## Customization

Users can override defaults:

```python
# Custom config for Instagram
config = {
    'platform': 'instagram',
    'max_caption_length': 200,
    'num_hashtags': 10,
    'quality_threshold': 80
}
```

## References

- [SEO Title Best Practices](./references/seo-title-optimization.md)
- [Hashtag Strategy Guide](./references/hashtag-strategy.md)
- [Platform Guidelines](./references/platform-guidelines.md)

## Templates

- [default.txt](./templates/default.txt) - Standard e-commerce
- [social.txt](./templates/social.txt) - Social media focused
- [shopee.txt](./templates/shopee.txt) - Shopee optimized
