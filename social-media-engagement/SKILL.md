---
name: social-media-engagement
description: |
  Automated social media engagement workflow across Instagram, Facebook, and TikTok. Finds relevant accounts, follows/likes them, reacts to posts, and drafts natural comments -- all via browser automation. Supports any brand with swappable brand context files (Table Clay is the default).

  Instagram: Explore-based discovery, follows, likes, comments.
  Facebook: Reels-based discovery, Page follows, reactions, comments on relevant Reels only.
  TikTok: FYP-based discovery, follows, likes, comments on creator videos.

  Use when user says "run engagement", "Instagram engagement", "Facebook engagement", "TikTok engagement", "social media engagement", "daily engagement run", "find accounts to follow", "run IG session", "run FB session", "run TikTok session", "run TK session", "run engagement on all", "all platforms", or "engagement for [brand name]".

  Runs in Chrome via browser automation. Does NOT post original content or manage feeds -- only engages with others' content.
---

# Social Media Engagement

## Overview

This skill runs engagement sessions on Instagram, Facebook, and/or TikTok. The goal is organic community growth by genuinely engaging with accounts in the brand's niche. Every action should feel like a real person -- a small brand owner -- naturally participating in a community they care about.

The skill is brand-agnostic. Brand context (products, target customers, voice, content themes) is loaded from a swappable reference file. Table Clay is the default.

**Supported platforms:** Instagram, Facebook (Business Page), TikTok
**Session time:** ~15-25 minutes per platform
**Frequency:** Up to 2 sessions per platform per day (morning + evening)

---

## Step 1: Platform Selection

Determine which platform to run based on what the user says:

| User says | Action |
|-----------|--------|
| "Instagram", "IG", "Insta" | Run Instagram workflow |
| "Facebook", "FB" | Run Facebook workflow |
| "TikTok", "TK" | Run TikTok workflow |
| "social media engagement", "run engagement" (no platform specified) | Ask the user which platform |
| "both", "IG and FB", "IG and TK", "FB and TK" | Run the two specified platforms sequentially with a **15-minute gap** |
| "all", "all three", "all platforms" | Run Instagram first, then Facebook, then TikTok, each with a **15-minute gap** |

**Never run multiple platforms simultaneously in one session.** If the user wants more than one, run them sequentially with a gap between each.

---

## Step 2: Load Brand Context

1. Check if the user specified a brand. If they said something like "engagement for Table Clay" or "run FB for [brand]", use that brand.
2. If no brand specified, default to **Table Clay**: read `references/brand-tableclay.md`
3. If a different brand is specified, look for `references/brand-{name}.md`. If the file doesn't exist, ask the user to provide brand details or create the file first.

The brand context file provides:
- Brand name and handles
- Products (so you know what NOT to mention in comments)
- Target customers (shapes what content feels relevant)
- Content themes (what topics to look for in the feed)
- Competitors (used for additional discovery on Instagram)
- Brand voice (used for comment tone)

Keep the brand context in mind throughout the entire session. It shapes what content you engage with and how you write comments.

---

## Step 3: Open the Platform

**Instagram:** Navigate to `https://www.instagram.com/`
**Facebook:** Navigate to `https://www.facebook.com/`
**TikTok:** Navigate to `https://www.tiktok.com/`

**Rules:**
1. Whatever account is signed into the browser is the correct one. Do NOT waste time verifying the handle, Page name, or asking the user to confirm. The browser is the source of truth.
2. If not logged in, ask the user to log in. Never enter credentials yourself.
3. If a CAPTCHA or verification appears, pause and ask the user to complete it.
4. If the platform shows any "suspicious activity" or rate-limiting warning at ANY point during the session, **STOP immediately** and inform the user. Do not attempt to continue.

---

## Step 4: Discover and Engage

Discovery and engagement are platform-specific. Read the appropriate reference file:

- **Instagram:** Read `references/instagram-workflow.md` for Explore-based discovery and engagement
- **Facebook:** Read `references/facebook-workflow.md` for Reels-based discovery and engagement
- **TikTok:** Read `references/tiktok-workflow.md` for FYP-based discovery and engagement

**Engage based on content, not account evaluation.** If a post/reel/video feels like it belongs in the brand's world -- pottery, coffee, cute finds, DIY, artsy stuff, cozy lifestyle -- engage with it directly. No need to visit profiles or check follower counts. The bar is vibes, not metrics.

**Only soft-skip** obviously massive accounts (100K+ visible at a glance, or well-known brands). If you can't tell, don't worry about it.

**Before engaging**, cross-check the handle/name against the **engagement log** (`engagement-log.csv` in this skill's directory):
- If the account appears in the log **for the current platform** -- skip it
- If the account appears in the log **for a different platform** -- don't skip, but add a note in the `notes` column

---

## Step 5: Engage

Run the engagement actions described in the platform-specific reference file:

**Instagram:** Follow + Like + Comment (on selected posts)
**Facebook:** Page Follow + React + Comment (all via Reels discovery)
**TikTok:** Follow + Like + Comment (on selected videos)

For writing comments on any platform, read `references/comment-guide.md`. This covers:
- Platform-specific comment length and tone
- Style distribution (compliments, questions, relatable, encouraging)
- Hard rules that apply universally
- Facebook reaction selection guide

### Universal Hard Rules (all platforms)

These apply regardless of platform or brand:

- **Never mention the brand's products** in comments. This looks spammy.
- **Never write generic comments** ("Great post!", "Love this!", "Amazing!"). Every comment must reference specific content.
- **Never use hashtags** in comments.
- **Never comment on controversial, negative, or drama content.** Skip it entirely.
- **Never exceed session limits.** The limits exist to protect the account from restrictions.
- **Always pace your actions.** Rapid-fire engagement gets flagged as bot behavior.

---

## Step 6: Session Logging and Engagement History

After each session, do **two things**:

### A. Show the User a Summary

```
Session Summary -- [Date, Time]
Platform: [Instagram / Facebook / TikTok]
Accounts followed: [count]
Posts liked/reacted to: [count]
Comments posted: [count]
Notable accounts found: [any standout accounts worth revisiting]
Any issues: [rate limiting, CAPTCHAs, errors, or "none"]
```

### B. Append to the Engagement Log

Save session data to `engagement-log.csv` in this skill's directory.

**CSV columns:**
```
date,time,platform,account_id,display_name,follower_count,account_type,content_type,action_taken,comment_text,post_url,notes
```

**Column definitions:**
- `date` -- YYYY-MM-DD
- `time` -- HH:MM (24-hour)
- `platform` -- "instagram", "facebook", or "tiktok"
- `account_id` -- @username (Instagram, TikTok) or Page name/URL slug (Facebook)
- `display_name` -- their profile or Page display name
- `follower_count` -- approximate follower/friend count at time of engagement (use "unknown" if not visible)
- `account_type` -- "profile" (Instagram), "creator" (TikTok), "page" (Facebook Page)
- `content_type` -- what they post (e.g., "pottery", "coffee lifestyle", "DIY crafts", "ceramics")
- `action_taken` -- "follow", "follow+like", "follow+like+comment", "page_follow", "page_follow+react", "page_follow+react+comment"
- `comment_text` -- the exact comment posted (blank if no comment)
- `post_url` -- URL of the post liked/reacted to/commented on
- `notes` -- anything notable (e.g., "great engagement on their posts", "potential collab", "also on IG as @xyz", "very active in pottery groups")

**Before each session, read this CSV** to check which accounts have already been engaged. This prevents re-following and keeps engagement fresh.

The log also serves as a future resource for re-engagement. Accounts with good notes can be revisited for deeper interaction later.

---

## Safety and Rate Limiting

All platforms actively detect and penalize bot-like behavior. These safeguards are non-negotiable.

### Universal Rules

1. **Never exceed session limits.** Limits are defined in the platform-specific reference files.
2. **Always pace actions.** Timing rules are in the platform-specific reference files.
3. **Vary patterns.** Don't do the same sequence (follow, like, comment) every time. Mix it up.
4. **Stop on any warning.** If the platform shows any blocking message, CAPTCHA, verification, or unusual behavior -- stop immediately and tell the user.
5. **Cool-down after being flagged:**
   - Instagram: Wait at least **4-6 hours**
   - Facebook: Wait at least **6-12 hours** (Facebook penalties escalate more aggressively)
   - TikTok: Wait at least **6-12 hours** (TikTok penalties escalate quickly to temporary bans)
6. **Daily maximums:** No more than **2 sessions per platform per day.**

### Platform-Specific Safety

For detailed stop triggers and safety protocols:
- Instagram: See "Safety and Stop Triggers" in `references/instagram-workflow.md`
- Facebook: See "Safety and Stop Triggers" in `references/facebook-workflow.md`
- TikTok: See "Safety and Stop Triggers" in `references/tiktok-workflow.md`

---

## First-Run Setup

On the very first run of this skill for a platform:

1. Open the platform -- whatever account is signed in is correct
2. Run a **smaller test session** (half the normal limits):
   - Instagram: 7 follows, 7 likes, 2 comments
   - Facebook: 4 Page follows, 6 reactions, 2 comments (all via Reels)
   - TikTok: 5 follows, 6 likes, 2 comments
3. Review the session summary with the user and ask if the engagement style feels right
4. Initialize or verify the `engagement-log.csv` has the correct headers
5. Adjust based on user feedback before running full sessions

This helps catch any issues (wrong account signed in, brand voice mismatch, platform UI changes) before committing to a full session.

---

## Quick Reference: Session Limits

| | Instagram | Facebook | TikTok |
|---|-----------|----------|--------|
| **Follows** | 15 per session | 8 per session | 10 per session |
| **Likes/Reactions** | 15 per session | 12 per session | 12 per session |
| **Comments** | 5 per session | 4 per session | 4 per session |
| **Sessions/day** | 2 max | 2 max | 2 max |
| **Cool-down if flagged** | 4-6 hours | 6-12 hours | 6-12 hours |
