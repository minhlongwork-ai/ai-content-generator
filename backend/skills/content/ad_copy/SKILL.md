---
name: ad-copy
description: Generate high-converting ad copy using proven copywriting formulas (PAS, BAB, Story)
version: 1.0.0
category: marketing
author: AI Content Generator
tags: [ad-copy, marketing, copywriting, conversion, facebook-ads, google-ads]
---

# Ad Copy Skill

## Overview

Generate high-converting ad copy for e-commerce products using proven copywriting formulas. This skill creates 3 variations:
- **PAS** (Problem-Agitation-Solution)
- **BAB** (Before-After-Bridge)
- **Story/Testimonial**

Each variation includes hook, body, and call-to-action.

## When to use this skill

✓ Creating Facebook/Instagram ads
✓ Writing Google Ads copy
✓ TikTok/YouTube ad scripts
✓ Email marketing campaigns
✓ Landing page copy
✓ A/B testing ad variations

## Not ideal for

✗ Product descriptions (use product-description skill)
✗ SEO content (use caption-seo skill)
✗ Long-form content (use blog-post skill)

## Required Inputs

1. **product_name** (string): Product name
2. **category** (string): Product category
3. **selling_points** (string): Key selling points, comma-separated

## Optional Inputs

1. **target_audience** (string): Who is this for? (default: "general")
2. **platform** (string): facebook | instagram | google | tiktok | youtube (default: "facebook")
3. **tone** (string): professional | casual | urgent | luxury (default: "professional")
4. **language** (string): Output language (default: "English")

## Output Format

```json
{
  "variations": [
    {
      "style": "Problem-Agitation-Solution",
      "hook": "Attention-grabbing first line",
      "body": "2-3 sentences explaining the solution",
      "cta": "Clear call-to-action"
    },
    {
      "style": "Before-After-Bridge",
      "hook": "Contrast hook",
      "body": "Transformation story",
      "cta": "Action-oriented CTA"
    },
    {
      "style": "Story/Testimonial",
      "hook": "Relatable story opening",
      "body": "Customer success story",
      "cta": "Social proof CTA"
    }
  ]
}
```

## Quality Checks

- ✓ Exactly 3 variations
- ✓ Each has hook, body, cta
- ✓ Hook length 10-20 words
- ✓ Body length 20-60 words
- ✓ CTA length 3-10 words
- ✓ CTA has action verb
- ✓ No duplicate hooks
- ✓ Styles match (PAS, BAB, Story)

## Configuration

Default config:
```yaml
platform: facebook
tone: professional
language: English
target_audience: general
num_variations: 3
min_hook_words: 10
max_hook_words: 20
min_body_words: 20
max_body_words: 60
min_cta_words: 3
max_cta_words: 10
quality_threshold: 75
```

## Examples

### Example 1: Facebook Ad - Electronics

Input:
```json
{
  "product_name": "Wireless Bluetooth Earbuds",
  "category": "Electronics",
  "selling_points": "noise cancellation, 24h battery, waterproof, affordable",
  "target_audience": "young professionals",
  "platform": "facebook",
  "tone": "professional"
}
```

Output:
```json
{
  "variations": [
    {
      "style": "Problem-Agitation-Solution",
      "hook": "Tired of earbuds that die halfway through your workday?",
      "body": "We've all been there—stuck on a call with 5% battery. Our Wireless Bluetooth Earbuds deliver 24 hours of uninterrupted listening, active noise cancellation, and waterproof protection. All at a price that won't break the bank.",
      "cta": "Get yours today—limited stock!"
    },
    {
      "style": "Before-After-Bridge",
      "hook": "Before: Constantly charging earbuds. After: All-day freedom.",
      "body": "Imagine starting your day with fully charged earbuds and ending it the same way—no charging breaks, no dead battery panic. Our 24-hour battery life makes it possible. Plus, noise cancellation keeps you focused wherever you are.",
      "cta": "Upgrade your audio experience now"
    },
    {
      "style": "Story/Testimonial",
      "hook": "\"These earbuds changed my daily commute completely.\"",
      "body": "Sarah, a marketing manager, used to dread her noisy train rides. Now with active noise cancellation and 24-hour battery, she catches up on podcasts and calls without interruption. Waterproof design means she never worries about rain or sweat.",
      "cta": "Join 10,000+ happy customers"
    }
  ]
}
```

### Example 2: Instagram Ad - Fashion

Input:
```json
{
  "product_name": "Summer Floral Dress",
  "category": "Women's Fashion",
  "selling_points": "breathable cotton, pockets, adjustable fit, versatile",
  "target_audience": "women 25-40",
  "platform": "instagram",
  "tone": "casual"
}
```

Output:
```json
{
  "variations": [
    {
      "style": "Problem-Agitation-Solution",
      "hook": "Another dress with no pockets? We feel your pain.",
      "body": "You love the style but hate carrying a purse everywhere. Our Summer Floral Dress solves that with hidden pockets, breathable cotton, and an adjustable fit that flatters every body. Dress it up or down—it works for everything.",
      "cta": "Shop now—free shipping today! 🌸"
    },
    {
      "style": "Before-After-Bridge",
      "hook": "Before: Choosing between style and comfort. After: Having both.",
      "body": "No more sacrificing comfort for a cute outfit. This dress gives you soft, breathable cotton that keeps you cool all day, adjustable straps for the perfect fit, and yes—pockets! Wear it to brunch, the beach, or date night.",
      "cta": "Add to cart before it sells out"
    },
    {
      "style": "Story/Testimonial",
      "hook": "\"I bought 3 colors and wear them on repeat!\" ⭐⭐⭐⭐⭐",
      "body": "Meet Emma's new favorite dress. She wore it to a wedding, then to the beach, then to work (with a blazer). The breathable cotton keeps her cool, the pockets hold her phone, and the adjustable straps mean it fits perfectly every time.",
      "cta": "Get yours—4.9★ from 2,000+ reviews"
    }
  ]
}
```

### Example 3: Google Ad - Vietnamese

Input:
```json
{
  "product_name": "Tai nghe Bluetooth không dây",
  "category": "Điện tử",
  "selling_points": "chống ồn, pin 24h, chống nước, giá rẻ",
  "target_audience": "sinh viên, nhân viên văn phòng",
  "platform": "google",
  "tone": "professional",
  "language": "Vietnamese"
}
```

Output:
```json
{
  "variations": [
    {
      "style": "Problem-Agitation-Solution",
      "hook": "Tai nghe hết pin giữa cuộc họp quan trọng?",
      "body": "Đừng để pin yếu làm gián đoạn công việc. Tai nghe Bluetooth của chúng tôi có pin 24 giờ, chống ồn chủ động, và chống nước IPX7. Giá chỉ từ 299K—phù hợp túi tiền sinh viên.",
      "cta": "Mua ngay—freeship toàn quốc"
    },
    {
      "style": "Before-After-Bridge",
      "hook": "Trước: Sạc tai nghe 3 lần/ngày. Sau: Sạc 1 lần/tuần.",
      "body": "Tưởng tượng bạn chỉ cần sạc tai nghe một lần và dùng cả tuần. Pin 24 giờ giúp bạn tự do làm việc, học tập, tập gym mà không lo hết pin. Chống ồn giúp tập trung hơn trong môi trường ồn ào.",
      "cta": "Đặt hàng ngay—còn 50 suất"
    },
    {
      "style": "Story/Testimonial",
      "hook": "\"Tai nghe tốt nhất tôi từng dùng!\" - Minh, sinh viên IT",
      "body": "Minh học online 8 tiếng/ngày và cần tai nghe bền. Sau khi thử 5 loại khác, anh tìm thấy tai nghe này: pin trâu, chống ồn tốt, chống nước khi đi mưa. Giá lại rẻ hơn các hãng nổi tiếng.",
      "cta": "Xem 1,000+ đánh giá 5 sao"
    }
  ]
}
```

## Copywriting Formulas Explained

### 1. PAS (Problem-Agitation-Solution)

**Structure:**
- **Problem:** Identify the pain point
- **Agitation:** Make it worse, amplify the frustration
- **Solution:** Present your product as the answer

**When to use:**
- Strong pain points exist
- Audience is aware of the problem
- Competitive market

**Example:**
- Problem: "Tired of earbuds that die halfway through your workday?"
- Agitation: "We've all been there—stuck on a call with 5% battery"
- Solution: "Our earbuds deliver 24 hours of uninterrupted listening"

### 2. BAB (Before-After-Bridge)

**Structure:**
- **Before:** Current frustrating situation
- **After:** Desired outcome
- **Bridge:** How your product gets them there

**When to use:**
- Clear transformation
- Visual/emotional contrast
- Aspirational products

**Example:**
- Before: "Constantly charging earbuds"
- After: "All-day freedom"
- Bridge: "Our 24-hour battery life makes it possible"

### 3. Story/Testimonial

**Structure:**
- **Hook:** Relatable character or quote
- **Body:** Their journey/transformation
- **CTA:** Social proof + action

**When to use:**
- Building trust
- New products
- High-consideration purchases

**Example:**
- Hook: "These earbuds changed my daily commute completely"
- Body: "Sarah used to dread her noisy train rides. Now..."
- CTA: "Join 10,000+ happy customers"

## Platform-Specific Guidelines

### Facebook/Instagram
- Length: 125-150 words max
- Emojis: Yes (sparingly)
- Tone: Conversational
- CTA: Direct ("Shop Now", "Learn More")

### Google Ads
- Headline: 30 chars max
- Description: 90 chars max
- Tone: Professional, benefit-focused
- CTA: Action-oriented ("Get Quote", "Buy Now")

### TikTok
- Length: 100 words max (video script)
- Tone: Casual, trendy
- Hook: First 3 seconds critical
- CTA: Soft ("Link in bio", "Check it out")

### YouTube
- Length: 150-200 words (15-30 sec video)
- Tone: Storytelling
- Hook: First 5 seconds
- CTA: Clear ("Click below", "Visit website")

## Best Practices

### Hook Writing

1. **Ask a question**
   - "Tired of [problem]?"
   - "What if you could [benefit]?"

2. **Make a bold statement**
   - "This changed everything"
   - "We solved [problem] once and for all"

3. **Use contrast**
   - "Before: [pain]. After: [gain]"
   - "Stop [bad thing]. Start [good thing]"

4. **Lead with social proof**
   - "10,000+ customers can't be wrong"
   - "Rated 4.9★ by [audience]"

### Body Copy

1. **Focus on benefits, not features**
   - ✗ "Has 24-hour battery"
   - ✓ "Never worry about charging during your workday"

2. **Use specific numbers**
   - ✗ "Long battery life"
   - ✓ "24 hours of continuous playback"

3. **Address objections**
   - Price: "All at a price that won't break the bank"
   - Quality: "Premium materials, affordable price"
   - Risk: "30-day money-back guarantee"

4. **Create urgency (when appropriate)**
   - "Limited stock"
   - "Sale ends tonight"
   - "Only 50 left"

### CTA Writing

1. **Use action verbs**
   - Shop, Get, Discover, Try, Join, Claim

2. **Add urgency**
   - "Shop now—limited stock"
   - "Get yours today"

3. **Reduce friction**
   - "Free shipping"
   - "No credit card required"
   - "30-day guarantee"

4. **Include social proof**
   - "Join 10,000+ customers"
   - "See why 5,000+ love it"

## Common Mistakes to Avoid

❌ Generic hooks ("Check this out!")
❌ Feature-focused body (not benefit-focused)
❌ Weak CTAs ("Click here")
❌ Too long (people won't read)
❌ No urgency or scarcity
❌ Ignoring platform guidelines
❌ Same copy for all platforms
❌ No social proof

## Customization

Users can override defaults:

```python
# Custom config for urgent sale
config = {
    'tone': 'urgent',
    'platform': 'facebook',
    'max_body_words': 40,  # Shorter for mobile
    'quality_threshold': 80
}
```

## References

- [Copywriting Formulas](./references/copywriting-formulas.md)
- [Platform Ad Specs](./references/platform-ad-specs.md)
- [CTA Best Practices](./references/cta-best-practices.md)

## Templates

- [default.txt](./templates/default.txt) - Standard ad copy
- [urgent.txt](./templates/urgent.txt) - Sale/limited time
- [luxury.txt](./templates/luxury.txt) - Premium products
