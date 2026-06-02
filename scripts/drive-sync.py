#!/opt/homebrew/bin/python3
"""
HaMm3r OS — Google Drive Sync (v2)
Syncs key HaMm3r-KB files → Google Drive AND pulls Drive docs → local KB
Uses Hermes Google OAuth token (no gws CLI needed)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Use homebrew python3 for google API support (system python3 is 3.9)
PYTHON = "/opt/homebrew/bin/python3"
GAPI = f"{PYTHON} /Users/ronaldmajewski/.hermes/skills/productivity/google-workspace/scripts/google_api.py"

KB = Path.home() / "HaMm3r-KB"
DRIVE_SYNC_DIR = KB / "Resources" / "Drive-Sync"
DRIVE_SYNC_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = KB / "Analytics"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG = LOG_DIR / "drive-sync.log"

HAMMER_DRIVE_FOLDER = "HaMm3r-KB"  # Name of folder to sync to on Drive


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    with open(LOG, "a") as f:
        f.write(entry + "\n")


def run_gapi(args: str) -> dict | list | None:
    """Run a google_api.py command and return parsed JSON."""
    cmd = f"{GAPI} {args}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        log(f"GAPI timeout (120s): {args[:80]}")
        return None
    if result.returncode != 0:
        log(f"GAPI error: {result.stderr.strip()[:200]}")
        return None
    try:
        # Strip warnings from stderr, parse stdout
        out = result.stdout.strip()
        if out:
            return json.loads(out)
    except json.JSONDecodeError as e:
        log(f"JSON parse error: {e} — output: {result.stdout[:100]}")
    return None


def is_file_readable(path: Path) -> bool:
    """Verify file is fully readable (catches iCloud deadlock stubs)."""
    try:
        import subprocess as sp
        r = sp.run(["cat", str(path)], capture_output=True, timeout=10)
        return r.returncode == 0 and len(r.stdout) > 0
    except Exception as e:
        log(f"  ⚠ Readability check failed for {path.name}: {e}")
        return False


def get_or_create_folder(folder_name: str, parent_id: str = None) -> str | None:
    """Find or create a Google Drive folder, return its ID."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = run_gapi(f"drive search \"{query}\" --raw-query --max 5")
    if results:
        log(f"Found existing Drive folder: {folder_name} (id: {results[0]['id']})")
        return results[0]["id"]

    # Create it
    parent_arg = f"--parent {parent_id}" if parent_id else ""
    result = run_gapi(f"drive create-folder \"{folder_name}\" {parent_arg}")
    if result and result.get("id"):
        log(f"Created Drive folder: {folder_name} (id: {result['id']})")
        return result["id"]
    return None


def upload_file_to_drive(local_path: Path, folder_id: str) -> bool:
    """Upload a local file to Google Drive."""
    if not is_file_readable(local_path):
        log(f"  ⚠ Skipped (unreadable/iCloud stub): {local_path.name}")
        return False
    try:
        result = run_gapi(f"drive upload \"{local_path}\" --parent {folder_id}")
    except OSError as e:
        log(f"  ✗ OSError uploading {local_path.name}: {e}")
        return False
    if result and result.get("status") == "uploaded":
        log(f"  ✓ Uploaded: {local_path.name}")
        return True
    log(f"  ✗ Failed: {local_path.name}")
    return False


def sync_kb_to_drive():
    """Upload key HaMm3r-KB folders to Google Drive."""
    log("--- Syncing local KB → Google Drive ---")

    # Get/create root HaMm3r-KB folder on Drive
    root_id = get_or_create_folder(HAMMER_DRIVE_FOLDER)
    if not root_id:
        log("ERROR: Could not get/create HaMm3r-KB folder on Drive")
        return 0

    uploaded = 0

    # Sync: Dream-Review logs
    dream_folder_id = get_or_create_folder("Dream-Review", root_id)
    if dream_folder_id:
        dream_dir = KB / "Dream-Review"
        for f in sorted(dream_dir.glob("*.md"))[-7:]:  # Last 7 dream review files
            if upload_file_to_drive(f, dream_folder_id):
                uploaded += 1

    # Sync: Agent definitions
    agents_folder_id = get_or_create_folder("Agents", root_id)
    if agents_folder_id:
        agents_dir = KB / "Agents"
        for f in agents_dir.glob("*.md"):
            if upload_file_to_drive(f, agents_folder_id):
                uploaded += 1

    # Sync: Memory files
    memory_folder_id = get_or_create_folder("Memory", root_id)
    if memory_folder_id:
        for f in [
            Path.home() / ".hermes" / "memory.md",
            Path.home() / ".hermes" / "user.md",
        ]:
            if f.exists() and upload_file_to_drive(f, memory_folder_id):
                uploaded += 1

    log(f"KB → Drive sync complete: {uploaded} files uploaded")
    return uploaded


def pull_drive_docs():
    """Pull recent Drive docs into local KB for reference."""
    log("--- Pulling Drive docs → local KB ---")

    # Search for recently modified files (last 7 days)
    results = run_gapi("drive search \"modifiedTime > '2026-01-01'\" --raw-query --max 20")
    if not results:
        log("No Drive files found or error")
        return 0

    pulled = 0
    for item in results:
        name = item.get("name", "")
        file_id = item.get("id", "")
        mime = item.get("mimeType", "")

        # Only pull docs/sheets/text (skip binaries)
        pullable = [
            "application/vnd.google-apps.document",
            "application/vnd.google-apps.spreadsheet",
            "text/plain",
            "text/markdown",
        ]
        if mime not in pullable:
            continue

        out_path = DRIVE_SYNC_DIR / f"{file_id[:8]}_{name}"
        if out_path.exists():
            continue  # Already have it

        result = run_gapi(f"drive download {file_id} --output \"{out_path}\"")
        if result and result.get("status") == "downloaded":
            log(f"  ✓ Pulled: {name}")
            pulled += 1

    log(f"Drive → KB pull complete: {pulled} new files")
    return pulled


def write_sync_status(uploaded: int, pulled: int):
    """Write sync status to README."""
    status_path = DRIVE_SYNC_DIR / "README.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_path.write_text(f"""# Google Drive Sync — HaMm3r OS

## Status: ✅ ACTIVE

**Last sync:** {ts}
**Files uploaded to Drive:** {uploaded}
**Files pulled from Drive:** {pulled}

## Drive Folder
- `HaMm3r-KB/` → Dream-Review, Agents, Memory

## Local KB Location
`~/HaMm3r-KB/Resources/Drive-Sync/`

## Schedule
Daily at 6am via HaMm3r cron job
""")


if __name__ == "__main__":
    log("=" * 50)
    log("=== HaMm3r Drive Sync v2 Started ===")

    uploaded = 0
    pulled = 0
    try:
        uploaded = sync_kb_to_drive()
        pulled = pull_drive_docs()
        write_sync_status(uploaded, pulled)
        log("=== Drive Sync Complete ===")
        print(f"\n🔨 HaMm3r Drive Sync Complete — {uploaded} uploaded, {pulled} pulled from Drive")
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        print(f"❌ Drive Sync Fatal Error: {e}")
        sys.exit(1)
