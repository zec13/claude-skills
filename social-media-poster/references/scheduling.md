# Scheduling System Reference

## Architecture

The scheduling system uses a file-based queue (`assets/schedule_queue.json`) processed by a cron job. This approach is simple, transparent, and requires no external dependencies like Redis or a database.

```
User → schedule_post.py → schedule_queue.json ← run_scheduler.py ← cron
                                                       ↓
                                                 post_facebook.py
                                                 post_instagram.py
                                                 post_tiktok.py
```

## Queue File Schema

`assets/schedule_queue.json` contains an array of scheduled post objects:

```json
{
  "version": 1,
  "posts": [
    {
      "id": "post_abc123",
      "status": "pending",
      "created_at": "2025-01-14T10:00:00Z",
      "scheduled_at": "2025-01-15T14:30:00-05:00",
      "timezone": "America/New_York",
      "platforms": ["facebook", "instagram"],
      "caption": "Check out our new product! #launch",
      "media": [
        {
          "path": "assets/scheduled_media/post_abc123/image1.jpg",
          "original_path": "/home/user/photos/product.jpg",
          "type": "image"
        }
      ],
      "results": {},
      "error": null,
      "completed_at": null
    }
  ]
}
```

### Post Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Awaiting scheduled time |
| `posting` | Currently being posted (prevents duplicate runs) |
| `completed` | Successfully posted to all platforms |
| `partial` | Posted to some platforms, failed on others |
| `failed` | Failed to post to any platform |
| `cancelled` | User cancelled the post |

### Results Object

After posting, the `results` field is populated per platform:

```json
{
  "results": {
    "facebook": {
      "success": true,
      "post_id": "123456789",
      "posted_at": "2025-01-15T14:30:05Z"
    },
    "instagram": {
      "success": false,
      "error": "RATE_LIMIT: Daily posting limit reached",
      "attempted_at": "2025-01-15T14:30:08Z"
    }
  }
}
```

## Media Storage

When a post is scheduled, media files are copied to `assets/scheduled_media/<post-id>/` to ensure they remain available at the scheduled time. Original file paths are preserved in the `original_path` field for reference.

The scheduler cleans up media files for completed posts after 7 days by default.

## Cron Configuration

### Recommended Setup

```bash
# Every 5 minutes — good balance of timeliness and resource usage
*/5 * * * * cd /path/to/social-media-poster && python scripts/run_scheduler.py --run >> logs/scheduler.log 2>&1
```

### Alternative Intervals

```bash
# Every minute — for time-sensitive posts
* * * * * cd /path/to/social-media-poster && ...

# Every 15 minutes — for less time-sensitive content
*/15 * * * * cd /path/to/social-media-poster && ...
```

### Log Rotation

The scheduler logs to `logs/scheduler.log`. To prevent unbounded growth, set up log rotation:

```bash
# In /etc/logrotate.d/social-media-poster
/path/to/social-media-poster/logs/scheduler.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
}
```

## Locking

The scheduler uses a file lock (`assets/.scheduler.lock`) to prevent concurrent runs from posting duplicates. If a run is already in progress, subsequent cron invocations will skip and log a message.

If the lock file is stale (older than 30 minutes), it is automatically cleaned up.

## Timezone Handling

- Scheduled times are stored with timezone info in ISO 8601 format
- The scheduler converts all times to UTC for comparison
- Display times use the timezone specified in the post
- If no timezone is provided, the system timezone is used

## Daily Auto-Posting Cadence

The `generate_daily_schedule.py` script creates organic posting rhythms. Here's how the algorithm works.

### Time Generation Algorithm

1. **Window Division**: The posting window (default 8:00 AM - 9:00 PM = 780 minutes) is divided into N equal segments, where N = posts per day.

2. **Segment Jitter**: Within each segment, a random time is selected. An inner padding of 15% is applied to each segment edge so times don't cluster at boundaries.

   ```
   Window: 8:00 ─────────────────────────────────── 21:00
   Segments:  |  seg 1  |  seg 2  |  seg 3  |  seg 4  |  seg 5  |
   Picks:     |    x    |   x     |     x   |  x      |      x  |
   ```

3. **Minimum Gap Enforcement**: After initial picks, any consecutive times closer than 30 minutes are nudged forward.

4. **Cross-Platform Offset**: Each platform generates its own random times using a deterministic seed (`date + platform_name`). If two platforms would post in the same minute, one is offset by 3-15 minutes.

### Example Output

For a 3-platform, 5-post day, the generated times might look like:

```
FACEBOOK:
  Post 1: 08:23
  Post 2: 10:47
  Post 3: 13:12
  Post 4: 16:38
  Post 5: 19:55

INSTAGRAM:
  Post 1: 08:41
  Post 2: 11:03
  Post 3: 13:28
  Post 4: 16:09
  Post 5: 20:14

TIKTOK:
  Post 1: 09:05
  Post 2: 11:31
  Post 3: 14:02
  Post 4: 16:52
  Post 5: 19:37
```

Notice: no two platforms share the same time, spacing varies organically, and all posts fall within the 8 AM - 9 PM window.

### Deterministic Seeding

The random seed is derived from `hash(date_string + platform_name)`. This means:
- **Same date + platform** always produces the same times (reproducible for debugging)
- **Different dates** produce different patterns (no day-to-day repetition)
- **Different platforms** get different times on the same day

### Content Manifest

The manifest is a JSON array where each entry maps to one scheduled post:

```json
[
  {
    "media": ["/path/to/image.jpg"],
    "caption": "Post caption with #hashtags"
  }
]
```

Content is assigned sequentially: for each time slot, a manifest entry is consumed. With 3 platforms and 5 posts/day, you need at least 15 entries per day.

### Recommended Cron Setup for Daily Auto-Posting

```bash
# Process the schedule queue every 5 minutes
*/5 * * * * cd /path/to/social-media-poster && python scripts/run_scheduler.py --run >> logs/scheduler.log 2>&1

# Clean up old posts weekly
0 2 * * 0 cd /path/to/social-media-poster && python scripts/run_scheduler.py --cleanup >> logs/scheduler.log 2>&1
```
