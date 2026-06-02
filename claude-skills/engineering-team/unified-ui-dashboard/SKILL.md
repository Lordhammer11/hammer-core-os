---
name: unified-ui-dashboard
description: "Launch HaMm3r's Unified Tool Hub — a single interactive HTML dashboard showing all 11 connected MCP tool categories with Google Antigravity physics. Use when: 'show me my tools', 'unified dashboard', 'tool hub', 'open dashboard', 'what tools do I have', 'antigravity UI', 'list all my MCP tools', '/unified-ui'. Writes a self-contained dashboard.html to disk that the user opens in their browser."
---

# HaMm3r's Unified Tool Hub

A self-contained browser dashboard that surfaces all 11 connected MCP tool categories in one place, complete with a Google Antigravity physics engine — press a button and every tool card floats, bounces, and reacts to your cursor.

**This skill is for visual browsing of connected tools.** It is NOT for executing tools (use the MCP tools directly), NOT for configuration (use settings), and NOT for workflow automation (use the relevant domain skill).

---

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Usage](#usage)
- [Delivery Modes](#delivery-modes)
- [Antigravity Physics Engine](#antigravity-physics-engine)
- [Tool Categories Reference](#tool-categories-reference)
- [Search and Navigation](#search-and-navigation)
- [Proactive Triggers](#proactive-triggers)
- [Examples](#examples)
- [Scripts](#scripts)
- [Anti-Patterns](#anti-patterns)
- [Related Skills](#related-skills)

---

## Description

HaMm3r's Unified Tool Hub is a fully self-contained, dark-mode HTML dashboard with zero external dependencies. It provides a single visual interface for all 11 connected MCP tool categories: Gmail, Google Drive, Google Calendar, Zoom, GitHub, Shopify, Adobe Creative Cloud, Canva, DocuSign, Hugging Face, and Ideabrowser.

The dashboard renders 11 tool category cards, each with an icon, subtitle, and capability pills. Clicking any card opens a modal showing all capabilities for that tool with descriptions. A real-time search bar filters all cards simultaneously. Antigravity mode launches every card into a physics simulation with upward gravity, mouse repulsion, and boundary bouncing.

This skill delivers `assets/dashboard.html` — a single HTML file that works in any modern browser without installation.

**Scope:** Visual tool browsing only. The dashboard does not make API calls, does not execute tools, and does not require authentication.

---

## Features

| Feature | Details |
|---------|---------|
| **11 tool category cards** | Gmail, Drive, Calendar, Zoom, GitHub, Shopify, Adobe CC, Canva, DocuSign, Hugging Face, Ideabrowser |
| **Capability pills** | Top 5 action names shown on each card at a glance |
| **Click-to-expand modal** | Full capability list with descriptions for every tool |
| **Real-time search** | Filters cards by tool name, subtitle, action name, or description |
| **Antigravity physics** | Google gravity Easter egg — cards float, bounce, and repel cursor |
| **Keyboard shortcuts** | `Ctrl+G` toggle gravity, `/` focus search, `Esc` close modal/exit gravity |
| **Zero dependencies** | Single HTML file, no CDN, no npm, no build step |
| **Dark mode** | Native dark theme, designed for developer environments |
| **CLI tool** | `dashboard_tool.py` — list categories, validate HTML, export JSON |

---

## Usage

### Invoke from Claude Code

```
/unified-ui
```

Or trigger naturally by asking:
- "show me my tools"
- "what tools do I have connected?"
- "open the tool hub"
- "what can you do?"
- "antigravity dashboard"

### What Claude does

1. Copies `assets/dashboard.html` to `./dashboard.html` in the working directory
2. Tells the user to open `dashboard.html` in their browser
3. Summarizes the 11 tool categories available

### CLI tool

```bash
# List all 11 tool categories with capability counts
python scripts/dashboard_tool.py --list

# Validate dashboard.html structure (checks 7 quality points)
python scripts/dashboard_tool.py --validate

# Export full capability data as JSON
python scripts/dashboard_tool.py --export --json

# Deep-dive on one category
python scripts/dashboard_tool.py --category "Adobe Creative Cloud"
```

---

## Delivery Modes

### Mode 1: Write to disk (Claude Code with file system access)

```bash
# Claude Code copies the HTML asset to the working directory
cp assets/dashboard.html ./dashboard.html
```

Tell the user:
> Open `dashboard.html` in your browser to access HaMm3r's Unified Tool Hub. Press `/` to search, click any card for details, and `Ctrl+G` for Antigravity mode.

### Mode 2: Inline display (chat / web context without file access)

Output the full `assets/dashboard.html` as a fenced HTML code block. The user pastes it into a local file and opens it:

````markdown
```html
<!-- paste full dashboard.html contents here -->
```
````

### Mode 3: Quick reference (text only)

If the user wants a fast text summary without the dashboard, provide the tool table from [Tool Categories Reference](#tool-categories-reference) directly in chat.

---

## Antigravity Physics Engine

The dashboard ships a JavaScript physics engine. Press `⬆ Antigravity` or `Ctrl+G` to activate.

| Control | Action |
|---------|--------|
| `⬆ Antigravity` button | Toggle physics mode on/off |
| `Ctrl+G` | Keyboard shortcut to toggle |
| Mouse cursor | Creates repulsion force within 220px radius |
| Click + drag | Grab a card and throw it |
| `Esc` | Exit gravity mode, restore grid layout |

**Physics parameters (from `references/antigravity-physics.md`):**

| Parameter | Value | Effect |
|-----------|-------|--------|
| Upward gravity `G` | `0.07` | Cards slowly drift upward |
| Velocity damping `DAMP` | `0.996` | Cards gradually slow down |
| Boundary bounce `BNC` | `0.45` | Cards rebound off viewport edges |
| Mouse repulsion radius | `220px` | Cursor pushes cards away |
| Particle count | `80` | Glowing particles stream upward |

Cards snap back to their grid positions when Antigravity is turned off.

---

## Tool Categories Reference

Full capability details in `references/mcp-tool-categories.md`.

| Tool | Subtitle | Key Capabilities |
|------|----------|-----------------|
| **Gmail** | Email & Messaging | search_threads, create_draft, label_message, get_thread, unlabel_thread |
| **Google Drive** | File Storage & Docs | list_recent_files, search_files, create_file, download_file_content, get_file_metadata |
| **Google Calendar** | Scheduling & Events | list_events, create_event, suggest_time, respond_to_event, update_event |
| **Zoom** | Video Meetings | recordings_list, search_meetings, get_meeting_assets, get_file_content, search_zoom |
| **GitHub** | Code & Collaboration | list_pull_requests, list_issues, search_code, push_files, create_branch, create_pull_request |
| **Shopify** | E-Commerce | get_product, list_orders, run_analytics_query, create_product, search_products |
| **Adobe Creative Cloud** | Image & Design | image_remove_background, image_crop_and_resize, image_fill_area, image_vectorize, image_generate |
| **Canva** | Graphic Design | generate_design, search_designs, export_design, list_brand_kits, get_design |
| **DocuSign** | e-Signatures & Contracts | getEnvelopes, createEnvelope, getTemplates, triggerWorkflow, listRecipients |
| **Hugging Face** | AI Models & Research | hub_repo_search, paper_search, space_search, hf_doc_search, hf_whoami |
| **Ideabrowser** | Startup Ideas & Market Research | browse_ideas, list_trends, get_market_insight_detail, list_projects, get_founder_profile |

**Total:** 11 categories, 80+ capabilities surfaced.

---

## Search and Navigation

The search bar at the top of the dashboard filters all 11 cards in real time across:

- Tool category name (e.g., "GitHub")
- Tool subtitle (e.g., "Code & Collaboration")
- Action names (e.g., "create_branch")
- Capability descriptions (e.g., "push files to a repository")

**Keyboard:** Press `/` from anywhere on the page to focus the search bar. Press `Esc` to clear the filter and show all cards.

---

## Proactive Triggers

Surface the dashboard proactively in these situations:

| Trigger | Response |
|---------|----------|
| "what can you do?" or "what tools do you have?" | Offer to open the dashboard for a visual overview of all 11 categories |
| User switches between many tools in one session | Suggest opening the dashboard to browse before deciding |
| First session after onboarding | Mention `/unified-ui` as a way to see all connected tools at a glance |
| User asks about a specific tool's capabilities | Answer the question, then note the full picture is in the dashboard |
| User seems confused about which tool to use for a task | Proactively open the dashboard and point to the right category |

---

## Examples

### Example 1: User asks to see their tools

**User:** What tools do I have connected?

**Claude:**
1. Runs `/unified-ui` to deliver `dashboard.html`
2. Replies: "You have 11 MCP tools connected. Open `dashboard.html` in your browser for the full interactive view — click any card for details, use `/` to search, and `Ctrl+G` for Antigravity mode."
3. Provides the quick text summary table

### Example 2: User wants to find an email capability

**User:** Can I search my emails from here?

**Claude:** Yes — Gmail's `search_threads` supports the full Gmail query syntax (`from:`, `subject:`, `after:`, labels, etc.). You can see all Gmail capabilities in the dashboard under the Gmail card. Want me to open the dashboard or run a search now?

### Example 3: Antigravity demo

**User:** Show me the antigravity thing

**Claude:**
1. Delivers `dashboard.html` to disk
2. Instructs: "Open `dashboard.html` in your browser, then press `Ctrl+G` or click the `⬆ Antigravity` button. Every card launches into physics simulation — move your mouse around to repel them, or click+drag to throw cards."

### Example 4: Exporting tool data as JSON

```bash
python scripts/dashboard_tool.py --export --json > tools.json
```

Output:
```json
{
  "Gmail": {
    "subtitle": "Email & Messaging",
    "icon": "✉️",
    "capabilities": [
      {"name": "search_threads", "desc": "Search email threads with Gmail query syntax"},
      ...
    ]
  },
  ...
}
```

### Example 5: Validating dashboard integrity

```bash
python scripts/dashboard_tool.py --validate
```

Output:
```
Dashboard validation: PASS (7/7 checks)

  ✅ has_antigravity_button
  ✅ has_search_bar
  ✅ has_tool_cards
  ✅ has_physics_engine
  ✅ has_modal
  ✅ no_external_deps
  ✅ dark_mode
```

---

## Scripts

### `scripts/dashboard_tool.py`

CLI tool for dashboard management.

```bash
python scripts/dashboard_tool.py --help
```

```
usage: dashboard_tool.py [-h] [--list] [--validate] [--export] [--category NAME] [--json]

Dashboard Tool — CLI for HaMm3r's Unified Tool Hub

options:
  --list          List all tool categories with capability counts
  --validate      Validate dashboard.html structure (7 checks)
  --export        Export full capability data
  --category NAME Show details for one category
  --json          Output as JSON
```

---

## Anti-Patterns

**Do NOT use this skill to:**

1. **Execute tool calls** — The dashboard is read-only. To send a Gmail draft, use the Gmail MCP tools directly; the dashboard is for browsing what's available.
2. **Configure MCP connections** — The dashboard shows already-connected tools. Adding or configuring MCP servers belongs in your MCP configuration file.
3. **Replace domain-specific skills** — For deep GitHub automation, use a GitHub skill. For Gmail workflows, use the Google Workspace skill. This skill only provides a visual index.
4. **Get full parameter documentation** — Capabilities shown in the dashboard are summarized. For full parameter specs, consult the specific MCP tool documentation or `references/mcp-tool-categories.md`.
5. **Auto-open on every session** — Only deliver the dashboard when the user explicitly asks for it or is clearly looking for a tool overview. Do not open it automatically on session start.

---

## Related Skills

| Skill | Use When |
|-------|----------|
| `google-workspace-cli` | Deep Google Workspace automation (Drive, Gmail, Calendar scripting) — NOT visual browsing |
| `session-start-hook` | Auto-setup actions on session start — NOT for interactive dashboards |
| `mcp-server-builder` | Building new MCP servers to add more connected tools — NOT for viewing existing ones |

---

**Version:** 1.0.0  
**Author:** lordhammer11  
**Category:** Engineering / Developer Tools  
**License:** MIT
