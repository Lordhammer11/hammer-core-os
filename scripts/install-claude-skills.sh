#!/usr/bin/env bash
# hammer-corp-os/scripts/install-claude-skills.sh
# Installs the bundled claude-skills into a target project's .claude directory
# Usage: bash scripts/install-claude-skills.sh [target-dir]

set -e

TARGET="${1:-$HOME}"
SKILLS_SRC="$(cd "$(dirname "$0")/.." && pwd)/claude-skills"
DEST="$TARGET/.claude"

if [ ! -d "$SKILLS_SRC" ]; then
  echo "ERROR: claude-skills directory not found at $SKILLS_SRC"
  exit 1
fi

echo "Installing Claude Skills Suite to $DEST"
mkdir -p "$DEST"

# Copy agents, commands, and skill directories
for dir in agents commands engineering engineering-team marketing-skill c-level-advisor finance compliance-os product-team project-management ra-qm-team business-growth research orchestration; do
  if [ -d "$SKILLS_SRC/$dir" ]; then
    cp -r "$SKILLS_SRC/$dir" "$DEST/"
    echo "  ✓ $dir"
  fi
done

# Copy top-level CLAUDE.md as reference
if [ -f "$SKILLS_SRC/CLAUDE.md" ]; then
  cp "$SKILLS_SRC/CLAUDE.md" "$DEST/CLAUDE-skills-reference.md"
  echo "  ✓ CLAUDE-skills-reference.md"
fi

echo ""
echo "Done. $DEST is ready for Claude Code."
echo "Run: claude  (from any project directory)"
