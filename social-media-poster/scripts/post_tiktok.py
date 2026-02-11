#!/usr/bin/env python3
"""Post content to TikTok via the TikTok Content Posting API v2.

Supports single video uploads (FILE_UPLOAD) and multi-image photo posts (PULL).
Mixed media (images + videos) in a single post is not supported by TikTok.
"""

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TIKTOK_API_BASE = "https://open.tiktokapis.com/v2"

VIDEO_INIT_URL = f"{TIKTOK_API_BASE}/post/publish/video/init/"
PHOTO_INIT_URL = f"{TIKTOK_API_BASE}/post/publish/content/init/"
STATUS_URL = f"{TIKTOK_API_BASE}/post/publish/status/fetch/"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}

CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB
POLL_INTERVAL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 10 * 60  # 10 minutes

MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 2

PRIVACY_CHOICES = [
    "PUBLIC_TO_EVERYONE",
    "MUTUAL_FOLLOW_FRIENDS",
    "FOLLOWER_OF_CREATOR",
    "SELF_ONLY",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def classify_media(paths: list[str]) -> tuple[list[str], list[str]]:
    """Split *paths* into (images, videos) based on file extension."""
    images: list[str] = []
    videos: list[str] = []
    for p in paths:
        ext = Path(p).suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            images.append(p)
        elif ext in VIDEO_EXTENSIONS:
            videos.append(p)
        else:
            fail(f"Unsupported file extension: {ext} ({p})")
    return images, videos


def fail(message: str, **extra) -> None:
    """Print a JSON error payload and exit with code 1."""
    payload = {"success": False, "platform": "tiktok", "error": message, **extra}
    print(json.dumps(payload, indent=2))
    sys.exit(1)


def success(publish_id: str, post_type: str, **extra) -> None:
    """Print a JSON success payload and exit with code 0."""
    payload = {
        "success": True,
        "platform": "tiktok",
        "publish_id": publish_id,
        "post_type": post_type,
        **extra,
    }
    print(json.dumps(payload, indent=2))
    sys.exit(0)


def auth_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
    }


def request_with_retry(method: str, url: str, retries: int = MAX_RETRIES, **kwargs):
    """Execute an HTTP request with exponential-backoff retry on transient errors."""
    last_exc = None
    for attempt in range(retries):
        try:
            resp = requests.request(method, url, timeout=60, **kwargs)
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.exceptions.HTTPError(
                    f"Transient HTTP {resp.status_code}", response=resp
                )
            return resp
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as exc:
            last_exc = exc
            if attempt < retries - 1:
                wait = BACKOFF_BASE_SECONDS ** (attempt + 1)
                print(
                    f"[retry] Attempt {attempt + 1} failed ({exc}). "
                    f"Retrying in {wait}s ...",
                    file=sys.stderr,
                )
                time.sleep(wait)
    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Video upload (FILE_UPLOAD)
# ---------------------------------------------------------------------------


def post_video(video_path: str, caption: str, privacy: str, access_token: str) -> None:
    """Upload a single video via FILE_UPLOAD and poll until published."""
    path = Path(video_path)
    if not path.is_file():
        fail(f"Video file not found: {video_path}")

    video_size = path.stat().st_size
    total_chunks = math.ceil(video_size / CHUNK_SIZE)

    # Step 1 -- Initialise the upload
    init_body = {
        "post_info": {
            "title": caption,
            "privacy_level": privacy,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": CHUNK_SIZE,
            "total_chunk_count": total_chunks,
        },
    }

    resp = request_with_retry(
        "POST",
        VIDEO_INIT_URL,
        headers=auth_headers(access_token),
        json=init_body,
    )

    data = resp.json()
    error_code = data.get("error", {}).get("code", "ok")
    if error_code not in ("ok", None):
        fail(
            f"Video init failed: {data.get('error', {}).get('message', resp.text)}",
            api_response=data,
        )

    publish_id = data.get("data", {}).get("publish_id", "")
    upload_url = data.get("data", {}).get("upload_url", "")

    if not upload_url:
        fail("Video init response did not include an upload_url.", api_response=data)

    # Step 2 -- Upload video in chunks
    with open(path, "rb") as fh:
        for chunk_idx in range(total_chunks):
            chunk_data = fh.read(CHUNK_SIZE)
            chunk_start = chunk_idx * CHUNK_SIZE
            chunk_end = chunk_start + len(chunk_data) - 1
            content_range = f"bytes {chunk_start}-{chunk_end}/{video_size}"

            upload_headers = {
                "Content-Type": "video/mp4",
                "Content-Range": content_range,
            }

            upload_resp = request_with_retry(
                "PUT",
                upload_url,
                headers=upload_headers,
                data=chunk_data,
            )

            if upload_resp.status_code not in (200, 201, 206):
                fail(
                    f"Chunk {chunk_idx + 1}/{total_chunks} upload failed "
                    f"(HTTP {upload_resp.status_code}): {upload_resp.text}",
                )

            print(
                f"[upload] Chunk {chunk_idx + 1}/{total_chunks} uploaded.",
                file=sys.stderr,
            )

    # Step 3 -- Poll for publish status
    poll_publish_status(publish_id, "video", access_token)


# ---------------------------------------------------------------------------
# Photo post (PULL with public URLs)
# ---------------------------------------------------------------------------


def post_photos(image_urls: list[str], caption: str, privacy: str, access_token: str) -> None:
    """Create a photo post using public image URLs (PULL source)."""
    # Validate that all paths look like URLs
    for url in image_urls:
        if not url.startswith(("http://", "https://")):
            fail(
                f"TikTok photo mode requires public image URLs, but got a local "
                f"path: {url}. Please upload images to a public host first and "
                f"provide their URLs, or use a service that returns public URLs."
            )

    init_body = {
        "post_info": {
            "title": caption,
            "privacy_level": privacy,
        },
        "source_info": {
            "source": "PULL",
            "photo_cover_index": 0,
            "photo_images": image_urls,
        },
        "post_mode": "DIRECT_POST",
        "media_type": "PHOTO",
    }

    resp = request_with_retry(
        "POST",
        PHOTO_INIT_URL,
        headers=auth_headers(access_token),
        json=init_body,
    )

    data = resp.json()
    error_code = data.get("error", {}).get("code", "ok")
    if error_code not in ("ok", None):
        fail(
            f"Photo init failed: {data.get('error', {}).get('message', resp.text)}",
            api_response=data,
        )

    publish_id = data.get("data", {}).get("publish_id", "")

    # Poll for publish status
    poll_publish_status(publish_id, "photo", access_token)


# ---------------------------------------------------------------------------
# Publish-status polling
# ---------------------------------------------------------------------------


def poll_publish_status(publish_id: str, post_type: str, access_token: str) -> None:
    """Poll the TikTok publish status endpoint until complete or timeout."""
    if not publish_id:
        fail("No publish_id returned from the API -- cannot poll status.")

    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    print(f"[poll] Waiting for publish to complete (id={publish_id}) ...", file=sys.stderr)

    while time.monotonic() < deadline:
        resp = request_with_retry(
            "POST",
            STATUS_URL,
            headers=auth_headers(access_token),
            json={"publish_id": publish_id},
        )

        data = resp.json()
        status = (
            data.get("data", {}).get("status", "UNKNOWN").upper()
        )

        print(f"[poll] Status: {status}", file=sys.stderr)

        if status == "PUBLISH_COMPLETE":
            success(publish_id, post_type)

        if status.startswith("FAILED") or status == "PUBLISH_FAILED":
            fail(
                f"Publish failed with status: {status}",
                publish_id=publish_id,
                api_response=data,
            )

        time.sleep(POLL_INTERVAL_SECONDS)

    fail(
        f"Publish timed out after {POLL_TIMEOUT_SECONDS}s (last status: {status}).",
        publish_id=publish_id,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Post content to TikTok via the Content Posting API v2.",
    )
    parser.add_argument(
        "--media",
        nargs="+",
        required=True,
        help="One or more media file paths (video) or public URLs (photo).",
    )
    parser.add_argument(
        "--caption",
        required=True,
        help="Post caption / title.",
    )
    parser.add_argument(
        "--privacy",
        default="SELF_ONLY",
        choices=PRIVACY_CHOICES,
        help="Privacy level (default: SELF_ONLY).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    load_dotenv()

    args = parse_args(argv)

    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    client_key = os.getenv("TIKTOK_CLIENT_KEY")

    if not access_token:
        fail("TIKTOK_ACCESS_TOKEN is not set. Add it to your .env file.")
    if not client_key:
        fail("TIKTOK_CLIENT_KEY is not set. Add it to your .env file.")

    images, videos = classify_media(args.media)

    # --- Mixed media: not supported ----------------------------------------
    if images and videos:
        fail(
            "TikTok does not support mixing images and videos in a single post. "
            "Please split them into separate posts (one video post and one photo post)."
        )

    # --- Single video post --------------------------------------------------
    if videos:
        if len(videos) > 1:
            fail(
                "TikTok only supports uploading one video per post. "
                "Please provide a single video file."
            )
        post_video(videos[0], args.caption, args.privacy, access_token)

    # --- Photo post ---------------------------------------------------------
    if images:
        post_photos(images, args.caption, args.privacy, access_token)


if __name__ == "__main__":
    main()
