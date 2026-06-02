# HaMm3r's Unified Tool Hub

A self-contained browser dashboard that surfaces all 11 connected MCP tool categories in one place, with a Google Antigravity physics engine.

See [SKILL.md](SKILL.md) for full documentation, usage, and workflow examples.

## Quick start

```bash
# List all tool categories
python scripts/dashboard_tool.py --list

# Validate dashboard.html integrity
python scripts/dashboard_tool.py --validate

# Export full capability data as JSON
python scripts/dashboard_tool.py --export --json

# Show details for one category
python scripts/dashboard_tool.py --category github
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Master documentation and Claude workflow instructions |
| `assets/dashboard.html` | Self-contained interactive browser dashboard |
| `scripts/dashboard_tool.py` | CLI for listing, validating, and exporting tool data |
| `references/mcp-tool-categories.md` | Full capability reference for all 11 MCP tools |
| `references/antigravity-physics.md` | Physics engine technical specification |
