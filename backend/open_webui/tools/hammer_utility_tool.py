"""
HaMm3r's Agent Utility Tool
============================
Open WebUI Tool — renders the full HaMm3r OS command panel as a rich HTML artifact.

Inspired by OpenJarvis AgentsPanel design (Catppuccin Mocha palette + HaMm3r branding).

Usage in chat: type /hammer or ask "show me the HaMm3r utility panel"
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Tool metadata (Open WebUI reads this)
# ---------------------------------------------------------------------------


class Tools:
    def __init__(self):
        self.name = "HaMm3r's Agent Utility Tool"
        self.description = (
            'Renders the full HaMm3r OS command panel: agent status, connectors, skills, and Dream Review.'
        )

    # -----------------------------------------------------------------------
    # Main entry point
    # -----------------------------------------------------------------------

    def render_utility_panel(self, __user__: dict = {}) -> str:
        """
        Render the HaMm3r OS Agent Utility Panel.
        Returns an HTML artifact showing all agents, connectors, skills, and Dream Review.
        """
        agents = self._load_agents()
        dream_review = self._load_dream_review()
        connectors = self._get_connectors()
        skills = self._get_skills()
        html = self._build_html(agents, connectors, skills, dream_review)
        return html

    # -----------------------------------------------------------------------
    # Data loaders
    # -----------------------------------------------------------------------

    def _load_agents(self) -> list:
        """Load agent definitions from HaMm3r-KB."""
        agents_dir = Path.home() / 'iCloudDrive' / 'HaMm3r-KB' / 'Agents'
        agents = []

        defaults = [
            {
                'name': 'VA Disability Specialist',
                'emoji': '🎖️',
                'role': 'AI Veterans Service Officer (VSO) & VR&E Counselor',
                'model': 'claude-sonnet-4',
                'tags': ['veterans', 'VA', 'disability', 'VRE'],
                'status': 'idle',
                'color': '#a6e3a1',
            },
            {
                'name': 'The Hawk — Business Coach',
                'emoji': '🦅',
                'role': 'Veteran entrepreneur coach — VR&E, transport, federal contracts',
                'model': 'claude-sonnet-4',
                'tags': ['business', 'grants', 'transport', 'VRE'],
                'status': 'idle',
                'color': '#fab387',
            },
            {
                'name': 'Investment Manager',
                'emoji': '💰',
                'role': 'Financial advisor, tax strategist & wealth protection specialist',
                'model': 'claude-sonnet-4',
                'tags': ['finance', 'real-estate', 'tax', 'wealth'],
                'status': 'idle',
                'color': '#f9e2af',
            },
            {
                'name': 'Vehicle Tech',
                'emoji': '🚗',
                'role': 'Vehicle diagnostics, maintenance & performance — 2018 Silverado 1500',
                'model': 'claude-sonnet-4',
                'tags': ['vehicles', 'diagnostics', 'silverado'],
                'status': 'idle',
                'color': '#89b4fa',
            },
        ]

        if agents_dir.exists():
            for md_file in sorted(agents_dir.glob('*.md')):
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                # Try to match with defaults by name keyword
                for d in defaults:
                    keyword = d['name'].split('—')[0].strip().split(' ')[0].lower()
                    if keyword in md_file.stem.lower():
                        d['loaded'] = True
                        break

        return defaults

    def _load_dream_review(self) -> dict:
        """Load the latest Dream Review from iCloud."""
        dr_dir = Path.home() / 'iCloudDrive' / 'HaMm3r-KB' / 'Dream-Review'
        latest = dr_dir / 'Latest.md'

        if latest.exists():
            content = latest.read_text(encoding='utf-8', errors='ignore')
            lines = content.strip().splitlines()
            # Parse basic stats
            total_chats = 0
            active_agents = 0
            chat_titles = []
            suggestions = []
            in_chats = False
            in_suggestions = False

            for line in lines:
                if 'Total chats' in line:
                    try:
                        total_chats = int(line.split(':')[-1].strip())
                    except Exception:
                        pass
                elif 'Active agents' in line:
                    try:
                        active_agents = int(line.split(':')[-1].strip())
                    except Exception:
                        pass
                elif '## 📋 Recent Chat Titles' in line:
                    in_chats = True
                    in_suggestions = False
                elif '## 💡 Optimization Suggestions' in line:
                    in_suggestions = True
                    in_chats = False
                elif '## ' in line:
                    in_chats = False
                    in_suggestions = False
                elif in_chats and line.startswith('- '):
                    chat_titles.append(line[2:].strip())
                elif in_suggestions and line.startswith('- '):
                    suggestions.append(line[2:].strip())

            # Get date from filename or header
            date_str = 'Today'
            for line in lines[:3]:
                if 'Dream Review —' in line:
                    date_str = line.split('—')[-1].strip().replace('#', '').strip()
                    break

            return {
                'date': date_str,
                'total_chats': total_chats,
                'active_agents': active_agents,
                'chat_titles': chat_titles[:5],
                'suggestions': suggestions[:3],
                'content': content[:800],
            }

        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_chats': 0,
            'active_agents': 0,
            'chat_titles': [],
            'suggestions': ['No dream review found yet — runs nightly at 3:00 AM'],
        }

    def _get_connectors(self) -> list:
        """Return connector status for all configured sources."""
        icloud_path = Path.home() / 'iCloudDrive' / 'HaMm3r-KB'
        gdrive_path = Path('g:/My Drive/HaMm3r-KB') if os.name == 'nt' else Path('/g/My Drive/HaMm3r-KB')

        connectors = [
            {
                'id': 'icloud',
                'name': 'iCloud Drive',
                'icon': '☁️',
                'status': 'connected' if icloud_path.exists() else 'disconnected',
                'detail': 'HaMm3r-KB synced',
                'color': '#89b4fa',
            },
            {
                'id': 'gdrive',
                'name': 'Google Drive',
                'icon': '📁',
                'status': 'connected' if gdrive_path.exists() else 'disconnected',
                'detail': 'HaMm3r-KB backup',
                'color': '#a6e3a1',
            },
            {
                'id': 'openai',
                'name': 'OpenAI',
                'icon': '⚡',
                'status': 'connected',
                'detail': 'GPT-4o, o3',
                'color': '#f9e2af',
            },
            {
                'id': 'anthropic',
                'name': 'Anthropic',
                'icon': '🧠',
                'status': 'connected',
                'detail': 'Claude Opus 4, Sonnet 4',
                'color': '#cba6f7',
            },
            {
                'id': 'openrouter',
                'name': 'OpenRouter',
                'icon': '🔀',
                'status': 'connected',
                'detail': '100+ models',
                'color': '#fab387',
            },
            {
                'id': 'telegram',
                'name': 'Telegram',
                'icon': '📱',
                'status': 'connected',
                'detail': 'Hermes gateway active',
                'color': '#89dceb',
            },
        ]
        return connectors

    def _get_skills(self) -> list:
        """Return HaMm3r OS active skills."""
        return [
            {'name': 'Dream Review', 'icon': '🌙', 'desc': 'Nightly 3AM OS analysis', 'active': True},
            {'name': 'Drive Sync', 'icon': '🔄', 'desc': 'Daily 6AM KB sync', 'active': True},
            {'name': 'Source Code Context', 'icon': '📦', 'desc': 'repomix repo fetcher', 'active': True},
            {'name': 'Code Structure Cleanup', 'icon': '🧹', 'desc': 'Service layer refactor', 'active': True},
            {'name': 'GrepLoop Review', 'icon': '🔁', 'desc': 'Automated PR review loop', 'active': True},
            {'name': 'Agentic Engineering', 'icon': '⚙️', 'desc': "Mickey's full workflow", 'active': True},
        ]

    # -----------------------------------------------------------------------
    # HTML builder
    # -----------------------------------------------------------------------

    def _build_html(self, agents: list, connectors: list, skills: list, dream_review: dict) -> str:
        """Build the full HaMm3r Utility Panel HTML."""

        now = datetime.now().strftime('%Y-%m-%d %H:%M')

        # Agent cards HTML
        agent_cards = ''
        for a in agents:
            tags_html = ''.join(f'<span class="tag">{t}</span>' for t in a['tags'])
            agent_cards += f"""
            <div class="agent-card">
                <div class="agent-header">
                    <span class="agent-emoji">{a['emoji']}</span>
                    <div class="agent-info">
                        <div class="agent-name">{a['name']}</div>
                        <div class="agent-model">{a['model']}</div>
                    </div>
                    <div class="status-dot" style="background:{a['color']};" title="{a['status']}"></div>
                </div>
                <div class="agent-role">{a['role']}</div>
                <div class="tags">{tags_html}</div>
                <div class="agent-actions">
                    <button class="btn-primary">💬 Chat</button>
                    <button class="btn-ghost">⚙️ Configure</button>
                </div>
            </div>"""

        # Connector rows HTML
        connector_rows = ''
        for c in connectors:
            status_class = 'status-connected' if c['status'] == 'connected' else 'status-disconnected'
            status_label = '● Connected' if c['status'] == 'connected' else '○ Disconnected'
            connector_rows += f"""
            <div class="connector-row">
                <span class="connector-icon">{c['icon']}</span>
                <div class="connector-info">
                    <div class="connector-name">{c['name']}</div>
                    <div class="connector-detail">{c['detail']}</div>
                </div>
                <span class="{status_class}">{status_label}</span>
            </div>"""

        # Skills HTML
        skills_html = ''
        for s in skills:
            active_class = 'skill-active' if s['active'] else 'skill-inactive'
            skills_html += f"""
            <div class="skill-item {active_class}">
                <span>{s['icon']}</span>
                <div>
                    <div class="skill-name">{s['name']}</div>
                    <div class="skill-desc">{s['desc']}</div>
                </div>
                <span class="skill-badge">{'ON' if s['active'] else 'OFF'}</span>
            </div>"""

        # Dream review HTML
        chat_list = ''
        for t in dream_review.get('chat_titles', []):
            chat_list += f'<div class="dr-chat">· {t}</div>'
        if not chat_list:
            chat_list = '<div class="dr-chat muted">No chats recorded</div>'

        suggestions_html = ''
        for s in dream_review.get('suggestions', []):
            suggestions_html += f'<div class="dr-suggestion">💡 {s}</div>'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HaMm3r OS — Agent Utility Tool</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg: #0a0a0b;
    --bg2: #121214;
    --bg3: #18181b;
    --surface: #1e1e2e;
    --surface2: #313244;
    --border: rgba(255,255,255,0.09);
    --text: #cdd6f4;
    --subtext: #a6adc8;
    --muted: #6c7086;
    --accent: #89b4fa;
    --green: #a6e3a1;
    --red: #f38ba8;
    --peach: #fab387;
    --yellow: #f9e2af;
    --purple: #cba6f7;
    --hammer: #f59e0b;
    --font: 'Space Grotesk', system-ui, sans-serif;
    --mono: 'IBM Plex Mono', monospace;
  }}

  body {{
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    min-height: 100vh;
    padding: 0;
  }}

  /* ── Header ── */
  .header {{
    background: linear-gradient(135deg, #0a0a0b 0%, #18181b 50%, #0a0a0b 100%);
    border-bottom: 1px solid var(--border);
    padding: 20px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .header-brand {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .hammer-logo {{
    font-size: 36px;
    filter: drop-shadow(0 0 12px rgba(245,158,11,0.6));
    animation: pulse-glow 3s ease-in-out infinite;
  }}
  @keyframes pulse-glow {{
    0%, 100% {{ filter: drop-shadow(0 0 8px rgba(245,158,11,0.4)); }}
    50% {{ filter: drop-shadow(0 0 20px rgba(245,158,11,0.8)); }}
  }}
  .header-title {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
    background: linear-gradient(135deg, #f59e0b, #fbbf24, #89b4fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .header-sub {{
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    margin-top: 2px;
    letter-spacing: 0.05em;
  }}
  .header-right {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .clock {{
    font-family: var(--mono);
    font-size: 13px;
    color: var(--subtext);
  }}
  .os-badge {{
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.3);
    color: var(--hammer);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
  }}

  /* ── Layout ── */
  .layout {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 20px;
    padding: 24px 32px;
    max-width: 1400px;
    margin: 0 auto;
  }}

  /* ── Section ── */
  .section {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
  }}
  .section-header {{
    padding: 16px 20px 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .section-title {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--subtext);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .section-count {{
    background: var(--surface2);
    color: var(--accent);
    font-family: var(--mono);
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
  }}
  .section-body {{
    padding: 16px 20px;
  }}

  /* ── Agent Cards ── */
  .agents-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding: 16px 20px;
  }}
  .agent-card {{
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    transition: border-color 0.2s, transform 0.15s;
  }}
  .agent-card:hover {{
    border-color: rgba(137,180,250,0.3);
    transform: translateY(-1px);
  }}
  .agent-header {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 8px;
  }}
  .agent-emoji {{ font-size: 22px; flex-shrink: 0; margin-top: 1px; }}
  .agent-info {{ flex: 1; min-width: 0; }}
  .agent-name {{
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.2;
  }}
  .agent-model {{
    font-family: var(--mono);
    font-size: 10px;
    color: var(--muted);
    margin-top: 2px;
  }}
  .status-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 4px;
    box-shadow: 0 0 6px currentColor;
  }}
  .agent-role {{
    font-size: 11px;
    color: var(--subtext);
    line-height: 1.4;
    margin-bottom: 8px;
  }}
  .tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 10px;
  }}
  .tag {{
    background: var(--surface2);
    color: var(--muted);
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 8px;
    font-family: var(--mono);
  }}
  .agent-actions {{
    display: flex;
    gap: 6px;
  }}
  .btn-primary {{
    flex: 1;
    background: rgba(137,180,250,0.15);
    border: 1px solid rgba(137,180,250,0.3);
    color: var(--accent);
    padding: 5px 10px;
    border-radius: 7px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    font-family: var(--font);
  }}
  .btn-primary:hover {{ background: rgba(137,180,250,0.25); }}
  .btn-ghost {{
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--subtext);
    padding: 5px 8px;
    border-radius: 7px;
    font-size: 11px;
    cursor: pointer;
    transition: background 0.2s;
    font-family: var(--font);
  }}
  .btn-ghost:hover {{ background: #414559; color: var(--text); }}

  /* ── Connectors ── */
  .connector-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
  }}
  .connector-row:last-child {{ border-bottom: none; }}
  .connector-icon {{ font-size: 18px; flex-shrink: 0; }}
  .connector-info {{ flex: 1; }}
  .connector-name {{ font-size: 13px; font-weight: 600; }}
  .connector-detail {{ font-size: 11px; color: var(--muted); margin-top: 1px; }}
  .status-connected {{
    font-size: 11px;
    font-family: var(--mono);
    color: var(--green);
    flex-shrink: 0;
  }}
  .status-disconnected {{
    font-size: 11px;
    font-family: var(--mono);
    color: var(--red);
    flex-shrink: 0;
  }}

  /* ── Skills ── */
  .skill-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
  }}
  .skill-item:last-child {{ border-bottom: none; }}
  .skill-item.skill-inactive {{ opacity: 0.4; }}
  .skill-info {{ flex: 1; }}
  .skill-name {{ font-size: 13px; font-weight: 600; }}
  .skill-desc {{ font-size: 11px; color: var(--muted); margin-top: 1px; }}
  .skill-badge {{
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(166,227,161,0.15);
    color: var(--green);
    letter-spacing: 0.05em;
    flex-shrink: 0;
  }}
  .skill-item.skill-inactive .skill-badge {{
    background: var(--surface2);
    color: var(--muted);
  }}

  /* ── Dream Review ── */
  .dr-stats {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }}
  .dr-stat {{
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    text-align: center;
  }}
  .dr-stat-value {{
    font-family: var(--mono);
    font-size: 24px;
    font-weight: 700;
    color: var(--accent);
  }}
  .dr-stat-label {{
    font-size: 10px;
    color: var(--muted);
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
  }}
  .dr-section-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin: 12px 0 6px;
  }}
  .dr-chat {{
    font-size: 12px;
    color: var(--subtext);
    padding: 3px 0;
    font-family: var(--mono);
  }}
  .dr-chat.muted {{ color: var(--muted); }}
  .dr-suggestion {{
    font-size: 12px;
    color: var(--subtext);
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    line-height: 1.4;
  }}
  .dr-suggestion:last-child {{ border-bottom: none; }}
  .dr-date {{
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
  }}

  /* ── Footer ── */
  .footer {{
    text-align: center;
    padding: 16px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    border-top: 1px solid var(--border);
  }}

  /* ── Agents spans full width ── */
  .agents-section {{
    grid-column: 1 / -1;
  }}

  @media (max-width: 900px) {{
    .layout {{ grid-template-columns: 1fr; }}
    .agents-grid {{ grid-template-columns: 1fr; }}
    .agents-section {{ grid-column: auto; }}
  }}
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div class="header-brand">
    <span class="hammer-logo">🔨</span>
    <div>
      <div class="header-title">HaMm3r's Agent Utility Tool</div>
      <div class="header-sub">HAMMER STRATEGIC HOLDINGS LLC · PERSONAL AI OS v1.0</div>
    </div>
  </div>
  <div class="header-right">
    <span class="clock">🕐 {now}</span>
    <span class="os-badge">⚡ OS ONLINE</span>
  </div>
</div>

<!-- Layout -->
<div class="layout">

  <!-- Agents — full width -->
  <div class="section agents-section">
    <div class="section-header">
      <div class="section-title">🤖 Active Agents</div>
      <span class="section-count">{len(agents)} agents</span>
    </div>
    <div class="agents-grid">
      {agent_cards}
    </div>
  </div>

  <!-- Connectors -->
  <div class="section">
    <div class="section-header">
      <div class="section-title">🔌 Connectors</div>
      <span class="section-count">{sum(1 for c in connectors if c['status'] == 'connected')}/{len(connectors)} active</span>
    </div>
    <div class="section-body">
      {connector_rows}
    </div>
  </div>

  <!-- Skills -->
  <div class="section">
    <div class="section-header">
      <div class="section-title">⚡ Skills &amp; Automations</div>
      <span class="section-count">{sum(1 for s in skills if s['active'])} active</span>
    </div>
    <div class="section-body">
      {skills_html}
    </div>
  </div>

  <!-- Dream Review -->
  <div class="section" style="grid-column: 1 / -1;">
    <div class="section-header">
      <div class="section-title">🌙 Dream Review</div>
      <span class="dr-date">Last run: {dream_review['date']}</span>
    </div>
    <div class="section-body">
      <div class="dr-stats">
        <div class="dr-stat">
          <div class="dr-stat-value">{dream_review['total_chats']}</div>
          <div class="dr-stat-label">Chats (24h)</div>
        </div>
        <div class="dr-stat">
          <div class="dr-stat-value">{dream_review['active_agents']}</div>
          <div class="dr-stat-label">Active Agents</div>
        </div>
      </div>
      <div class="dr-section-title">Recent Sessions</div>
      {chat_list}
      <div class="dr-section-title" style="margin-top:14px;">Optimization Suggestions</div>
      {suggestions_html}
    </div>
  </div>

</div>

<div class="footer">
  🔨 HaMm3r OS v1.0 · Built for Mr. Hammer · Powered by OpenJarvis + Open WebUI
</div>

</body>
</html>"""
