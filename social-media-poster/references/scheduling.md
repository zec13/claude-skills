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
