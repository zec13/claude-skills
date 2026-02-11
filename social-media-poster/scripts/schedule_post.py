#!/usr/bin/env python3
"""
Schedule a social media post for future publishing.

Validates media, copies files to a staging area, and adds an entry to the
schedule queue (assets/schedule_queue.json). Designed to be invoked by the
Claude skill or directly from the command line.
"""

import argparse
import fcntl
import json
import mimetypes
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Resolve paths relative to the project root (one level above scripts/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
QUEUE_FILE = ASSETS_DIR / "schedule_queue.json"
SCHEDULED_MEDIA_DIR = ASSETS_DIR / "scheduled_media"
VALIDATE_SCRIPT = SCRIPT_DIR / "validate_media.py"


def get_local_timezone_name():
    """Return the IANA timezone name for the local system, or UTC offset."""
    try:
        # Try reading the /etc/timezone file (Debian/Ubuntu)
        tz_file = Path("/etc/timezone")
        if tz_file.exists():
            name = tz_file.read_text().strip()
            if name:
                return name
        # Try the TZ environment variable
        tz_env = os.environ.get("TZ")
        if tz_env:
            return tz_env
        # Try resolving /etc/localtime symlink
        localtime = Path("/etc/localtime")
        if localtime.is_symlink():
            target = str(localtime.resolve())
            if "zoneinfo/" in target:
                return target.split("zoneinfo/", 1)[1]
    except Exception:
        pass
    return "UTC"


def detect_media_type(filepath):
    """Classify a media file as 'image' or 'video' based on its MIME type."""
    mime, _ = mimetypes.guess_type(filepath)
    if mime:
        if mime.startswith("image"):
            return "image"
        if mime.startswith("video"):
            return "video"
    ext = Path(filepath).suffix.lower()
    image_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
    video_exts = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
    if ext in image_exts:
        return "image"
    if ext in video_exts:
        return "video"
    return "unknown"


def parse_schedule_time(schedule_str, tz_name):
    """Parse the schedule string and attach timezone info.

    Returns a timezone-aware datetime in the specified timezone.
    Raises ValueError if the time is in the past.
    """
    try:
        naive_dt = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(
            f"Invalid schedule format: '{schedule_str}'. "
            "Expected YYYY-MM-DD HH:MM"
        )

    # Try to resolve the IANA timezone using the zoneinfo module (Python 3.9+)
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(tz_name)
    except (ImportError, KeyError):
        # Fallback: assume UTC if the timezone cannot be resolved
        tz = timezone.utc

    aware_dt = naive_dt.replace(tzinfo=tz)

    if aware_dt <= datetime.now(tz=tz):
        raise ValueError(
            f"Scheduled time {aware_dt.isoformat()} is in the past."
        )

    return aware_dt


def load_queue():
    """Load the schedule queue from disk, creating it if needed."""
    if not QUEUE_FILE.exists():
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        initial = {"version": 1, "posts": []}
        QUEUE_FILE.write_text(json.dumps(initial, indent=2) + "\n")
        return initial

    with open(QUEUE_FILE, "r") as fh:
        return json.load(fh)


def save_queue(queue_data):
    """Atomically save the queue file with an exclusive file lock."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_FILE, "r+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            fh.seek(0)
            fh.write(json.dumps(queue_data, indent=2) + "\n")
            fh.truncate()
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def validate_media(media_files, platforms):
    """Run validate_media.py as a subprocess. Return (success, output)."""
    if not VALIDATE_SCRIPT.exists():
        return True, "validate_media.py not found; skipping validation."

    cmd = [
        sys.executable,
        str(VALIDATE_SCRIPT),
        "--files", *media_files,
        "--platforms", *platforms,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip()
    if result.returncode != 0:
        error_msg = result.stderr.strip() or output or "Validation failed."
        return False, error_msg
    return True, output


def copy_media(media_files, post_id):
    """Copy media files into assets/scheduled_media/<post_id>/."""
    dest_dir = SCHEDULED_MEDIA_DIR / post_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for filepath in media_files:
        src = Path(filepath).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Media file not found: {src}")
        dest = dest_dir / src.name
        # Handle name collisions by appending a counter
        counter = 1
        while dest.exists():
            dest = dest_dir / f"{src.stem}_{counter}{src.suffix}"
            counter += 1
        shutil.copy2(str(src), str(dest))
        copied.append({
            "path": str(dest),
            "original_path": str(src),
            "type": detect_media_type(str(src)),
        })
    return copied


def build_post_entry(post_id, scheduled_at, tz_name, platforms, caption, media_entries):
    """Construct the queue entry dict for a new scheduled post."""
    return {
        "id": post_id,
        "status": "pending",
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "scheduled_at": scheduled_at.isoformat(),
        "timezone": tz_name,
        "platforms": platforms,
        "caption": caption,
        "media": media_entries,
        "results": {},
        "error": None,
        "completed_at": None,
    }


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Schedule a social media post for future publishing."
    )
    parser.add_argument(
        "--media",
        nargs="+",
        required=True,
        help="Path(s) to media files (images and/or videos).",
    )
    parser.add_argument(
        "--caption",
        required=True,
        help="Post caption / text.",
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        required=True,
        choices=["facebook", "instagram", "tiktok"],
        help="Target platform(s).",
    )
    parser.add_argument(
        "--schedule",
        required=True,
        help='Scheduled date/time in "YYYY-MM-DD HH:MM" format.',
    )
    parser.add_argument(
        "--timezone",
        default=None,
        help="IANA timezone name (default: local system timezone).",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    tz_name = args.timezone or get_local_timezone_name()

    # --- Parse and validate schedule time ---
    try:
        scheduled_at = parse_schedule_time(args.schedule, tz_name)
    except ValueError as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        sys.exit(1)

    # --- Validate media files exist ---
    for f in args.media:
        if not Path(f).exists():
            print(json.dumps({"success": False, "error": f"File not found: {f}"}))
            sys.exit(1)

    # --- Validate media against platform requirements ---
    valid, validation_msg = validate_media(args.media, args.platforms)
    if not valid:
        print(json.dumps({
            "success": False,
            "error": f"Media validation failed: {validation_msg}",
        }))
        sys.exit(1)

    # --- Generate post ID and copy media ---
    post_id = f"post_{uuid4().hex[:12]}"
    try:
        media_entries = copy_media(args.media, post_id)
    except (FileNotFoundError, OSError) as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        sys.exit(1)

    # --- Build queue entry ---
    entry = build_post_entry(
        post_id=post_id,
        scheduled_at=scheduled_at,
        tz_name=tz_name,
        platforms=args.platforms,
        caption=args.caption,
        media_entries=media_entries,
    )

    # --- Load queue, append, and save with lock ---
    queue = load_queue()
    queue["posts"].append(entry)
    save_queue(queue)

    # --- Print success result ---
    result = {
        "success": True,
        "post_id": post_id,
        "scheduled_at": scheduled_at.isoformat(),
        "platforms": args.platforms,
    }
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
