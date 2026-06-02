# Jarvis Brain 🧠
> Persistent knowledge index for lordhammer11 — everything built, developed, and imagined.
> Auto-updated by GitHub Actions. Query interactively with `/brain` in Claude Code.

---

## Active Work

| Project | Repo | Status | Tags |
|---------|------|--------|------|
| [Gemma 3 Homebrew Formula — Metal GPU + Chat UI](#gemma3-metal-macos) | homebrew-tap | active | `gemma3` `metal` `macos` `ollama` `ai` |
| [Apex Agent Homebrew Formula](#apex-agent) | homebrew-tap | active | `agent` `homebrew` |
| [Claude Skills Library (235+ skills)](#claude-skills-library) | claude-skills | active | `skills` `claude` `agents` `engineering` `marketing` |
| [Jarvis Brain — persistent knowledge index](#jarvis-brain) | claude-skills | active | `brain` `jarvis` `meta` `knowledge` `index` |
| [HaMm3rOS iOS App](#hammeros-ios-app) | claude-code-together | active | `ios` `swift` `swiftui` `hammeros` `gemma3` |

---

## Detail Entries

### gemma3-metal-macos
**Gemma 3 Homebrew Formula — Metal GPU + Chat UI**
- **Repo:** lordhammer11/homebrew-tap · branch `main` · PR #1
- **Created:** 2026-05-18  **Updated:** 2026-05-29
- **Status:** active
- **Tags:** `gemma3` `metal` `macos` `ollama` `ai` `llm` `homebrew` `ui` `gpu`
- **Summary:** Homebrew formula that installs Google Gemma 3 locally on macOS with Metal GPU acceleration via Ollama. Embeds a Python interactive chat UI with model-size picker, coloured output, slash commands (/help /model /clear /save /quit), readline history, and conversation save-to-file.
- **Files:** `Formula/gemma3.rb`
- **Notes:** HEAD-only formula. Install: brew install --HEAD lordhammer11/tap/gemma3. Metal is auto-enabled on Apple Silicon via Ollama.

---

### apex-agent
**Apex Agent Homebrew Formula**
- **Repo:** lordhammer11/homebrew-tap · branch `main`
- **Created:** 2026-05-18  **Updated:** 2026-05-18
- **Status:** active
- **Tags:** `agent` `homebrew`
- **Summary:** Existing Homebrew formula for Apex Agent in the tap.
- **Files:** `Formula/apex-agent.rb`
- **Notes:** Pre-existing formula — not modified in current sprint.

---

### claude-skills-library
**Claude Skills Library (235+ skills)**
- **Repo:** lordhammer11/claude-skills · branch `main`
- **Created:** 2026-05-18  **Updated:** 2026-05-29
- **Status:** active
- **Tags:** `skills` `claude` `agents` `engineering` `marketing` `finance` `product` `c-level`
- **Summary:** 235+ production-ready skills across 9 domains: engineering, marketing, C-level advisory, product, project management, RA/QM, business growth, finance. Supports Claude Code, Cursor, VS Code/Copilot, Goose, Gemini CLI, Codex, OpenClaw.
- **Files:** `engineering-team/` · `marketing-skill/` · `c-level-advisor/` · `product-team/` · `project-management/` · `ra-qm-team/` · `business-growth/` · `finance/` · `engineering/`
- **Notes:** See INSTALLATION.md for per-agent install commands.

---

### jarvis-brain
**Jarvis Brain — persistent knowledge index**
- **Repo:** lordhammer11/claude-skills · branch `dev`
- **Created:** 2026-05-18  **Updated:** 2026-05-29
- **Status:** active
- **Tags:** `brain` `jarvis` `meta` `knowledge` `index` `automation`
- **Summary:** Central knowledge brain tracking all work, ideas, and creations across every repo. Includes index.json, per-entry files, BRAIN.md human-readable dashboard, /brain Claude Code slash command, brain_update.py script, and GitHub Actions daily sync workflow.
- **Files:** `brain/index.json` · `brain/entries/` · `BRAIN.md` · `.claude/commands/brain.md` · `scripts/brain_update.py` · `.github/workflows/brain-sync.yml`
- **Notes:** Query with /brain in Claude Code. Auto-syncs daily via GitHub Actions.

---

### hammeros-ios-app
**HaMm3rOS iOS App**
- **Repo:** lordhammer11/claude-code-together · branch `dev` · PR #2
- **Created:** 2026-05-29  **Updated:** 2026-05-29
- **Status:** active
- **Tags:** `ios` `swift` `swiftui` `hammeros` `gemma3` `ollama` `brain` `mobile`
- **Summary:** SwiftUI iOS app (iPhone + iPad, iOS 16+) serving as the HaMm3rOS mobile command centre. 5 tabs: Dashboard, Brain (searchable Jarvis Brain entries), Gemma (local AI chat via Ollama), Ideas, Settings. Full context persistence: chat history survives kill/relaunch, brain cached offline with 1h TTL, tab state via @SceneStorage.
- **Files:** `Sources/` · `Package.swift` · `README.md`
- **Notes:** Open HaMm3rOS.swiftpm in Swift Playgrounds on iPhone or iPad — signs automatically with your Apple ID. Set Ollama host to your Mac's local IP in Settings for Gemma chat.

---

## Ideas (Backlog)

| Idea | Tags | Description |
|------|------|-------------|
| Native macOS SwiftUI app for Gemma 3 | `macos` `swift` `ui` `gemma3` | A native macOS SwiftUI wrapper around the gemma3 CLI for a polished app-store-style experience. |
| Web dashboard for the Jarvis brain | `web` `brain` `dashboard` `visualization` | A GitHub Pages site that renders brain/index.json as a visual knowledge map — timeline, tag cloud, repo graph. |

---

## Stats

| Metric | Count |
|--------|-------|
| Total entries | 5 |
| Active | 5 |
| Draft/Open PR | 0 |
| Ideas backlog | 2 |
| Repos tracked | 4 |

---

*Last updated: 2026-06-02 · Auto-synced by `.github/workflows/brain-sync.yml`*
