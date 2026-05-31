# ⚡ HaMm3r Corp OS

> **Personal AI Operating System** — AG Attack LLC  
> Built on Open WebUI · Powered by Claude Skills · Deployed on Railway

![HaMm3r Corp OS](banner.png)

---

## What Is This?

HaMm3r Corp OS is a fully self-hosted AI operating system that combines:

| Component | Source | Description |
|-----------|--------|-------------|
| **HaMm3r Agent OS** | `Lordhammer11/hammer-agent-os` | Open WebUI fork with custom branding, 4 specialist agents, dashboard, cron automations |
| **Claude Skills Suite** | `alirezarezvani/claude-skills` | 235+ production-ready skills across engineering, marketing, C-level advisory, finance, compliance, and more |

Together they form a single deployable package: a branded AI platform with a rich skills library built in.

---

## Stack

- **Frontend**: SvelteKit (Open WebUI fork, HaMm3r branded)
- **Backend**: Python / FastAPI
- **AI Models**: Gemini 2.5 Pro (default), Ollama local, OpenAI-compatible APIs
- **Integrations**: Chroma (RAG), Firecrawl (web), Whisper (STT), Ollama
- **Deploy**: Railway (`Dockerfile.railway`) or Docker Compose

---

## Quick Deploy — Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repo
2. Connect to Railway
3. Railway auto-detects `railway.json` → builds `Dockerfile.railway`
4. Set environment variables (see below)
5. Done — your Corp OS is live

### Required Environment Variables

```
WEBUI_SECRET_KEY=your-secret-key
OPENAI_API_KEY=optional
GEMINI_API_KEY=your-gemini-key
ANTHROPIC_API_KEY=your-anthropic-key
WEBUI_AUTH=False   # disable auth for personal use
```

---

## Local Development

```bash
# Clone
git clone https://github.com/Lordhammer11/hammer-corp-os.git
cd hammer-corp-os

# Install frontend deps
npm ci

# Start backend (Python venv)
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Run
bash run.sh
```

App runs at `http://localhost:3000`

---

## Claude Skills Suite

The `claude-skills/` directory contains 235+ agent skills from `alirezarezvani/claude-skills`:

```
claude-skills/
├── agents/              # 28 specialized agents
├── commands/            # 27 slash commands
├── engineering/         # Fullstack, AI/ML, DevOps, security
├── engineering-team/    # 37 core engineering skills
├── marketing-skill/     # 44 marketing skills
├── c-level-advisor/     # 34 C-level advisory skills
├── finance/             # DCF, SaaS metrics, forecasting
├── compliance-os/       # ISO 13485, MDR, FDA, GDPR
├── product-team/        # RICE, OKRs, UX research
└── ...
```

To use with Claude Code:
```bash
cp -r claude-skills/.claude /path/to/your-project/
```

Or add to your global `~/.claude/` directory.

---

## HaMm3r Agents

Four custom agents built for AG Attack LLC:

| Agent | Role |
|-------|------|
| **Investment Manager** | Portfolio analysis, market research, real estate intel |
| **Vehicle Tech** | Silverado diagnostics, fleet management, maintenance |
| **VA Disability Specialist** | Chapter 31 VR&E navigation, benefits guidance |
| **The Hawk** | Business coaching, federal contracts, growth strategy |

---

## Automated Crons

| Job | Schedule | Purpose |
|-----|----------|---------|
| Dream | 3:00 AM | Overnight knowledge processing |
| Drive | 6:00 AM | Google Drive sync + KB update |
| KB-Index | 7:00 AM | Knowledge base indexing |

---

## Branding

Dark SaaS aesthetic (Vercel/Linear style):
- Canvas: `#09090F`
- Accents: cyan · coral · purple
- Font: Inter
- Icon: The Hammer ⚡

---

## Project Structure

```
hammer-corp-os/
├── backend/             # Python FastAPI backend
├── src/                 # SvelteKit frontend
├── static/              # HaMm3r branding assets
├── claude-skills/       # 235+ Claude agent skills (from alirezarezvani)
├── Dockerfile.railway   # Production deploy (Railway-optimized)
├── docker-compose.yaml  # Local multi-service compose
├── railway.json         # Railway config
└── run.sh               # Local run script
```

---

## Credits

- [Open WebUI](https://github.com/open-webui/open-webui) — base platform
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — skills library
- Built and maintained by **Ronald Majewski / AG Attack LLC**

---

*"The Hammer always falls." — Mr. Hammer*
