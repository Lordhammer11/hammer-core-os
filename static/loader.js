/* ============================================================
   HaMm3r's Agent OS — loader.js v5 FINAL
   Original Utility Tool design: #090D16 · #00D8FF · #818CF8
   Deferred JS runs AFTER Tailwind — always wins the cascade
   ============================================================ */
(function () {
  'use strict';

  const root = document.documentElement;

  // ── 1. SET TAILWIND v4 OKLCH VARS INLINE (inline style = max specificity) ──
  const twVars = {
    '--color-gray-950': 'oklch(5.5% 0.022 265)',   // #090D16 — canvas
    '--color-gray-900': 'oklch(7.5% 0.024 265)',   // #0D1120 — near-canvas
    '--color-gray-850': 'oklch(9.5% 0.026 265)',   // #0F1525 — between
    '--color-gray-800': 'oklch(12%  0.030 265)',   // #131B2E — cards
    '--color-gray-700': 'oklch(15%  0.028 265)',   // #182035
    '--color-gray-600': 'oklch(18%  0.025 265)',   // #1E293B — elevated
    '--color-gray-500': 'oklch(26%  0.020 265)',   // #334155 — borders
    '--color-gray-400': 'oklch(37%  0.016 265)',   // #475569
    '--color-gray-300': 'oklch(48%  0.014 265)',   // #64748B
    '--color-gray-200': 'oklch(64%  0.012 265)',   // #94A3B8
    '--color-gray-100': 'oklch(81%  0.009 265)',   // #CBD5E1
    '--color-gray-50':  'oklch(90%  0.006 265)',   // #E2E8F0
  };

  function applyVars() {
    for (const [k, v] of Object.entries(twVars)) {
      root.style.setProperty(k, v);
    }
  }
  applyVars();

  // ── 2. RE-APPLY WHEN .dark CLASS IS ADDED BY OPEN WEBUI ──
  new MutationObserver(applyVars)
    .observe(root, { attributes: true, attributeFilter: ['class'] });

  // ── 3. INJECT FULL DESIGN SYSTEM AS <style> AT END OF <head> ──
  const css = `
/* ══════════════════════════════════════════════════════════════
   HaMm3r's Agent OS — Original Utility Tool Design System
   Canvas #090D16  ·  Cards #131B2E  ·  Cyan #00D8FF  ·  Lavender #818CF8
══════════════════════════════════════════════════════════════ */

/* ── CUSTOM PROPERTIES ── */
:root {
  --h-bg:          #090D16;
  --h-surface:     #131B2E;
  --h-surface2:    #0D1120;
  --h-elevated:    #1E293B;
  --h-border:      rgba(255,255,255,0.06);
  --h-border-cyan: rgba(0,216,255,0.12);
  --h-text:        #E2E8F0;
  --h-muted:       #94A3B8;
  --h-cyan:        #00D8FF;
  --h-lavender:    #818CF8;
  --h-purple:      #A855F7;
  --h-glow-cyan:   0 0 20px rgba(0,216,255,0.12), 0 0 40px rgba(0,216,255,0.06);
  --h-glow-purple: 0 0 20px rgba(168,85,247,0.12), 0 0 40px rgba(168,85,247,0.06);
}

/* ── CINEMATIC TOP GLOW LINE ── */
body::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(0,216,255,0.7) 25%,
    rgba(129,140,248,0.6) 60%,
    rgba(168,85,247,0.4) 80%,
    transparent 100%
  );
  z-index: 99999;
  pointer-events: none;
}

/* ── CANVAS / BODY ── */
html, body {
  background-color: #090D16 !important;
  color: #E2E8F0 !important;
  font-family: 'Inter', ui-sans-serif, system-ui, sans-serif !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
}

/* ── SIDEBAR ── */
#sidebar,
nav[aria-label="Sidebar"],
[id="sidebar"],
[id*="sidebar"],
aside {
  background-color: #0D1120 !important;
  border-right: 1px solid rgba(0,216,255,0.08) !important;
}

/* Active chat item */
.dark\:bg-gray-900,
[class*="bg-gray-900"] {
  background-color: #131B2E !important;
}

/* ── TOP NAVBAR ── */
header,
#nav,
nav[aria-label],
[class*="navbar"],
[class*="topbar"] {
  background-color: #090D16 !important;
  border-bottom: 1px solid rgba(0,216,255,0.08) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
}

/* ── MAIN CHAT AREA ── */
main,
#content,
#main,
[class*="chat-container"] {
  background-color: #090D16 !important;
}

/* ── USER MESSAGE BUBBLE ── */
.dark\:bg-gray-800,
[class*="bg-gray-800"] {
  background-color: #131B2E !important;
  border: 1px solid rgba(0,216,255,0.08) !important;
  border-radius: 14px !important;
}

/* ── CHAT INPUT ── */
textarea,
[contenteditable="true"],
[contenteditable=""] {
  background-color: #131B2E !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-top: 1px solid rgba(0,216,255,0.1) !important;
  border-radius: 14px !important;
  color: #E2E8F0 !important;
  caret-color: #00D8FF !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 14px !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

textarea:focus,
[contenteditable]:focus {
  border-color: rgba(0,216,255,0.3) !important;
  box-shadow: 0 0 0 2px rgba(0,216,255,0.08), 0 0 16px rgba(0,216,255,0.06) !important;
  outline: none !important;
}

/* Chat input wrapper */
.dark\:bg-gray-800.rounded-\[20px\],
[class*="rounded"][class*="bg-gray-8"] {
  background-color: #0D1120 !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
  border-top: 1px solid rgba(0,216,255,0.1) !important;
}

/* ── SEND BUTTON — cyan → lavender gradient ── */
button[type="submit"],
button[aria-label="Send message"],
button[aria-label*="Send"],
.dark\:bg-white.dark\:text-black {
  background: linear-gradient(135deg, #00D8FF, #818CF8) !important;
  color: #090D16 !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 12px rgba(0,216,255,0.3) !important;
  transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
}
button[type="submit"]:hover,
button[aria-label="Send message"]:hover {
  opacity: 0.92 !important;
  transform: scale(1.04) !important;
  box-shadow: 0 4px 20px rgba(0,216,255,0.5) !important;
}

/* ── INPUTS (forms, settings) ── */
input[type="text"],
input[type="email"],
input[type="password"],
input[type="search"],
input[type="url"],
input[type="number"] {
  background-color: #0D1120 !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 8px !important;
  color: #E2E8F0 !important;
  font-family: 'Inter', sans-serif !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus {
  border-color: rgba(0,216,255,0.3) !important;
  box-shadow: 0 0 0 2px rgba(0,216,255,0.06) !important;
  outline: none !important;
}
input::placeholder,
textarea::placeholder { color: #64748B !important; }

/* ── MODEL SELECTOR ── */
button[aria-haspopup="listbox"],
button[aria-haspopup="menu"],
[class*="model-selector"],
select,
.dark\:bg-gray-850 {
  background-color: #131B2E !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 10px !important;
  color: #E2E8F0 !important;
}
button[aria-haspopup="listbox"]:hover,
button[aria-haspopup="menu"]:hover {
  border-color: rgba(0,216,255,0.2) !important;
  background-color: rgba(0,216,255,0.04) !important;
}

/* ── DROPDOWNS / MENUS / DIALOGS ── */
[role="listbox"],
[role="menu"],
[role="dialog"],
[role="tooltip"],
.dark\:bg-gray-900.rounded-xl,
[class*="dropdown"],
[class*="popover"] {
  background-color: #131B2E !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-top: 1px solid rgba(0,216,255,0.12) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.55),
              0 0 20px rgba(0,216,255,0.08) !important;
}
[role="option"]:hover,
[role="menuitem"]:hover,
[role="option"][aria-selected="true"] {
  background-color: rgba(0,216,255,0.07) !important;
  border-radius: 8px !important;
}

/* ── CARDS / PANELS ── */
[class*="rounded-xl"],
[class*="rounded-2xl"],
[class*="card"],
[class*="panel"] {
  background-color: #131B2E !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
}

/* ── PROMPT SUGGESTION CARDS ── */
[class*="suggestion"],
[class*="prompt-card"],
[class*="starter"] {
  background-color: #131B2E !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
  border-top: 1px solid rgba(0,216,255,0.08) !important;
  border-radius: 12px !important;
  transition: all 0.15s ease !important;
}
[class*="suggestion"]:hover,
[class*="prompt-card"]:hover,
[class*="starter"]:hover {
  border-color: rgba(0,216,255,0.22) !important;
  background-color: rgba(0,216,255,0.05) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}

/* ── CODE BLOCKS ── */
pre, code {
  background-color: #0D1120 !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
  border-radius: 10px !important;
  font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', ui-monospace, monospace !important;
}
pre > div:first-child {
  background-color: #131B2E !important;
  border-bottom: 1px solid rgba(255,255,255,0.05) !important;
  border-radius: 10px 10px 0 0 !important;
}
code { padding: 2px 6px !important; color: #00D8FF !important; }

/* ── BUTTONS ── */
button.dark\:bg-gray-800,
button.dark\:hover\:bg-gray-700:hover {
  background-color: #131B2E !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 8px !important;
  color: #E2E8F0 !important;
  transition: all 0.15s ease !important;
}
button.dark\:hover\:bg-gray-700:hover {
  border-color: rgba(0,216,255,0.2) !important;
  background-color: rgba(0,216,255,0.06) !important;
}
/* Primary buttons */
.dark\:bg-white,
button[class*="primary"] {
  background: linear-gradient(135deg, #00D8FF, #818CF8) !important;
  color: #090D16 !important;
  font-weight: 600 !important;
}

/* ── BADGES / TAGS / CHIPS ── */
[class*="badge"],
[class*="chip"],
[class*="tag"] {
  background-color: rgba(129,140,248,0.12) !important;
  color: #818CF8 !important;
  border: 1px solid rgba(129,140,248,0.2) !important;
  border-radius: 6px !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
}

/* ── TOGGLES / SWITCHES ── */
[role="switch"][aria-checked="true"] {
  background-color: #00D8FF !important;
}

/* ── SETTINGS PANELS ── */
[class*="settings"],
[class*="Settings"] {
  background-color: #131B2E !important;
}
[class*="settings"] button:hover {
  background-color: rgba(0,216,255,0.06) !important;
  border-radius: 8px !important;
}
[class*="settings"] [aria-selected="true"],
[class*="settings"] [class*="active"] {
  background-color: rgba(0,216,255,0.1) !important;
  border-left: 2px solid #00D8FF !important;
  color: #00D8FF !important;
  border-radius: 8px !important;
}

/* ── DIVIDERS / BORDERS ── */
hr,
[class*="divider"],
.dark\:border-gray-800,
.dark\:border-gray-700 {
  border-color: rgba(255,255,255,0.05) !important;
}

/* ── SCROLLBARS ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(0,216,255,0.2);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,216,255,0.45); }

/* ── SELECTION ── */
::selection { background: rgba(0,216,255,0.2); color: #E2E8F0; }

/* ── LINKS ── */
a:not([class]) { color: #00D8FF !important; text-decoration: none !important; }
a:not([class]):hover { color: #80EEFF !important; }

/* ── FOCUS RINGS ── */
*:focus-visible {
  outline: 2px solid rgba(0,216,255,0.4) !important;
  outline-offset: 2px !important;
}

/* ── SPINNERS / LOADING ── */
[class*="spinner"],
[class*="loading"] {
  border-color: rgba(0,216,255,0.15) !important;
  border-top-color: #00D8FF !important;
}

/* ── TEXT COLORS ── */
.dark\:text-white,
.dark\:text-gray-100 { color: #E2E8F0 !important; }
.dark\:text-gray-200,
.dark\:text-gray-300 { color: #CBD5E1 !important; }
.dark\:text-gray-400  { color: #94A3B8 !important; }
.dark\:text-gray-500  { color: #64748B !important; }

/* ── MODAL BACKDROP ── */
.dark\:bg-gray-900\/60,
[class*="backdrop"],
[class*="overlay"] {
  background-color: rgba(9,13,22,0.85) !important;
  backdrop-filter: blur(8px) !important;
}

/* ── WELCOME / EMPTY STATE ── */
[class*="welcome"],
[class*="empty-state"],
[class*="landing"] {
  background-color: #090D16 !important;
}

/* ── ACTIVE SIDEBAR CHAT ITEM ── */
.dark\:bg-gray-900 {
  background-color: #131B2E !important;
  border-left: 2px solid #00D8FF !important;
  border-radius: 8px !important;
}

/* ── WATERMARK BADGE ── */
@keyframes hammerPulse {
  0%, 100% {
    box-shadow: 0 0 8px rgba(0,216,255,0.25),
                0 0 0 1px rgba(0,216,255,0.15);
  }
  50% {
    box-shadow: 0 0 18px rgba(0,216,255,0.55),
                0 0 32px rgba(129,140,248,0.25),
                0 0 0 1px rgba(0,216,255,0.35);
  }
}
body::after {
  content: "⚡ HaMm3r's Agent OS";
  position: fixed;
  bottom: 14px;
  left: 16px;
  z-index: 99999;
  font-family: 'Inter', sans-serif;
  font-size: 0.67rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 999px;
  background: rgba(9,13,22,0.95);
  border: 1px solid rgba(0,216,255,0.28);
  color: rgba(0,216,255,0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  pointer-events: none;
  user-select: none;
  text-shadow: 0 0 10px rgba(0,216,255,0.6);
  animation: hammerPulse 3s ease-in-out infinite;
}
`;

  // Remove old version if exists
  const old = document.getElementById('hammer-os-theme');
  if (old) old.remove();

  const style = document.createElement('style');
  style.id = 'hammer-os-theme';
  style.textContent = css;
  document.head.appendChild(style);

})();
