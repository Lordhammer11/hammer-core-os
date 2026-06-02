<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import ThemeCustomizer from '$lib/components/layout/ThemeCustomizer.svelte';
	import { themeStore, applyThemeToDom } from '$lib/stores/theme';

	let showCustomizer = false;
	let currentTheme: any;
	themeStore.subscribe(t => currentTheme = t);

	let greeting = 'Good morning';
	let greetingSub = 'Your agents are standing by.';
	let currentTime = '';
	let obsidianConnected = false;

	const agents = [
		{
			id: 'investment-manager',
			emoji: '💰',
			name: 'Investment Manager',
			desc: 'Stocks, real estate, wealth protection & tax strategy',
			color: '#00D8FF'
		},
		{
			id: 'vehicle-tech',
			emoji: '🚗',
			name: 'Vehicle Tech',
			desc: '2018 Silverado 5.3L diagnostics, maintenance & upgrades',
			color: '#818CF8'
		},
		{
			id: 'va-disability-specialist',
			emoji: '🎖️',
			name: 'VA Disability Specialist',
			desc: 'Claims navigation, VR&E Chapter 31, 38 CFR & M28C',
			color: '#A855F7'
		},
		{
			id: 'the-hawk',
			emoji: '🦅',
			name: 'The Hawk',
			desc: 'Veteran entrepreneur — transport, grants, federal contracts',
			color: '#FF6B8A'
		},
		{
			id: 'utility-tool',
			emoji: '🔧',
			name: "HaMm3r's Utility Tool",
			desc: '16 integrations — Gmail, Drive, GitHub, Shopify, Adobe & more',
			color: '#F59E0B',
			external: '/static/hammer-utility.html'
		}
	];

	const stats = [
		{ label: 'Active Models', value: '5', icon: '🤖', color: '#00D8FF' },
		{ label: 'Agents Ready', value: '5', icon: '⚡', color: '#818CF8' },
		{ label: 'Skills Loaded', value: '92', icon: '🛠️', color: '#A855F7' },
		{ label: 'Tool Integrations', value: '16', icon: '🔧', color: '#FF6B8A', link: '/static/hammer-utility.html' }
	];

	const memoryTiers = [
		{ label: 'Operating Manual', tier: 'Short-Term', dot: '#00D8FF', status: 'Active', link: 'obsidian://open?vault=HaMm3r-KB&file=Memory/Short-Term/Operating-Manual' },
		{ label: 'Active Sprint', tier: 'Mid-Term', dot: '#F59E0B', status: '3 items', link: 'obsidian://open?vault=HaMm3r-KB&file=Memory/Mid-Term/Sprint' },
		{ label: 'HaMm3r-KB', tier: 'Long-Term', dot: '#818CF8', status: 'Obsidian Vault', link: 'obsidian://open?vault=HaMm3r-KB' }
	];

	const modelBreakdown = [
		{ name: 'Claude', pct: 60, color: '#00D8FF' },
		{ name: 'Llama 3.2', pct: 25, color: '#818CF8' },
		{ name: 'Mistral', pct: 15, color: '#A855F7' }
	];

	onMount(() => {
		applyThemeToDom(currentTheme);
		const h = new Date().getHours();
		if (h < 12) { greeting = 'Good morning'; greetingSub = 'Ready to build something great today?'; }
		else if (h < 17) { greeting = 'Good afternoon'; greetingSub = 'Your agents are standing by.'; }
		else if (h < 21) { greeting = 'Good evening'; greetingSub = 'Let\'s review the day\'s progress.'; }
		else { greeting = 'Working late, Mr. Hammer.'; greetingSub = 'Dream Review will run overnight.'; }

		const tick = () => {
			const now = new Date();
			currentTime = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
		};
		tick();
		const interval = setInterval(tick, 60000);
		return () => clearInterval(interval);
	});

	function launchAgent(agent: any) {
		if (agent.external) {
			window.open(agent.external, '_blank');
		} else {
			goto(`/?agent=${agent.id}`);
		}
	}

	function openObsidian(link: string) {
		window.location.href = link;
	}
</script>

<div class="hammer-dashboard">
	<!-- ═══════════ LEFT SIDEBAR ═══════════ -->
	<aside class="sidebar">
		<div class="sidebar-logo">
			<div class="logo-icon">
				<svg viewBox="0 0 32 32" width="28" height="28">
					<path d="M16 4 C10 4 6 8 6 14 C6 18 8 21 12 23 C10 27 12 30 16 30 C20 30 22 27 20 23 C24 21 26 18 26 14 C26 8 22 4 16 4Z" fill="none" stroke="#818CF8" stroke-width="2"/>
					<path d="M16 4 C22 10 22 22 16 30 C10 22 10 10 16 4Z" fill="#818CF8" opacity="0.3"/>
				</svg>
			</div>
			<div class="logo-text">
				<span class="logo-name">HaMm3r OS</span>
				<span class="logo-sub">Agent Platform</span>
			</div>
		</div>

		<nav class="sidebar-nav">
			<a href="/dashboard" class="nav-item active">
				<span class="nav-icon">⚡</span>
				<span>Dashboard</span>
			</a>
			<a href="/" class="nav-item">
				<span class="nav-icon">💬</span>
				<span>Chats</span>
			</a>
			<a href="/workspace" class="nav-item">
				<span class="nav-icon">🤖</span>
				<span>Agents</span>
			</a>
			<a href="/workspace/models" class="nav-item">
				<span class="nav-icon">🧬</span>
				<span>Models</span>
			</a>
			<a href="/dashboard/analytics" class="nav-item">
				<span class="nav-icon">📊</span>
				<span>Analytics</span>
			</a>
			<a href="/workspace/knowledge" class="nav-item">
				<span class="nav-icon">🧠</span>
				<span>Memory</span>
			</a>
			<a href="/workspace/tools" class="nav-item">
				<span class="nav-icon">🛠️</span>
				<span>Tools</span>
			</a>
			<a href="/static/hammer-utility.html" class="nav-item" target="_blank">
				<span class="nav-icon">🔧</span>
				<span>Utility Tool</span>
			</a>
			<a href="/admin" class="nav-item">
				<span class="nav-icon">⚙️</span>
				<span>Settings</span>
			</a>
		</nav>

		<div class="sidebar-section-label">YOUR AGENTS</div>
		<div class="agent-list">
			{#each agents as agent}
				<button class="agent-item" on:click={() => launchAgent(agent)}>
					<span class="agent-emoji">{agent.emoji}</span>
					<div class="agent-info">
						<span class="agent-name">{agent.name}</span>
					</div>
					<span class="agent-arrow">›</span>
				</button>
			{/each}
			<a href="/dashboard/agent-builder" class="agent-item new-agent">
				<span class="agent-emoji">＋</span>
				<div class="agent-info">
					<span class="agent-name">New Agent</span>
				</div>
			</a>
		</div>

		<div class="sidebar-bottom">
			<div class="status-dot"></div>
			<span class="status-text">Online · {currentTime}</span>
		</div>
	</aside>

	<!-- ═══════════ MAIN CENTER PANE ═══════════ -->
	<main class="main-pane">
	<div class="main-header">
		<div class="welcome-block">
			<h1 class="welcome-title">Welcome back, Mr. Hammer.</h1>
			<p class="welcome-sub">{greeting} — {greetingSub}</p>
		</div>
		<div class="header-actions">
			<button class="customize-btn" on:click={() => showCustomizer = true}>🎨 Customize</button>
			<div class="header-avatar">
				<img src="/claude-bot.svg" alt="HaMm3r Bot" width="56" height="56"/>
			</div>
		</div>
	</div>

		<!-- Stats row -->
		<div class="stats-row">
			{#each stats as stat}
				<div class="stat-card">
					<div class="stat-icon">{stat.icon}</div>
					<div class="stat-value" style="color: {stat.color}">{stat.value}</div>
					<div class="stat-label">{stat.label}</div>
				</div>
			{/each}
		</div>

		<!-- Quick Launch -->
		<div class="section-header">
			<span class="section-label">QUICK LAUNCH</span>
			<span class="section-divider"></span>
		</div>
		<div class="agent-grid">
		{#each agents as agent}
			<button class="agent-card" on:click={() => launchAgent(agent)} style="--accent: {agent.color}">
					<div class="agent-card-emoji">{agent.emoji}</div>
					<div class="agent-card-name">{agent.name}</div>
					<div class="agent-card-desc">{agent.desc}</div>
					<div class="agent-card-cta">Start Chat →</div>
				</button>
			{/each}
		</div>

		<!-- Recent Activity -->
		<div class="section-header">
			<span class="section-label">RECENT ACTIVITY</span>
			<span class="section-divider"></span>
		</div>
		<div class="activity-list">
			<div class="activity-item">
				<span class="activity-emoji">💰</span>
				<div class="activity-content">
					<span class="activity-title">Investment Manager</span>
					<span class="activity-time">Reviewed Q3 real estate strategy</span>
				</div>
				<span class="activity-ago">Ready</span>
			</div>
			<div class="activity-item">
				<span class="activity-emoji">🎖️</span>
				<div class="activity-content">
					<span class="activity-title">VA Disability Specialist</span>
					<span class="activity-time">Chapter 31 VR&E self-employment track</span>
				</div>
				<span class="activity-ago">Ready</span>
			</div>
			<div class="activity-item">
				<span class="activity-emoji">🦅</span>
				<div class="activity-content">
					<span class="activity-title">The Hawk — Business Coach</span>
					<span class="activity-time">Federal contracts & grant writing</span>
				</div>
				<span class="activity-ago">Ready</span>
			</div>
		</div>
	</main>

	<!-- ═══════════ RIGHT PANEL ═══════════ -->
	<aside class="right-panel">
		<!-- Memory System -->
		<div class="panel-section">
			<div class="panel-section-title">🧠 Memory System</div>
			{#each memoryTiers as tier}
				<button class="memory-tier" on:click={() => openObsidian(tier.link)}>
					<div class="tier-left">
						<span class="tier-dot" style="background: {tier.dot}"></span>
						<div>
							<div class="tier-label">{tier.label}</div>
							<div class="tier-sub">{tier.tier}</div>
						</div>
					</div>
					<span class="tier-status">{tier.status}</span>
				</button>
			{/each}
		</div>

		<!-- Analytics -->
		<div class="panel-section">
			<div class="panel-section-title">📊 Analytics</div>
			<div class="analytics-row">
				<div class="analytics-stat">
					<div class="analytics-val" style="color: #00D8FF">24,831</div>
					<div class="analytics-lbl">Tokens Today</div>
				</div>
				<div class="analytics-stat">
					<div class="analytics-val" style="color: #818CF8">$0.18</div>
					<div class="analytics-lbl">Est. Cost</div>
				</div>
			</div>
			<div class="model-bars">
				{#each modelBreakdown as m}
					<div class="model-bar-row">
						<span class="model-bar-name">{m.name}</span>
						<div class="model-bar-track">
							<div class="model-bar-fill" style="width: {m.pct}%; background: {m.color}"></div>
						</div>
						<span class="model-bar-pct">{m.pct}%</span>
					</div>
				{/each}
			</div>
		</div>

		<!-- Dream Review -->
		<div class="panel-section">
			<div class="panel-section-title">🌙 Dream Review</div>
			<div class="dream-content">
				<div class="dream-badge">Latest · Tonight</div>
				<p class="dream-text">Identified 3 recurring patterns in VA claims workflow. Agent prompt update suggested for improved accuracy on VASRD ratings.</p>
				<button class="dream-link" on:click={() => openObsidian('obsidian://open?vault=HaMm3r-KB&file=Dream-Review/Latest')}>
					View Full Report →
				</button>
			</div>
		</div>

		<!-- Obsidian Vault Link -->
		<div class="panel-section">
			<div class="panel-section-title">📁 HaMm3r-KB Vault</div>
			<button class="vault-btn" on:click={() => openObsidian('obsidian://open?vault=HaMm3r-KB')}>
				<span>Open in Obsidian</span>
				<span>↗</span>
			</button>
		</div>
	</aside>
</div>

<!-- Theme Customizer Overlay -->
{#if showCustomizer}
	<div class="customizer-overlay" on:click|self={() => showCustomizer = false}>
		<ThemeCustomizer on:close={() => showCustomizer = false}/>
	</div>
{/if}

<style>
	.hammer-dashboard {
		display: flex;
		height: 100vh;
		width: 100%;
		overflow: hidden;
		background: #090D16;
		font-family: 'Inter', -apple-system, sans-serif;
		color: #E2E8F0;
	}

	/* ─── LEFT SIDEBAR ─── */
	.sidebar {
		width: 230px;
		min-width: 230px;
		background: #131B2E;
		border-right: 1px solid rgba(255,255,255,0.06);
		display: flex;
		flex-direction: column;
		padding: 0;
		overflow-y: auto;
		overflow-x: hidden;
	}

	.sidebar-logo {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 20px 16px 16px;
		border-bottom: 1px solid rgba(255,255,255,0.06);
	}
	.logo-icon { flex-shrink: 0; }
	.logo-name {
		font-size: 15px;
		font-weight: 700;
		color: #818CF8;
		display: block;
		line-height: 1.2;
	}
	.logo-sub {
		font-size: 10px;
		color: #4A5568;
		display: block;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.sidebar-nav {
		display: flex;
		flex-direction: column;
		padding: 10px 8px;
		gap: 2px;
	}

	.nav-item {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 10px;
		border-radius: 8px;
		color: #718096;
		text-decoration: none;
		font-size: 13px;
		font-weight: 500;
		transition: all 0.15s ease;
		cursor: pointer;
		background: transparent;
		border: none;
	}
	.nav-item:hover { background: rgba(129,140,248,0.08); color: #E2E8F0; }
	.nav-item.active { background: rgba(129,140,248,0.14); color: #818CF8; }
	.nav-icon { font-size: 15px; width: 20px; text-align: center; }

	.sidebar-section-label {
		font-size: 10px;
		font-weight: 600;
		color: #4A5568;
		letter-spacing: 1.2px;
		padding: 12px 18px 6px;
		text-transform: uppercase;
	}

	.agent-list {
		display: flex;
		flex-direction: column;
		padding: 0 8px;
		gap: 2px;
	}

	.agent-item {
		display: flex;
		align-items: center;
		gap: 9px;
		padding: 7px 10px;
		border-radius: 8px;
		cursor: pointer;
		background: transparent;
		border: none;
		color: #A0AEC0;
		font-size: 13px;
		text-align: left;
		width: 100%;
		transition: all 0.15s ease;
		text-decoration: none;
	}
	.agent-item:hover { background: rgba(255,255,255,0.05); color: #E2E8F0; }
	.agent-emoji { font-size: 16px; }
	.agent-name { font-size: 12px; font-weight: 500; }
	.agent-info { flex: 1; }
	.agent-arrow { color: #4A5568; font-size: 16px; }
	.new-agent { color: #818CF8; border: 1px dashed rgba(129,140,248,0.3); margin-top: 4px; }
	.new-agent:hover { border-color: rgba(129,140,248,0.6); }

	.sidebar-bottom {
		margin-top: auto;
		padding: 16px;
		display: flex;
		align-items: center;
		gap: 8px;
		border-top: 1px solid rgba(255,255,255,0.06);
	}
	.status-dot {
		width: 7px; height: 7px; border-radius: 50%;
		background: #48BB78;
		box-shadow: 0 0 6px #48BB78;
	}
	.status-text { font-size: 11px; color: #4A5568; }

	/* ─── MAIN PANE ─── */
	.main-pane {
		flex: 1;
		overflow-y: auto;
		padding: 32px 36px;
		display: flex;
		flex-direction: column;
		gap: 28px;
	}

	.main-header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
	}
	.header-actions {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.customize-btn {
		background: rgba(129,140,248,0.1);
		border: 1px solid rgba(129,140,248,0.25);
		border-radius: 10px;
		padding: 8px 16px;
		color: #818CF8;
		font-size: 13px;
		font-weight: 500;
		cursor: pointer;
		font-family: inherit;
		transition: all 0.15s ease;
	}
	.customize-btn:hover {
		background: rgba(129,140,248,0.18);
		border-color: rgba(129,140,248,0.5);
	}
	.customizer-overlay {
		position: fixed;
		inset: 0;
		background: rgba(0,0,0,0.6);
		backdrop-filter: blur(8px);
		z-index: 1000;
		display: flex;
		align-items: center;
		justify-content: flex-end;
		padding: 20px;
	}
	.welcome-title {
		font-size: 28px;
		font-weight: 700;
		color: #F7FAFC;
		margin: 0 0 6px;
		letter-spacing: -0.5px;
	}
	.welcome-sub {
		font-size: 14px;
		color: #718096;
		margin: 0;
	}
	.header-avatar img {
		border-radius: 12px;
		border: 1px solid rgba(129,140,248,0.3);
		box-shadow: 0 0 16px rgba(129,140,248,0.2);
	}

	/* Stats */
	.stats-row {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 14px;
	}
	.stat-card {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.06);
		border-radius: 12px;
		padding: 18px 16px;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 4px;
		transition: all 0.2s ease;
	}
	.stat-card:hover { border-color: rgba(129,140,248,0.2); box-shadow: 0 0 20px rgba(129,140,248,0.07); }
	.stat-icon { font-size: 20px; margin-bottom: 4px; }
	.stat-value { font-size: 26px; font-weight: 700; line-height: 1; }
	.stat-label { font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }

	/* Section header */
	.section-header {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.section-label {
		font-size: 10px;
		font-weight: 700;
		color: #4A5568;
		letter-spacing: 1.5px;
		white-space: nowrap;
	}
	.section-divider {
		flex: 1;
		height: 1px;
		background: rgba(255,255,255,0.05);
	}

	/* Agent grid */
	.agent-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 14px;
	}
	.agent-card {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.06);
		border-radius: 14px;
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 6px;
		cursor: pointer;
		text-align: left;
		transition: all 0.2s ease;
		position: relative;
		overflow: hidden;
	}
	.agent-card::before {
		content: '';
		position: absolute;
		top: 0; left: 0; right: 0;
		height: 2px;
		background: var(--accent);
		opacity: 0;
		transition: opacity 0.2s ease;
	}
	.agent-card:hover {
		border-color: rgba(255,255,255,0.1);
		box-shadow: 0 0 24px rgba(0,0,0,0.3);
		transform: translateY(-1px);
	}
	.agent-card:hover::before { opacity: 1; }
	.agent-card:hover .agent-card-cta { color: var(--accent); }
	.agent-card-emoji { font-size: 28px; }
	.agent-card-name { font-size: 14px; font-weight: 600; color: #E2E8F0; }
	.agent-card-desc { font-size: 12px; color: #718096; line-height: 1.5; }
	.agent-card-cta { font-size: 12px; color: #4A5568; margin-top: 6px; transition: color 0.2s ease; font-weight: 500; }

	/* Activity */
	.activity-list {
		display: flex;
		flex-direction: column;
		gap: 2px;
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.06);
		border-radius: 12px;
		overflow: hidden;
	}
	.activity-item {
		display: flex;
		align-items: center;
		gap: 14px;
		padding: 14px 18px;
		border-bottom: 1px solid rgba(255,255,255,0.04);
		transition: background 0.15s ease;
		cursor: pointer;
	}
	.activity-item:last-child { border-bottom: none; }
	.activity-item:hover { background: rgba(255,255,255,0.03); }
	.activity-emoji { font-size: 20px; }
	.activity-content { flex: 1; }
	.activity-title { display: block; font-size: 13px; font-weight: 500; color: #E2E8F0; }
	.activity-time { display: block; font-size: 11px; color: #718096; margin-top: 2px; }
	.activity-ago { font-size: 11px; color: #48BB78; white-space: nowrap; background: rgba(72,187,120,0.1); padding: 3px 8px; border-radius: 20px; }

	/* ─── RIGHT PANEL ─── */
	.right-panel {
		width: 290px;
		min-width: 290px;
		background: #131B2E;
		border-left: 1px solid rgba(255,255,255,0.06);
		display: flex;
		flex-direction: column;
		padding: 0;
		overflow-y: auto;
	}

	.panel-section {
		padding: 20px 18px;
		border-bottom: 1px solid rgba(255,255,255,0.06);
	}
	.panel-section-title {
		font-size: 11px;
		font-weight: 700;
		color: #818CF8;
		letter-spacing: 1.2px;
		text-transform: uppercase;
		margin-bottom: 14px;
	}

	/* Memory tiers */
	.memory-tier {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px 12px;
		border-radius: 8px;
		background: rgba(255,255,255,0.03);
		border: 1px solid rgba(255,255,255,0.05);
		cursor: pointer;
		margin-bottom: 7px;
		width: 100%;
		text-align: left;
		transition: all 0.15s ease;
	}
	.memory-tier:hover { background: rgba(255,255,255,0.06); border-color: rgba(129,140,248,0.2); }
	.tier-left { display: flex; align-items: center; gap: 10px; }
	.tier-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
	.tier-label { font-size: 12px; font-weight: 500; color: #E2E8F0; }
	.tier-sub { font-size: 10px; color: #4A5568; margin-top: 1px; text-transform: uppercase; letter-spacing: 0.8px; }
	.tier-status { font-size: 11px; color: #718096; white-space: nowrap; }

	/* Analytics */
	.analytics-row {
		display: flex;
		gap: 14px;
		margin-bottom: 14px;
	}
	.analytics-stat {
		flex: 1;
		background: rgba(255,255,255,0.03);
		border: 1px solid rgba(255,255,255,0.05);
		border-radius: 8px;
		padding: 10px;
		text-align: center;
	}
	.analytics-val { font-size: 18px; font-weight: 700; }
	.analytics-lbl { font-size: 10px; color: #718096; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.8px; }

	.model-bars { display: flex; flex-direction: column; gap: 8px; }
	.model-bar-row { display: flex; align-items: center; gap: 8px; }
	.model-bar-name { font-size: 11px; color: #A0AEC0; width: 62px; flex-shrink: 0; }
	.model-bar-track { flex: 1; height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
	.model-bar-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
	.model-bar-pct { font-size: 10px; color: #718096; width: 28px; text-align: right; }

	/* Dream Review */
	.dream-content { }
	.dream-badge {
		display: inline-block;
		font-size: 10px;
		color: #A855F7;
		background: rgba(168,85,247,0.12);
		border: 1px solid rgba(168,85,247,0.25);
		padding: 2px 8px;
		border-radius: 20px;
		margin-bottom: 10px;
		letter-spacing: 0.5px;
	}
	.dream-text { font-size: 12px; color: #A0AEC0; line-height: 1.6; margin: 0 0 12px; }
	.dream-link {
		font-size: 12px;
		color: #818CF8;
		cursor: pointer;
		background: none;
		border: none;
		padding: 0;
		font-weight: 500;
		transition: color 0.15s ease;
	}
	.dream-link:hover { color: #A5B4FC; }

	/* Vault button */
	.vault-btn {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px 14px;
		background: rgba(129,140,248,0.08);
		border: 1px solid rgba(129,140,248,0.2);
		border-radius: 8px;
		color: #818CF8;
		font-size: 13px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.15s ease;
	}
	.vault-btn:hover { background: rgba(129,140,248,0.14); border-color: rgba(129,140,248,0.4); }

	/* Scrollbar styling */
	:global(*::-webkit-scrollbar) { width: 5px; }
	:global(*::-webkit-scrollbar-track) { background: transparent; }
	:global(*::-webkit-scrollbar-thumb) { background: rgba(255,255,255,0.08); border-radius: 3px; }
</style>
