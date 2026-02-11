---
name: social-media-poster
description: Post content (images, videos, carousels, mixed media) to Facebook, Instagram, and TikTok using platform APIs. Use when the user wants to publish or schedule social media posts, upload content to social platforms, share media across Facebook/Instagram/TikTok, create scheduled posts, or manage cross-platform publishing. Triggers include "post to Instagram", "upload to TikTok", "share on Facebook", "schedule a post", "publish to social media", "post this to all platforms", "cross-post", "social media upload", "schedule content", "queue this post".
---

# Social Media Poster

## Overview

Publish images, videos, carousels, and mixed media to Facebook, Instagram, and TikTok through their official APIs. Supports platform-selective posting, media validation, and scheduled publishing via a cron-based queue.

## Prerequisites

Before using this skill, the user must have:

1. **Environment variables** configured in a `.env` file (see `.env.example` in this skill's root)
2. **Python dependencies** installed: `pip install -r requirements.txt` (from this skill's root)
3. **API credentials** for each target platform (Meta Graph API for Facebook + Instagram, TikTok Content Posting API)

If the user hasn't set these up yet, remind them to configure credentials before attempting to post. Do NOT attempt to post without valid credentials — it will fail.

## Workflow Decision Tree

When the user wants to post or schedule social media content, follow this decision tree:

```
User request
├── Wants to post NOW → Go to "Immediate Posting Workflow"
├── Wants to SCHEDULE a post → Go to "Scheduling Workflow"
├── Wants to check SCHEDULE → Run: python scripts/run_scheduler.py --list
└── Wants to cancel a SCHEDULED post → Run: python scripts/run_scheduler.py --cancel <post-id>
```

## Immediate Posting Workflow

### Step 1: Gather Inputs

Collect the following from the user (ask if not provided):

| Input | Required | Details |
|-------|----------|---------|
| **Media files** | Yes | Absolute path(s) to image(s) and/or video(s) |
| **Caption** | Yes | Post text/caption |
| **Platforms** | Yes | Which platforms: `facebook`, `instagram`, `tiktok` (one or more) |
| **Hashtags** | No | Appended to caption if provided |

### Step 2: Validate Media

Before posting, ALWAYS run the validation script to check media meets platform requirements:

```bash
python scripts/validate_media.py --files <file1> <file2> ... --platforms <platform1> <platform2> ...
```

This checks:
- File exists and is readable
- File format is supported by the target platform(s)
- File size is within platform limits
- Image dimensions meet minimum requirements
- Video duration and codec compatibility

If validation fails, report the specific issues to the user and ask them to provide corrected media. Do NOT attempt to post invalid media.

### Step 3: Determine Post Type

Based on the media provided, determine the post type:

| Media Provided | Post Type | FB Support | IG Support | TK Support |
|---------------|-----------|------------|------------|------------|
| 1 image | Single image | Yes | Yes | Yes (photo mode) |
| 2-10 images | Carousel | Yes | Yes (carousel) | Yes (photo mode, max 35) |
| 1 video | Single video | Yes | Yes (Reel) | Yes |
| Images + videos mixed | Mixed carousel | Yes | Yes (carousel) | No — split into separate posts |

**Important platform rules:**
- **Instagram carousels**: Max 10 items. Images + videos can be mixed.
- **Instagram Reels**: Single video only. Aspect ratio 9:16 recommended.
- **TikTok**: Video posts are standard. Photo mode supports multiple images (up to 35). Cannot mix images and videos in one post.
- **Facebook**: Most flexible — supports all combinations.

### Step 4: Post to Selected Platforms

Execute posts sequentially per platform. For each selected platform, run the appropriate script:

**Facebook:**
```bash
python scripts/post_facebook.py --media <file1> <file2> ... --caption "Your caption here"
```

**Instagram:**
```bash
python scripts/post_instagram.py --media <file1> <file2> ... --caption "Your caption here"
```

**TikTok:**
```bash
python scripts/post_tiktok.py --media <file1> <file2> ... --caption "Your caption here"
```

### Step 5: Report Results

After posting, report to the user:
- Which platforms succeeded with post IDs/URLs
- Which platforms failed and why
- Any warnings (e.g., media was auto-adjusted)

## Scheduling Workflow

### Adding a Scheduled Post

To schedule a post for later, run:

```bash
python scripts/schedule_post.py \
  --media <file1> <file2> ... \
  --caption "Your caption here" \
  --platforms facebook instagram tiktok \
  --schedule "2025-01-15 14:30" \
  --timezone "America/New_York"
```

The schedule script:
1. Validates the media (same checks as immediate posting)
2. Copies media to `assets/scheduled_media/` to ensure files are available at post time
3. Adds the post to the schedule queue (`assets/schedule_queue.json`)
4. Returns a post ID the user can use to check status or cancel

### Managing the Schedule

**List scheduled posts:**
```bash
python scripts/run_scheduler.py --list
```

**Cancel a scheduled post:**
```bash
python scripts/run_scheduler.py --cancel <post-id>
```

**Manually trigger the scheduler (process all due posts now):**
```bash
python scripts/run_scheduler.py --run
```

### Cron Setup

For automated scheduling, the user needs a cron job that runs the scheduler periodically. Suggest this crontab entry:

```bash
# Run social media scheduler every 5 minutes
*/5 * * * * cd /path/to/social-media-poster && python scripts/run_scheduler.py --run >> logs/scheduler.log 2>&1
```

The scheduler checks `assets/schedule_queue.json` for posts whose scheduled time has passed, posts them, and marks them as completed or failed.

## Media Requirements Quick Reference

### Images
| Platform | Formats | Max Size | Min Dimensions | Max Dimensions |
|----------|---------|----------|----------------|----------------|
| Facebook | JPG, PNG | 10 MB | 100x100 | 2048x2048 recommended |
| Instagram | JPG, PNG | 8 MB | 320x320 | 1440x1440 recommended |
| TikTok | JPG, PNG, WEBP | 20 MB | 360x360 | — |

### Videos
| Platform | Formats | Max Size | Max Duration | Recommended Aspect |
|----------|---------|----------|--------------|--------------------|
| Facebook | MP4, MOV | 10 GB | 240 min | 16:9 or 9:16 |
| Instagram (Reel) | MP4, MOV | 1 GB | 15 min | 9:16 |
| Instagram (Carousel) | MP4, MOV | 1 GB | 60 sec | 1:1 or 9:16 |
| TikTok | MP4, MOV, WEBM | 4 GB | 10 min | 9:16 |

## Error Handling

Common errors and how to handle them:

| Error | Cause | Resolution |
|-------|-------|------------|
| `AUTH_ERROR` | Invalid or expired token | User needs to refresh their API token and update `.env` |
| `RATE_LIMIT` | Too many API calls | Wait and retry. Scripts auto-retry with exponential backoff |
| `MEDIA_TOO_LARGE` | File exceeds platform limit | Compress or resize the file before posting |
| `INVALID_FORMAT` | Unsupported file type | Convert to a supported format (MP4 for video, JPG/PNG for images) |
| `PERMISSION_DENIED` | App lacks required permissions | User needs to check app permissions in platform developer console |
| `CONTAINER_ERROR` (IG) | Instagram container creation failed | Check that Instagram Business Account is properly linked |

## Environment Variables

The skill uses these environment variables (loaded from `.env`):

```
# Meta (Facebook + Instagram)
META_ACCESS_TOKEN=            # Long-lived Page Access Token
FACEBOOK_PAGE_ID=             # Facebook Page ID
INSTAGRAM_BUSINESS_ACCOUNT_ID= # Instagram Business Account ID

# TikTok
TIKTOK_CLIENT_KEY=            # TikTok App Client Key
TIKTOK_CLIENT_SECRET=         # TikTok App Client Secret
TIKTOK_ACCESS_TOKEN=          # TikTok OAuth Access Token
```

## Resources

### scripts/
- `post_facebook.py` — Post content to Facebook Pages via Graph API
- `post_instagram.py` — Post content to Instagram via Content Publishing API
- `post_tiktok.py` — Post content to TikTok via Content Posting API
- `validate_media.py` — Validate media files against platform requirements
- `schedule_post.py` — Add a post to the scheduling queue
- `run_scheduler.py` — Process the scheduling queue (designed for cron execution)

### references/
- `api-reference.md` — Detailed API endpoint documentation for all three platforms
- `scheduling.md` — In-depth scheduling system documentation

### assets/
- `schedule_queue.json` — Scheduling queue (auto-created on first scheduled post)
- `scheduled_media/` — Stored media files for scheduled posts (auto-created)
