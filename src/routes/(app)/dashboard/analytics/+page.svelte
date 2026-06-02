<script lang="ts">
	import { onMount } from 'svelte';

	let stats = {
		tokensToday: 0,
		tokensCost: '$0.00',
		totalChats: 0,
		modelBreakdown: [] as { name: string; count: number; pct: number; color: string }[],
		recentChats: [] as { title: string; model: string; time: string }[],
		agentUsage: [] as { name: string; count: number; emoji: string }[],
	};

	let loading = true;

	const MODEL_COLORS: Record<string, string> = {
		'claude': '#00D8FF',
		'llama': '#818CF8',
		'mistral': '#A855F7',
		'gemma': '#FF6B8A',
		'phi': '#F59E0B',
	};

	function getModelColor(model: string): string {
		const key = Object.keys(MODEL_COLORS).find(k => model.toLowerCase().includes(k));
		return key ? MODEL_COLORS[key] : '#718096';
	}

	async function loadAnalytics() {
		const token = localStorage.getItem('token');
		if (!token) return;

		try {
			// Fetch recent chats
			const res = await fetch('/api/v1/chats/?page=1', {
				headers: { 'Authorization': `Bearer ${token}` }
			});
			if (!res.ok) return;
			const data = await res.json();
			const chats = Array.isArray(data) ? data : data.items || [];

			// Build stats
			const modelCounts: Record<string, number> = {};
			const agentCounts: Record<string, number> = {};
			let totalTokens = 0;

			// Filter to today
			const today = new Date();
			today.setHours(0, 0, 0, 0);

			const todayChats = chats.filter((c: any) => {
				const d = new Date((c.created_at || 0) * 1000);
				return d >= today;
			});

			stats.totalChats = todayChats.length;

			// Parse model usage from chats
			for (const chat of chats.slice(0, 50)) {
				try {
					const chatData = typeof chat.chat === 'string' ? JSON.parse(chat.chat) : chat.chat;
					const messages = chatData?.messages || [];
					for (const msg of messages) {
						const model = msg.model || msg.info?.model || '';
						if (model) {
							modelCounts[model] = (modelCounts[model] || 0) + 1;
						}
						// Estimate tokens
						if (msg.info?.usage) {
							totalTokens += (msg.info.usage.prompt_tokens || 0) + (msg.info.usage.completion_tokens || 0);
						}
					}
				} catch {}
			}

			stats.tokensToday = totalTokens;
			// Rough cost estimate (Claude ~$3/1M input, $15/1M output, average ~$6/1M)
			const estimatedCost = (totalTokens / 1000000) * 6;
			stats.tokensCost = `$${estimatedCost.toFixed(3)}`;

			// Build model breakdown
			const total = Object.values(modelCounts).reduce((a, b) => a + b, 0) || 1;
			stats.modelBreakdown = Object.entries(modelCounts)
				.sort((a, b) => b[1] - a[1])
				.slice(0, 5)
				.map(([name, count]) => ({
					name: name.length > 20 ? name.slice(0, 20) + '…' : name,
					count,
					pct: Math.round((count / total) * 100),
					color: getModelColor(name)
				}));

			// Recent chats list
			stats.recentChats = chats.slice(0, 8).map((c: any) => ({
				title: c.title || 'Untitled',
				model: c.models?.[0] || '—',
				time: new Date((c.updated_at || c.created_at || 0) * 1000).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
			}));

		} catch (err) {
			console.error('Analytics load error:', err);
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		loadAnalytics();
		const interval = setInterval(loadAnalytics, 60000);
		return () => clearInterval(interval);
	});
</script>

<div class="analytics-page">
	<div class="page-header">
		<a href="/dashboard" class="back-btn">← Dashboard</a>
		<div class="header-center">
			<h1>📊 Analytics</h1>
			<p>Real-time usage across HaMm3r OS</p>
		</div>
		<button class="refresh-btn" on:click={loadAnalytics}>↻ Refresh</button>
	</div>

	{#if loading}
		<div class="loading">Loading analytics…</div>
	{:else}
	<div class="analytics-body">

		<!-- Top stats -->
		<div class="stats-grid">
			<div class="stat-card">
				<div class="stat-val" style="color:#00D8FF">{stats.tokensToday.toLocaleString()}</div>
				<div class="stat-lbl">Tokens Today</div>
			</div>
			<div class="stat-card">
				<div class="stat-val" style="color:#818CF8">{stats.tokensCost}</div>
				<div class="stat-lbl">Est. Cost</div>
			</div>
			<div class="stat-card">
				<div class="stat-val" style="color:#A855F7">{stats.totalChats}</div>
				<div class="stat-lbl">Chats Today</div>
			</div>
			<div class="stat-card">
				<div class="stat-val" style="color:#48BB78">{stats.modelBreakdown.length}</div>
				<div class="stat-lbl">Models Used</div>
			</div>
		</div>

		<div class="two-col">
			<!-- Model breakdown -->
			<div class="panel">
				<div class="panel-title">Model Usage</div>
				{#if stats.modelBreakdown.length}
					{#each stats.modelBreakdown as m}
						<div class="model-row">
							<span class="model-name">{m.name}</span>
							<div class="bar-track">
								<div class="bar-fill" style="width:{m.pct}%;background:{m.color}"></div>
							</div>
							<span class="model-pct" style="color:{m.color}">{m.pct}%</span>
						</div>
					{/each}
				{:else}
					<div class="empty">No model data yet — start a chat!</div>
				{/if}
			</div>

			<!-- Recent chats -->
			<div class="panel">
				<div class="panel-title">Recent Chats</div>
				{#if stats.recentChats.length}
					{#each stats.recentChats as chat}
						<div class="chat-row">
							<div class="chat-info">
								<span class="chat-title">{chat.title}</span>
								<span class="chat-model">{chat.model}</span>
							</div>
							<span class="chat-time">{chat.time}</span>
						</div>
					{/each}
				{:else}
					<div class="empty">No chats yet today</div>
				{/if}
			</div>
		</div>

	</div>
	{/if}
</div>

<style>
	.analytics-page {
		min-height: 100vh;
		background: #090D16;
		color: #E2E8F0;
		font-family: 'Inter', -apple-system, sans-serif;
	}
	.page-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20px 32px;
		border-bottom: 1px solid rgba(255,255,255,0.06);
		background: #131B2E;
	}
	.back-btn, .refresh-btn {
		color: #718096;
		text-decoration: none;
		font-size: 13px;
		font-weight: 500;
		background: none;
		border: none;
		cursor: pointer;
		font-family: inherit;
		transition: color 0.15s;
	}
	.back-btn:hover, .refresh-btn:hover { color: #818CF8; }
	.header-center { text-align: center; }
	.header-center h1 { font-size: 20px; font-weight: 700; margin: 0 0 4px; }
	.header-center p { font-size: 13px; color: #718096; margin: 0; }
	.loading { text-align: center; padding: 60px; color: #718096; }
	.analytics-body { padding: 28px 32px; max-width: 1100px; margin: 0 auto; }
	.stats-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 14px;
		margin-bottom: 24px;
	}
	.stat-card {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.06);
		border-radius: 14px;
		padding: 20px;
		text-align: center;
	}
	.stat-val { font-size: 28px; font-weight: 700; }
	.stat-lbl { font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
	.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
	.panel {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.06);
		border-radius: 14px;
		padding: 20px;
	}
	.panel-title {
		font-size: 11px;
		font-weight: 700;
		color: #818CF8;
		text-transform: uppercase;
		letter-spacing: 1.2px;
		margin-bottom: 16px;
	}
	.model-row { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
	.model-name { font-size: 12px; color: #A0AEC0; width: 100px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
	.bar-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
	.model-pct { font-size: 11px; width: 32px; text-align: right; font-weight: 600; }
	.chat-row { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
	.chat-row:last-child { border-bottom: none; }
	.chat-info { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
	.chat-title { font-size: 13px; color: #E2E8F0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.chat-model { font-size: 11px; color: #718096; }
	.chat-time { font-size: 11px; color: #4A5568; white-space: nowrap; margin-left: 12px; }
	.empty { font-size: 13px; color: #4A5568; text-align: center; padding: 20px 0; }
</style>
