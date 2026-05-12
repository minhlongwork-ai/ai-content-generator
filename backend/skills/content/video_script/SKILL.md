---
name: video-script
description: Generate engaging video scripts for short-form content (TikTok, Reels, YouTube Shorts)
version: 1.0.0
category: video-marketing
author: AI Content Generator
tags: [video, script, tiktok, reels, youtube-shorts, short-form]
---

# Video Script Skill

## Overview

Generate engaging video scripts for short-form content (15-60 seconds). This skill creates:
- Hook (first 3-5 seconds)
- Multiple scenes with visuals + narration
- Call-to-action (last 3-5 seconds)
- Background music suggestion
- Platform hashtags

## When to use this skill

✓ Creating TikTok videos
✓ Instagram Reels
✓ YouTube Shorts
✓ Facebook Reels
✓ Product demo videos
✓ Unboxing videos
✓ Tutorial videos

## Not ideal for

✗ Long-form videos (>60 seconds)
✗ Static image ads (use ad-copy skill)
✗ Product descriptions (use product-description skill)

## Required Inputs

1. **product_name** (string): Product name
2. **category** (string): Product category
3. **features** (string): Key features, comma-separated

## Optional Inputs

1. **target_audience** (string): Who is this for? (default: "general")
2. **platform** (string): tiktok | reels | youtube-shorts (default: "tiktok")
3. **tone** (string): professional | casual | energetic | calm (default: "energetic")
4. **language** (string): Output language (default: "English")
5. **duration** (int): Total video duration in seconds (default: 30)
6. **n_scenes** (int): Number of scenes (default: 3)

## Output Format

```json
{
  "title": "Video title (max 60 chars)",
  "hook": {
    "text": "Hook text",
    "visual": "Visual description",
    "duration": 3
  },
  "scenes": [
    {
      "scene_number": 1,
      "visual": "What viewer sees",
      "narration": "Voiceover text",
      "duration": 5
    }
  ],
  "cta": {
    "text": "Call to action",
    "visual": "CTA visual",
    "duration": 3
  },
  "music_suggestion": "Upbeat pop, 120 BPM",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]
}
```

## Quality Checks

- ✓ Has title (≤60 chars)
- ✓ Has hook with text, visual, duration
- ✓ Hook duration 3-5 seconds
- ✓ Has scenes (min 2, max 5)
- ✓ Each scene has visual, narration, duration
- ✓ Scene duration 3-10 seconds each
- ✓ Has CTA with text, visual, duration
- ✓ CTA duration 3-5 seconds
- ✓ Total duration matches target (±3 seconds)
- ✓ Has music suggestion
- ✓ Has 5 hashtags

## Configuration

Default config:
```yaml
platform: tiktok
tone: energetic
language: English
target_audience: general
duration: 30
n_scenes: 3
min_hook_duration: 3
max_hook_duration: 5
min_scene_duration: 3
max_scene_duration: 10
min_cta_duration: 3
max_cta_duration: 5
min_scenes: 2
max_scenes: 5
num_hashtags: 5
max_title_length: 60
duration_tolerance: 3
quality_threshold: 75
```

## Examples

### Example 1: TikTok - Electronics

Input:
```json
{
  "product_name": "Wireless Bluetooth Earbuds",
  "category": "Electronics",
  "features": "noise cancellation, 24h battery, waterproof IPX7",
  "target_audience": "young professionals",
  "platform": "tiktok",
  "tone": "energetic",
  "duration": 30,
  "n_scenes": 3
}
```

Output:
```json
{
  "title": "These Earbuds Changed My Life 🎧",
  "hook": {
    "text": "POV: You finally found earbuds that don't die mid-call",
    "visual": "Close-up of earbuds in case, dramatic lighting",
    "duration": 3
  },
  "scenes": [
    {
      "scene_number": 1,
      "visual": "Person wearing earbuds in busy coffee shop, focused on laptop",
      "narration": "Active noise cancellation blocks out all the chaos",
      "duration": 7
    },
    {
      "scene_number": 2,
      "visual": "Time-lapse showing 24 hours passing, earbuds still playing",
      "narration": "24-hour battery means you charge once a week, not three times a day",
      "duration": 8
    },
    {
      "scene_number": 3,
      "visual": "Person running in rain, earbuds still working perfectly",
      "narration": "IPX7 waterproof—rain, sweat, spilled coffee, no problem",
      "duration": 7
    }
  ],
  "cta": {
    "text": "Link in bio—limited stock!",
    "visual": "Product shot with price and 'Shop Now' button animation",
    "duration": 5
  },
  "music_suggestion": "Upbeat electronic, 128 BPM, trending TikTok sound",
  "hashtags": ["#WirelessEarbuds", "#TechTok", "#ProductReview", "#NoiseCancelling", "#TechGadgets"]
}
```

### Example 2: Instagram Reels - Fashion

Input:
```json
{
  "product_name": "Summer Floral Dress",
  "category": "Women's Fashion",
  "features": "breathable cotton, pockets, adjustable straps",
  "target_audience": "women 25-40",
  "platform": "reels",
  "tone": "casual",
  "duration": 25,
  "n_scenes": 3
}
```

Output:
```json
{
  "title": "The Dress With Pockets Everyone's Talking About 🌸",
  "hook": {
    "text": "Wait for the pockets... 👀",
    "visual": "Model spinning in dress, camera zooms in",
    "duration": 3
  },
  "scenes": [
    {
      "scene_number": 1,
      "visual": "Close-up of soft cotton fabric flowing in breeze",
      "narration": "Breathable cotton that keeps you cool all day",
      "duration": 6
    },
    {
      "scene_number": 2,
      "visual": "Model adjusting straps to perfect fit",
      "narration": "Adjustable straps mean it fits YOUR body perfectly",
      "duration": 6
    },
    {
      "scene_number": 3,
      "visual": "Model pulls out phone from hidden pocket, surprised reaction",
      "narration": "And yes—it has POCKETS! Deep ones!",
      "duration": 6
    }
  ],
  "cta": {
    "text": "Shop now—link in bio! Free shipping today 🚚",
    "visual": "Product carousel showing 3 color options",
    "duration": 4
  },
  "music_suggestion": "Upbeat indie pop, 110 BPM, feel-good vibes",
  "hashtags": ["#SummerDress", "#DressWithPockets", "#OOTD", "#FashionFinds", "#SummerStyle"]
}
```

### Example 3: YouTube Shorts - Vietnamese

Input:
```json
{
  "product_name": "Tai nghe Bluetooth không dây",
  "category": "Điện tử",
  "features": "chống ồn, pin 24h, chống nước IPX7",
  "target_audience": "sinh viên, nhân viên văn phòng",
  "platform": "youtube-shorts",
  "tone": "professional",
  "language": "Vietnamese",
  "duration": 35,
  "n_scenes": 4
}
```

Output:
```json
{
  "title": "Tai Nghe Pin Trâu Nhất 2026 🔋",
  "hook": {
    "text": "Tai nghe này sạc 1 lần dùng cả tuần!",
    "visual": "Tai nghe trong hộp sạc, màn hình hiển thị 100% pin",
    "duration": 4
  },
  "scenes": [
    {
      "scene_number": 1,
      "visual": "Người đeo tai nghe làm việc trong văn phòng ồn ào",
      "narration": "Chống ồn chủ động giúp tập trung 100%",
      "duration": 6
    },
    {
      "scene_number": 2,
      "visual": "Đồng hồ hiển thị 24 giờ trôi qua, tai nghe vẫn hoạt động",
      "narration": "Pin 24 giờ—sạc 1 lần dùng cả tuần",
      "duration": 7
    },
    {
      "scene_number": 3,
      "visual": "Người chạy bộ dưới mưa, tai nghe vẫn hoạt động tốt",
      "narration": "Chống nước IPX7—mưa hay mồ hôi đều OK",
      "duration": 7
    },
    {
      "scene_number": 4,
      "visual": "So sánh giá với các hãng khác trên màn hình",
      "narration": "Giá chỉ bằng 1/3 các hãng nổi tiếng",
      "duration": 6
    }
  ],
  "cta": {
    "text": "Link mua hàng ở phần mô tả—freeship toàn quốc!",
    "visual": "Sản phẩm với giá và nút 'Mua Ngay'",
    "duration": 5
  },
  "music_suggestion": "Nhạc nền tech review, 115 BPM, hiện đại",
  "hashtags": ["#TaiNgheBluetooth", "#Review", "#CongNghe", "#TechVietnam", "#GadgetReview"]
}
```

## Best Practices

### Hook Writing (First 3-5 Seconds)

**Critical:** 50% of viewers drop off in first 3 seconds!

1. **Pattern interrupt**
   - "Wait for it..."
   - "POV: You finally found..."
   - "This changed everything"

2. **Ask a question**
   - "Tired of [problem]?"
   - "What if I told you..."

3. **Make a bold claim**
   - "Best [product] I've ever used"
   - "This [product] is going viral for a reason"

4. **Show the payoff first**
   - Start with the "wow" moment
   - Then explain how

### Scene Structure

1. **Show, don't tell**
   - Visual proof > verbal claims
   - Demonstrate features in action

2. **One idea per scene**
   - Don't overload
   - Keep it simple

3. **Smooth transitions**
   - Match cuts
   - Visual continuity
   - Music beats

4. **Build momentum**
   - Start strong
   - Build interest
   - Peak at CTA

### CTA (Call-to-Action)

1. **Be specific**
   - ✗ "Check it out"
   - ✓ "Link in bio—limited stock"

2. **Add urgency**
   - "Today only"
   - "Limited stock"
   - "Sale ends tonight"

3. **Reduce friction**
   - "Free shipping"
   - "No credit card required"
   - "30-day guarantee"

4. **Visual CTA**
   - Show product + price
   - Animated button
   - Clear next step

### Music Selection

1. **Match energy to content**
   - Product demo: Upbeat, energetic
   - Tutorial: Calm, focused
   - Unboxing: Exciting, building

2. **Use trending sounds (TikTok)**
   - Boosts visibility
   - Familiar to audience
   - Check TikTok Creative Center

3. **BPM matters**
   - Fast (120-140 BPM): Energetic, exciting
   - Medium (100-120 BPM): Upbeat, positive
   - Slow (80-100 BPM): Calm, emotional

### Platform-Specific Tips

#### TikTok
- Hook: First 1-2 seconds critical
- Length: 15-30 seconds ideal
- Trends: Use trending sounds/effects
- Text: On-screen text for no-sound viewers
- Hashtags: Mix trending + niche

#### Instagram Reels
- Hook: First 3 seconds
- Length: 15-30 seconds (can go to 90)
- Quality: Higher production value
- Music: Instagram music library
- Hashtags: 3-5 relevant

#### YouTube Shorts
- Hook: First 3-5 seconds
- Length: Up to 60 seconds
- SEO: Title + description matter
- Thumbnails: Auto-generated, make first frame count
- Hashtags: #Shorts + 2-3 relevant

## Common Mistakes to Avoid

❌ Slow hook (lose viewers immediately)
❌ Too much text on screen
❌ Poor lighting/audio quality
❌ No clear CTA
❌ Too long (attention span is short!)
❌ Boring visuals (static shots)
❌ No music or wrong music
❌ Ignoring platform trends

## Customization

Users can override defaults:

```python
# Custom config for longer YouTube Short
config = {
    'platform': 'youtube-shorts',
    'duration': 50,
    'n_scenes': 5,
    'tone': 'professional',
    'quality_threshold': 80
}
```

## References

- [Video Hook Formulas](./references/video-hook-formulas.md)
- [Platform Specs](./references/platform-video-specs.md)
- [Music Selection Guide](./references/music-selection.md)
- [Trending Sounds](./references/trending-sounds.md)

## Templates

- [default.txt](./templates/default.txt) - Standard product video
- [unboxing.txt](./templates/unboxing.txt) - Unboxing format
- [tutorial.txt](./templates/tutorial.txt) - How-to format
- [comparison.txt](./templates/comparison.txt) - Before/after
