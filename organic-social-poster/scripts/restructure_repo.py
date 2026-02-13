#!/usr/bin/env python3
"""
restructure_repo.py — Reorganize the GitHub repo from 'Business Research/' to 'Brands/' structure.

This script:
1. Reads current files from Business Research/{Brand}/*.docx
2. Creates new Brands/{Brand}/research/ folders and moves dossiers there
3. Creates empty organic-images/ and already-posted/ folders (with .gitkeep)
4. Deletes old Business Research/ files after confirming the move

Usage:
    export GITHUB_TOKEN="your_token"
    python3 scripts/restructure_repo.py

    # Dry run (show what would happen without making changes):
    python3 scripts/restructure_repo.py --dry-run
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.parse


REPO = os.environ.get("GITHUB_REPO", "Nsf34/claude-skills")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
BRANCH = "main"
BASE_URL = "https://api.github.com"

BRANDS = ["Aniwove", "LeafLofts", "PrepPack", "ScrollMerch", "TableClay"]


def api_request(method: str, path: str, data: dict = None) -> dict:
    """Make a GitHub API request."""
    url = f"{BASE_URL}/repos/{REPO}/contents/{urllib.parse.quote(path, safe='/')}"

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if body:
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        if e.code == 404:
            return None
        print(f"  API Error {e.code}: {error_body[:200]}")
        return None


def list_contents(path: str) -> list:
    """List files/dirs at a GitHub path."""
    result = api_request("GET", path)
    if result and isinstance(result, list):
        return result
    return []


def create_file(path: str, content_b64: str, message: str, dry_run: bool):
    """Create a file in the repo."""
    if dry_run:
        print(f"  [DRY RUN] Would create: {path}")
        return True

    result = api_request("PUT", path, {
        "message": message,
        "content": content_b64,
        "branch": BRANCH,
    })
    time.sleep(0.5)  # Rate limit courtesy
    return result is not None


def delete_file(path: str, sha: str, message: str, dry_run: bool):
    """Delete a file from the repo."""
    if dry_run:
        print(f"  [DRY RUN] Would delete: {path}")
        return True

    url = f"{BASE_URL}/repos/{REPO}/contents/{urllib.parse.quote(path, safe='/')}"
    body = json.dumps({
        "message": message,
        "sha": sha,
        "branch": BRANCH,
    }).encode()

    req = urllib.request.Request(url, data=body, method="DELETE")
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            time.sleep(0.5)
            return True
    except Exception as e:
        print(f"  Delete failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Restructure repo: Business Research → Brands")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")
    args = parser.parse_args()

    if not TOKEN:
        print("ERROR: Set GITHUB_TOKEN environment variable first.")
        print("  export GITHUB_TOKEN='your_github_personal_access_token'")
        sys.exit(1)

    print("=" * 60)
    print("REPO RESTRUCTURE: Business Research → Brands")
    print(f"Repo: {REPO}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)

    # Step 1: Create Brands/{Brand}/research/, organic-images/, already-posted/ for each brand
    gitkeep_content = base64.b64encode(b"").decode()  # empty .gitkeep file

    for brand in BRANDS:
        print(f"\n--- {brand} ---")

        # Create folder structure with .gitkeep files
        for subfolder in ["research", "organic-images", "already-posted"]:
            path = f"Brands/{brand}/{subfolder}/.gitkeep"
            print(f"  Creating {path}...")
            create_file(
                path,
                gitkeep_content,
                f"Create Brands/{brand}/{subfolder}/ folder",
                args.dry_run,
            )

        # Step 2: Move research dossiers from Business Research/{Brand}/ to Brands/{Brand}/research/
        old_path = f"Business Research/{brand}"
        files = list_contents(old_path)

        if not files:
            print(f"  No files found in Business Research/{brand}/")
            continue

        for file_info in files:
            if file_info["type"] != "file":
                continue

            filename = file_info["name"]
            old_file_path = file_info["path"]
            new_file_path = f"Brands/{brand}/research/{filename}"

            print(f"  Moving: {filename}")
            print(f"    From: {old_file_path}")
            print(f"    To:   {new_file_path}")

            # Get file content
            if not args.dry_run:
                file_data = api_request("GET", old_file_path)
                if not file_data:
                    print(f"    ERROR: Could not read {old_file_path}")
                    continue

                file_content = file_data.get("content", "").replace("\n", "")
                file_sha = file_data["sha"]

                # Create at new location
                success = create_file(
                    new_file_path,
                    file_content,
                    f"Move {filename} to Brands/{brand}/research/",
                    False,
                )

                if success:
                    # Delete from old location
                    delete_file(
                        old_file_path,
                        file_sha,
                        f"Moved to Brands/{brand}/research/",
                        False,
                    )
                    print(f"    ✅ Moved successfully")
                else:
                    print(f"    ❌ Failed to create at new location")
            else:
                print(f"    [DRY RUN] Would move")

    print("\n" + "=" * 60)
    if args.dry_run:
        print("DRY RUN COMPLETE. Run without --dry-run to make changes.")
    else:
        print("RESTRUCTURE COMPLETE!")
        print("Your repo now has:")
        for brand in BRANDS:
            print(f"  Brands/{brand}/research/")
            print(f"  Brands/{brand}/organic-images/")
            print(f"  Brands/{brand}/already-posted/")
    print("=" * 60)


if __name__ == "__main__":
    main()
