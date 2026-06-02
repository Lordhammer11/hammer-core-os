#!/usr/bin/env python3
"""
HaMm3r OS — Dream Review Automation
Runs nightly, analyzes agent usage patterns, writes optimization notes to Obsidian vault.
"""

import json
import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path

VAULT = Path.home() / "HaMm3r-KB" / "Dream-Review"
DB = Path.home() / "open-webui" / "data" / "webui.db"
VAULT.mkdir(parents=True, exist_ok=True)

def get_recent_chats():
    """Pull last 24h of chats from Open WebUI SQLite DB."""
    try:
        conn = sqlite3.connect(DB)
        cutoff = int((datetime.now() - timedelta(hours=24)).timestamp())
        rows = conn.execute(
            "SELECT id, title, created_at, updated_at FROM chat WHERE created_at > ? ORDER BY created_at DESC",
            (cutoff,)
        ).fetchall()
        conn.close()
        return rows
    except Exception as e:
        return []

def get_model_usage():
    """Count model usage from recent chats."""
    try:
        conn = sqlite3.connect(DB)
        cutoff = int((datetime.now() - timedelta(hours=24)).timestamp())
        rows = conn.execute(
            "SELECT chat FROM chat WHERE created_at > ?", (cutoff,)
        ).fetchall()
        conn.close()

        model_counts = {}
        for (chat_json,) in rows:
            try:
                data = json.loads(chat_json)
                messages = data.get("messages", []) if isinstance(data, dict) else []
                for msg in messages:
                    model = msg.get("model", "")
                    if model:
                        model_counts[model] = model_counts.get(model, 0) + 1
            except:
                pass
        return model_counts
    except:
        return {}

def write_dream_review():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M %p")

    chats = get_recent_chats()
    model_usage = get_model_usage()

    # Build report
    lines = [
        f"# 🌙 Dream Review — {date_str}",
        f"*Generated at {time_str} by HaMm3r OS automation*",
        "",
        "## 📊 Session Summary",
        f"- **Total chats (24h):** {len(chats)}",
        f"- **Active agents:** {len(set(c[1] for c in chats if c[1]))}",
        "",
        "## 🤖 Model Usage",
    ]

    if model_usage:
        total = sum(model_usage.values())
        for model, count in sorted(model_usage.items(), key=lambda x: -x[1]):
            pct = int((count / total) * 100)
            lines.append(f"- **{model}:** {count} messages ({pct}%)")
    else:
        lines.append("- No model usage data for this period")

    lines += [
        "",
        "## 💡 Optimization Suggestions",
    ]

    # Generate smart suggestions based on data
    suggestions = []

    if len(chats) == 0:
        suggestions.append("No activity today — consider scheduling a morning check-in with your Investment Manager agent")
    elif len(chats) > 10:
        suggestions.append("High activity day — consider reviewing your most-used agent prompts for refinement")

    if model_usage:
        top_model = max(model_usage, key=model_usage.get)
        if "llama" in top_model.lower():
            suggestions.append(f"Heavy local model usage ({top_model}) — for complex tasks consider routing to Claude 3.5 Sonnet")
        if "claude" in top_model.lower():
            suggestions.append(f"Claude is your primary model — ensure your Anthropic API usage stays within budget")

    suggestions += [
        "Review VA Disability Specialist agent for any new 38 CFR regulation updates",
        "Check if The Hawk agent needs updated SBA grant information for current fiscal year",
        "Consider adding new Ollama models: `ollama pull deepseek-r1` for reasoning tasks",
    ]

    for s in suggestions[:5]:
        lines.append(f"- {s}")

    lines += [
        "",
        "## 📋 Recent Chat Titles",
    ]

    for chat in chats[:8]:
        title = chat[1] or "Untitled"
        ts = datetime.fromtimestamp(chat[2]).strftime("%H:%M") if chat[2] else "?"
        lines.append(f"- `{ts}` {title}")

    if not chats:
        lines.append("- No chats recorded today")

    lines += [
        "",
        "---",
        f"*Next Dream Review scheduled for tomorrow at 3:00 AM*",
        f"*HaMm3r OS v1.0 — Built for Mr. Hammer*",
    ]

    report = "\n".join(lines)

    # Write dated report
    report_path = VAULT / f"Dream-Review-{date_str}.md"
    with open(report_path, "w") as f:
        f.write(report)

    # Also overwrite the "Latest" file for the dashboard
    latest_path = VAULT / "Latest.md"
    with open(latest_path, "w") as f:
        f.write(report)

    print(f"✅ Dream Review written: {report_path}")
    return report_path

if __name__ == "__main__":
    path = write_dream_review()
    print(f"Report: {path}")
