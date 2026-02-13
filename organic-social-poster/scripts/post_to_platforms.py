#!/usr/bin/env python3
"""
post_to_platforms.py — Post an image to Instagram, Facebook, Threads, and TikTok.

Usage:
    python3 scripts/post_to_platforms.py \
        --brand "TableClay" \
        --image "/tmp/organic-poster/TableClay/blue-mug.jpg" \
        --ig-caption "Your IG caption here" \
        --ig-hashtags "#pottery #handmade #ceramics" \
        --fb-caption "Your FB caption here" \
        --threads-caption "Your Threads caption here" \
        --tiktok-caption "Your TikTok caption here"

Requires environment variables (see references/api-setup-guide.md):
    META_ACCESS_TOKEN, FB_PAGE_ID, IG_BUSINESS_ACCOUNT_ID, THREADS_USER_ID
    TIKTOK_ACCESS_TOKEN

Per-brand overrides supported (e.g., TABLECLAY_IG_BUSINESS_ACCOUNT_ID).
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import base64


def get_env(brand: str, key: str) -> str:
    """Get env var with brand-specific override. E.g., TABLECLAY_FB_PAGE_ID or FB_PAGE_ID."""
    brand_key = f"{brand.upper()}_{key}"
    return os.environ.get(brand_key, os.environ.get(key, ""))


def post_instagram(brand: str, image_url: str, caption: str, hashtags: str) -> dict:
    """Post to Instagram via Meta Graph API."""
    token = get_env(brand, "META_ACCESS_TOKEN")
    ig_id = get_env(brand, "IG_BUSINESS_ACCOUNT_ID")

    if not token or not ig_id:
        return {"success": False, "error": "Missing META_ACCESS_TOKEN or IG_BUSINESS_ACCOUNT_ID"}

    # Step 1: Create media container
    params = urllib.parse.urlencode({
        "image_url": image_url,
        "caption": caption,
        "access_token": token,
    })
    url = f"https://graph.facebook.com/v19.0/{ig_id}/media?{params}"

    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            container_id = data.get("id")
    except Exception as e:
        return {"success": False, "error": f"Container creation failed: {e}"}

    # Step 2: Publish
    params = urllib.parse.urlencode({
        "creation_id": container_id,
        "access_token": token,
    })
    url = f"https://graph.facebook.com/v19.0/{ig_id}/media_publish?{params}"

    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            media_id = data.get("id")
    except Exception as e:
        return {"success": False, "error": f"Publishing failed: {e}"}

    # Step 3: Post hashtags as first comment
    if hashtags:
        params = urllib.parse.urlencode({
            "message": hashtags,
            "access_token": token,
        })
        url = f"https://graph.facebook.com/v19.0/{media_id}/comments?{params}"
        try:
            req = urllib.request.Request(url, method="POST")
            urllib.request.urlopen(req)
        except Exception:
            pass  # Non-critical if comment fails

    return {"success": True, "media_id": media_id}


def post_facebook(brand: str, image_url: str, caption: str) -> dict:
    """Post to Facebook Page via Meta Graph API."""
    token = get_env(brand, "META_ACCESS_TOKEN")
    page_id = get_env(brand, "FB_PAGE_ID")

    if not token or not page_id:
        return {"success": False, "error": "Missing META_ACCESS_TOKEN or FB_PAGE_ID"}

    params = urllib.parse.urlencode({
        "url": image_url,
        "message": caption,
        "access_token": token,
    })
    url = f"https://graph.facebook.com/v19.0/{page_id}/photos?{params}"

    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return {"success": True, "post_id": data.get("id")}
    except Exception as e:
        return {"success": False, "error": f"Facebook post failed: {e}"}


def post_threads(brand: str, image_url: str, caption: str) -> dict:
    """Post to Threads via Meta Threads API."""
    token = get_env(brand, "META_ACCESS_TOKEN")
    threads_id = get_env(brand, "THREADS_USER_ID")

    if not token or not threads_id:
        return {"success": False, "error": "Missing META_ACCESS_TOKEN or THREADS_USER_ID"}

    # Step 1: Create container
    params = urllib.parse.urlencode({
        "media_type": "IMAGE",
        "image_url": image_url,
        "text": caption,
        "access_token": token,
    })
    url = f"https://graph.threads.net/v1.0/{threads_id}/threads?{params}"

    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            container_id = data.get("id")
    except Exception as e:
        return {"success": False, "error": f"Threads container failed: {e}"}

    # Step 2: Publish
    params = urllib.parse.urlencode({
        "creation_id": container_id,
        "access_token": token,
    })
    url = f"https://graph.threads.net/v1.0/{threads_id}/threads_publish?{params}"

    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return {"success": True, "media_id": data.get("id")}
    except Exception as e:
        return {"success": False, "error": f"Threads publish failed: {e}"}


def post_tiktok(brand: str, image_url: str, caption: str) -> dict:
    """Post photo to TikTok via Content Posting API."""
    token = get_env(brand, "TIKTOK_ACCESS_TOKEN")

    if not token:
        return {"success": False, "error": "Missing TIKTOK_ACCESS_TOKEN"}

    body = json.dumps({
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "photo_cover_index": 0,
            "photo_images": [image_url],
        },
        "media_type": "PHOTO",
    }).encode()

    url = "https://open.tiktokapis.com/v2/post/publish/content/init/"

    try:
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            publish_id = data.get("data", {}).get("publish_id")
            return {"success": True, "publish_id": publish_id}
    except Exception as e:
        return {"success": False, "error": f"TikTok post failed: {e}"}


def main():
    parser = argparse.ArgumentParser(description="Post to social media platforms")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--image", required=True, help="Local path or public URL")
    parser.add_argument("--ig-caption", default="")
    parser.add_argument("--ig-hashtags", default="")
    parser.add_argument("--fb-caption", default="")
    parser.add_argument("--threads-caption", default="")
    parser.add_argument("--tiktok-caption", default="")
    args = parser.parse_args()

    # The image needs to be publicly accessible for Meta and TikTok APIs.
    # If it's a local path, the calling script should upload it to a public URL first
    # (e.g., GitHub raw URL or a temp hosting service).
    image_url = args.image

    results = {}

    # Post to each platform
    if args.ig_caption:
        print("Posting to Instagram...")
        results["instagram"] = post_instagram(args.brand, image_url, args.ig_caption, args.ig_hashtags)
        time.sleep(2)  # Brief pause between API calls

    if args.fb_caption:
        print("Posting to Facebook...")
        results["facebook"] = post_facebook(args.brand, image_url, args.fb_caption)
        time.sleep(2)

    if args.threads_caption:
        print("Posting to Threads...")
        results["threads"] = post_threads(args.brand, image_url, args.threads_caption)
        time.sleep(2)

    if args.tiktok_caption:
        print("Posting to TikTok...")
        results["tiktok"] = post_tiktok(args.brand, image_url, args.tiktok_caption)

    # Summary
    print("\n" + "=" * 40)
    print(f"POSTING RESULTS — {args.brand}")
    print("=" * 40)

    for platform, result in results.items():
        status = "✅" if result.get("success") else "❌"
        detail = result.get("error", result.get("media_id", result.get("post_id", result.get("publish_id", ""))))
        print(f"  {status} {platform}: {detail}")

    # Write results to JSON
    output_path = f"/tmp/organic-poster/{args.brand}/post_result.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    # Exit with error if any platform failed
    if any(not r.get("success") for r in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
