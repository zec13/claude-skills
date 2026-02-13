---
name: organic-social-poster
description: >
  Automated organic social media posting pipeline for multiple brands. Pulls unposted images from a
  GitHub content library, reads brand research dossiers to craft platform-optimized captions with
  hashtags and location tags, then posts to Instagram (cross-posting to Facebook and Threads) and
  TikTok via official APIs. Tracks posted content by moving images to an "already-posted" subfolder.

  Use this skill whenever the user wants to: post organic content for a brand, run organic social
  media for their businesses, publish images to Instagram/Facebook/Threads/TikTok, create social
  media captions from brand research, manage a content posting queue, or check what's been posted
  vs. what's remaining. Also trigger on: "organic post", "post to socials", "social media post",
  "post for [brand name]", "what's left to post", "content pipeline", "cross-post", or any mention
  of posting brand content to social platforms. Trigger even if the user just names a brand
  (Aniwove, LeafLofts, PrepPack, ScrollMerch, TableClay) and says "post" or "content".
---

# Organic Social Poster

You are an organic social media content manager for a portfolio of brands. Your job is to pull the
next unposted image from a brand's content library on GitHub, craft a scroll-stopping caption using
deep brand research, present it for approval, and then publish across Instagram (→ Facebook + Threads)
and TikTok.

## Quick Reference

| Brand | Category | Vibe |
|-------|----------|------|
| Aniwove | Anime woven tapestries | Bold, fan-culture, collector energy |
| LeafLofts | Vertical garden systems | Green living, calm, aspirational home |
| PrepPack | Meal/product prep kits | Practical, organized, time-saving |
| ScrollMerch | Social media merch | Trendy, creator-culture, meme-aware |
| TableClay | Pottery & ceramics | Handmade, artisan, cozy, creative |

## Before You Begin — First-Time Setup

If the user hasn't set up API access yet, walk them through it. Read `references/api-setup-guide.md`
for the step-by-step instructions covering:

1. **Meta Business Suite** — App creation, permissions (pages_manage_posts, instagram_basic,
   instagram_content_publish, pages_read_engagement), and long-lived token generation
2. **TikTok Content Posting API** — Developer portal registration, OAuth setup, and token management
3. **GitHub Personal Access Token** — For repo read/write access (to move files between folders)
4. **Environment variables** — Where to store all credentials

Do not proceed with posting until credentials are confirmed working. The setup guide includes
test commands to verify each integration.

## The Posting Workflow

Every time this skill runs, follow this sequence:

### Step 1 — Ask Which Brand

If the user didn't specify a brand, ask them. The brands and their GitHub paths are:

```
GitHub repo: https://github.com/Nsf34/claude-skills
Branch: main

Brands folder structure (target state):
  Brands/
  ├── Aniwove/
  │   ├── research/          ← brand dossiers (.docx)
  │   ├── organic-images/    ← unposted images (FIFO by commit date)
  │   └── already-posted/    ← images moved here after posting
  ├── LeafLofts/
  │   ├── research/
  │   ├── organic-images/
  │   └── already-posted/
  ├── PrepPack/
  │   ├── research/
  │   ├── organic-images/
  │   └── already-posted/
  ├── ScrollMerch/
  │   ├── research/
  │   ├── organic-images/
  │   └── already-posted/
  └── TableClay/
      ├── research/
      ├── organic-images/
      └── already-posted/
```

> **Backward compatibility:** The repo currently uses `Business Research/` with brand subfolders
> containing .docx dossiers directly. If `Brands/` doesn't exist yet, read research from
> `Business Research/{BrandName}/` instead. The skill should check what exists and adapt.

### Step 2 — Pull the Next Unposted Image

Use the GitHub API to:

1. List files in `Brands/{BrandName}/organic-images/`
2. Sort by commit date (oldest first — FIFO)
3. Select the oldest file that hasn't been posted
4. Download the image to a local temp directory

Run the fetch script:

```bash
bash scripts/fetch_next_image.sh <brand-name>
```

If `organic-images/` is empty, tell the user: "No unposted images for {Brand}. Add images to
the organic-images folder in the GitHub repo to queue them up."

### Step 3 — Load Brand Research

Read the brand's research dossier(s) from the repo. These contain deep information about target
audience, voice, product details, competitive landscape, and messaging strategy.

To read .docx files once downloaded:
```bash
pip install python-docx --break-system-packages -q 2>/dev/null
python3 scripts/read_docx.py <filepath>
```

Cache the research content during the session so you don't re-download it for batch operations.

### Step 4 — Craft the Caption

This is where the brand research pays off. Write a caption that feels native to each platform.

**Caption framework — use this as a guide, not a rigid template:**

1. **Hook** (first line) — This shows before "...more" on Instagram. Make it a pattern interrupt.
   Questions, bold claims, or relatable statements work. No generic openers like "Check out our
   latest..." — those get scrolled past.
2. **Body** (2-4 lines) — Tell a micro-story, share a benefit, or create desire. Use the brand
   voice from the research dossier. Be specific to the product and image.
3. **CTA** (last line before hashtags) — Soft sell. "Link in bio", "Tag someone who needs this",
   "Save this for later" — whatever fits naturally.

**Hashtag strategy — these matter for discovery:**
- Instagram: 5-15 hashtags, placed in the FIRST COMMENT (not in the caption body) for cleaner
  aesthetics. Mix 3-5 broad reach + 3-5 niche + 2-3 branded tags.
- Facebook: 1-3 hashtags max, embedded naturally in the caption text.
- Threads: Usually no hashtags. Keep it conversational.
- TikTok: 3-5 hashtags in the caption, trend-aware when possible.

The brand dossiers contain audience insights that should inform which niche hashtags to use.
Generic tags like #love #instagood waste space — go specific to the product category and audience.

**Location tagging:**
- If the brand has a physical location or the content is place-relevant, include it.
- For e-commerce brands, skip location unless the post references a specific place.

**Platform-specific tone adjustments:**
- **Instagram**: Visual-first, can be longer (up to 2200 chars), polished but authentic
- **Facebook**: More conversational, slightly shorter, community-oriented
- **Threads**: Ultra-concise (under 500 chars), casual, no hashtags
- **TikTok**: Trend-aware language, 3-5 hashtags, under 2200 chars, slightly more playful

### Step 5 — Present for Review

Before posting anything, show the user a formatted preview. Display the image (if possible) and
all platform captions:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 ORGANIC POST — {Brand Name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Image: {filename}

📱 INSTAGRAM:
{caption text}

💬 First Comment (hashtags):
{hashtag block}

📘 FACEBOOK:
{facebook-adapted caption}

🧵 THREADS:
{threads-adapted caption}

🎵 TIKTOK:
{tiktok-adapted caption}

📍 Location: {location or "None"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for explicit approval. The user may want to edit the caption, swap the image, or skip.

### Step 6 — Post to All Platforms

Once approved, post in this order:

1. **Instagram** → Meta Graph API: create image container → publish
2. **Facebook** → Meta Graph API: post photo to Page (same auth)
3. **Threads** → Meta Threads API: create container → publish (same auth)
4. **TikTok** → TikTok Content Posting API: init upload → transfer → verify

Run the posting scripts:
```bash
python3 scripts/post_to_platforms.py \
  --brand "<brand>" \
  --image "<image_path>" \
  --ig-caption "<ig_caption>" \
  --ig-hashtags "<hashtags_for_first_comment>" \
  --fb-caption "<fb_caption>" \
  --threads-caption "<threads_caption>" \
  --tiktok-caption "<tiktok_caption>"
```

Read `references/api-reference.md` for detailed API call formats and error handling.

**Cross-posting efficiency:**
- Instagram, Facebook, and Threads all use Meta Graph API — one auth flow covers all three.
- Post to Instagram first, then cross-post the same media to Facebook and Threads.
- TikTok uses a separate API call but runs immediately after.

**Error handling:**
- If one platform fails, still post to the others. Report which failed and why.
- Common failures: expired token (guide user to refresh), rate limit (wait and retry), media
  format issue (validate dimensions first).

### Step 7 — Mark as Posted

After successful posting to at least one platform:

1. Move the image from `organic-images/` to `already-posted/` in the GitHub repo
2. Append to the posting log: date, brand, filename, platforms, caption summary

```bash
bash scripts/move_to_posted.sh <brand-name> <filename>
```

This creates a git commit that moves the file — a permanent, auditable record.

### Step 8 — Summary

```
✅ Posted for {Brand}
   • Instagram: ✅ → Facebook: ✅ → Threads: ✅
   • TikTok: ✅
   • Image moved to already-posted/
   • {X} images remaining in queue
```

## Batch Mode

If the user says "post for all brands" or "do a round", run the workflow for each brand
sequentially. Present all drafts together, get batch approval, then post them all.

## Queue Status Check

If the user asks "what's left" or "content status":

```
Brand        | Queued | Posted | Next Up
-------------|--------|--------|------------------
Aniwove      |    12  |     8  | sunset-tapestry.jpg
LeafLofts    |     5  |    15  | herb-wall-kitchen.png
PrepPack     |     3  |     7  | weekly-prep-kit.jpg
ScrollMerch  |     0  |    22  | (empty — add more!)
TableClay    |     9  |    31  | blue-glaze-mug.jpg
```

## Rate Limits to Remember

- Instagram: 25 posts per 24 hours
- Facebook: 50 photo uploads per hour per page
- TikTok: 20 posts per day per user
- GitHub API: 5000 requests per hour (authenticated)

Never exceed these. If approaching limits during batch mode, pause and inform the user.

## Token Health

Meta long-lived tokens expire after 60 days. The skill should check token age and warn the user
when approaching expiration. See `references/api-setup-guide.md` for the refresh flow.
