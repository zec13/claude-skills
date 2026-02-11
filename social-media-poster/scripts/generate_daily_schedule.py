#!/usr/bin/env python3
"""
Generate a daily posting schedule with non-identical rhythm.

Creates 5 posting times per day per platform within a configurable window
(default 8:00 AM - 9:00 PM), using staggered timing so posts land at
organic-looking intervals that differ across platforms.

Each platform gets its own unique set of times — they never post
simultaneously. A minimum gap between consecutive posts is enforced.

Usage:
    # Schedule 5 posts per platform for tomorrow using a content manifest
    python generate_daily_schedule.py \
        --manifest content_manifest.json \
        --platforms facebook instagram tiktok \
        --date 2025-02-15 \
        --timezone "America/New_York"

    # Preview times only (dry run, no posts queued)
    python generate_daily_schedule.py \
        --manifest content_manifest.json \
        --platforms facebook instagram \
        --date 2025-02-15 \
        --dry-run

    # Custom window and post count
    python generate_daily_schedule.py \
        --manifest content_manifest.json \
        --platforms facebook instagram tiktok \
        --date 2025-02-15 \
        --start-hour 9 --end-hour 20 --posts-per-day 4

Content Manifest Format (JSON):
    [
        {
            "media": ["/path/to/image1.jpg"],
            "caption": "First post caption #hashtag"
        },
        {
            "media": ["/path/to/video.mp4"],
            "caption": "Second post caption"
        },
        ...
    ]

    The manifest must contain at least (posts_per_day * num_platforms) entries.
    Content is assigned round-robin: post 1 goes to all platforms, post 2 to
    all platforms, etc. If you want different content per platform, create
    separate manifests and run the script once per platform.
"""

import argparse
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCHEDULE_SCRIPT = SCRIPT_DIR / "schedule_post.py"

DEFAULT_POSTS_PER_DAY = 5
DEFAULT_START_HOUR = 8    # 8:00 AM
DEFAULT_END_HOUR = 21     # 9:00 PM
MIN_GAP_MINUTES = 30      # Minimum gap between consecutive posts on same platform
PLATFORM_OFFSET_RANGE = (3, 15)  # Random offset in minutes between platforms


def generate_times(posts_per_day, start_hour, end_hour, seed=None):
    """Generate organic-looking posting times within a daily window.

    Divides the window into segments, then picks a random time within each
    segment with jitter. This produces varied but evenly-distributed times
    that never cluster too closely.

    Returns a sorted list of (hour, minute) tuples.
    """
    if seed is not None:
        random.seed(seed)

    window_start = start_hour * 60  # minutes from midnight
    window_end = end_hour * 60
    total_minutes = window_end - window_start

    if posts_per_day <= 0:
        return []

    # Divide window into segments with padding
    segment_size = total_minutes / posts_per_day
    if segment_size < MIN_GAP_MINUTES:
        print(
            f"Warning: Window too small for {posts_per_day} posts with "
            f"{MIN_GAP_MINUTES}min gaps. Reducing gap enforcement.",
            file=sys.stderr,
        )

    times = []
    for i in range(posts_per_day):
        seg_start = window_start + (i * segment_size)
        seg_end = window_start + ((i + 1) * segment_size)

        # Add inner padding so times don't land on segment edges
        padding = min(segment_size * 0.15, 10)
        pick_start = seg_start + padding
        pick_end = seg_end - padding

        minute_of_day = random.uniform(pick_start, pick_end)
        minute_of_day = int(round(minute_of_day))

        # Clamp to window
        minute_of_day = max(window_start, min(window_end - 1, minute_of_day))

        hour = minute_of_day // 60
        minute = minute_of_day % 60
        times.append((hour, minute))

    # Enforce minimum gap
    times.sort()
    for i in range(1, len(times)):
        prev_total = times[i - 1][0] * 60 + times[i - 1][1]
        curr_total = times[i][0] * 60 + times[i][1]
        if curr_total - prev_total < MIN_GAP_MINUTES:
            nudged = prev_total + MIN_GAP_MINUTES
            if nudged < window_end:
                times[i] = (nudged // 60, nudged % 60)

    return times


def generate_platform_schedules(platforms, posts_per_day, start_hour, end_hour, date_str):
    """Generate unique time slots for each platform.

    Each platform gets its own randomized times. Cross-platform times are
    offset so no two platforms post in the same minute.
    """
    schedules = {}
    all_used_minutes = set()

    for platform in platforms:
        # Each platform gets a different random seed based on date + name
        # so the same date always produces different-but-reproducible times
        seed_str = f"{date_str}-{platform}"
        seed = hash(seed_str) & 0xFFFFFFFF
        times = generate_times(posts_per_day, start_hour, end_hour, seed=seed)

        # Offset any collisions with already-used minutes
        adjusted = []
        for hour, minute in times:
            total = hour * 60 + minute
            attempts = 0
            while total in all_used_minutes and attempts < 30:
                offset = random.randint(*PLATFORM_OFFSET_RANGE)
                total += offset
                attempts += 1
            if total >= end_hour * 60:
                total = end_hour * 60 - random.randint(1, 15)
            all_used_minutes.add(total)
            adjusted.append((total // 60, total % 60))

        adjusted.sort()
        schedules[platform] = adjusted

    return schedules


def load_manifest(manifest_path):
    """Load and validate the content manifest JSON file."""
    path = Path(manifest_path)
    if not path.exists():
        print(json.dumps({"success": False, "error": f"Manifest not found: {manifest_path}"}))
        sys.exit(1)

    try:
        with open(path, "r") as fh:
            manifest = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"success": False, "error": f"Failed to read manifest: {exc}"}))
        sys.exit(1)

    if not isinstance(manifest, list):
        print(json.dumps({"success": False, "error": "Manifest must be a JSON array of post objects."}))
        sys.exit(1)

    for i, entry in enumerate(manifest):
        if "media" not in entry or "caption" not in entry:
            print(json.dumps({
                "success": False,
                "error": f"Manifest entry {i} missing 'media' or 'caption' field.",
            }))
            sys.exit(1)

    return manifest


def schedule_one_post(media_files, caption, platforms, date_str, hour, minute, tz_name):
    """Call schedule_post.py to queue a single post."""
    time_str = f"{date_str} {hour:02d}:{minute:02d}"
    cmd = [
        sys.executable,
        str(SCHEDULE_SCRIPT),
        "--media", *media_files,
        "--caption", caption,
        "--platforms", *platforms,
        "--schedule", time_str,
        "--timezone", tz_name,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        error = result.stderr.strip() or result.stdout.strip()
        return {"success": False, "time": time_str, "error": error}

    try:
        output = json.loads(result.stdout.strip())
        return {"success": True, "time": time_str, **output}
    except (json.JSONDecodeError, ValueError):
        return {"success": True, "time": time_str, "raw_output": result.stdout.strip()}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Generate a daily posting schedule with non-identical rhythm. "
            "Creates staggered posting times across platforms."
        ),
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to content manifest JSON file.",
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        required=True,
        choices=["facebook", "instagram", "tiktok"],
        help="Target platforms.",
    )
    parser.add_argument(
        "--date",
        required=True,
        help="Target date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--timezone",
        default="America/New_York",
        help="IANA timezone name (default: America/New_York).",
    )
    parser.add_argument(
        "--posts-per-day",
        type=int,
        default=DEFAULT_POSTS_PER_DAY,
        help=f"Number of posts per platform per day (default: {DEFAULT_POSTS_PER_DAY}).",
    )
    parser.add_argument(
        "--start-hour",
        type=int,
        default=DEFAULT_START_HOUR,
        help=f"Earliest posting hour in 24h format (default: {DEFAULT_START_HOUR}).",
    )
    parser.add_argument(
        "--end-hour",
        type=int,
        default=DEFAULT_END_HOUR,
        help=f"Latest posting hour in 24h format (default: {DEFAULT_END_HOUR}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the generated schedule without actually queuing posts.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    # Validate date
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(json.dumps({"success": False, "error": f"Invalid date format: {args.date}. Use YYYY-MM-DD."}))
        sys.exit(1)

    if args.start_hour >= args.end_hour:
        print(json.dumps({"success": False, "error": "start-hour must be less than end-hour."}))
        sys.exit(1)

    # Load content manifest
    manifest = load_manifest(args.manifest)
    total_needed = args.posts_per_day * len(args.platforms)

    if len(manifest) < total_needed:
        print(json.dumps({
            "success": False,
            "error": (
                f"Manifest has {len(manifest)} entries but {total_needed} are needed "
                f"({args.posts_per_day} posts x {len(args.platforms)} platforms)."
            ),
        }))
        sys.exit(1)

    # Generate platform-specific schedules
    schedules = generate_platform_schedules(
        args.platforms, args.posts_per_day,
        args.start_hour, args.end_hour, args.date,
    )

    # Display the schedule
    print(f"\n{'='*60}")
    print(f"  Daily Schedule for {args.date}")
    print(f"  Window: {args.start_hour:02d}:00 - {args.end_hour:02d}:00 ({args.timezone})")
    print(f"  Posts per platform: {args.posts_per_day}")
    print(f"{'='*60}\n")

    for platform, times in schedules.items():
        print(f"  {platform.upper()}:")
        for i, (hour, minute) in enumerate(times):
            print(f"    Post {i+1}: {hour:02d}:{minute:02d}")
        print()

    if args.dry_run:
        print("[DRY RUN] No posts were queued. Remove --dry-run to schedule.\n")
        # Output JSON summary
        summary = {
            "dry_run": True,
            "date": args.date,
            "schedules": {
                p: [f"{h:02d}:{m:02d}" for h, m in times]
                for p, times in schedules.items()
            },
        }
        print(json.dumps(summary, indent=2))
        sys.exit(0)

    # Queue the posts
    results = []
    content_idx = 0

    for slot_idx in range(args.posts_per_day):
        for platform in args.platforms:
            hour, minute = schedules[platform][slot_idx]
            entry = manifest[content_idx]
            content_idx += 1

            print(f"Scheduling: {platform} at {hour:02d}:{minute:02d} ...", end=" ")
            result = schedule_one_post(
                media_files=entry["media"],
                caption=entry["caption"],
                platforms=[platform],
                date_str=args.date,
                hour=hour,
                minute=minute,
                tz_name=args.timezone,
            )
            results.append({**result, "platform": platform})

            if result["success"]:
                print(f"OK (id={result.get('post_id', '?')})")
            else:
                print(f"FAILED: {result.get('error', 'unknown')}")

    # Summary
    successes = sum(1 for r in results if r["success"])
    failures = len(results) - successes

    print(f"\n{'='*60}")
    print(f"  Scheduled: {successes}/{len(results)} posts")
    if failures:
        print(f"  Failed: {failures}")
    print(f"{'='*60}\n")

    output = {
        "success": failures == 0,
        "scheduled": successes,
        "failed": failures,
        "results": results,
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
