---
name: tableclay-instagram-engagement
description: |
  Automated Instagram engagement workflow for Table Clay, an artisan pottery brand selling ceramic travel cups and mini pottery wheel kits. Finds relevant accounts, follows them, likes recent posts, and drafts natural comment replies — all via browser automation. Use when user says "run engagement", "Instagram engagement", "social media engagement", "Table Clay engagement", "daily engagement run", or "find accounts to follow". Runs on Instagram using Claude in Chrome. Does NOT post original content or manage the Table Clay feed — only engages with others' content.
---

# Table Clay Instagram Engagement

## Overview

This skill runs a daily Instagram engagement session for @tableclay. The goal is organic community growth by genuinely engaging with accounts that Table Clay's target customers follow and interact with. Every action should feel like a real person — a small pottery brand owner — naturally participating in the ceramics, coffee, and creative wellness community.

**Session targets:**
- Follow 15 relevant accounts
- Like their most recent post
- Leave 5 comments across those posts

**Time per session:** ~15–20 minutes of browser work
**Frequency:** Twice daily (morning + evening)

---

## Step 1: Open Instagram

1. Navigate to `https://www.instagram.com/` in the browser
2. Whatever account is signed into the browser is the correct one — do NOT waste time verifying the handle or asking the user to confirm. The browser is the source of truth.
3. If not logged in, ask the user to log in (never enter credentials)
4. If a CAPTCHA or verification appears, pause and ask the user to complete it

**Important:** If Instagram shows any "suspicious activity" or rate-limiting warning at ANY point during the session, STOP immediately and inform the user. Do not attempt to continue.

---

## Step 2: Find Relevant Accounts via Explore

**Use the Explore tab** (compass icon in the sidebar) — NOT the Search bar. The Explore page surfaces fresh, algorithmically relevant content every time, which means natural variety across sessions without repeating the same accounts. Searching by hashtag/name brings up the same results repeatedly and looks less organic.

### How to Browse Explore

1. Click the **Explore** icon (compass) in the left sidebar
2. Scroll through the grid and look for posts related to pottery, ceramics, coffee, handmade goods, DIY crafts, or wellness/lifestyle
3. When you spot a relevant post, click into it to see the account
4. Check the account against the qualifying criteria below
5. Before following, cross-check the account handle against the **engagement log** (see Step 5) to avoid re-following accounts from previous sessions

### Additional Discovery (mix in occasionally)

- **Suggested accounts:** When visiting a relevant profile, Instagram shows "Suggested for you" — these are great leads
- **Commenters on relevant posts:** People leaving thoughtful comments on ceramics/pottery content are often ideal target accounts
- **Competitor followers:** Occasionally browse who's following/commenting on @moraceramics, @sculpd, @pottdceramics, @wandpdesign

### Qualifying an Account (applies to ALL methods)

Before following, check that the account meets at least 3 of these criteria:
- **Active:** Posted within the last 2 weeks
- **Engaged audience:** Posts get real comments (not just emoji spam or bots)
- **Relevant content:** Posts about pottery, ceramics, coffee culture, handmade goods, creative hobbies, or mindful living
- **Real person or small brand:** Not a massive brand (50k+ followers) — focus on micro-creators, hobbyists, small businesses, and enthusiasts (500–20k followers is the sweet spot)
- **Target customer signal:** The account looks like someone who would actually buy a ceramic travel cup or pottery wheel kit — coffee enthusiasts, craft hobbyists, eco-conscious lifestyle people, parents into creative activities with kids
- **Not a bot:** Has a profile photo, bio, and genuine-looking post history

**Accounts to SKIP:**
- Obvious bot/spam accounts
- Accounts with 50k+ followers (they won't notice or reciprocate)
- Accounts that only post promotional/sales content
- Accounts in unrelated niches
- Private accounts (can't see their content)
- Accounts Table Clay already follows

---

## Step 3: Follow + Like + Engage

For each qualifying account:

1. **Follow the account**
2. **Like their most recent post** (or their best recent post if the latest isn't great)
3. **For 5 of the accounts:** Leave a genuine comment on their post

### Pacing is Critical

Instagram flags rapid-fire actions. Space out engagement to mimic natural behavior:
- **Wait 30–60 seconds between follows**
- **Wait 15–30 seconds between likes**
- **Wait 1–2 minutes between comments**
- **Never do more than 15 follows in a single session**
- **Never do more than 5 comments in a single session**
- If anything feels "off" (slow loading, repeated errors, unusual prompts), stop and tell the user

---

## Step 4: Writing Comments

This is the most important part. Comments represent the Table Clay brand and need to feel genuinely human — like a pottery enthusiast and small brand owner naturally reacting to content they love.

### Core Principles

1. **React to the SPECIFIC content.** Never write a comment that could apply to any post. Reference what you actually see — the glaze color, the shape, the technique, the coffee setup, the kid's reaction.

2. **Vary your style.** Use a natural mix of these approaches:
   - **Genuine compliment** (40%): "the texture on that rim is beautiful"
   - **Curious question** (30%): "that glaze is stunning, is that a celadon?"
   - **Relatable reaction** (20%): "this makes me want to slow down and enjoy every sip"
   - **Encouraging/supportive** (10%): "your progress is wild, keep throwing"

3. **Match the energy of the post.** A polished studio shot gets a more refined comment. A messy first-try pottery video gets warm encouragement. A coffee ritual post gets cozy/relatable energy.

4. **Keep it natural length.** Most comments should be 1–2 sentences. Occasionally go to 3 if you're asking a genuine question. Never write a paragraph.

5. **Use emojis sparingly.** 0–1 emoji per comment max. Never lead with an emoji. Never use more than one. Skip them entirely on ~half your comments.

### Comment Examples (for tone reference only, never copy these verbatim)

**Pottery/ceramics:** "that glaze is unreal", "the form on this is so clean wow", "obsessed with this texture", "how long have you been throwing?", "makes me want to get back on the wheel"

**Coffee/lifestyle:** "ceramic + pour over just hits different", "that setup though", "what are you brewing?", "this is the morning routine i aspire to"

**DIY/craft:** "so satisfying to watch", "love seeing people get into clay", "how did you get started with this?"

**Family/kids:** "their focus is the best part", "way better than screen time", "love seeing families making stuff together"

### Hard Rules
- NEVER use emdashes (—) in comments. Use commas, periods, or just write shorter sentences
- NEVER mention Table Clay products (looks spammy)
- NEVER repeat a comment within a session
- NEVER write generic comments like "Great post!" "Love this!" "Amazing!" "Fire!"
- NEVER use hashtags in comments
- NEVER sound robotic or templated. Write like you're texting a friend about something cool you saw
- NEVER comment on controversial, negative, or drama content
- Keep comments SHORT. 1 sentence is ideal, 2 max. No paragraphs
- Do NOT ask the user for permission before posting comments. Just post them naturally as part of the session flow

---

## Step 5: Session Logging & Engagement History

After each session, do TWO things:

### A. Show the user a summary

```
Session Summary — [Date, Time]
Accounts followed: [count]
Posts liked: [count]
Comments posted: [count]
Notable accounts found: [any standout accounts worth revisiting]
Any issues: [rate limiting, CAPTCHAs, errors, or "none"]
```

### B. Save to the engagement log

Append each session's data to a persistent CSV file at:
**`/sessions/eager-amazing-cori/mnt/outputs/tableclay-instagram-engagement/engagement-log.csv`**

The CSV should have these columns:
`date, time, handle, display_name, follower_count, content_type, action_taken, comment_text, post_url, notes`

Where:
- `date` — YYYY-MM-DD
- `time` — HH:MM (24h)
- `handle` — @username of the account engaged with
- `display_name` — their profile name
- `follower_count` — approximate follower count at time of engagement
- `content_type` — what they post (e.g. "pottery", "coffee lifestyle", "DIY crafts", "ceramics")
- `action_taken` — "follow", "follow+like", "follow+like+comment"
- `comment_text` — the exact comment posted (blank if no comment)
- `post_url` — URL of the post liked/commented on
- `notes` — anything notable (e.g. "great engagement on their posts", "potential collab", "very active commenter")

**Before each session, read this CSV** to check which accounts have already been followed. Skip any account that appears in the log. This prevents wasted effort and keeps engagement fresh.

This log also serves as a future resource for re-engagement — accounts with good notes can be revisited for deeper interaction later.

---

## Brand Context (for reference)

**Table Clay** is an artisan pottery brand selling:
1. **Ceramic Travel Cup** ($24.99) — 15oz handmade ceramic with silicone lid, pure ceramic construction, no metallic aftertaste, dishwasher/microwave safe
2. **Mini Pottery Wheel Starter Bundle** ($60–80) — Complete kit with electric wheel, air-dry clay, tools, paints, workspace mat. No kiln required. Ages 8+.

**Target customers:**
- Coffee enthusiasts who care about taste (pour-over crowd, specialty coffee lovers)
- Eco-conscious consumers reducing plastic/disposable use
- Creative adults seeking stress relief and new hobbies
- Parents looking for screen-free family activities
- Gift-givers seeking unique, meaningful presents
- Aesthetic/lifestyle consumers who curate their daily rituals

**Brand voice:** Warm, genuine, knowledgeable about pottery and craft, encouraging but not preachy, celebrates imperfection. Think "pottery friend who knows their stuff" — not "brand trying to sell you something."

**Instagram handle:** Whatever is signed into the browser — don't verify, just go.

---

## Safety & Rate Limiting

Instagram actively detects and penalizes bot-like behavior. These safeguards are non-negotiable:

1. **Session limits:** Max 15 follows, 15 likes, 5 comments per session. Never exceed these.
2. **Pacing:** Always wait between actions (see Step 3 for timing).
3. **Pattern variation:** Don't follow → like → comment in the exact same order every time. Mix it up.
4. **Stop triggers:** If you encounter ANY of these, stop immediately and inform the user:
   - "Action Blocked" message
   - CAPTCHA or phone verification request
   - Unusual loading times or errors
   - "Try Again Later" message
   - Any warning about suspicious activity
5. **Cool-down:** If a session gets blocked or flagged, recommend waiting at least 4–6 hours before the next session.
6. **Daily maximums:** No more than 2 sessions per day. That's 30 follows, 30 likes, and 10 comments max per day.

---

## First-Run Setup

On the very first run of this skill:
1. Open Instagram — whatever account is signed in is correct
2. Do a smaller test session (5 follows, 5 likes, 2 comments) to make sure everything works smoothly
3. Review the session summary with the user and ask if the engagement style feels right
4. Initialize the engagement log CSV with headers
5. Adjust based on their feedback before running full sessions
