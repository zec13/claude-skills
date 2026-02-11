#!/usr/bin/env python3
"""Validate media files against social media platform requirements before posting."""

import argparse
import json
import os
import shutil
import subprocess
import sys

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ---------------------------------------------------------------------------
# Platform requirement definitions
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}

# Per-platform image constraints
PLATFORM_IMAGE_REQUIREMENTS = {
    "facebook": {
        "extensions": {".jpg", ".jpeg", ".png"},
        "max_size_bytes": 10 * 1024 * 1024,  # 10 MB
        "min_width": 100,
        "min_height": 100,
    },
    "instagram": {
        "extensions": {".jpg", ".jpeg", ".png"},
        "max_size_bytes": 8 * 1024 * 1024,  # 8 MB
        "min_width": 320,
        "min_height": 320,
    },
    "tiktok": {
        "extensions": {".jpg", ".jpeg", ".png", ".webp"},
        "max_size_bytes": 20 * 1024 * 1024,  # 20 MB
        "min_width": 360,
        "min_height": 360,
    },
}

# Per-platform video constraints
# duration_max_seconds == None means no duration limit enforced here
PLATFORM_VIDEO_REQUIREMENTS = {
    "facebook": {
        "extensions": {".mp4", ".mov"},
        "max_size_bytes": 10 * 1024 * 1024 * 1024,  # 10 GB
        "duration_max_seconds": 240 * 60,  # 240 min
    },
    "instagram": {
        "extensions": {".mp4", ".mov"},
        "max_size_bytes": 1 * 1024 * 1024 * 1024,  # 1 GB
        "duration_max_seconds": 15 * 60,  # 15 min (Reels)
    },
    "tiktok": {
        "extensions": {".mp4", ".mov", ".webm"},
        "max_size_bytes": 4 * 1024 * 1024 * 1024,  # 4 GB
        "duration_max_seconds": 10 * 60,  # 10 min
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def classify_media(filepath):
    """Return 'image', 'video', or None based on file extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return None


def get_file_size_mb(filepath):
    """Return file size in megabytes, rounded to two decimals."""
    return round(os.path.getsize(filepath) / (1024 * 1024), 2)


def get_image_dimensions(filepath):
    """Return (width, height) using PIL. Returns None if PIL is unavailable."""
    if not PIL_AVAILABLE:
        return None
    try:
        with Image.open(filepath) as img:
            return img.size  # (width, height)
    except Exception:
        return None


def get_video_duration(filepath):
    """Return video duration in seconds via ffprobe, or None if unavailable."""
    if not shutil.which("ffprobe"):
        return None
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                filepath,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except Exception:
        pass
    return None


def fmt_bytes(num_bytes):
    """Human-readable byte size string."""
    if num_bytes >= 1024 * 1024 * 1024:
        return f"{num_bytes / (1024 ** 3):.1f} GB"
    if num_bytes >= 1024 * 1024:
        return f"{num_bytes / (1024 ** 2):.1f} MB"
    if num_bytes >= 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes} B"


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------


def validate_file(filepath, platforms):
    """Validate a single file against the given platforms.

    Returns a dict with keys: file, type, size_mb, issues, warnings.
    """
    result = {
        "file": filepath,
        "type": None,
        "size_mb": 0.0,
        "issues": [],
        "warnings": [],
    }

    # --- Existence / readability ---
    if not os.path.isfile(filepath):
        result["issues"].append(f"File does not exist: {filepath}")
        return result

    if not os.access(filepath, os.R_OK):
        result["issues"].append(f"File is not readable: {filepath}")
        return result

    # --- Classify ---
    media_type = classify_media(filepath)
    if media_type is None:
        ext = os.path.splitext(filepath)[1].lower()
        result["issues"].append(
            f"Unsupported file extension '{ext}'. "
            f"Supported: {', '.join(sorted(IMAGE_EXTENSIONS | VIDEO_EXTENSIONS))}"
        )
        return result

    result["type"] = media_type
    file_size = os.path.getsize(filepath)
    result["size_mb"] = round(file_size / (1024 * 1024), 2)
    ext = os.path.splitext(filepath)[1].lower()

    # --- Per-platform checks ---
    for platform in platforms:
        if media_type == "image":
            reqs = PLATFORM_IMAGE_REQUIREMENTS[platform]
            _validate_image(filepath, ext, file_size, reqs, platform, result)
        else:
            reqs = PLATFORM_VIDEO_REQUIREMENTS[platform]
            _validate_video(filepath, ext, file_size, reqs, platform, result)

    return result


def _validate_image(filepath, ext, file_size, reqs, platform, result):
    """Check image-specific constraints for a single platform."""
    # Extension
    if ext not in reqs["extensions"]:
        result["issues"].append(
            f"[{platform}] Extension '{ext}' not supported. "
            f"Allowed: {', '.join(sorted(reqs['extensions']))}"
        )

    # File size
    if file_size > reqs["max_size_bytes"]:
        result["issues"].append(
            f"[{platform}] File size ({fmt_bytes(file_size)}) exceeds "
            f"maximum ({fmt_bytes(reqs['max_size_bytes'])})"
        )

    # Dimensions
    if not PIL_AVAILABLE:
        result["warnings"].append(
            f"[{platform}] PIL/Pillow not installed — skipping dimension check"
        )
    else:
        dims = get_image_dimensions(filepath)
        if dims is None:
            result["warnings"].append(
                f"[{platform}] Could not read image dimensions"
            )
        else:
            width, height = dims
            min_w = reqs["min_width"]
            min_h = reqs["min_height"]
            if width < min_w or height < min_h:
                result["issues"].append(
                    f"[{platform}] Image dimensions {width}x{height} below "
                    f"minimum {min_w}x{min_h}"
                )


def _validate_video(filepath, ext, file_size, reqs, platform, result):
    """Check video-specific constraints for a single platform."""
    # Extension
    if ext not in reqs["extensions"]:
        result["issues"].append(
            f"[{platform}] Extension '{ext}' not supported. "
            f"Allowed: {', '.join(sorted(reqs['extensions']))}"
        )

    # File size
    if file_size > reqs["max_size_bytes"]:
        result["issues"].append(
            f"[{platform}] File size ({fmt_bytes(file_size)}) exceeds "
            f"maximum ({fmt_bytes(reqs['max_size_bytes'])})"
        )

    # Duration
    max_dur = reqs.get("duration_max_seconds")
    if max_dur is not None:
        duration = get_video_duration(filepath)
        if duration is None:
            result["warnings"].append(
                f"[{platform}] ffprobe not available — skipping duration check"
            )
        elif duration > max_dur:
            dur_min = duration / 60
            limit_min = max_dur / 60
            result["issues"].append(
                f"[{platform}] Video duration ({dur_min:.1f} min) exceeds "
                f"maximum ({limit_min:.1f} min)"
            )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

PLATFORM_CHOICES = ["facebook", "instagram", "tiktok"]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate media files against social media platform requirements."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="One or more media file paths to validate.",
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        required=True,
        choices=PLATFORM_CHOICES,
        help="Target platforms to validate against.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    file_results = []
    for filepath in args.files:
        file_results.append(validate_file(filepath, args.platforms))

    valid_count = sum(1 for r in file_results if not r["issues"])
    invalid_count = len(file_results) - valid_count
    all_valid = invalid_count == 0

    output = {
        "valid": all_valid,
        "files": file_results,
        "summary": {
            "total": len(file_results),
            "valid": valid_count,
            "invalid": invalid_count,
        },
    }

    print(json.dumps(output, indent=2))
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
