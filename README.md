# 🔨 HaMm3r Core OS

**Personal AI Operating System** — powered by Gemini, Claude & Ollama

Built on [Open WebUI](https://github.com/open-webui/open-webui) with full HaMm3r branding, autonomous agents, knowledge base integration, and multi-device access via Tailscale.

---

## What's Inside

| Layer | Technology |
|---|---|
| **UI Base** | Open WebUI (SvelteKit + Python) |
| **AI Providers** | Gemini 2.5 Pro · Claude · Ollama (local) |
| **Skills Library** | 330+ Claude Code skills (see `claude-skills/`) |
| **Knowledge Base** | Chroma vector DB + Obsidian vault viewer |
| **Web Research** | Firecrawl v2 + SearXNG |
| **Access** | Tailscale private network (Mac · iPhone · PC) |
| **Always-on** | macOS LaunchAgent (no Docker needed) |

---

## Custom Agents

1. **Investment Manager** — portfolio strategy, market analysis
2. **Vehicle Tech** — 2018 Chevy Silverado 5.3L diagnostics
3. **VA Disability Specialist** — VR&E Chapter 31 guidance
4. **The Hawk** — AG Attack LLC business coach
5. **HaMm3r's Utility Tool** — task automation, research, productivity

---

## Setup

```bash
# 1. Clone
git clone https://github.com/Lordhammer11/hammer-core-os.git
cd hammer-core-os

# 2. Create venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install uv -q
uv pip install -e ".[hf,code]"

# 3. Configure
cp .env.example .env
# Edit .env — add your Gemini API key at minimum

# 4. Build frontend
npm install && npm run build

# 5. Launch
cd backend
PYTHONPATH=$(pwd) python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 3000
```

---

## Multi-Device Access (Tailscale)

HaMm3r Core OS runs on your Mac and is accessible from all devices via Tailscale:

```
http://<your-mac-tailscale-ip>:3000
```

Run `tailscale ip -4` on your Mac to get the IP.

**Devices:** Mac (server) · iPhone (PWA) · MacBook · Windows PC

---

## Always-On (LaunchAgent)

Copy plists from `launchagents/` to `~/Library/LaunchAgents/` and load:

```bash
cp launchagents/com.hammer.agentOS.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.hammer.agentOS.plist
```

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/dream-review.py` | Nightly agent usage analysis → Obsidian |
| `scripts/drive-sync.py` | Google Drive ↔ HaMm3r-KB sync |
| `scripts/index-kb.py` | Index ~/HaMm3r-KB into Chroma vector DB |
| `scripts/import_hammer_agents.py` | Import all 5 agents into Open WebUI |

---

## Skills Library

`claude-skills/` — 330+ skills for Claude Code, Codex, Gemini CLI, Cursor and more.
Covers: engineering, marketing, finance, C-level advisory, compliance, research, productivity.

---

## Homebrew Tools

`homebrew-tap/` — Homebrew formulas for Apex agent tools.

---

## Key Patches (vs upstream Open WebUI)

- **WEBUI_AUTH=False bypass** — 4-file patch for auth-free single-user mode
- **HaMm3r branding** — custom CSS design system, glassmorphism cards, cyan palette
- **Touch ID / WebAuthn** — biometric login support
- **Dashboard** — 3-pane layout (chat · KB · analytics)
- **Agent Builder** — custom agent creation UI

---

*Built for AG Attack LLC · Ronald Majewski · HaMm3r Corp*
