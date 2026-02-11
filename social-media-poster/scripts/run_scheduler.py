#!/usr/bin/env python3
"""
Process the social-media-poster scheduling queue.

Designed to be executed by cron on a recurring interval (e.g. every 5 minutes).
Supports four modes of operation:

    --run       Process all posts whose scheduled time has passed.
    --list      Display pending/posting posts in a human-readable table.
    --cancel    Cancel a specific post by its ID.
    --cleanup   Remove completed/failed/cancelled posts older than 7 days.
"""

import argparse
import fcntl
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
QUEUE_FILE = ASSETS_DIR / "schedule_queue.json"
LOCK_FILE = ASSETS_DIR / ".scheduler.lock"
SCHEDULED_MEDIA_DIR = ASSETS_DIR / "scheduled_media"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "scheduler.log"

# Mapping from platform name to posting script filename
PLATFORM_SCRIPTS = {
    "facebook": SCRIPT_DIR / "post_facebook.py",
    "instagram": SCRIPT_DIR / "post_instagram.py",
    "tiktok": SCRIPT_DIR / "post_tiktok.py",
}

STALE_LOCK_MINUTES = 30
CLEANUP_DAYS = 7

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def setup_logging():
    """Configure file + console logging."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(LOG_FILE)),
            logging.StreamHandler(sys.stdout),
        ],
    )


# ---------------------------------------------------------------------------
# Queue helpers
# ---------------------------------------------------------------------------


def load_queue():
    """Load schedule_queue.json. Returns dict or None on error."""
    if not QUEUE_FILE.exists():
        logging.warning("Queue file does not exist: %s", QUEUE_FILE)
        return None
    try:
        with open(QUEUE_FILE, "r") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logging.error("Failed to load queue file: %s", exc)
        return None


def save_queue(queue_data):
    """Save queue with an exclusive file lock."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_FILE, "r+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            fh.seek(0)
            fh.write(json.dumps(queue_data, indent=2) + "\n")
            fh.truncate()
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# Lock helpers
# ---------------------------------------------------------------------------


def acquire_lock():
    """Acquire the scheduler lock file.

    Returns True if the lock was acquired, False otherwise.
    Cleans up stale locks older than STALE_LOCK_MINUTES.
    """
    if LOCK_FILE.exists():
        try:
            lock_age_seconds = time.time() - LOCK_FILE.stat().st_mtime
            lock_age_minutes = lock_age_seconds / 60
            if lock_age_minutes < STALE_LOCK_MINUTES:
                logging.info(
                    "Scheduler already running (lock is %.1f min old). Skipping.",
                    lock_age_minutes,
                )
                return False
            # Stale lock — clean it up
            logging.warning(
                "Removing stale lock (%.1f min old).", lock_age_minutes
            )
            LOCK_FILE.unlink(missing_ok=True)
        except OSError as exc:
            logging.error("Error checking lock file: %s", exc)
            return False

    try:
        LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOCK_FILE.write_text(json.dumps({
            "pid": os.getpid(),
            "started_at": datetime.now(tz=timezone.utc).isoformat(),
        }))
        return True
    except OSError as exc:
        logging.error("Failed to create lock file: %s", exc)
        return False


def release_lock():
    """Remove the scheduler lock file."""
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except OSError as exc:
        logging.error("Failed to remove lock file: %s", exc)


# ---------------------------------------------------------------------------
# Posting
# ---------------------------------------------------------------------------


def post_to_platform(platform, media_paths, caption):
    """Run the platform posting script as a subprocess.

    Returns a result dict with 'success', and either 'post_id'/'posted_at'
    or 'error'/'attempted_at'.
    """
    script = PLATFORM_SCRIPTS.get(platform)
    if script is None or not script.exists():
        return {
            "success": False,
            "error": f"Posting script not found for {platform}",
            "attempted_at": datetime.now(tz=timezone.utc).isoformat(),
        }

    cmd = [
        sys.executable,
        str(script),
        "--media", *media_paths,
        "--caption", caption,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            # Try to parse JSON output from the posting script
            try:
                output = json.loads(result.stdout.strip())
                return {
                    "success": True,
                    "post_id": output.get("post_id", "unknown"),
                    "posted_at": datetime.now(tz=timezone.utc).isoformat(),
                }
            except (json.JSONDecodeError, ValueError):
                return {
                    "success": True,
                    "post_id": "unknown",
                    "posted_at": datetime.now(tz=timezone.utc).isoformat(),
                }
        else:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            return {
                "success": False,
                "error": error_msg,
                "attempted_at": datetime.now(tz=timezone.utc).isoformat(),
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Posting script timed out after 300 seconds.",
            "attempted_at": datetime.now(tz=timezone.utc).isoformat(),
        }
    except OSError as exc:
        return {
            "success": False,
            "error": str(exc),
            "attempted_at": datetime.now(tz=timezone.utc).isoformat(),
        }


def parse_scheduled_at(post):
    """Parse a post's scheduled_at field into a UTC-aware datetime."""
    raw = post.get("scheduled_at", "")
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_run():
    """Process all due posts in the queue."""
    if not acquire_lock():
        return

    try:
        queue = load_queue()
        if queue is None:
            logging.info("No queue file found. Nothing to do.")
            return

        now = datetime.now(tz=timezone.utc)
        due_posts = []

        for post in queue["posts"]:
            if post["status"] != "pending":
                continue
            scheduled_utc = parse_scheduled_at(post)
            if scheduled_utc is None:
                logging.warning(
                    "Post %s has invalid scheduled_at; skipping.", post["id"]
                )
                continue
            if scheduled_utc <= now:
                due_posts.append(post)

        if not due_posts:
            logging.info("No due posts to process.")
            return

        logging.info("Found %d due post(s) to process.", len(due_posts))

        for post in due_posts:
            post["status"] = "posting"
            logging.info("Processing post %s ...", post["id"])

            media_paths = [m["path"] for m in post.get("media", [])]
            caption = post.get("caption", "")
            results = {}
            success_count = 0
            failure_count = 0

            for platform in post.get("platforms", []):
                logging.info("  Posting to %s ...", platform)
                result = post_to_platform(platform, media_paths, caption)
                results[platform] = result
                if result.get("success"):
                    success_count += 1
                    logging.info("  %s: success", platform)
                else:
                    failure_count += 1
                    logging.error(
                        "  %s: failed — %s", platform, result.get("error", "")
                    )

            post["results"] = results
            post["completed_at"] = datetime.now(tz=timezone.utc).isoformat()

            if failure_count == 0:
                post["status"] = "completed"
            elif success_count == 0:
                post["status"] = "failed"
            else:
                post["status"] = "partial"

            logging.info(
                "Post %s finished with status: %s", post["id"], post["status"]
            )

        save_queue(queue)
        logging.info("Queue updated successfully.")

    finally:
        release_lock()


def cmd_list():
    """Display pending and posting posts in a readable table, plus JSON."""
    queue = load_queue()
    if queue is None:
        print("No schedule queue found.")
        return

    active = [
        p for p in queue["posts"] if p["status"] in ("pending", "posting")
    ]

    if not active:
        print("No pending or posting entries in the queue.")
        return

    # Human-readable table
    header = f"{'ID':<25} {'Status':<10} {'Scheduled At':<30} {'Platforms':<25} {'Caption'}"
    print(header)
    print("-" * len(header))
    for post in active:
        caption_preview = post.get("caption", "")[:40]
        if len(post.get("caption", "")) > 40:
            caption_preview += "..."
        platforms_str = ", ".join(post.get("platforms", []))
        print(
            f"{post['id']:<25} {post['status']:<10} "
            f"{post.get('scheduled_at', 'N/A'):<30} "
            f"{platforms_str:<25} {caption_preview}"
        )
    print()

    # JSON output
    print(json.dumps(active, indent=2))


def cmd_cancel(post_id):
    """Cancel a scheduled post by ID and remove its media files."""
    queue = load_queue()
    if queue is None:
        print(json.dumps({"success": False, "error": "Queue file not found."}))
        sys.exit(1)

    target = None
    for post in queue["posts"]:
        if post["id"] == post_id:
            target = post
            break

    if target is None:
        print(json.dumps({
            "success": False,
            "error": f"Post '{post_id}' not found in queue.",
        }))
        sys.exit(1)

    if target["status"] not in ("pending", "posting"):
        print(json.dumps({
            "success": False,
            "error": (
                f"Post '{post_id}' cannot be cancelled "
                f"(current status: {target['status']})."
            ),
        }))
        sys.exit(1)

    target["status"] = "cancelled"
    target["completed_at"] = datetime.now(tz=timezone.utc).isoformat()

    # Remove copied media directory
    media_dir = SCHEDULED_MEDIA_DIR / post_id
    if media_dir.exists():
        try:
            shutil.rmtree(str(media_dir))
            logging.info("Removed media directory: %s", media_dir)
        except OSError as exc:
            logging.warning("Failed to remove media directory: %s", exc)

    save_queue(queue)
    print(json.dumps({"success": True, "post_id": post_id, "status": "cancelled"}))
    logging.info("Post %s cancelled.", post_id)


def cmd_cleanup():
    """Remove completed/failed/cancelled posts older than 7 days."""
    queue = load_queue()
    if queue is None:
        print("No queue file found. Nothing to clean up.")
        return

    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=CLEANUP_DAYS)
    removable_statuses = {"completed", "failed", "cancelled"}
    keep = []
    removed_count = 0

    for post in queue["posts"]:
        if post["status"] not in removable_statuses:
            keep.append(post)
            continue

        # Determine the completion/creation timestamp for age comparison
        ts_raw = post.get("completed_at") or post.get("created_at")
        if ts_raw is None:
            keep.append(post)
            continue

        try:
            ts = datetime.fromisoformat(ts_raw)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            keep.append(post)
            continue

        if ts < cutoff:
            # Remove associated media directory
            media_dir = SCHEDULED_MEDIA_DIR / post["id"]
            if media_dir.exists():
                try:
                    shutil.rmtree(str(media_dir))
                    logging.info("Cleaned up media: %s", media_dir)
                except OSError as exc:
                    logging.warning(
                        "Failed to clean up media for %s: %s", post["id"], exc
                    )
            removed_count += 1
            logging.info("Removed old post: %s (status=%s)", post["id"], post["status"])
        else:
            keep.append(post)

    queue["posts"] = keep
    save_queue(queue)
    print(f"Cleanup complete. Removed {removed_count} old post(s).")
    logging.info("Cleanup finished. Removed %d post(s).", removed_count)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process the social-media-poster scheduling queue."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Process all due posts in the queue.",
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="Show pending/posting posts.",
    )
    group.add_argument(
        "--cancel",
        metavar="POST_ID",
        help="Cancel a scheduled post by its ID.",
    )
    group.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove completed/failed/cancelled posts older than 7 days.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    setup_logging()
    args = parse_args(argv)

    if args.run:
        cmd_run()
    elif args.list:
        cmd_list()
    elif args.cancel:
        cmd_cancel(args.cancel)
    elif args.cleanup:
        cmd_cleanup()

    sys.exit(0)


if __name__ == "__main__":
    main()
