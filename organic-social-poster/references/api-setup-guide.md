# API Setup Guide — Organic Social Poster

This guide walks through setting up all the API credentials needed for automated posting.
Complete each section, then run the verification commands to confirm everything works.

## 1. Meta Business Suite (Instagram + Facebook + Threads)

All three platforms use the same Meta Graph API authentication.

### Create a Meta App

1. Go to https://developers.facebook.com/apps/
2. Click "Create App" → select "Business" type
3. Name it something like "Organic Poster" and connect it to your Business account
4. Under "Add Products", add:
   - **Facebook Login**
   - **Instagram Graph API**

### Required Permissions

Request these permissions for your app:

- `pages_manage_posts` — Post to Facebook Pages
- `pages_read_engagement` — Read post engagement metrics
- `instagram_basic` — Read Instagram profile info
- `instagram_content_publish` — Publish to Instagram
- `threads_basic` — Access Threads profiles
- `threads_content_publish` — Publish to Threads
- `pages_show_list` — List connected Pages

### Generate a Long-Lived Token

Short-lived tokens expire in 1 hour. You need a long-lived one (60 days):

1. Go to Graph API Explorer: https://developers.facebook.com/tools/explorer/
2. Select your app from the dropdown
3. Click "Generate Access Token" and approve all permissions
4. Copy the short-lived token
5. Exchange it for a long-lived token:

```bash
curl -s "https://graph.facebook.com/v19.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id=YOUR_APP_ID&\
client_secret=YOUR_APP_SECRET&\
fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
```

6. Save the `access_token` from the response — this is your 60-day token.

### Get Your Page and Instagram IDs

```bash
# List your Pages
curl -s "https://graph.facebook.com/v19.0/me/accounts?access_token=YOUR_TOKEN" | python3 -m json.tool

# Get Instagram Business Account ID linked to your Page
curl -s "https://graph.facebook.com/v19.0/YOUR_PAGE_ID?fields=instagram_business_account&access_token=YOUR_TOKEN"
```

Save the Page ID and Instagram Business Account ID.

### Get Your Threads User ID

```bash
curl -s "https://graph.threads.net/v1.0/me?access_token=YOUR_TOKEN"
```

### Token Refresh (Before Expiry)

Long-lived tokens can be refreshed before they expire:

```bash
curl -s "https://graph.facebook.com/v19.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id=YOUR_APP_ID&\
client_secret=YOUR_APP_SECRET&\
fb_exchange_token=YOUR_CURRENT_LONG_LIVED_TOKEN"
```

Set a calendar reminder for day 50 to refresh the token.

### Verify Meta Setup

```bash
# Test Facebook posting (dry run — creates unpublished post)
curl -s -X POST "https://graph.facebook.com/v19.0/YOUR_PAGE_ID/photos" \
  -F "url=https://picsum.photos/1080/1080" \
  -F "message=Test post — will delete" \
  -F "published=false" \
  -F "access_token=YOUR_TOKEN"

# Test Instagram container creation
curl -s -X POST "https://graph.facebook.com/v19.0/YOUR_IG_ID/media" \
  -F "image_url=https://picsum.photos/1080/1080" \
  -F "caption=Test" \
  -F "access_token=YOUR_TOKEN"
```

If both return JSON with an `id` field, you're good.

---

## 2. TikTok Content Posting API

### Register as a Developer

1. Go to https://developers.tiktok.com/
2. Create a developer account
3. Create a new app → select "Content Posting API"
4. Fill in the required app info

### Scopes Needed

- `video.publish` — Upload and publish videos
- `video.upload` — Upload video content

Note: TikTok's Content Posting API requires app review before going live. During development,
you can test with sandbox accounts.

### OAuth 2.0 Flow

TikTok uses OAuth 2.0 for authentication:

1. Direct the user to authorize:
```
https://www.tiktok.com/v2/auth/authorize/?
  client_key=YOUR_CLIENT_KEY&
  scope=video.publish,video.upload&
  response_type=code&
  redirect_uri=YOUR_REDIRECT_URI
```

2. Exchange the auth code for an access token:
```bash
curl -s -X POST "https://open.tiktokapis.com/v2/oauth/token/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_key=YOUR_CLIENT_KEY" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=AUTH_CODE" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=YOUR_REDIRECT_URI"
```

3. Save the `access_token` and `refresh_token`.

### Verify TikTok Setup

```bash
curl -s "https://open.tiktokapis.com/v2/user/info/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Should return your TikTok user info.

---

## 3. GitHub Personal Access Token

Needed to read images from the repo and move files (commit changes).

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it "Organic Social Poster"
4. Select scopes: `repo` (full control of private repositories)
5. Generate and save the token

### Verify GitHub Setup

```bash
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" \
  "https://api.github.com/repos/Nsf34/claude-skills/contents/Brands"
```

Should return the directory listing.

---

## 4. Environment Variables

Store all credentials as environment variables. Add these to your shell profile
(`~/.bashrc`, `~/.zshrc`, or equivalent):

```bash
# Meta / Facebook / Instagram / Threads
export META_ACCESS_TOKEN="your_long_lived_token"
export META_APP_ID="your_app_id"
export META_APP_SECRET="your_app_secret"
export FB_PAGE_ID="your_page_id"
export IG_BUSINESS_ACCOUNT_ID="your_instagram_business_account_id"
export THREADS_USER_ID="your_threads_user_id"

# TikTok
export TIKTOK_ACCESS_TOKEN="your_tiktok_access_token"
export TIKTOK_CLIENT_KEY="your_client_key"
export TIKTOK_CLIENT_SECRET="your_client_secret"

# GitHub
export GITHUB_TOKEN="your_github_pat"
export GITHUB_REPO="Nsf34/claude-skills"
```

**Per-brand overrides:** If different brands post to different social accounts, use brand-prefixed
variables:

```bash
export ANIWOVE_IG_BUSINESS_ACCOUNT_ID="..."
export ANIWOVE_FB_PAGE_ID="..."
export TABLECLAY_IG_BUSINESS_ACCOUNT_ID="..."
export TABLECLAY_FB_PAGE_ID="..."
```

The posting scripts check for brand-prefixed variables first, then fall back to the generic ones.

### Verify All Setup

Run the comprehensive check:

```bash
python3 scripts/verify_setup.py
```

This tests all API connections and reports which are working.
