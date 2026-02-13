#!/usr/bin/env python3
"""
verify_setup.py — Check that all API credentials are configured and working.

Usage: python3 scripts/verify_setup.py

Tests connections to: Meta (IG/FB/Threads), TikTok, and GitHub.
Reports which are working and which need attention.
"""

import json
import os
import sys
import urllib.request


def check_env(name: str) -> bool:
    val = os.environ.get(name, "")
    return bool(val)


def test_github():
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPO", "Nsf34/claude-skills")

    if not token:
        return {"status": "missing", "detail": "GITHUB_TOKEN not set"}

    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return {"status": "ok", "detail": f"Connected to {data.get('full_name')}"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def test_meta():
    token = os.environ.get("META_ACCESS_TOKEN", "")

    if not token:
        return {"status": "missing", "detail": "META_ACCESS_TOKEN not set"}

    url = f"https://graph.facebook.com/v19.0/me?access_token={token}"

    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
            return {"status": "ok", "detail": f"Connected as {data.get('name', 'unknown')}"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def test_tiktok():
    token = os.environ.get("TIKTOK_ACCESS_TOKEN", "")

    if not token:
        return {"status": "missing", "detail": "TIKTOK_ACCESS_TOKEN not set"}

    url = "https://open.tiktokapis.com/v2/user/info/"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return {"status": "ok", "detail": "Connected to TikTok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def main():
    print("=" * 50)
    print("ORGANIC SOCIAL POSTER — SETUP VERIFICATION")
    print("=" * 50)
    print()

    # Check environment variables
    env_vars = {
        "META_ACCESS_TOKEN": "Meta API token",
        "FB_PAGE_ID": "Facebook Page ID",
        "IG_BUSINESS_ACCOUNT_ID": "Instagram Business Account ID",
        "THREADS_USER_ID": "Threads User ID",
        "TIKTOK_ACCESS_TOKEN": "TikTok access token",
        "GITHUB_TOKEN": "GitHub personal access token",
        "GITHUB_REPO": "GitHub repo (default: Nsf34/claude-skills)",
    }

    print("Environment Variables:")
    for var, desc in env_vars.items():
        status = "✅" if check_env(var) else "❌"
        print(f"  {status} {var} — {desc}")

    print()
    print("API Connectivity:")

    # Test GitHub
    gh = test_github()
    icon = "✅" if gh["status"] == "ok" else "❌"
    print(f"  {icon} GitHub: {gh['detail']}")

    # Test Meta
    meta = test_meta()
    icon = "✅" if meta["status"] == "ok" else "❌"
    print(f"  {icon} Meta (IG/FB/Threads): {meta['detail']}")

    # Test TikTok
    tt = test_tiktok()
    icon = "✅" if tt["status"] == "ok" else "❌"
    print(f"  {icon} TikTok: {tt['detail']}")

    print()

    all_ok = all(s["status"] == "ok" for s in [gh, meta, tt])
    if all_ok:
        print("All systems go! Ready to post.")
    else:
        print("Some services need setup. See references/api-setup-guide.md for instructions.")
        sys.exit(1)


if __name__ == "__main__":
    main()
