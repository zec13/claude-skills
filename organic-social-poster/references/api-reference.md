# API Reference — Platform Posting

Quick reference for the exact API calls used by the posting scripts.

## Meta Graph API (v19.0)

Base URL: `https://graph.facebook.com/v19.0`

### Instagram — Single Image Post

**Step 1: Create media container**
```
POST /{ig-user-id}/media
  image_url={public_url}
  caption={caption_text}
  access_token={token}
```

The `image_url` must be publicly accessible. If using GitHub-hosted images, use the raw URL.

**Step 2: Publish container**
```
POST /{ig-user-id}/media_publish
  creation_id={container_id}
  access_token={token}
```

**Step 3: Add first comment (hashtags)**
```
POST /{media-id}/comments
  message={hashtag_text}
  access_token={token}
```

Image requirements:
- JPEG or PNG
- Between 320px and 1440px wide
- Aspect ratio between 4:5 and 1.91:1
- Max file size: 8MB

Rate limit: 25 posts per 24-hour period.

### Facebook Page — Photo Post

```
POST /{page-id}/photos
  url={public_url}       (or use source= for file upload)
  message={caption_text}
  access_token={page_token}
```

Rate limit: 50 photo uploads per hour per page.

### Threads — Single Post

**Step 1: Create container**
```
POST /{threads-user-id}/threads
  media_type=IMAGE
  image_url={public_url}
  text={caption_text}
  access_token={token}
```

**Step 2: Publish**
```
POST /{threads-user-id}/threads_publish
  creation_id={container_id}
  access_token={token}
```

Rate limit: 250 posts per 24 hours.

---

## TikTok Content Posting API

Base URL: `https://open.tiktokapis.com/v2`

### Photo Post (1-35 images)

**Step 1: Initialize upload**
```
POST /post/publish/content/init/
Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json
Body:
{
  "post_info": {
    "title": "{caption}",
    "privacy_level": "PUBLIC_TO_EVERYONE",
    "disable_duet": false,
    "disable_comment": false,
    "disable_stitch": false
  },
  "source_info": {
    "source": "PULL_FROM_URL",
    "photo_cover_index": 0,
    "photo_images": ["{image_url}"]
  },
  "media_type": "PHOTO"
}
```

**Step 2: Check publish status**
```
POST /post/publish/status/fetch/
Headers:
  Authorization: Bearer {access_token}
Body:
{
  "publish_id": "{publish_id_from_init}"
}
```

Rate limit: 20 posts per day per user.

---

## GitHub API

Base URL: `https://api.github.com`

### List directory contents
```
GET /repos/{owner}/{repo}/contents/{path}
Headers:
  Authorization: token {github_token}
  Accept: application/vnd.github.v3+json
```

### Download file
```
GET /repos/{owner}/{repo}/contents/{path}
Headers:
  Authorization: token {github_token}
  Accept: application/vnd.github.v3.raw
```

### Move file (delete + create)

GitHub API doesn't have a "move" endpoint. Moving = creating at new path + deleting at old path.

**Get file SHA (needed for delete):**
```
GET /repos/{owner}/{repo}/contents/{old_path}
```

**Create file at new location:**
```
PUT /repos/{owner}/{repo}/contents/{new_path}
Headers:
  Authorization: token {github_token}
Body:
{
  "message": "Posted: {filename} for {brand}",
  "content": "{base64_file_content}",
  "branch": "main"
}
```

**Delete file at old location:**
```
DELETE /repos/{owner}/{repo}/contents/{old_path}
Headers:
  Authorization: token {github_token}
Body:
{
  "message": "Moved to already-posted: {filename}",
  "sha": "{file_sha}",
  "branch": "main"
}
```

Rate limit: 5000 requests per hour (authenticated).

---

## Error Codes to Watch For

| Platform | Code | Meaning | Action |
|----------|------|---------|--------|
| Meta | 190 | Token expired | Refresh token (see setup guide) |
| Meta | 4 | Rate limit hit | Wait 1 hour, retry |
| Meta | 36003 | IG rate limit | Wait until next 24h window |
| TikTok | spam_risk_too_many_posts | Daily limit | Wait until tomorrow |
| TikTok | token_expired | Token expired | Re-authenticate via OAuth |
| GitHub | 403 | Rate limited or permission denied | Check token scopes |
