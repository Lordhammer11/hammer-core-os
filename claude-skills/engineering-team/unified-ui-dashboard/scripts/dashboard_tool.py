#!/usr/bin/env python3
"""
Dashboard Tool — CLI for HaMm3r's Unified Tool Hub

Lists MCP tool categories, validates dashboard.html structure,
and exports tool capability data in JSON or human-readable format.

Usage:
    python dashboard_tool.py --list
    python dashboard_tool.py --validate
    python dashboard_tool.py --export --json
    python dashboard_tool.py --category github

Dependencies: Python Standard Library Only
"""

import argparse
import json
import sys
from pathlib import Path

TOOLS = {
    "Gmail": {
        "subtitle": "Email & Messaging",
        "icon": "✉️",
        "capabilities": [
            {"name": "search_threads", "desc": "Search email threads with Gmail query syntax"},
            {"name": "create_draft", "desc": "Create a draft email with recipients and body"},
            {"name": "label_message", "desc": "Apply Gmail label to a specific message"},
            {"name": "get_thread", "desc": "Retrieve full email thread by thread ID"},
            {"name": "unlabel_thread", "desc": "Remove label from an entire thread"},
            {"name": "list_labels", "desc": "List all Gmail labels in the account"},
            {"name": "list_drafts", "desc": "List saved draft emails"},
        ],
    },
    "Google Drive": {
        "subtitle": "File Storage & Docs",
        "icon": "📁",
        "capabilities": [
            {"name": "list_recent_files", "desc": "List recently modified Drive files"},
            {"name": "search_files", "desc": "Search Drive by name, type, or content"},
            {"name": "create_file", "desc": "Create a new file in Google Drive"},
            {"name": "download_file_content", "desc": "Download and read file contents"},
            {"name": "get_file_metadata", "desc": "Retrieve file metadata including permissions"},
            {"name": "get_file_permissions", "desc": "Check who has access to a file"},
            {"name": "read_file_content", "desc": "Read text content of a Drive document"},
        ],
    },
    "Google Calendar": {
        "subtitle": "Scheduling & Events",
        "icon": "📅",
        "capabilities": [
            {"name": "list_events", "desc": "List upcoming events in a date range"},
            {"name": "create_event", "desc": "Create a new calendar event with attendees"},
            {"name": "suggest_time", "desc": "Find available meeting slots for attendees"},
            {"name": "respond_to_event", "desc": "Accept, decline, or tentatively accept an invite"},
            {"name": "update_event", "desc": "Modify event details, time, or attendees"},
            {"name": "delete_event", "desc": "Cancel and remove a calendar event"},
            {"name": "get_event", "desc": "Retrieve full event details by ID"},
        ],
    },
    "Zoom": {
        "subtitle": "Video Meetings",
        "icon": "🎥",
        "capabilities": [
            {"name": "recordings_list", "desc": "List recorded meetings and webinars"},
            {"name": "search_meetings", "desc": "Search for meetings by topic or date"},
            {"name": "get_meeting_assets", "desc": "Retrieve transcript and recording assets"},
            {"name": "get_file_content", "desc": "Download meeting recording or transcript"},
            {"name": "search_zoom", "desc": "Full-text search across Zoom content"},
        ],
    },
    "GitHub": {
        "subtitle": "Code & Collaboration",
        "icon": "🐙",
        "capabilities": [
            {"name": "list_pull_requests", "desc": "List open or closed PRs in a repository"},
            {"name": "list_issues", "desc": "List issues filtered by label or state"},
            {"name": "search_code", "desc": "Search across repositories with code queries"},
            {"name": "push_files", "desc": "Push one or more files to a branch"},
            {"name": "create_branch", "desc": "Create a new branch from a base ref"},
            {"name": "create_pull_request", "desc": "Open a PR between two branches"},
            {"name": "get_file_contents", "desc": "Read file content from any branch"},
        ],
    },
    "Shopify": {
        "subtitle": "E-Commerce",
        "icon": "🛒",
        "capabilities": [
            {"name": "get_product", "desc": "Retrieve product details and variants"},
            {"name": "list_orders", "desc": "List recent orders with filters"},
            {"name": "run_analytics_query", "desc": "Run ShopifyQL analytics queries"},
            {"name": "create_product", "desc": "Add a new product to the store"},
            {"name": "search_products", "desc": "Search products by name or tag"},
            {"name": "list_customers", "desc": "List customers with pagination"},
            {"name": "get_inventory_levels", "desc": "Check stock levels by location"},
        ],
    },
    "Adobe Creative Cloud": {
        "subtitle": "Image & Design",
        "icon": "🎨",
        "capabilities": [
            {"name": "image_remove_background", "desc": "Remove background from any image"},
            {"name": "image_crop_and_resize", "desc": "Crop and resize to specific dimensions"},
            {"name": "image_fill_area", "desc": "Generatively fill a selected region"},
            {"name": "image_vectorize", "desc": "Convert raster image to vector SVG"},
            {"name": "image_generate", "desc": "Generate images with Firefly AI"},
            {"name": "image_generative_expand", "desc": "Expand image canvas with AI fill"},
            {"name": "asset_search", "desc": "Search Creative Cloud asset library"},
        ],
    },
    "Canva": {
        "subtitle": "Graphic Design",
        "icon": "✏️",
        "capabilities": [
            {"name": "generate_design", "desc": "Create a design from a text prompt"},
            {"name": "search_designs", "desc": "Search existing Canva designs"},
            {"name": "export_design", "desc": "Export design as PNG, PDF, or SVG"},
            {"name": "list_brand_kits", "desc": "List available brand kits and colors"},
            {"name": "get_design", "desc": "Retrieve design details and thumbnail"},
            {"name": "copy_design", "desc": "Duplicate an existing design"},
            {"name": "resize_design", "desc": "Resize design to a new format"},
        ],
    },
    "DocuSign": {
        "subtitle": "e-Signatures & Contracts",
        "icon": "📝",
        "capabilities": [
            {"name": "getEnvelopes", "desc": "List signature envelopes by status"},
            {"name": "createEnvelope", "desc": "Send a document for signature"},
            {"name": "getTemplates", "desc": "List available document templates"},
            {"name": "triggerWorkflow", "desc": "Start a DocuSign workflow automation"},
            {"name": "listRecipients", "desc": "List recipients for an envelope"},
            {"name": "getEnvelope", "desc": "Get full envelope details and status"},
            {"name": "sendReminder", "desc": "Send a reminder to pending signers"},
        ],
    },
    "Hugging Face": {
        "subtitle": "AI Models & Research",
        "icon": "🤗",
        "capabilities": [
            {"name": "hub_repo_search", "desc": "Search models, datasets, and spaces"},
            {"name": "paper_search", "desc": "Search arXiv papers linked to HF"},
            {"name": "space_search", "desc": "Find Hugging Face Spaces by topic"},
            {"name": "hf_doc_search", "desc": "Search Hugging Face documentation"},
            {"name": "hf_whoami", "desc": "Get authenticated user profile info"},
            {"name": "hub_repo_details", "desc": "Get detailed repo metadata and files"},
            {"name": "hf_doc_fetch", "desc": "Fetch a specific documentation page"},
        ],
    },
    "Ideabrowser": {
        "subtitle": "Startup Ideas & Market Research",
        "icon": "💡",
        "capabilities": [
            {"name": "browse_ideas", "desc": "Browse curated startup ideas with filters"},
            {"name": "list_trends", "desc": "List trending market categories"},
            {"name": "get_market_insight_detail", "desc": "Deep dive into a market insight"},
            {"name": "list_projects", "desc": "List your saved startup projects"},
            {"name": "get_founder_profile", "desc": "Get founder profile and preferences"},
            {"name": "save_idea", "desc": "Save an idea to your collection"},
            {"name": "start_idea_research", "desc": "Kick off AI research on an idea"},
        ],
    },
}


def cmd_list(args) -> int:
    """List all tool categories."""
    total_caps = sum(len(t["capabilities"]) for t in TOOLS.values())
    if args.json:
        out = {
            "total_categories": len(TOOLS),
            "total_capabilities": total_caps,
            "categories": list(TOOLS.keys()),
        }
        print(json.dumps(out, indent=2))
    else:
        print(f"HaMm3r's Unified Tool Hub — {len(TOOLS)} categories, {total_caps} capabilities\n")
        for name, info in TOOLS.items():
            caps = len(info["capabilities"])
            print(f"  {info['icon']}  {name:<26} {info['subtitle']:<30} ({caps} capabilities)")
    return 0


def cmd_validate(args) -> int:
    """Validate dashboard.html structure."""
    assets_dir = Path(__file__).parent.parent / "assets"
    html_path = assets_dir / "dashboard.html"

    if not html_path.exists():
        msg = f"dashboard.html not found at {html_path}"
        if args.json:
            print(json.dumps({"valid": False, "error": msg}))
        else:
            print(f"FAIL: {msg}")
        return 1

    content = html_path.read_text(encoding="utf-8")
    checks = {
        "has_antigravity_button": "Antigravity" in content,
        "has_search_bar": 'type="text"' in content or "search" in content.lower(),
        "has_tool_cards": content.count("card") >= 11,
        "has_physics_engine": "requestAnimationFrame" in content,
        "has_modal": "modal" in content.lower(),
        "no_external_deps": "cdn.jsdelivr" not in content and "unpkg.com" not in content,
        "dark_mode": "#1a1a2e" in content or "background" in content,
    }
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    valid = passed == total

    if args.json:
        print(json.dumps({"valid": valid, "score": f"{passed}/{total}", "checks": checks}, indent=2))
    else:
        status = "PASS" if valid else "FAIL"
        print(f"Dashboard validation: {status} ({passed}/{total} checks)\n")
        for check, result in checks.items():
            icon = "✅" if result else "❌"
            print(f"  {icon} {check}")
    return 0 if valid else 1


def cmd_export(args) -> int:
    """Export full tool capability data."""
    if args.json:
        print(json.dumps(TOOLS, indent=2))
    else:
        for name, info in TOOLS.items():
            print(f"\n{'='*60}")
            print(f"{info['icon']} {name} — {info['subtitle']}")
            print(f"{'='*60}")
            for cap in info["capabilities"]:
                print(f"  • {cap['name']:<35} {cap['desc']}")
    return 0


def cmd_category(args) -> int:
    """Show details for a single tool category."""
    key = next((k for k in TOOLS if k.lower() == args.category.lower()), None)
    if not key:
        available = ", ".join(TOOLS.keys())
        msg = f"Category '{args.category}' not found. Available: {available}"
        if args.json:
            print(json.dumps({"error": msg}))
        else:
            print(f"Error: {msg}")
        return 1

    info = TOOLS[key]
    if args.json:
        print(json.dumps({key: info}, indent=2))
    else:
        print(f"\n{info['icon']} {key} — {info['subtitle']}\n")
        print(f"{'Capability':<35} Description")
        print("-" * 70)
        for cap in info["capabilities"]:
            print(f"{cap['name']:<35} {cap['desc']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dashboard Tool — CLI for HaMm3r's Unified Tool Hub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dashboard_tool.py --list
  python dashboard_tool.py --list --json
  python dashboard_tool.py --validate
  python dashboard_tool.py --export --json
  python dashboard_tool.py --category github
        """,
    )
    parser.add_argument("--list", action="store_true", help="List all tool categories")
    parser.add_argument("--validate", action="store_true", help="Validate dashboard.html structure")
    parser.add_argument("--export", action="store_true", help="Export full capability data")
    parser.add_argument("--category", metavar="NAME", help="Show details for one category")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.list:
        return cmd_list(args)
    elif args.validate:
        return cmd_validate(args)
    elif args.export:
        return cmd_export(args)
    elif args.category:
        return cmd_category(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
