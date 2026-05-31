<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { settings, user, models, config } from '$lib/stores';
	import { goto } from '$app/navigation';
	import { updateUserSettings } from '$lib/apis/users';
	import { toast } from 'svelte-sonner';

	// ─── Live Activity Feed ───────────────────────────────────────────────────
	interface ActivityEvent {
		id: string;
		timestamp: Date;
		type: 'chat' | 'agent' | 'tool' | 'system';
		agent?: string;
		model?: string;
		message: string;
		tokens?: number;
	}

	let liveActivity: ActivityEvent[] = [];
	let activityPollInterval: ReturnType<typeof setInterval> | null = null;
	let lastChatCount = 0;
	let totalTokensToday = 0;
	let activeAgentId: string | null = null;
	let pulseAgents: Set<string> = new Set();

	async function fetchLiveActivity() {
		try {
			const res = await fetch('/api/v1/chats/?page=1', {
				headers: { Authorization: `Bearer ${$user?.token ?? ''}` }
			});
			if (!res.ok) return;
			const data = await res.json();
			const chats = Array.isArray(data) ? data : (data.items ?? []);

			if (chats.length > lastChatCount && lastChatCount > 0) {
				const newest = chats[0];
				const modelId = newest?.chat?.models?.[0] ?? newest?.models?.[0] ?? 'unknown';
				const shortModel = modelId.split('/').pop() ?? modelId;
				const agentMatch = allAgents.find(
					(a) =>
						a.id === newest?.title?.toLowerCase().replace(/\s/g, '-') || modelId.includes(a.model)
				);

				const event: ActivityEvent = {
					id: newest.id ?? Math.random().toString(36),
					timestamp: new Date(),
					type: 'chat',
					model: shortModel,
					agent: agentMatch?.name,
					message: `New chat started${agentMatch ? ` via ${agentMatch.name}` : ''} · ${shortModel}`
				};
				liveActivity = [event, ...liveActivity].slice(0, 20);

				if (agentMatch) {
					pulseAgents = new Set([...pulseAgents, agentMatch.id]);
					activeAgentId = agentMatch.id;
					setTimeout(() => {
						pulseAgents.delete(agentMatch.id);
						pulseAgents = pulseAgents;
						if (activeAgentId === agentMatch.id) activeAgentId = null;
					}, 5000);
				}
			}
			lastChatCount = chats.length;

			// Compute today's token estimate from chat count delta
			totalTokensToday = Math.max(totalTokensToday, chats.length * 1200);
		} catch (_) {
			// silent fail
		}
	}

	function startActivityPolling() {
		fetchLiveActivity();
		activityPollInterval = setInterval(fetchLiveActivity, 8000);
	}
	function stopActivityPolling() {
		if (activityPollInterval) clearInterval(activityPollInterval);
	}

	// ─── Types ───────────────────────────────────────────────────────────────
	type Theme = 'dark' | 'light' | 'system';
	type AccentColor = 'cyan' | 'purple' | 'coral' | 'green' | 'orange' | 'gold';
	type FontFamily = 'IBM Plex Mono' | 'Chakra Petch' | 'Inter' | 'Archivo' | 'Mona Sans';
	type PanelId = 'agents' | 'connectors' | 'skills' | 'dreamReview' | 'modelStats' | 'quickChat';

	interface PanelConfig {
		id: PanelId;
		label: string;
		icon: string;
		visible: boolean;
		col: 1 | 2 | 3;
		order: number;
	}

	interface AgentDef {
		id: string;
		name: string;
		role: string;
		icon: string;
		description: string;
		model: string;
		tools: string[];
		status: 'active' | 'idle' | 'offline';
		color: string;
		source: 'hammer' | 'jarvis';
	}

	interface ConnectorDef {
		id: string;
		name: string;
		icon: string;
		type: 'llm' | 'data' | 'service';
		status: 'connected' | 'disconnected' | 'error';
		description: string;
	}

	interface SkillDef {
		id: string;
		name: string;
		description: string;
		icon: string;
		category: string;
		source: 'hammer' | 'jarvis';
	}

	// ─── Settings State ───────────────────────────────────────────────────────
	let theme: Theme = 'dark';
	let accentColor: AccentColor = 'cyan';
	let fontFamily: FontFamily = 'IBM Plex Mono';
	let glowEnabled = true;
	let animationsEnabled = true;
	let compactMode = false;
	let showSettings = false;
	let activeSettingsTab: 'appearance' | 'panels' | 'theme' | 'fonts' = 'appearance';
	let draggingPanel: PanelId | null = null;
	let dragOverCol: 1 | 2 | 3 | null = null;

	// ─── Panel Layout ─────────────────────────────────────────────────────────
	let panels: PanelConfig[] = [
		{ id: 'agents', label: '⚡ Agents', icon: '🤖', visible: true, col: 1, order: 0 },
		{ id: 'connectors', label: '🔌 Connectors', icon: '🔌', visible: true, col: 2, order: 1 },
		{ id: 'skills', label: '🧠 Skills', icon: '🧠', visible: true, col: 3, order: 2 },
		{ id: 'dreamReview', label: '💤 Dream Review', icon: '💤', visible: true, col: 1, order: 3 },
		{ id: 'modelStats', label: '📊 Model Stats', icon: '📊', visible: true, col: 2, order: 4 },
		{ id: 'quickChat', label: '💬 Quick Chat', icon: '💬', visible: true, col: 3, order: 5 }
	];

	// ─── Agents ───────────────────────────────────────────────────────────────
	const allAgents: AgentDef[] = [
		// Your 4 HaMm3r agents
		{
			id: 'va-specialist',
			name: 'VA Specialist',
			role: 'Veterans Affairs',
			icon: '🎖️',
			description:
				'Expert in VA benefits, claims, disability ratings, appeals and GI Bill guidance.',
			model: 'gpt-4o',
			tools: ['web_search', 'file_read', 'memory_store', 'think'],
			status: 'active',
			color: '#00D8FF',
			source: 'hammer'
		},
		{
			id: 'the-hawk',
			name: 'The Hawk',
			role: 'Intelligence & Research',
			icon: '🦅',
			description:
				'Deep research, OSINT, competitive analysis and strategic intelligence gathering.',
			model: 'claude-sonnet-4-5',
			tools: ['web_search', 'http_request', 'file_write', 'memory_store', 'think'],
			status: 'active',
			color: '#818CF8',
			source: 'hammer'
		},
		{
			id: 'investment-manager',
			name: 'Investment Manager',
			role: 'Finance & Markets',
			icon: '📈',
			description:
				'Portfolio analysis, market research, investment strategy and financial planning.',
			model: 'gpt-4o',
			tools: ['web_search', 'http_request', 'calculator', 'memory_store', 'think'],
			status: 'idle',
			color: '#A855F7',
			source: 'hammer'
		},
		{
			id: 'vehicle-tech',
			name: 'Vehicle Tech',
			role: 'Automotive Expert',
			icon: '🔧',
			description: 'Diagnostics, repair guides, parts lookup and vehicle service recommendations.',
			model: 'gpt-4o-mini',
			tools: ['web_search', 'http_request', 'file_read', 'think'],
			status: 'idle',
			color: '#FF6B8A',
			source: 'hammer'
		},
		// OpenJarvis agents
		{
			id: 'code-reviewer',
			name: 'Code Reviewer',
			role: 'Repository Monitor',
			icon: '🔍',
			description:
				'Monitors repo for changes, reviews code quality and identifies bugs. Runs hourly.',
			model: 'claude-sonnet-4-5',
			tools: ['git_status', 'git_diff', 'git_log', 'file_read', 'shell_exec', 'apply_patch'],
			status: 'idle',
			color: '#34D399',
			source: 'jarvis'
		},
		{
			id: 'inbox-triager',
			name: 'Inbox Triager',
			role: 'Message Monitor',
			icon: '📥',
			description: 'Monitors email and messaging channels, categorizes and prioritizes by urgency.',
			model: 'gpt-4o-mini',
			tools: ['channel_send', 'channel_list', 'memory_store', 'think', 'web_search'],
			status: 'idle',
			color: '#FBBF24',
			source: 'jarvis'
		},
		{
			id: 'research-monitor',
			name: 'Research Monitor',
			role: 'Daily Research',
			icon: '🔬',
			description:
				'Searches papers, news, blogs on your topic daily at 9am. Stores findings in memory.',
			model: 'claude-sonnet-4-5',
			tools: ['web_search', 'http_request', 'file_write', 'memory_store', 'think'],
			status: 'idle',
			color: '#F472B6',
			source: 'jarvis'
		},
		{
			id: 'deep-research',
			name: 'Personal Deep Research',
			role: 'Knowledge Search',
			icon: '📚',
			description: 'Searches your personal knowledge base and produces cited research reports.',
			model: 'gpt-4o',
			tools: ['knowledge_search', 'knowledge_sql', 'scan_chunks', 'think'],
			status: 'idle',
			color: '#60A5FA',
			source: 'jarvis'
		}
	];

	// ─── Connectors ───────────────────────────────────────────────────────────
	const allConnectors: ConnectorDef[] = [
		// LLM Connections
		{
			id: 'openai',
			name: 'OpenAI',
			icon: '🟢',
			type: 'llm',
			status: 'connected',
			description: 'GPT-4o, GPT-4o-mini, o1, o3'
		},
		{
			id: 'anthropic',
			name: 'Anthropic',
			icon: '🟣',
			type: 'llm',
			status: 'connected',
			description: 'Claude Sonnet, Haiku, Opus'
		},
		{
			id: 'openrouter',
			name: 'OpenRouter',
			icon: '🔵',
			type: 'llm',
			status: 'connected',
			description: '200+ models via unified API'
		},
		// Data Connectors (OpenJarvis)
		{
			id: 'gmail',
			name: 'Gmail',
			icon: '📧',
			type: 'data',
			status: 'disconnected',
			description: 'Email read/search/draft'
		},
		{
			id: 'gdrive',
			name: 'Google Drive',
			icon: '📁',
			type: 'data',
			status: 'disconnected',
			description: 'Files, docs, spreadsheets'
		},
		{
			id: 'gcalendar',
			name: 'G Calendar',
			icon: '📅',
			type: 'data',
			status: 'disconnected',
			description: 'Events, scheduling, reminders'
		},
		{
			id: 'notion',
			name: 'Notion',
			icon: '📝',
			type: 'data',
			status: 'disconnected',
			description: 'Pages, databases, wikis'
		},
		{
			id: 'obsidian',
			name: 'Obsidian',
			icon: '💎',
			type: 'data',
			status: 'disconnected',
			description: 'Local markdown knowledge base'
		},
		{
			id: 'icloud',
			name: 'iCloud Drive',
			icon: '☁️',
			type: 'data',
			status: 'connected',
			description: 'HaMm3r-KB, Dream Reviews'
		},
		{
			id: 'slack',
			name: 'Slack',
			icon: '💬',
			type: 'service',
			status: 'disconnected',
			description: 'Channels, DMs, threads'
		},
		{
			id: 'github',
			name: 'GitHub',
			icon: '🐙',
			type: 'service',
			status: 'connected',
			description: 'Repos, PRs, issues (Lordhammer11)'
		},
		{
			id: 'spotify',
			name: 'Spotify',
			icon: '🎵',
			type: 'service',
			status: 'disconnected',
			description: 'Playback, playlists, history'
		},
		{
			id: 'oura',
			name: 'Oura Ring',
			icon: '💍',
			type: 'service',
			status: 'disconnected',
			description: 'Sleep, HRV, activity metrics'
		},
		{
			id: 'strava',
			name: 'Strava',
			icon: '🏃',
			type: 'service',
			status: 'disconnected',
			description: 'Runs, rides, fitness tracking'
		},
		{
			id: 'hackernews',
			name: 'Hacker News',
			icon: '🔶',
			type: 'service',
			status: 'connected',
			description: 'Tech news, trending discussions'
		}
	];

	// ─── Skills ───────────────────────────────────────────────────────────────
	const allSkills: SkillDef[] = [
		// HaMm3r Skills
		{
			id: 'dream-review',
			name: 'Dream Review',
			description: 'Log and review daily sessions to iCloud',
			icon: '💤',
			category: 'Personal',
			source: 'hammer'
		},
		{
			id: 'source-context',
			name: 'Source Context',
			description: 'Fetch repo source via repomix for AI ctx',
			icon: '📦',
			category: 'Dev',
			source: 'hammer'
		},
		{
			id: 'code-refactor',
			name: 'Code Refactor',
			description: 'Post-feature cleanup and structure fix',
			icon: '🔨',
			category: 'Dev',
			source: 'hammer'
		},
		{
			id: 'grep-loop',
			name: 'Grep Loop',
			description: 'Automated PR review and CI fix loop',
			icon: '🔁',
			category: 'Dev',
			source: 'hammer'
		},
		{
			id: 'agentic-workflow',
			name: 'Agentic Workflow',
			description: 'Master playbook for AI-driven engineering',
			icon: '⚡',
			category: 'Dev',
			source: 'hammer'
		},
		// OpenJarvis Skills
		{
			id: 'backup-files',
			name: 'Backup Files',
			description: 'Timestamped archive of files/directories',
			icon: '💾',
			category: 'System',
			source: 'jarvis'
		},
		{
			id: 'calendar-prep',
			name: 'Calendar Prep',
			description: 'Prepare briefings for upcoming meetings',
			icon: '📅',
			category: 'Productivity',
			source: 'jarvis'
		},
		{
			id: 'code-lint',
			name: 'Code Lint',
			description: 'Run linters and report style issues',
			icon: '🔍',
			category: 'Dev',
			source: 'jarvis'
		},
		{
			id: 'code-test-gen',
			name: 'Test Generator',
			description: 'Generate unit tests for code files',
			icon: '🧪',
			category: 'Dev',
			source: 'jarvis'
		},
		{
			id: 'compare-docs',
			name: 'Compare Docs',
			description: 'Diff and compare two documents',
			icon: '📄',
			category: 'Research',
			source: 'jarvis'
		},
		{
			id: 'daily-digest',
			name: 'Daily Digest',
			description: 'Summarize stored info and recent activity',
			icon: '📰',
			category: 'Personal',
			source: 'jarvis'
		},
		{
			id: 'data-analyze',
			name: 'Data Analysis',
			description: 'Analyze datasets and generate insights',
			icon: '📊',
			category: 'Research',
			source: 'jarvis'
		},
		{
			id: 'dependency-audit',
			name: 'Dependency Audit',
			description: 'Audit package deps for security issues',
			icon: '🔐',
			category: 'Dev',
			source: 'jarvis'
		},
		{
			id: 'email-draft',
			name: 'Email Drafting',
			description: 'Draft professional email responses',
			icon: '📧',
			category: 'Productivity',
			source: 'jarvis'
		},
		{
			id: 'file-organizer',
			name: 'File Organizer',
			description: 'Sort and organize files by type/date',
			icon: '📂',
			category: 'System',
			source: 'jarvis'
		},
		{
			id: 'knowledge-extract',
			name: 'Knowledge Extract',
			description: 'Extract key knowledge from documents',
			icon: '🧠',
			category: 'Research',
			source: 'jarvis'
		},
		{
			id: 'meeting-notes',
			name: 'Meeting Notes',
			description: 'Structure notes from meeting transcripts',
			icon: '📋',
			category: 'Productivity',
			source: 'jarvis'
		},
		{
			id: 'pdf-summarize',
			name: 'PDF Summary',
			description: 'Summarize long PDF documents',
			icon: '📕',
			category: 'Research',
			source: 'jarvis'
		},
		{
			id: 'security-scan',
			name: 'Security Scan',
			description: 'Scan code/files for vulnerabilities',
			icon: '🛡️',
			category: 'Dev',
			source: 'jarvis'
		},
		{
			id: 'todo-from-notes',
			name: 'Todo Extractor',
			description: 'Extract action items from raw notes',
			icon: '✅',
			category: 'Productivity',
			source: 'jarvis'
		},
		{
			id: 'topic-research',
			name: 'Topic Research',
			description: 'Research a topic via web + memory',
			icon: '🔎',
			category: 'Research',
			source: 'jarvis'
		},
		{
			id: 'translate-doc',
			name: 'Doc Translator',
			description: 'Translate documents to target language',
			icon: '🌍',
			category: 'Productivity',
			source: 'jarvis'
		},
		{
			id: 'web-summarize',
			name: 'Web Summarizer',
			description: 'Summarize any URL/article',
			icon: '🌐',
			category: 'Research',
			source: 'jarvis'
		},
		{
			id: 'search-index',
			name: 'Search & Index',
			description: 'Index local files for fast search',
			icon: '🗂️',
			category: 'System',
			source: 'jarvis'
		}
	];

	// ─── Dream Review ─────────────────────────────────────────────────────────
	let dreamReviewContent = 'Loading dream review...';
	let dreamReviewDate = '';

	// ─── Reactive UI State ───────────────────────────────────────────────────
	let activeAgentFilter: 'all' | 'hammer' | 'jarvis' = 'all';
	let activeConnectorFilter: 'all' | 'llm' | 'data' | 'service' = 'all';
	let activeSkillFilter:
		| 'all'
		| 'hammer'
		| 'jarvis'
		| 'Dev'
		| 'Research'
		| 'Productivity'
		| 'Personal'
		| 'System' = 'all';
	let skillSearch = '';
	let quickChatInput = '';
	let quickChatHistory: { role: 'user' | 'assistant'; text: string }[] = [];

	$: filteredAgents = allAgents.filter((a) =>
		activeAgentFilter === 'all' ? true : a.source === activeAgentFilter
	);
	$: filteredConnectors = allConnectors.filter((c) =>
		activeConnectorFilter === 'all' ? true : c.type === activeConnectorFilter
	);
	$: filteredSkills = allSkills.filter((s) => {
		const matchFilter =
			activeSkillFilter === 'all'
				? true
				: s.source === activeSkillFilter || s.category === activeSkillFilter;
		const matchSearch = skillSearch
			? s.name.toLowerCase().includes(skillSearch.toLowerCase()) ||
				s.description.toLowerCase().includes(skillSearch.toLowerCase())
			: true;
		return matchFilter && matchSearch;
	});
	$: availableModels = $models?.filter((m) => !m.id.includes('arena')) ?? [];

	// ─── Theme & CSS Variables ───────────────────────────────────────────────
	const accentMap: Record<AccentColor, { primary: string; glow: string; muted: string }> = {
		cyan: { primary: '#00D8FF', glow: 'rgba(0,216,255,0.15)', muted: 'rgba(0,216,255,0.08)' },
		purple: { primary: '#A855F7', glow: 'rgba(168,85,247,0.15)', muted: 'rgba(168,85,247,0.08)' },
		coral: { primary: '#FF6B8A', glow: 'rgba(255,107,138,0.15)', muted: 'rgba(255,107,138,0.08)' },
		green: { primary: '#34D399', glow: 'rgba(52,211,153,0.15)', muted: 'rgba(52,211,153,0.08)' },
		orange: { primary: '#FB923C', glow: 'rgba(251,146,60,0.15)', muted: 'rgba(251,146,60,0.08)' },
		gold: { primary: '#FBBF24', glow: 'rgba(251,191,36,0.15)', muted: 'rgba(251,191,36,0.08)' }
	};

	const themeMap: Record<
		Theme,
		{ bg: string; surface: string; border: string; text: string; muted: string; dim: string }
	> = {
		dark: {
			bg: '#090D16',
			surface: '#131B2E',
			border: 'rgba(255,255,255,0.06)',
			text: '#E2E8F0',
			muted: '#94A3B8',
			dim: '#64748B'
		},
		light: {
			bg: '#F1F5F9',
			surface: '#FFFFFF',
			border: 'rgba(0,0,0,0.08)',
			text: '#0F172A',
			muted: '#475569',
			dim: '#94A3B8'
		},
		system: {
			bg: '#090D16',
			surface: '#131B2E',
			border: 'rgba(255,255,255,0.06)',
			text: '#E2E8F0',
			muted: '#94A3B8',
			dim: '#64748B'
		}
	};

	$: accent = accentMap[accentColor];
	$: themeVars =
		themeMap[
			theme === 'system'
				? window?.matchMedia?.('(prefers-color-scheme: dark)')?.matches
					? 'dark'
					: 'light'
				: theme
		];

	function applyThemeVars() {
		const root = document.documentElement;
		root.style.setProperty('--hcc-bg', themeVars.bg);
		root.style.setProperty('--hcc-surface', themeVars.surface);
		root.style.setProperty('--hcc-border', themeVars.border);
		root.style.setProperty('--hcc-text', themeVars.text);
		root.style.setProperty('--hcc-muted', themeVars.muted);
		root.style.setProperty('--hcc-dim', themeVars.dim);
		root.style.setProperty('--hcc-accent', accent.primary);
		root.style.setProperty('--hcc-glow', accent.glow);
		root.style.setProperty('--hcc-glow-sm', accent.muted);
		root.style.setProperty('--hcc-font', `"${fontFamily}", monospace`);
	}

	$: if (typeof document !== 'undefined') {
		theme;
		accentColor;
		fontFamily;
		applyThemeVars();
	}

	// ─── Drag & Drop Panels ───────────────────────────────────────────────────
	function onPanelDragStart(id: PanelId) {
		draggingPanel = id;
	}
	function onColDragOver(e: DragEvent, col: 1 | 2 | 3) {
		e.preventDefault();
		dragOverCol = col;
	}
	function onColDrop(col: 1 | 2 | 3) {
		if (draggingPanel) {
			panels = panels.map((p) => (p.id === draggingPanel ? { ...p, col } : p));
			draggingPanel = null;
		}
		dragOverCol = null;
	}

	function togglePanel(id: PanelId) {
		panels = panels.map((p) => (p.id === id ? { ...p, visible: !p.visible } : p));
	}

	// ─── Quick Chat ───────────────────────────────────────────────────────────
	async function sendQuickChat() {
		if (!quickChatInput.trim()) return;
		const msg = quickChatInput.trim();
		quickChatInput = '';
		quickChatHistory = [...quickChatHistory, { role: 'user', text: msg }];
		// Navigate to new chat with pre-filled message
		await goto(`/?q=${encodeURIComponent(msg)}`);
	}

	// ─── Save preferences ────────────────────────────────────────────────────
	async function savePreferences() {
		try {
			await updateUserSettings(localStorage.token, {
				ui: {
					...$settings,
					hammerCC: {
						theme,
						accentColor,
						fontFamily,
						glowEnabled,
						animationsEnabled,
						compactMode,
						panels
					}
				}
			});
			toast.success('Preferences saved!');
			showSettings = false;
		} catch (e) {
			toast.error('Failed to save preferences');
		}
	}

	// ─── Load saved prefs ────────────────────────────────────────────────────
	onMount(() => {
		const saved = $settings?.hammerCC;
		if (saved) {
			if (saved.theme) theme = saved.theme;
			if (saved.accentColor) accentColor = saved.accentColor;
			if (saved.fontFamily) fontFamily = saved.fontFamily;
			if (saved.glowEnabled !== undefined) glowEnabled = saved.glowEnabled;
			if (saved.animationsEnabled !== undefined) animationsEnabled = saved.animationsEnabled;
			if (saved.compactMode !== undefined) compactMode = saved.compactMode;
			if (saved.panels) panels = saved.panels;
		}
		applyThemeVars();

		// Mock dream review
		dreamReviewDate = new Date().toLocaleDateString('en-US', {
			weekday: 'long',
			month: 'long',
			day: 'numeric'
		});
		dreamReviewContent = `**Session Summary — ${dreamReviewDate}**\n\nHaMm3r OS Command Center deployed. Fixed Railway persistence issues, CI green on all Python versions. Utility tool installed. OpenJarvis agents and skills integrated. Full customization panel added with drag-and-drop layout, theme switching, accent colors, and font selection.\n\n**Key wins:** 8 agents live, 24 skills catalogued, 15 connectors mapped, dream reviews centralized to iCloud.`;

		// Seed activity log with startup events
		liveActivity = [
			{
				id: 'boot-1',
				timestamp: new Date(),
				type: 'system',
				message: '⚡ HaMm3r OS online · Postgres connected · Models loaded'
			},
			{
				id: 'boot-2',
				timestamp: new Date(Date.now() - 5000),
				type: 'system',
				message: `🔌 OpenRouter + Anthropic connected · ${$models?.length ?? 0} models available`
			}
		];

		// Start live polling
		startActivityPolling();

		// System theme watcher
		if (theme === 'system') {
			const mq = window.matchMedia('(prefers-color-scheme: dark)');
			mq.addEventListener('change', applyThemeVars);
		}
	});

	onDestroy(() => {
		stopActivityPolling();
	});

	const statusColor = (s: string) =>
		s === 'connected' || s === 'active' ? '#34D399' : s === 'idle' ? '#FBBF24' : '#EF4444';
	const statusDot = (s: string) =>
		s === 'connected' || s === 'active' ? '🟢' : s === 'idle' ? '🟡' : '🔴';

	// ─── Top 6 pinned models with provider logos ─────────────────────────────
	const pinnedModels = [
		{
			id: 'anthropic/claude-haiku-4.5',
			label: 'Haiku 4.5',
			provider: 'Anthropic',
			logo: 'https://upload.wikimedia.org/wikipedia/commons/7/78/Anthropic_logo.svg',
			color: '#D97706'
		},
		{
			id: 'anthropic/claude-sonnet-4.5',
			label: 'Sonnet 4.5',
			provider: 'Anthropic',
			logo: 'https://upload.wikimedia.org/wikipedia/commons/7/78/Anthropic_logo.svg',
			color: '#D97706'
		},
		{
			id: 'openai/gpt-4o',
			label: 'GPT-4o',
			provider: 'OpenAI',
			logo: 'https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg',
			color: '#10A37F'
		},
		{
			id: 'openai/gpt-4.1',
			label: 'GPT-4.1',
			provider: 'OpenAI',
			logo: 'https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg',
			color: '#10A37F'
		},
		{
			id: 'google/gemini-2.5-pro',
			label: 'Gemini 2.5 Pro',
			provider: 'Google',
			logo: 'https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg',
			color: '#4285F4'
		},
		{
			id: 'meta-llama/llama-4-maverick',
			label: 'Llama 4',
			provider: 'Meta',
			logo: 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png',
			color: '#0082FB'
		}
	];

	function launchModel(modelId: string) {
		goto(`/?models=${encodeURIComponent(modelId)}`);
	}

	$: col1Panels = panels.filter((p) => p.col === 1 && p.visible).sort((a, b) => a.order - b.order);
	$: col2Panels = panels.filter((p) => p.col === 2 && p.visible).sort((a, b) => a.order - b.order);
	$: col3Panels = panels.filter((p) => p.col === 3 && p.visible).sort((a, b) => a.order - b.order);
</script>

<!-- ══════════════════════════════════════════════════════════════
     HAMMER COMMAND CENTER
══════════════════════════════════════════════════════════════ -->
<div class="hcc-root" style="font-family: var(--hcc-font);">
	<!-- ── Top 6 Model Bar ── -->
	<div class="hcc-model-bar">
		{#each pinnedModels as m}
			<button
				class="hcc-model-pill"
				style="--mp-color:{m.color}"
				on:click={() => launchModel(m.id)}
				title="Chat with {m.label}"
			>
				<img
					class="hcc-model-logo"
					src={m.logo}
					alt={m.provider}
					on:error={(e) => {
						(e.target as HTMLImageElement).style.display = 'none';
					}}
				/>
				<span class="hcc-model-label">{m.label}</span>
			</button>
		{/each}
		<a href="/brain" class="hcc-model-pill hcc-brain-pill" title="Brain Tree">
			🧠 <span class="hcc-model-label">Brain Tree</span>
		</a>
	</div>

	<!-- ── Top Bar ── -->
	<header class="hcc-topbar">
		<div class="hcc-topbar-left">
			<span class="hcc-logo">⚡</span>
			<div>
				<div class="hcc-title">HaMm3r Command Center</div>
				<div class="hcc-subtitle">
					AG Attack LLC · {availableModels.length} models · {allConnectors.filter(
						(c) => c.status === 'connected'
					).length} connections live
				</div>
			</div>
		</div>
		<div class="hcc-topbar-right">
			<div class="hcc-status-bar">
				{#each allConnectors.filter((c) => c.type === 'llm') as c}
					<span
						class="hcc-status-chip"
						style="border-color: {statusColor(c.status)}; color: {statusColor(c.status)}"
					>
						{statusDot(c.status)}
						{c.name}
					</span>
				{/each}
			</div>
			<button class="hcc-btn-icon" title="Customize" on:click={() => (showSettings = !showSettings)}
				>⚙️</button
			>
			<button class="hcc-btn-icon" title="Back to Chat" on:click={() => goto('/')}>💬</button>
		</div>
	</header>

	<!-- ── Settings Panel ── -->
	{#if showSettings}
		<div class="hcc-settings-overlay" on:click|self={() => (showSettings = false)}>
			<div class="hcc-settings-panel">
				<div class="hcc-settings-header">
					<span>⚙️ Customize HaMm3r CC</span>
					<button on:click={() => (showSettings = false)}>✕</button>
				</div>

				<!-- Tab nav -->
				<div class="hcc-settings-tabs">
					{#each ['appearance', 'panels', 'theme', 'fonts'] as tab}
						<button
							class="hcc-tab {activeSettingsTab === tab ? 'active' : ''}"
							on:click={() => (activeSettingsTab = tab as typeof activeSettingsTab)}
							>{tab.charAt(0).toUpperCase() + tab.slice(1)}</button
						>
					{/each}
				</div>

				<div class="hcc-settings-body">
					<!-- APPEARANCE -->
					{#if activeSettingsTab === 'appearance'}
						<div class="hcc-setting-group">
							<label class="hcc-label">Accent Color</label>
							<div class="hcc-color-row">
								{#each Object.entries(accentMap) as [key, val]}
									<button
										class="hcc-color-swatch {accentColor === key ? 'active' : ''}"
										style="background:{val.primary}"
										on:click={() => (accentColor = key as AccentColor)}
										title={key}
									></button>
								{/each}
							</div>
						</div>
						<div class="hcc-setting-group">
							<label class="hcc-label">Options</label>
							<label class="hcc-toggle-row">
								<input type="checkbox" bind:checked={glowEnabled} />
								<span>Glow effects</span>
							</label>
							<label class="hcc-toggle-row">
								<input type="checkbox" bind:checked={animationsEnabled} />
								<span>Animations</span>
							</label>
							<label class="hcc-toggle-row">
								<input type="checkbox" bind:checked={compactMode} />
								<span>Compact mode</span>
							</label>
						</div>

						<!-- PANELS -->
					{:else if activeSettingsTab === 'panels'}
						<div class="hcc-setting-group">
							<label class="hcc-label">Show / Hide Panels</label>
							{#each panels as panel}
								<label class="hcc-toggle-row">
									<input
										type="checkbox"
										checked={panel.visible}
										on:change={() => togglePanel(panel.id)}
									/>
									<span>{panel.label}</span>
								</label>
							{/each}
						</div>
						<div class="hcc-setting-group">
							<label class="hcc-label">Layout — Drag panels to reorder</label>
							<p class="hcc-hint">
								You can drag any panel card to a different column by grabbing the ⠿ handle.
							</p>
						</div>

						<!-- THEME -->
					{:else if activeSettingsTab === 'theme'}
						<div class="hcc-setting-group">
							<label class="hcc-label">Color Scheme</label>
							<div class="hcc-theme-row">
								{#each ['dark', 'light', 'system'] as t}
									<button
										class="hcc-theme-btn {theme === t ? 'active' : ''}"
										on:click={() => (theme = t as Theme)}
									>
										{t === 'dark' ? '🌙 Dark' : t === 'light' ? '☀️ Light' : '🖥 System'}
									</button>
								{/each}
							</div>
						</div>

						<!-- FONTS -->
					{:else if activeSettingsTab === 'fonts'}
						<div class="hcc-setting-group">
							<label class="hcc-label">Font Family</label>
							{#each ['IBM Plex Mono', 'Chakra Petch', 'Inter', 'Archivo', 'Mona Sans'] as f}
								<button
									class="hcc-font-btn {fontFamily === f ? 'active' : ''}"
									style="font-family: '{f}', monospace"
									on:click={() => (fontFamily = f as FontFamily)}>{f} — The Quick Brown Fox</button
								>
							{/each}
						</div>
					{/if}
				</div>

				<div class="hcc-settings-footer">
					<button class="hcc-btn-ghost" on:click={() => (showSettings = false)}>Cancel</button>
					<button class="hcc-btn-accent" on:click={savePreferences}>Save Preferences</button>
				</div>
			</div>
		</div>
	{/if}

	<!-- ── 3-Column Grid ── -->
	<div class="hcc-grid">
		<!-- COL 1 -->
		<div
			class="hcc-col {dragOverCol === 1 ? 'drop-target' : ''}"
			on:dragover={(e) => onColDragOver(e, 1)}
			on:drop={() => onColDrop(1)}
		>
			{#each col1Panels as panel (panel.id)}
				<div class="hcc-card" draggable="true" on:dragstart={() => onPanelDragStart(panel.id)}>
					<div class="hcc-card-header">
						<span class="hcc-card-title">{panel.label}</span>
						<span class="hcc-drag-handle" title="Drag to move">⠿</span>
					</div>

					<!-- AGENTS PANEL -->
					{#if panel.id === 'agents'}
						<div class="hcc-filter-row">
							{#each ['all', 'hammer', 'jarvis'] as f}
								<button
									class="hcc-filter-chip {activeAgentFilter === f ? 'active' : ''}"
									on:click={() => (activeAgentFilter = f as typeof activeAgentFilter)}
								>
									{f === 'all' ? 'All' : f === 'hammer' ? '⚡ HaMm3r' : '🤖 Jarvis'}
								</button>
							{/each}
						</div>
						<div class="hcc-agent-list">
							{#each filteredAgents as agent}
								<div
									class="hcc-agent-card {pulseAgents.has(agent.id) ? 'hcc-agent-active' : ''}"
									style="--agent-color: {agent.color}"
								>
									<div class="hcc-agent-top">
										<span class="hcc-agent-icon">{agent.icon}</span>
										<div class="hcc-agent-info">
											<div class="hcc-agent-name">{agent.name}</div>
											<div class="hcc-agent-role">{agent.role}</div>
										</div>
										<div style="display:flex;align-items:center;gap:6px">
											{#if pulseAgents.has(agent.id)}
												<span class="hcc-live-badge">● LIVE</span>
											{/if}
											<span
												class="hcc-status-dot {pulseAgents.has(agent.id) ? 'hcc-status-pulse' : ''}"
												style="background:{statusColor(agent.status)}"
												title={agent.status}
											></span>
										</div>
									</div>
									<div class="hcc-agent-desc">{agent.description}</div>
									<div class="hcc-agent-meta">
										<span class="hcc-tag">{agent.model}</span>
										<span class="hcc-source-badge {agent.source}"
											>{agent.source === 'hammer' ? '⚡' : '🤖'} {agent.source}</span
										>
									</div>
									<div class="hcc-agent-tools">
										{#each agent.tools.slice(0, 4) as tool}
											<span class="hcc-tool-chip">{tool}</span>
										{/each}
										{#if agent.tools.length > 4}
											<span class="hcc-tool-chip dim">+{agent.tools.length - 4}</span>
										{/if}
									</div>
									<button class="hcc-agent-btn" on:click={() => goto(`/?agent=${agent.id}`)}>
										Chat with {agent.name} →
									</button>
								</div>
							{/each}
						</div>

						<!-- DREAM REVIEW PANEL -->
					{:else if panel.id === 'dreamReview'}
						<div class="hcc-dream-content">
							<div class="hcc-dream-date">📅 {dreamReviewDate}</div>
							<div class="hcc-dream-body">
								{#each dreamReviewContent.split('\n') as line}
									{#if line.startsWith('**') && line.endsWith('**')}
										<p class="hcc-dream-heading">{line.replaceAll('**', '')}</p>
									{:else if line.trim()}
										<p class="hcc-dream-p">{line}</p>
									{:else}
										<br />
									{/if}
								{/each}
							</div>
							<div class="hcc-dream-footer">
								<span class="hcc-dim">📁 iCloud/HaMm3r-KB/Dream-Review/</span>
							</div>
						</div>
					{/if}
				</div>
			{/each}
		</div>

		<!-- COL 2 -->
		<div
			class="hcc-col {dragOverCol === 2 ? 'drop-target' : ''}"
			on:dragover={(e) => onColDragOver(e, 2)}
			on:drop={() => onColDrop(2)}
		>
			{#each col2Panels as panel (panel.id)}
				<div class="hcc-card" draggable="true" on:dragstart={() => onPanelDragStart(panel.id)}>
					<div class="hcc-card-header">
						<span class="hcc-card-title">{panel.label}</span>
						<span class="hcc-drag-handle">⠿</span>
					</div>

					<!-- CONNECTORS PANEL -->
					{#if panel.id === 'connectors'}
						<div class="hcc-filter-row">
							{#each ['all', 'llm', 'data', 'service'] as f}
								<button
									class="hcc-filter-chip {activeConnectorFilter === f ? 'active' : ''}"
									on:click={() => (activeConnectorFilter = f as typeof activeConnectorFilter)}
								>
									{f === 'all'
										? 'All'
										: f === 'llm'
											? '🧠 LLM'
											: f === 'data'
												? '📁 Data'
												: '🔧 Service'}
								</button>
							{/each}
						</div>
						<div class="hcc-connector-list">
							{#each filteredConnectors as conn}
								<div class="hcc-connector-row">
									<span class="hcc-conn-icon">{conn.icon}</span>
									<div class="hcc-conn-info">
										<div class="hcc-conn-name">{conn.name}</div>
										<div class="hcc-conn-desc">{conn.description}</div>
									</div>
									<span
										class="hcc-status-dot"
										style="background:{statusColor(conn.status)}"
										title={conn.status}
									></span>
								</div>
							{/each}
						</div>

						<!-- MODEL STATS PANEL -->
					{:else if panel.id === 'modelStats'}
						<div class="hcc-model-list">
							{#if availableModels.length === 0}
								<p class="hcc-dim">No models loaded yet. Check connections above.</p>
							{:else}
								{#each availableModels.slice(0, 12) as model}
									<div class="hcc-model-row">
										<span
											class="hcc-model-dot"
											style="background: {model.owned_by?.includes('anthropic')
												? '#A855F7'
												: model.owned_by?.includes('openai')
													? '#34D399'
													: '#00D8FF'}"
										></span>
										<span class="hcc-model-name">{model.name ?? model.id}</span>
										<button
											class="hcc-model-use"
											on:click={() => goto(`/?models=${encodeURIComponent(model.id)}`)}
											>Use →</button
										>
									</div>
								{/each}
								{#if availableModels.length > 12}
									<p class="hcc-dim">+{availableModels.length - 12} more in chat</p>
								{/if}
							{/if}
						</div>
					{/if}
				</div>
			{/each}
		</div>

		<!-- COL 3 -->
		<div
			class="hcc-col {dragOverCol === 3 ? 'drop-target' : ''}"
			on:dragover={(e) => onColDragOver(e, 3)}
			on:drop={() => onColDrop(3)}
		>
			{#each col3Panels as panel (panel.id)}
				<div class="hcc-card" draggable="true" on:dragstart={() => onPanelDragStart(panel.id)}>
					<div class="hcc-card-header">
						<span class="hcc-card-title">{panel.label}</span>
						<span class="hcc-drag-handle">⠿</span>
					</div>

					<!-- SKILLS PANEL -->
					{#if panel.id === 'skills'}
						<input class="hcc-search" placeholder="Search skills..." bind:value={skillSearch} />
						<div class="hcc-filter-row hcc-filter-wrap">
							{#each ['all', 'hammer', 'jarvis', 'Dev', 'Research', 'Productivity', 'Personal', 'System'] as f}
								<button
									class="hcc-filter-chip {activeSkillFilter === f ? 'active' : ''}"
									on:click={() => (activeSkillFilter = f as typeof activeSkillFilter)}
								>
									{f === 'all' ? 'All' : f === 'hammer' ? '⚡' : f === 'jarvis' ? '🤖' : f}
								</button>
							{/each}
						</div>
						<div class="hcc-skill-grid">
							{#each filteredSkills as skill}
								<div class="hcc-skill-card">
									<span class="hcc-skill-icon">{skill.icon}</span>
									<div class="hcc-skill-info">
										<div class="hcc-skill-name">{skill.name}</div>
										<div class="hcc-skill-desc">{skill.description}</div>
									</div>
									<span class="hcc-source-badge {skill.source}"
										>{skill.source === 'hammer' ? '⚡' : '🤖'}</span
									>
								</div>
							{/each}
						</div>

						<!-- QUICK CHAT PANEL -->
					{:else if panel.id === 'quickChat'}
						<!-- LIVE ACTIVITY FEED injected above quick chat -->
						<div class="hcc-activity-feed">
							<div class="hcc-activity-header">
								<span class="hcc-activity-dot"></span>
								<span>Live Activity</span>
								<span class="hcc-activity-count">{liveActivity.length}</span>
							</div>
							<div class="hcc-activity-list">
								{#if liveActivity.length === 0}
									<div class="hcc-dim" style="padding:8px 0;font-size:0.75rem">
										Waiting for activity…
									</div>
								{/if}
								{#each liveActivity as evt (evt.id)}
									<div class="hcc-activity-item hcc-activity-{evt.type}">
										<span class="hcc-activity-time"
											>{evt.timestamp.toLocaleTimeString([], {
												hour: '2-digit',
												minute: '2-digit',
												second: '2-digit'
											})}</span
										>
										<span class="hcc-activity-msg">{evt.message}</span>
									</div>
								{/each}
							</div>
						</div>
						<div class="hcc-qc-container">
							<div class="hcc-qc-history">
								{#if quickChatHistory.length === 0}
									<p class="hcc-dim">Start a quick chat — you'll be taken to the full chat view.</p>
								{/if}
								{#each quickChatHistory as msg}
									<div class="hcc-qc-msg {msg.role}">
										<span class="hcc-qc-role">{msg.role === 'user' ? '🧑' : '⚡'}</span>
										<span>{msg.text}</span>
									</div>
								{/each}
							</div>
							<div class="hcc-qc-input-row">
								<input
									class="hcc-qc-input"
									placeholder="Ask anything..."
									bind:value={quickChatInput}
									on:keydown={(e) => e.key === 'Enter' && sendQuickChat()}
								/>
								<button class="hcc-btn-accent" on:click={sendQuickChat}>→</button>
							</div>
							<div class="hcc-qc-shortcuts">
								{#each ['VA claim status', 'Market analysis', 'Vehicle diagnostic', 'Research topic'] as sc}
									<button
										class="hcc-shortcut-chip"
										on:click={() => {
											quickChatInput = sc;
											sendQuickChat();
										}}>{sc}</button
									>
								{/each}
							</div>
						</div>
					{/if}
				</div>
			{/each}
		</div>
	</div>
	<!-- /grid -->
</div>

<!-- /root -->

<style>
	/* ── CSS Custom Properties (set by JS) ── */
	:global(:root) {
		--hcc-bg: #090d16;
		--hcc-surface: #131b2e;
		--hcc-border: rgba(255, 255, 255, 0.06);
		--hcc-text: #e2e8f0;
		--hcc-muted: #94a3b8;
		--hcc-dim: #64748b;
		--hcc-accent: #00d8ff;
		--hcc-glow: rgba(0, 216, 255, 0.15);
		--hcc-glow-sm: rgba(0, 216, 255, 0.08);
		--hcc-font: 'IBM Plex Mono', monospace;
	}

	@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Chakra+Petch:wght@400;500;600&display=swap');

	/* ── Root ── */
	.hcc-root {
		min-height: 100vh;
		background: var(--hcc-bg);
		color: var(--hcc-text);
		font-family: var(--hcc-font);
		padding: 0;
	}

	/* ── Top 6 Model Bar ── */
	.hcc-model-bar {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 8px 16px;
		border-bottom: 1px solid var(--hcc-border);
		background: rgba(0, 0, 0, 0.25);
		overflow-x: auto;
		scrollbar-width: none;
		flex-wrap: nowrap;
	}
	.hcc-model-bar::-webkit-scrollbar {
		display: none;
	}
	.hcc-model-pill {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 5px 12px;
		border-radius: 20px;
		border: 1px solid color-mix(in srgb, var(--mp-color, #888) 40%, transparent);
		background: color-mix(in srgb, var(--mp-color, #888) 10%, transparent);
		color: var(--hcc-text);
		font-size: 0.72rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.15s ease;
		white-space: nowrap;
		text-decoration: none;
	}
	.hcc-model-pill:hover {
		background: color-mix(in srgb, var(--mp-color, #888) 25%, transparent);
		border-color: var(--mp-color, #888);
		transform: translateY(-1px);
		box-shadow: 0 3px 10px color-mix(in srgb, var(--mp-color, #888) 25%, transparent);
	}
	.hcc-model-logo {
		width: 16px;
		height: 16px;
		object-fit: contain;
		border-radius: 3px;
		flex-shrink: 0;
	}
	.hcc-model-label {
		font-size: 0.72rem;
	}
	.hcc-brain-pill {
		--mp-color: #a78bfa;
		margin-left: auto;
		flex-shrink: 0;
	}

	/* ── Top Bar ── */
	.hcc-topbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 12px 20px;
		background: var(--hcc-surface);
		border-bottom: 1px solid var(--hcc-border);
		position: sticky;
		top: 0;
		z-index: 100;
		gap: 12px;
	}
	.hcc-topbar-left {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.hcc-topbar-right {
		display: flex;
		align-items: center;
		gap: 10px;
		flex-wrap: wrap;
	}
	.hcc-logo {
		font-size: 28px;
		line-height: 1;
	}
	.hcc-title {
		font-size: 16px;
		font-weight: 600;
		color: var(--hcc-accent);
		letter-spacing: 0.05em;
	}
	.hcc-subtitle {
		font-size: 11px;
		color: var(--hcc-dim);
		margin-top: 1px;
	}
	.hcc-status-bar {
		display: flex;
		gap: 6px;
		flex-wrap: wrap;
	}
	.hcc-status-chip {
		font-size: 10px;
		padding: 2px 8px;
		border-radius: 999px;
		border: 1px solid;
		font-weight: 500;
	}
	.hcc-btn-icon {
		background: transparent;
		border: 1px solid var(--hcc-border);
		border-radius: 8px;
		padding: 6px 10px;
		cursor: pointer;
		font-size: 16px;
		color: var(--hcc-muted);
		transition: all 0.15s;
	}
	.hcc-btn-icon:hover {
		border-color: var(--hcc-accent);
		color: var(--hcc-accent);
	}

	/* ── Grid ── */
	.hcc-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 16px;
		padding: 16px;
	}
	@media (max-width: 1100px) {
		.hcc-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}
	@media (max-width: 720px) {
		.hcc-grid {
			grid-template-columns: 1fr;
		}
	}

	.hcc-col {
		display: flex;
		flex-direction: column;
		gap: 16px;
		min-height: 100px;
		border-radius: 12px;
		padding: 4px;
		transition: background 0.15s;
	}
	.hcc-col.drop-target {
		background: var(--hcc-glow-sm);
	}

	/* ── Card ── */
	.hcc-card {
		background: var(--hcc-surface);
		border: 1px solid var(--hcc-border);
		border-radius: 12px;
		overflow: hidden;
		transition:
			border-color 0.2s,
			box-shadow 0.2s;
	}
	.hcc-card:hover {
		border-color: var(--hcc-accent);
		box-shadow: 0 0 24px var(--hcc-glow-sm);
	}
	.hcc-card-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 12px 14px 8px;
		border-bottom: 1px solid var(--hcc-border);
	}
	.hcc-card-title {
		font-size: 12px;
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--hcc-accent);
	}
	.hcc-drag-handle {
		cursor: grab;
		color: var(--hcc-dim);
		font-size: 16px;
	}
	.hcc-drag-handle:active {
		cursor: grabbing;
	}

	/* ── Filter chips ── */
	.hcc-filter-row {
		display: flex;
		gap: 6px;
		padding: 8px 14px;
		flex-wrap: wrap;
	}
	.hcc-filter-wrap {
		flex-wrap: wrap;
	}
	.hcc-filter-chip {
		font-size: 10px;
		padding: 3px 10px;
		border-radius: 999px;
		border: 1px solid var(--hcc-border);
		background: transparent;
		color: var(--hcc-muted);
		cursor: pointer;
		font-family: var(--hcc-font);
		transition: all 0.15s;
	}
	.hcc-filter-chip.active,
	.hcc-filter-chip:hover {
		border-color: var(--hcc-accent);
		color: var(--hcc-accent);
		background: var(--hcc-glow-sm);
	}

	/* ── Agents ── */
	.hcc-agent-list {
		display: flex;
		flex-direction: column;
		gap: 10px;
		padding: 10px 14px 14px;
		max-height: 520px;
		overflow-y: auto;
	}
	.hcc-agent-card {
		background: color-mix(in srgb, var(--hcc-bg) 60%, transparent);
		border: 1px solid var(--hcc-border);
		border-radius: 10px;
		padding: 12px;
		transition:
			border-color 0.15s,
			box-shadow 0.15s;
	}
	.hcc-agent-card:hover {
		border-color: var(--agent-color, var(--hcc-accent));
		box-shadow: 0 0 16px color-mix(in srgb, var(--agent-color, #00d8ff) 20%, transparent);
	}
	.hcc-agent-top {
		display: flex;
		align-items: center;
		gap: 10px;
		margin-bottom: 6px;
	}
	.hcc-agent-icon {
		font-size: 22px;
		line-height: 1;
	}
	.hcc-agent-name {
		font-size: 13px;
		font-weight: 600;
		color: var(--hcc-text);
	}
	.hcc-agent-role {
		font-size: 10px;
		color: var(--hcc-dim);
	}
	.hcc-agent-desc {
		font-size: 11px;
		color: var(--hcc-muted);
		margin-bottom: 8px;
		line-height: 1.5;
	}
	.hcc-agent-meta {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-bottom: 6px;
	}
	.hcc-agent-tools {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		margin-bottom: 10px;
	}
	.hcc-tool-chip {
		font-size: 9px;
		padding: 2px 7px;
		border-radius: 4px;
		background: color-mix(in srgb, var(--hcc-accent) 8%, transparent);
		color: var(--hcc-accent);
		border: 1px solid color-mix(in srgb, var(--hcc-accent) 20%, transparent);
	}
	.hcc-tool-chip.dim {
		color: var(--hcc-dim);
		background: transparent;
		border-color: var(--hcc-border);
	}
	.hcc-agent-btn {
		width: 100%;
		padding: 7px;
		border-radius: 7px;
		background: var(--hcc-glow-sm);
		border: 1px solid var(--hcc-accent);
		color: var(--hcc-accent);
		font-size: 11px;
		font-family: var(--hcc-font);
		cursor: pointer;
		transition: background 0.15s;
	}
	.hcc-agent-btn:hover {
		background: var(--hcc-glow);
	}

	/* ── Status dot ── */
	.hcc-status-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		flex-shrink: 0;
	}

	/* ── Tags ── */
	.hcc-tag {
		font-size: 9px;
		padding: 2px 7px;
		border-radius: 4px;
		background: color-mix(in srgb, var(--hcc-muted) 10%, transparent);
		color: var(--hcc-muted);
		border: 1px solid var(--hcc-border);
	}
	.hcc-source-badge {
		font-size: 9px;
		padding: 2px 7px;
		border-radius: 4px;
		font-weight: 600;
	}
	.hcc-source-badge.hammer {
		background: color-mix(in srgb, #00d8ff 10%, transparent);
		color: #00d8ff;
	}
	.hcc-source-badge.jarvis {
		background: color-mix(in srgb, #a855f7 10%, transparent);
		color: #a855f7;
	}

	/* ── Connectors ── */
	.hcc-connector-list {
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: 8px 14px 14px;
		max-height: 460px;
		overflow-y: auto;
	}
	.hcc-connector-row {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 10px;
		border-radius: 8px;
		transition: background 0.1s;
	}
	.hcc-connector-row:hover {
		background: var(--hcc-glow-sm);
	}
	.hcc-conn-icon {
		font-size: 18px;
		width: 28px;
		text-align: center;
		flex-shrink: 0;
	}
	.hcc-conn-name {
		font-size: 12px;
		font-weight: 500;
		color: var(--hcc-text);
	}
	.hcc-conn-desc {
		font-size: 10px;
		color: var(--hcc-dim);
	}
	.hcc-conn-info {
		flex: 1;
		min-width: 0;
	}

	/* ── Model Stats ── */
	.hcc-model-list {
		padding: 10px 14px 14px;
	}
	.hcc-model-row {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 6px 0;
		border-bottom: 1px solid var(--hcc-border);
	}
	.hcc-model-dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		flex-shrink: 0;
	}
	.hcc-model-name {
		font-size: 11px;
		color: var(--hcc-text);
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.hcc-model-use {
		font-size: 10px;
		padding: 2px 8px;
		border-radius: 5px;
		border: 1px solid var(--hcc-accent);
		background: transparent;
		color: var(--hcc-accent);
		cursor: pointer;
		font-family: var(--hcc-font);
	}
	.hcc-model-use:hover {
		background: var(--hcc-glow-sm);
	}

	/* ── Skills ── */
	.hcc-search {
		width: calc(100% - 28px);
		margin: 8px 14px 2px;
		padding: 7px 12px;
		background: var(--hcc-bg);
		border: 1px solid var(--hcc-border);
		border-radius: 8px;
		color: var(--hcc-text);
		font-family: var(--hcc-font);
		font-size: 12px;
		outline: none;
	}
	.hcc-search:focus {
		border-color: var(--hcc-accent);
	}
	.hcc-skill-grid {
		display: flex;
		flex-direction: column;
		gap: 4px;
		padding: 6px 14px 14px;
		max-height: 460px;
		overflow-y: auto;
	}
	.hcc-skill-card {
		display: flex;
		align-items: flex-start;
		gap: 10px;
		padding: 8px 10px;
		border-radius: 8px;
		border: 1px solid transparent;
		transition:
			background 0.1s,
			border-color 0.1s;
	}
	.hcc-skill-card:hover {
		background: var(--hcc-glow-sm);
		border-color: var(--hcc-border);
	}
	.hcc-skill-icon {
		font-size: 16px;
		margin-top: 1px;
		flex-shrink: 0;
	}
	.hcc-skill-name {
		font-size: 12px;
		font-weight: 500;
		color: var(--hcc-text);
	}
	.hcc-skill-desc {
		font-size: 10px;
		color: var(--hcc-dim);
	}
	.hcc-skill-info {
		flex: 1;
	}

	/* ── Dream Review ── */
	.hcc-dream-content {
		padding: 14px;
	}
	.hcc-dream-date {
		font-size: 11px;
		color: var(--hcc-accent);
		margin-bottom: 10px;
		font-weight: 600;
	}
	.hcc-dream-body {
		max-height: 280px;
		overflow-y: auto;
	}
	.hcc-dream-heading {
		font-size: 13px;
		font-weight: 600;
		color: var(--hcc-text);
		margin: 8px 0 4px;
	}
	.hcc-dream-p {
		font-size: 12px;
		color: var(--hcc-muted);
		line-height: 1.6;
		margin: 4px 0;
	}
	.hcc-dream-footer {
		margin-top: 10px;
		padding-top: 8px;
		border-top: 1px solid var(--hcc-border);
	}

	/* ── Quick Chat ── */
	.hcc-qc-container {
		padding: 10px 14px 14px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.hcc-qc-history {
		min-height: 60px;
		max-height: 160px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.hcc-qc-msg {
		display: flex;
		gap: 8px;
		font-size: 12px;
	}
	.hcc-qc-role {
		flex-shrink: 0;
	}
	.hcc-qc-msg.user {
		color: var(--hcc-text);
	}
	.hcc-qc-msg.assistant {
		color: var(--hcc-accent);
	}
	.hcc-qc-input-row {
		display: flex;
		gap: 8px;
	}
	.hcc-qc-input {
		flex: 1;
		padding: 8px 12px;
		background: var(--hcc-bg);
		border: 1px solid var(--hcc-border);
		border-radius: 8px;
		color: var(--hcc-text);
		font-family: var(--hcc-font);
		font-size: 12px;
		outline: none;
	}
	.hcc-qc-input:focus {
		border-color: var(--hcc-accent);
	}
	.hcc-qc-shortcuts {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}
	.hcc-shortcut-chip {
		font-size: 10px;
		padding: 4px 10px;
		border-radius: 999px;
		background: transparent;
		border: 1px solid var(--hcc-border);
		color: var(--hcc-muted);
		cursor: pointer;
		font-family: var(--hcc-font);
		transition: all 0.15s;
	}
	.hcc-shortcut-chip:hover {
		border-color: var(--hcc-accent);
		color: var(--hcc-accent);
	}

	/* ── Buttons ── */
	.hcc-btn-accent {
		padding: 8px 16px;
		background: var(--hcc-accent);
		border: none;
		border-radius: 8px;
		color: #000;
		font-family: var(--hcc-font);
		font-size: 12px;
		font-weight: 600;
		cursor: pointer;
		transition: opacity 0.15s;
	}
	.hcc-btn-accent:hover {
		opacity: 0.85;
	}
	.hcc-btn-ghost {
		padding: 8px 16px;
		background: transparent;
		border: 1px solid var(--hcc-border);
		border-radius: 8px;
		color: var(--hcc-muted);
		font-family: var(--hcc-font);
		font-size: 12px;
		cursor: pointer;
	}
	.hcc-btn-ghost:hover {
		border-color: var(--hcc-accent);
		color: var(--hcc-accent);
	}

	/* ── Settings Panel ── */
	.hcc-settings-overlay {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.6);
		z-index: 999;
		display: flex;
		align-items: flex-start;
		justify-content: flex-end;
		padding: 70px 20px 20px;
	}
	.hcc-settings-panel {
		background: var(--hcc-surface);
		border: 1px solid var(--hcc-border);
		border-radius: 14px;
		width: 360px;
		max-height: 80vh;
		display: flex;
		flex-direction: column;
		box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5);
	}
	.hcc-settings-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 14px 16px;
		border-bottom: 1px solid var(--hcc-border);
		font-size: 13px;
		font-weight: 600;
		color: var(--hcc-accent);
	}
	.hcc-settings-header button {
		background: none;
		border: none;
		color: var(--hcc-muted);
		cursor: pointer;
		font-size: 16px;
	}
	.hcc-settings-tabs {
		display: flex;
		gap: 2px;
		padding: 8px 10px;
		border-bottom: 1px solid var(--hcc-border);
	}
	.hcc-tab {
		flex: 1;
		padding: 6px 8px;
		border-radius: 7px;
		border: none;
		background: transparent;
		color: var(--hcc-dim);
		font-family: var(--hcc-font);
		font-size: 11px;
		cursor: pointer;
		transition: all 0.15s;
	}
	.hcc-tab.active {
		background: var(--hcc-glow-sm);
		color: var(--hcc-accent);
	}
	.hcc-settings-body {
		flex: 1;
		overflow-y: auto;
		padding: 14px 16px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	.hcc-settings-footer {
		display: flex;
		gap: 8px;
		padding: 12px 16px;
		border-top: 1px solid var(--hcc-border);
		justify-content: flex-end;
	}
	.hcc-setting-group {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.hcc-label {
		font-size: 11px;
		font-weight: 600;
		color: var(--hcc-muted);
		text-transform: uppercase;
		letter-spacing: 0.08em;
	}
	.hcc-hint {
		font-size: 11px;
		color: var(--hcc-dim);
		line-height: 1.5;
	}
	.hcc-dim {
		font-size: 11px;
		color: var(--hcc-dim);
	}

	/* Colors */
	.hcc-color-row {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
	}
	.hcc-color-swatch {
		width: 28px;
		height: 28px;
		border-radius: 50%;
		border: 2px solid transparent;
		cursor: pointer;
		transition:
			transform 0.15s,
			border-color 0.15s;
	}
	.hcc-color-swatch:hover {
		transform: scale(1.15);
	}
	.hcc-color-swatch.active {
		border-color: var(--hcc-text);
		transform: scale(1.15);
	}

	/* Theme */
	.hcc-theme-row {
		display: flex;
		gap: 8px;
	}
	.hcc-theme-btn {
		flex: 1;
		padding: 8px 6px;
		border-radius: 8px;
		border: 1px solid var(--hcc-border);
		background: transparent;
		color: var(--hcc-muted);
		font-family: var(--hcc-font);
		font-size: 11px;
		cursor: pointer;
		transition: all 0.15s;
	}
	.hcc-theme-btn.active,
	.hcc-theme-btn:hover {
		border-color: var(--hcc-accent);
		color: var(--hcc-accent);
		background: var(--hcc-glow-sm);
	}

	/* Fonts */
	.hcc-font-btn {
		width: 100%;
		padding: 10px 12px;
		border-radius: 8px;
		border: 1px solid var(--hcc-border);
		background: transparent;
		color: var(--hcc-muted);
		font-size: 13px;
		cursor: pointer;
		text-align: left;
		transition: all 0.15s;
	}
	.hcc-font-btn.active,
	.hcc-font-btn:hover {
		border-color: var(--hcc-accent);
		color: var(--hcc-accent);
		background: var(--hcc-glow-sm);
	}

	/* Toggle rows */
	.hcc-toggle-row {
		display: flex;
		align-items: center;
		gap: 10px;
		font-size: 12px;
		color: var(--hcc-text);
		cursor: pointer;
	}
	.hcc-toggle-row input {
		accent-color: var(--hcc-accent);
		width: 14px;
		height: 14px;
		cursor: pointer;
	}

	/* Scrollbar styling */
	.hcc-agent-list::-webkit-scrollbar,
	.hcc-connector-list::-webkit-scrollbar,
	.hcc-skill-grid::-webkit-scrollbar,
	.hcc-qc-history::-webkit-scrollbar,
	.hcc-dream-body::-webkit-scrollbar,
	.hcc-settings-body::-webkit-scrollbar {
		width: 4px;
	}
	.hcc-agent-list::-webkit-scrollbar-track,
	.hcc-connector-list::-webkit-scrollbar-track,
	.hcc-skill-grid::-webkit-scrollbar-track,
	.hcc-settings-body::-webkit-scrollbar-track {
		background: transparent;
	}
	.hcc-agent-list::-webkit-scrollbar-thumb,
	.hcc-connector-list::-webkit-scrollbar-thumb,
	.hcc-skill-grid::-webkit-scrollbar-thumb,
	.hcc-settings-body::-webkit-scrollbar-thumb {
		background: var(--hcc-border);
		border-radius: 2px;
	}

	/* ── Live Activity Feed ── */
	.hcc-activity-feed {
		border: 1px solid var(--hcc-border);
		border-radius: 8px;
		padding: 10px 12px;
		margin-bottom: 10px;
		background: rgba(0, 0, 0, 0.2);
	}
	.hcc-activity-header {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.7rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--hcc-accent);
		margin-bottom: 8px;
	}
	.hcc-activity-dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		background: var(--hcc-accent);
		animation: hcc-blink 1.2s ease-in-out infinite;
	}
	.hcc-activity-count {
		margin-left: auto;
		background: var(--hcc-border);
		border-radius: 10px;
		padding: 1px 6px;
		font-size: 0.65rem;
		color: var(--hcc-muted);
	}
	.hcc-activity-list {
		display: flex;
		flex-direction: column;
		gap: 4px;
		max-height: 140px;
		overflow-y: auto;
	}
	.hcc-activity-item {
		display: flex;
		gap: 8px;
		font-size: 0.72rem;
		padding: 3px 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.04);
		animation: hcc-slide-in 0.3s ease;
	}
	.hcc-activity-time {
		color: var(--hcc-muted);
		white-space: nowrap;
		font-family: monospace;
		font-size: 0.65rem;
	}
	.hcc-activity-msg {
		color: var(--hcc-text);
		flex: 1;
	}
	.hcc-activity-chat .hcc-activity-msg {
		color: var(--hcc-accent);
	}
	.hcc-activity-system .hcc-activity-msg {
		color: var(--hcc-muted);
		font-style: italic;
	}
	.hcc-activity-agent .hcc-activity-msg {
		color: #34d399;
	}

	/* ── Agent live pulse ── */
	.hcc-agent-active {
		border-color: var(--agent-color) !important;
		box-shadow: 0 0 12px color-mix(in srgb, var(--agent-color) 30%, transparent) !important;
	}
	.hcc-live-badge {
		font-size: 0.6rem;
		font-weight: 800;
		color: #34d399;
		letter-spacing: 0.05em;
		animation: hcc-blink 1s ease-in-out infinite;
	}
	.hcc-status-pulse {
		animation: hcc-ring 1s ease-in-out infinite;
	}

	@keyframes hcc-blink {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0.3;
		}
	}
	@keyframes hcc-ring {
		0% {
			box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.6);
		}
		70% {
			box-shadow: 0 0 0 6px rgba(52, 211, 153, 0);
		}
		100% {
			box-shadow: 0 0 0 0 rgba(52, 211, 153, 0);
		}
	}
	@keyframes hcc-slide-in {
		from {
			opacity: 0;
			transform: translateY(-4px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
