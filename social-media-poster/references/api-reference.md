# API Reference — Social Media Poster

Detailed endpoint documentation for Facebook, Instagram, and TikTok posting APIs.

## Meta Graph API (Facebook + Instagram)

**Base URL:** `https://graph.facebook.com/v21.0`

**Authentication:** All requests require a valid access token passed as `access_token` parameter or `Authorization: Bearer <token>` header.

### Facebook Page Posting

#### Single Photo Post
```
POST /{page-id}/photos
```
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source` | file | Yes* | Photo file upload (multipart) |
| `url` | string | Yes* | Public URL of the photo |
| `message` | string | No | Caption text |
| `published` | boolean | No | Default `true`. Set `false` for unpublished (used in multi-photo) |

*One of `source` or `url` is required.

**Response:** `{ "id": "photo_id", "post_id": "page_post_id" }`

#### Multi-Photo Post (Carousel)
Two-step process:
1. Upload each photo as **unpublished** (`published=false`) to get photo IDs
2. Create a feed post referencing all photos

**Step 1 — Upload each photo:**
```
POST /{page-id}/photos
  source=<file>
  published=false
```

**Step 2 — Create post with attached media:**
```
POST /{page-id}/feed
  message=<caption>
  attached_media[0]={"media_fbid":"<photo_id_1>"}
  attached_media[1]={"media_fbid":"<photo_id_2>"}
  ...
```

#### Video Post
```
POST /{page-id}/videos
```
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source` | file | Yes* | Video file upload (multipart) |
| `file_url` | string | Yes* | Public URL of the video |
| `description` | string | No | Caption text |

**Response:** `{ "id": "video_id" }`

For large videos (>1GB), use resumable upload:
1. `POST /{page-id}/videos` with `upload_phase=start`, `file_size=<bytes>`
2. `POST /{page-id}/videos` with `upload_phase=transfer`, `upload_session_id`, `start_offset`, video chunk
3. `POST /{page-id}/videos` with `upload_phase=finish`, `upload_session_id`, `description`

### Instagram Content Publishing API

Instagram uses a container-based publishing model: create a media container, then publish it.

#### Single Image
**Step 1 — Create container:**
```
POST /{ig-user-id}/media
  image_url=<public_url>
  caption=<text>
```

**Step 2 — Publish:**
```
POST /{ig-user-id}/media_publish
  creation_id=<container_id>
```

**Note:** Instagram requires a **publicly accessible URL** for images. For local files, the script uploads to a temporary hosting service or uses the Facebook photo upload endpoint to generate a URL.

#### Single Video (Reel)
**Step 1 — Create container:**
```
POST /{ig-user-id}/media
  video_url=<public_url>
  caption=<text>
  media_type=REELS
```

**Step 2 — Check status (poll until ready):**
```
GET /<container_id>?fields=status_code
```
Wait until `status_code` is `FINISHED`.

**Step 3 — Publish:**
```
POST /{ig-user-id}/media_publish
  creation_id=<container_id>
```

#### Carousel (Multiple Images/Videos)
**Step 1 — Create item containers** (for each image/video):
```
POST /{ig-user-id}/media
  image_url=<url>       # for images
  # OR
  video_url=<url>       # for videos
  media_type=VIDEO      # only for video items
  is_carousel_item=true
```

**Step 2 — Create carousel container:**
```
POST /{ig-user-id}/media
  media_type=CAROUSEL
  caption=<text>
  children=<container_id_1>,<container_id_2>,...
```

**Step 3 — Publish:**
```
POST /{ig-user-id}/media_publish
  creation_id=<carousel_container_id>
```

**Carousel limits:** 2-10 items. Mixed images and videos allowed.

### Meta API Rate Limits

| Endpoint | Limit |
|----------|-------|
| Page photo upload | 50 per hour per page |
| Page video upload | 50 per hour per page |
| Instagram content publish | 25 per 24 hours |
| Instagram carousel publish | 25 per 24 hours |
| General Graph API | 200 calls per hour per user |

---

## TikTok Content Posting API

**Base URL:** `https://open.tiktokapis.com/v2`

**Authentication:** OAuth 2.0 Bearer token in `Authorization` header. Requires `video.publish` and/or `video.upload` scopes.

### Direct Post (Video)

#### Step 1 — Initialize upload
```
POST /post/publish/inbox/video/init/
Headers:
  Authorization: Bearer <access_token>
  Content-Type: application/json
Body:
{
  "post_info": {
    "title": "<caption>",
    "privacy_level": "SELF_ONLY",
    "disable_duet": false,
    "disable_comment": false,
    "disable_stitch": false
  },
  "source_info": {
    "source": "FILE_UPLOAD",
    "video_size": <file_size_bytes>,
    "chunk_size": <chunk_size_bytes>,
    "total_chunk_count": <num_chunks>
  }
}
```

**Response:**
```json
{
  "data": {
    "publish_id": "<publish_id>",
    "upload_url": "<upload_url>"
  }
}
```

**Privacy levels:** `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`

#### Step 2 — Upload video chunks
```
PUT <upload_url>
Headers:
  Content-Type: video/mp4
  Content-Range: bytes <start>-<end>/<total>
Body: <video_chunk_bytes>
```

#### Step 3 — Check publish status
```
POST /post/publish/status/fetch/
Headers:
  Authorization: Bearer <access_token>
Body:
{
  "publish_id": "<publish_id>"
}
```

Poll until `status` is `PUBLISH_COMPLETE`.

### Direct Post (Photo Mode)

#### Initialize photo post
```
POST /post/publish/content/init/
Headers:
  Authorization: Bearer <access_token>
  Content-Type: application/json
Body:
{
  "post_info": {
    "title": "<caption>",
    "privacy_level": "SELF_ONLY"
  },
  "source_info": {
    "source": "PULL",
    "photo_cover_index": 0,
    "photo_images": [
      "<public_url_1>",
      "<public_url_2>"
    ]
  },
  "post_mode": "DIRECT_POST",
  "media_type": "PHOTO"
}
```

**Photo limits:** 1-35 images per photo post.

### TikTok API Rate Limits

| Resource | Limit |
|----------|-------|
| Content publish | 20 per day per user |
| Upload init | 100 per day per user |
| Status check | 200 per day per user |

### TikTok Error Codes

| Code | Meaning |
|------|---------|
| `ok` | Success |
| `spam_risk_too_many_pending_share` | Too many pending uploads |
| `spam_risk_too_many_posts` | Daily post limit reached |
| `invalid_publish_id` | Publish ID not found or expired |
| `token_expired` | Access token expired — need to re-authenticate |
| `scope_not_authorized` | App doesn't have required permissions |
