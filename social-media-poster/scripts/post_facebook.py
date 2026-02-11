#!/usr/bin/env python3
"""
Post content to Facebook Pages via the Meta Graph API.

Supports single image, multi-image carousel, single video, and mixed media posts.
Uses Graph API v21.0 with retry logic and exponential backoff for rate limits.

Required environment variables (loaded from .env):
    META_ACCESS_TOKEN   - A valid Page access token for the Facebook Page.
    FACEBOOK_PAGE_ID    - The numeric ID of the Facebook Page to post to.

Usage examples:
    # Single image post
    python post_facebook.py --media photo.jpg --caption "Hello world"

    # Multi-image carousel
    python post_facebook.py --media img1.jpg img2.png img3.jpg --caption "Gallery"

    # Single video post
    python post_facebook.py --media clip.mp4 --caption "Watch this"

    # Mixed media (images + videos)
    python post_facebook.py --media photo.jpg clip.mp4 --caption "Mixed content"
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov"}

MAX_RETRIES = 3
BACKOFF_DELAYS = [2, 4, 8]

RESUMABLE_UPLOAD_THRESHOLD = 100 * 1024 * 1024  # 100 MB


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def classify_media(file_path: str) -> str:
    """Return 'image' or 'video' based on the file extension, or raise."""
    ext = Path(file_path).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    raise ValueError(
        f"Unsupported media extension '{ext}' for file '{file_path}'. "
        f"Supported: {sorted(IMAGE_EXTENSIONS | VIDEO_EXTENSIONS)}"
    )


def output_success(post_id: str, post_type: str) -> None:
    """Print success JSON and exit 0."""
    print(json.dumps({
        "success": True,
        "platform": "facebook",
        "post_id": post_id,
        "post_type": post_type,
    }))
    sys.exit(0)


def output_error(error: str, error_code: str = "") -> None:
    """Print failure JSON and exit 1."""
    print(json.dumps({
        "success": False,
        "platform": "facebook",
        "error": error,
        "error_code": str(error_code),
    }))
    sys.exit(1)


def request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """Execute an HTTP request with exponential-backoff retry on rate limits.

    Retries up to MAX_RETRIES times when the Graph API returns HTTP 429 or an
    error body containing code 4 / code 32 (rate-limit / too-many-calls).
    """
    last_exc: Exception | None = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.request(method, url, timeout=300, **kwargs)

            # Detect rate-limit responses
            if _is_rate_limited(response) and attempt < MAX_RETRIES:
                delay = BACKOFF_DELAYS[attempt]
                time.sleep(delay)
                continue

            return response
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < MAX_RETRIES:
                delay = BACKOFF_DELAYS[attempt]
                time.sleep(delay)
                continue
            raise

    # Should not be reached, but just in case:
    if last_exc:
        raise last_exc
    raise RuntimeError("Retry loop exited unexpectedly")


def _is_rate_limited(response: requests.Response) -> bool:
    """Return True if the response indicates a Graph API rate-limit error."""
    if response.status_code == 429:
        return True
    try:
        data = response.json()
        error_obj = data.get("error", {})
        if error_obj.get("code") in (4, 32, 613):
            return True
    except (ValueError, AttributeError):
        pass
    return False


def _raise_for_api_error(response: requests.Response, context: str = "") -> dict:
    """Parse the JSON body; if it contains an API error, call output_error.

    Returns the parsed JSON dict on success.
    """
    try:
        data = response.json()
    except ValueError:
        output_error(
            f"Non-JSON response from API{f' ({context})' if context else ''}: "
            f"{response.text[:500]}",
            error_code=str(response.status_code),
        )

    if "error" in data:
        err = data["error"]
        msg = err.get("message", "Unknown API error")
        code = err.get("code", response.status_code)
        output_error(
            f"{context + ': ' if context else ''}{msg}",
            error_code=str(code),
        )

    return data


# ---------------------------------------------------------------------------
# Upload helpers
# ---------------------------------------------------------------------------

def upload_image_unpublished(
    page_id: str, access_token: str, file_path: str
) -> str:
    """Upload an image as unpublished and return its media fbid."""
    url = f"{GRAPH_API_BASE}/{page_id}/photos"
    with open(file_path, "rb") as f:
        response = request_with_retry(
            "POST",
            url,
            files={"source": (Path(file_path).name, f)},
            data={
                "published": "false",
                "access_token": access_token,
            },
        )
    data = _raise_for_api_error(response, context=f"Uploading image '{file_path}'")
    photo_id = data.get("id")
    if not photo_id:
        output_error(f"No photo id returned for '{file_path}'", error_code="upload_error")
    return photo_id


def upload_video(
    page_id: str, access_token: str, file_path: str, published: bool = True, description: str = ""
) -> str:
    """Upload a video to the Page.

    Uses resumable upload protocol for files larger than 100 MB.
    Returns the video id.
    """
    file_size = os.path.getsize(file_path)

    if file_size > RESUMABLE_UPLOAD_THRESHOLD:
        return _upload_video_resumable(page_id, access_token, file_path, published, description)
    return _upload_video_simple(page_id, access_token, file_path, published, description)


def _upload_video_simple(
    page_id: str, access_token: str, file_path: str, published: bool, description: str
) -> str:
    """Upload a video using the simple (non-resumable) method."""
    url = f"{GRAPH_API_BASE}/{page_id}/videos"
    with open(file_path, "rb") as f:
        data_fields: dict = {
            "access_token": access_token,
            "published": str(published).lower(),
        }
        if description:
            data_fields["description"] = description
        response = request_with_retry(
            "POST",
            url,
            files={"source": (Path(file_path).name, f)},
            data=data_fields,
        )
    result = _raise_for_api_error(response, context=f"Uploading video '{file_path}'")
    video_id = result.get("id")
    if not video_id:
        output_error(f"No video id returned for '{file_path}'", error_code="upload_error")
    return video_id


def _upload_video_resumable(
    page_id: str, access_token: str, file_path: str, published: bool, description: str
) -> str:
    """Upload a video using the resumable upload protocol (for >100 MB files).

    Three phases: start, transfer, finish.
    """
    file_size = os.path.getsize(file_path)
    file_name = Path(file_path).name
    url = f"{GRAPH_API_BASE}/{page_id}/videos"

    # --- Phase 1: Start --------------------------------------------------
    start_response = request_with_retry(
        "POST",
        url,
        data={
            "access_token": access_token,
            "upload_phase": "start",
            "file_size": str(file_size),
        },
    )
    start_data = _raise_for_api_error(start_response, context="Resumable upload start")
    upload_session_id = start_data.get("upload_session_id")
    start_offset = int(start_data.get("start_offset", 0))
    end_offset = int(start_data.get("end_offset", file_size))

    if not upload_session_id:
        output_error("No upload_session_id returned", error_code="upload_error")

    # --- Phase 2: Transfer -----------------------------------------------
    with open(file_path, "rb") as f:
        while start_offset < file_size:
            chunk_size = end_offset - start_offset
            f.seek(start_offset)
            chunk = f.read(chunk_size)

            transfer_response = request_with_retry(
                "POST",
                url,
                data={
                    "access_token": access_token,
                    "upload_phase": "transfer",
                    "upload_session_id": upload_session_id,
                    "start_offset": str(start_offset),
                },
                files={"video_file_chunk": (file_name, chunk)},
            )
            transfer_data = _raise_for_api_error(
                transfer_response, context="Resumable upload transfer"
            )
            start_offset = int(transfer_data.get("start_offset", file_size))
            end_offset = int(transfer_data.get("end_offset", file_size))

    # --- Phase 3: Finish -------------------------------------------------
    finish_fields: dict = {
        "access_token": access_token,
        "upload_phase": "finish",
        "upload_session_id": upload_session_id,
        "published": str(published).lower(),
    }
    if description:
        finish_fields["description"] = description

    finish_response = request_with_retry("POST", url, data=finish_fields)
    finish_data = _raise_for_api_error(finish_response, context="Resumable upload finish")

    video_id = finish_data.get("id")
    if not video_id:
        output_error("No video id returned after resumable upload", error_code="upload_error")
    return video_id


# ---------------------------------------------------------------------------
# Post-type handlers
# ---------------------------------------------------------------------------

def post_single_image(
    page_id: str, access_token: str, file_path: str, caption: str
) -> None:
    """Publish a single-image post."""
    url = f"{GRAPH_API_BASE}/{page_id}/photos"
    with open(file_path, "rb") as f:
        response = request_with_retry(
            "POST",
            url,
            files={"source": (Path(file_path).name, f)},
            data={
                "message": caption,
                "access_token": access_token,
            },
        )
    data = _raise_for_api_error(response, context="Publishing single image")
    post_id = data.get("post_id") or data.get("id", "")
    output_success(post_id, "single_image")


def post_carousel(
    page_id: str, access_token: str, file_paths: list[str], caption: str
) -> None:
    """Publish a multi-image carousel post."""
    media_ids = []
    for path in file_paths:
        fbid = upload_image_unpublished(page_id, access_token, path)
        media_ids.append(fbid)

    url = f"{GRAPH_API_BASE}/{page_id}/feed"
    data: dict = {
        "message": caption,
        "access_token": access_token,
    }
    for idx, mid in enumerate(media_ids):
        data[f"attached_media[{idx}]"] = json.dumps({"media_fbid": mid})

    response = request_with_retry("POST", url, data=data)
    result = _raise_for_api_error(response, context="Publishing carousel")
    post_id = result.get("id", "")
    output_success(post_id, "carousel")


def post_single_video(
    page_id: str, access_token: str, file_path: str, caption: str
) -> None:
    """Publish a single-video post."""
    video_id = upload_video(
        page_id, access_token, file_path, published=True, description=caption
    )
    output_success(video_id, "video")


def post_mixed_media(
    page_id: str,
    access_token: str,
    media_files: list[dict],
    caption: str,
) -> None:
    """Publish a mixed-media post (images + videos) attached to a feed post.

    Each entry in *media_files* is ``{"path": str, "type": "image"|"video"}``.
    """
    media_ids = []
    for item in media_files:
        if item["type"] == "image":
            fbid = upload_image_unpublished(page_id, access_token, item["path"])
            media_ids.append(fbid)
        else:
            vid = upload_video(
                page_id, access_token, item["path"], published=False
            )
            media_ids.append(vid)

    url = f"{GRAPH_API_BASE}/{page_id}/feed"
    data: dict = {
        "message": caption,
        "access_token": access_token,
    }
    for idx, mid in enumerate(media_ids):
        data[f"attached_media[{idx}]"] = json.dumps({"media_fbid": mid})

    response = request_with_retry("POST", url, data=data)
    result = _raise_for_api_error(response, context="Publishing mixed media")
    post_id = result.get("id", "")
    output_success(post_id, "mixed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post content to a Facebook Page via the Meta Graph API."
    )
    parser.add_argument(
        "--media",
        nargs="+",
        required=False,
        help="Path(s) to media files (.jpg, .jpeg, .png, .mp4, .mov).",
    )
    parser.add_argument(
        "--caption",
        required=True,
        help="Text caption / message for the post.",
    )
    args = parser.parse_args()

    # --- Load environment -------------------------------------------------
    load_dotenv()

    access_token = os.getenv("META_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")

    if not access_token:
        output_error(
            "META_ACCESS_TOKEN is not set. Add it to your .env file.",
            error_code="missing_env",
        )
    if not page_id:
        output_error(
            "FACEBOOK_PAGE_ID is not set. Add it to your .env file.",
            error_code="missing_env",
        )

    media_paths: list[str] = args.media or []

    # --- Validate files ---------------------------------------------------
    media_items: list[dict] = []
    for path in media_paths:
        if not os.path.isfile(path):
            output_error(f"File not found: {path}", error_code="file_not_found")
        try:
            media_type = classify_media(path)
        except ValueError as exc:
            output_error(str(exc), error_code="unsupported_media")
        media_items.append({"path": path, "type": media_type})

    images = [m for m in media_items if m["type"] == "image"]
    videos = [m for m in media_items if m["type"] == "video"]

    # --- Dispatch to the appropriate handler ------------------------------
    try:
        if not media_items:
            # Text-only post (no media)
            url = f"{GRAPH_API_BASE}/{page_id}/feed"
            response = request_with_retry(
                "POST",
                url,
                data={"message": args.caption, "access_token": access_token},
            )
            data = _raise_for_api_error(response, context="Publishing text post")
            output_success(data.get("id", ""), "single_image")

        elif len(images) == 1 and len(videos) == 0:
            post_single_image(page_id, access_token, images[0]["path"], args.caption)

        elif len(images) >= 2 and len(videos) == 0:
            post_carousel(
                page_id, access_token, [m["path"] for m in images], args.caption
            )

        elif len(videos) == 1 and len(images) == 0:
            post_single_video(page_id, access_token, videos[0]["path"], args.caption)

        elif images and videos:
            post_mixed_media(page_id, access_token, media_items, args.caption)

        elif len(videos) >= 2 and len(images) == 0:
            # Multiple videos, no images -- treat as mixed media
            post_mixed_media(page_id, access_token, media_items, args.caption)

        else:
            output_error("Unable to determine post type from provided media.", error_code="invalid_media")

    except requests.exceptions.ConnectionError as exc:
        output_error(f"Connection error: {exc}", error_code="connection_error")
    except requests.exceptions.Timeout as exc:
        output_error(f"Request timed out: {exc}", error_code="timeout")
    except requests.exceptions.RequestException as exc:
        output_error(f"HTTP error: {exc}", error_code="request_error")
    except Exception as exc:
        output_error(f"Unexpected error: {exc}", error_code="unknown_error")


if __name__ == "__main__":
    main()
