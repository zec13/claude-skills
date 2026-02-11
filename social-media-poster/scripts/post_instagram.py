#!/usr/bin/env python3
"""Post content to Instagram via the Meta Graph API Content Publishing API.

Supports single image posts, single video posts (Reels), and carousel posts
containing a mix of images and videos. Local files are uploaded via the
Facebook Photos/Videos API to obtain publicly accessible URLs before being
submitted to the Instagram container workflow.

Environment variables (loaded from .env):
    META_ACCESS_TOKEN              - Long-lived access token for the Meta API.
    INSTAGRAM_BUSINESS_ACCOUNT_ID  - The Instagram Business or Creator account ID.
    FACEBOOK_PAGE_ID               - The Facebook Page ID linked to the Instagram account.
"""

import argparse
import json
import mimetypes
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov"}

POLL_INTERVAL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 300  # 5 minutes

MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 2

CAROUSEL_MIN_ITEMS = 2
CAROUSEL_MAX_ITEMS = 10


# ---------------------------------------------------------------------------
# Helpers – HTTP with retry logic
# ---------------------------------------------------------------------------

def _request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """Execute an HTTP request with exponential-backoff retry on rate limits.

    Retries up to MAX_RETRIES times when the server responds with 429
    (Too Many Requests) or a transient 5xx error.  The back-off doubles
    with each attempt.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.request(method, url, **kwargs)

        if response.status_code == 429 or response.status_code >= 500:
            if attempt == MAX_RETRIES:
                response.raise_for_status()
            wait = BACKOFF_BASE_SECONDS ** attempt
            print(
                f"[retry] Attempt {attempt}/{MAX_RETRIES} got status "
                f"{response.status_code}. Retrying in {wait}s …",
                file=sys.stderr,
            )
            time.sleep(wait)
            continue

        return response

    # Should never reach here, but satisfy the type checker.
    return response  # type: ignore[possibly-undefined]


def _raise_for_graph_error(response: requests.Response, context: str) -> None:
    """Raise a RuntimeError if the Graph API response contains an error."""
    if response.status_code >= 400:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"{context}: HTTP {response.status_code} – {detail}")

    body = response.json()
    if "error" in body:
        raise RuntimeError(f"{context}: {body['error']}")


# ---------------------------------------------------------------------------
# Media classification
# ---------------------------------------------------------------------------

def classify_media(path: str) -> str:
    """Return ``'image'`` or ``'video'`` based on the file extension.

    Raises ``ValueError`` for unsupported extensions.
    """
    ext = Path(path).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    raise ValueError(
        f"Unsupported media extension '{ext}' for file '{path}'. "
        f"Supported: {sorted(IMAGE_EXTENSIONS | VIDEO_EXTENSIONS)}"
    )


def _is_url(path: str) -> bool:
    """Return True when *path* looks like an HTTP(S) URL."""
    return path.startswith("http://") or path.startswith("https://")


# ---------------------------------------------------------------------------
# Local file upload helpers (Facebook API)
# ---------------------------------------------------------------------------

def _upload_image_to_facebook(
    file_path: str, page_id: str, access_token: str
) -> str:
    """Upload a local image via the Facebook Photos API (unpublished).

    Returns the CDN URL of the uploaded image.
    """
    url = f"{GRAPH_API_BASE}/{page_id}/photos"

    content_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"

    with open(file_path, "rb") as fh:
        response = _request_with_retry(
            "POST",
            url,
            data={"published": "false", "access_token": access_token},
            files={"source": (Path(file_path).name, fh, content_type)},
        )

    _raise_for_graph_error(response, "Facebook image upload")
    body = response.json()

    # Retrieve the image URL from the photo object.
    photo_id = body.get("id")
    if not photo_id:
        raise RuntimeError(f"Facebook image upload returned no photo ID: {body}")

    detail_url = f"{GRAPH_API_BASE}/{photo_id}"
    detail_resp = _request_with_retry(
        "GET",
        detail_url,
        params={"fields": "images", "access_token": access_token},
    )
    _raise_for_graph_error(detail_resp, "Facebook image detail fetch")
    images = detail_resp.json().get("images", [])
    if not images:
        raise RuntimeError("Could not retrieve CDN URL for uploaded image.")

    # The first entry is typically the largest / original.
    return images[0]["source"]


def _upload_video_to_facebook(
    file_path: str, page_id: str, access_token: str
) -> str:
    """Upload a local video via the Facebook Videos API.

    Returns the CDN source URL of the uploaded video.
    """
    url = f"{GRAPH_API_BASE}/{page_id}/videos"

    content_type = mimetypes.guess_type(file_path)[0] or "video/mp4"

    with open(file_path, "rb") as fh:
        response = _request_with_retry(
            "POST",
            url,
            data={
                "published": "false",
                "access_token": access_token,
            },
            files={"source": (Path(file_path).name, fh, content_type)},
        )

    _raise_for_graph_error(response, "Facebook video upload")
    body = response.json()

    video_id = body.get("id")
    if not video_id:
        raise RuntimeError(f"Facebook video upload returned no video ID: {body}")

    detail_url = f"{GRAPH_API_BASE}/{video_id}"
    detail_resp = _request_with_retry(
        "GET",
        detail_url,
        params={"fields": "source", "access_token": access_token},
    )
    _raise_for_graph_error(detail_resp, "Facebook video detail fetch")
    source = detail_resp.json().get("source")
    if not source:
        raise RuntimeError("Could not retrieve CDN URL for uploaded video.")

    return source


def resolve_media_url(
    path: str,
    media_type: str,
    page_id: str,
    access_token: str,
) -> str:
    """Return a publicly accessible URL for the given media.

    If *path* is already an HTTP(S) URL it is returned as-is.  Otherwise the
    local file is uploaded to Facebook and the resulting CDN URL is returned.
    """
    if _is_url(path):
        return path

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Local media file not found: {path}")

    if media_type == "image":
        print(f"[upload] Uploading local image to Facebook: {path}", file=sys.stderr)
        return _upload_image_to_facebook(path, page_id, access_token)

    print(f"[upload] Uploading local video to Facebook: {path}", file=sys.stderr)
    return _upload_video_to_facebook(path, page_id, access_token)


# ---------------------------------------------------------------------------
# Instagram container helpers
# ---------------------------------------------------------------------------

def _create_image_container(
    ig_user_id: str,
    image_url: str,
    caption: str | None,
    access_token: str,
    is_carousel_item: bool = False,
) -> str:
    """Create an Instagram image media container and return its ID."""
    url = f"{GRAPH_API_BASE}/{ig_user_id}/media"
    payload: dict = {
        "image_url": image_url,
        "access_token": access_token,
    }
    if caption and not is_carousel_item:
        payload["caption"] = caption
    if is_carousel_item:
        payload["is_carousel_item"] = "true"

    resp = _request_with_retry("POST", url, data=payload)
    _raise_for_graph_error(resp, "Create image container")
    container_id = resp.json().get("id")
    if not container_id:
        raise RuntimeError(f"No container ID returned: {resp.json()}")
    return container_id


def _create_video_container(
    ig_user_id: str,
    video_url: str,
    caption: str | None,
    access_token: str,
    is_carousel_item: bool = False,
) -> str:
    """Create an Instagram Reel / video media container and return its ID."""
    url = f"{GRAPH_API_BASE}/{ig_user_id}/media"
    payload: dict = {
        "video_url": video_url,
        "media_type": "REELS",
        "access_token": access_token,
    }
    if caption and not is_carousel_item:
        payload["caption"] = caption
    if is_carousel_item:
        payload["is_carousel_item"] = "true"

    resp = _request_with_retry("POST", url, data=payload)
    _raise_for_graph_error(resp, "Create video container")
    container_id = resp.json().get("id")
    if not container_id:
        raise RuntimeError(f"No container ID returned: {resp.json()}")
    return container_id


def _poll_container_status(container_id: str, access_token: str) -> None:
    """Poll an Instagram media container until its status is FINISHED.

    Raises ``RuntimeError`` on timeout or if the container enters an ERROR
    state.
    """
    url = f"{GRAPH_API_BASE}/{container_id}"
    params = {"fields": "status_code", "access_token": access_token}
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS

    while time.monotonic() < deadline:
        resp = _request_with_retry("GET", url, params=params)
        _raise_for_graph_error(resp, "Poll container status")
        status = resp.json().get("status_code", "UNKNOWN")
        print(f"[poll] Container {container_id} status: {status}", file=sys.stderr)

        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(
                f"Container {container_id} entered ERROR state: {resp.json()}"
            )

        time.sleep(POLL_INTERVAL_SECONDS)

    raise RuntimeError(
        f"Timed out after {POLL_TIMEOUT_SECONDS}s waiting for container "
        f"{container_id} to finish processing."
    )


def _publish_container(
    ig_user_id: str, creation_id: str, access_token: str
) -> str:
    """Publish a media container and return the published post ID."""
    url = f"{GRAPH_API_BASE}/{ig_user_id}/media_publish"
    payload = {"creation_id": creation_id, "access_token": access_token}
    resp = _request_with_retry("POST", url, data=payload)
    _raise_for_graph_error(resp, "Publish container")
    post_id = resp.json().get("id")
    if not post_id:
        raise RuntimeError(f"No post ID returned after publish: {resp.json()}")
    return post_id


# ---------------------------------------------------------------------------
# High-level post workflows
# ---------------------------------------------------------------------------

def post_single_image(
    ig_user_id: str,
    image_url: str,
    caption: str,
    access_token: str,
) -> dict:
    """Post a single image to Instagram."""
    container_id = _create_image_container(
        ig_user_id, image_url, caption, access_token
    )
    print(f"[info] Image container created: {container_id}", file=sys.stderr)

    post_id = _publish_container(ig_user_id, container_id, access_token)
    return {
        "success": True,
        "platform": "instagram",
        "post_id": post_id,
        "post_type": "single_image",
        "container_id": container_id,
    }


def post_reel(
    ig_user_id: str,
    video_url: str,
    caption: str,
    access_token: str,
) -> dict:
    """Post a single video as an Instagram Reel."""
    container_id = _create_video_container(
        ig_user_id, video_url, caption, access_token
    )
    print(f"[info] Reel container created: {container_id}", file=sys.stderr)

    _poll_container_status(container_id, access_token)

    post_id = _publish_container(ig_user_id, container_id, access_token)
    return {
        "success": True,
        "platform": "instagram",
        "post_id": post_id,
        "post_type": "reel",
        "container_id": container_id,
    }


def post_carousel(
    ig_user_id: str,
    media_items: list[tuple[str, str]],
    caption: str,
    access_token: str,
) -> dict:
    """Post a carousel of images and/or videos to Instagram.

    *media_items* is a list of ``(public_url, media_type)`` tuples where
    *media_type* is ``'image'`` or ``'video'``.
    """
    child_ids: list[str] = []

    for public_url, media_type in media_items:
        if media_type == "image":
            cid = _create_image_container(
                ig_user_id, public_url, None, access_token, is_carousel_item=True
            )
        else:
            cid = _create_video_container(
                ig_user_id, public_url, None, access_token, is_carousel_item=True
            )
        print(
            f"[info] Carousel child container created: {cid} ({media_type})",
            file=sys.stderr,
        )

        # Videos need to finish processing before the carousel is assembled.
        if media_type == "video":
            _poll_container_status(cid, access_token)

        child_ids.append(cid)

    # Create the carousel container.
    url = f"{GRAPH_API_BASE}/{ig_user_id}/media"
    payload = {
        "media_type": "CAROUSEL",
        "caption": caption,
        "children": ",".join(child_ids),
        "access_token": access_token,
    }
    resp = _request_with_retry("POST", url, data=payload)
    _raise_for_graph_error(resp, "Create carousel container")
    carousel_id = resp.json().get("id")
    if not carousel_id:
        raise RuntimeError(f"No carousel container ID returned: {resp.json()}")

    print(f"[info] Carousel container created: {carousel_id}", file=sys.stderr)

    post_id = _publish_container(ig_user_id, carousel_id, access_token)
    return {
        "success": True,
        "platform": "instagram",
        "post_id": post_id,
        "post_type": "carousel",
        "container_id": carousel_id,
        "children": child_ids,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Post content to Instagram via the Meta Graph API."
    )
    parser.add_argument(
        "--media",
        nargs="+",
        required=True,
        help=(
            "One or more media file paths or public URLs. "
            "Supported extensions: .jpg, .jpeg, .png (image), .mp4, .mov (video). "
            "Provide 2-10 items for a carousel."
        ),
    )
    parser.add_argument(
        "--caption",
        required=True,
        help="Caption / text for the Instagram post.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    load_dotenv()

    args = parse_args(argv)

    # ---- Validate environment variables --------------------------------
    access_token = os.getenv("META_ACCESS_TOKEN")
    ig_user_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    page_id = os.getenv("FACEBOOK_PAGE_ID")

    missing: list[str] = []
    if not access_token:
        missing.append("META_ACCESS_TOKEN")
    if not ig_user_id:
        missing.append("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    if not page_id:
        missing.append("FACEBOOK_PAGE_ID")
    if missing:
        result = {
            "success": False,
            "platform": "instagram",
            "error": f"Missing environment variables: {', '.join(missing)}",
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    # Type narrowing after validation.
    assert access_token is not None
    assert ig_user_id is not None
    assert page_id is not None

    media_paths: list[str] = args.media
    caption: str = args.caption

    # ---- Classify & validate media -------------------------------------
    try:
        media_types = [classify_media(m) for m in media_paths]
    except ValueError as exc:
        result = {
            "success": False,
            "platform": "instagram",
            "error": str(exc),
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    if len(media_paths) > 1 and (
        len(media_paths) < CAROUSEL_MIN_ITEMS
        or len(media_paths) > CAROUSEL_MAX_ITEMS
    ):
        result = {
            "success": False,
            "platform": "instagram",
            "error": (
                f"Carousel requires {CAROUSEL_MIN_ITEMS}-{CAROUSEL_MAX_ITEMS} "
                f"items, got {len(media_paths)}."
            ),
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    # ---- Resolve publicly accessible URLs ------------------------------
    try:
        public_urls = [
            resolve_media_url(path, mtype, page_id, access_token)
            for path, mtype in zip(media_paths, media_types)
        ]
    except (FileNotFoundError, RuntimeError) as exc:
        result = {
            "success": False,
            "platform": "instagram",
            "error": f"Media upload failed: {exc}",
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    # ---- Dispatch to the appropriate workflow --------------------------
    try:
        if len(public_urls) == 1 and media_types[0] == "image":
            result = post_single_image(
                ig_user_id, public_urls[0], caption, access_token
            )
        elif len(public_urls) == 1 and media_types[0] == "video":
            result = post_reel(ig_user_id, public_urls[0], caption, access_token)
        else:
            items = list(zip(public_urls, media_types))
            result = post_carousel(ig_user_id, items, caption, access_token)
    except RuntimeError as exc:
        result = {
            "success": False,
            "platform": "instagram",
            "error": str(exc),
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
