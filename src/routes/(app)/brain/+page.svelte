<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { user, models } from '$lib/stores';
	import { goto } from '$app/navigation';

	// ── Node types ────────────────────────────────────────────────────────────
	interface BrainNode {
		id: string;
		label: string;
		type: 'chat' | 'agent' | 'model' | 'memory' | 'project' | 'skill' | 'connector';
		size: number;
		color: string;
		x: number;
		y: number;
		vx: number;
		vy: number;
		pinned?: boolean;
		meta?: string;
		href?: string;
	}

	interface BrainEdge {
		source: string;
		target: string;
		strength: number;
	}

	// ── State ─────────────────────────────────────────────────────────────────
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;
	let width = 1200;
	let height = 800;
	let nodes: BrainNode[] = [];
	let edges: BrainEdge[] = [];
	let animFrame: number;
	let hoveredNode: BrainNode | null = null;
	let selectedNode: BrainNode | null = null;
	let dragging: BrainNode | null = null;
	let panX = 0;
	let panY = 0;
	let zoom = 1;
	let isPanning = false;
	let lastMouseX = 0;
	let lastMouseY = 0;
	let loading = true;
	let chatCount = 0;

	// ── Color palette ─────────────────────────────────────────────────────────
	const COLORS = {
		chat: '#00D8FF',
		agent: '#34D399',
		model: '#D97706',
		memory: '#A78BFA',
		project: '#F472B6',
		skill: '#FBBF24',
		connector: '#60A5FA',
		center: '#F59E0B'
	};

	// ── Build graph from live data ─────────────────────────────────────────────
	async function buildGraph() {
		loading = true;
		nodes = [];
		edges = [];

		const cx = width / 2;
		const cy = height / 2;

		// Central node: Ronald / HaMm3r OS
		nodes.push({
			id: 'center',
			label: '⚡ HaMm3r OS',
			type: 'project',
			size: 28,
			color: COLORS.center,
			x: cx,
			y: cy,
			vx: 0,
			vy: 0,
			pinned: true,
			meta: 'AG Attack LLC · Your Personal AI OS'
		});

		// Agent nodes
		const agents = [
			{ id: 'va-specialist', label: '🎖️ VA Specialist', model: 'gpt-4o', color: '#00D8FF' },
			{ id: 'the-hawk', label: '🦅 The Hawk', model: 'claude-sonnet-4.5', color: '#34D399' },
			{ id: 'investment-manager', label: '📈 Investment Mgr', model: 'gpt-4o', color: '#FBBF24' },
			{ id: 'vehicle-tech', label: '🔧 Vehicle Tech', model: 'gpt-4o-mini', color: '#F97316' },
			{
				id: 'code-reviewer',
				label: '👁️ Code Reviewer',
				model: 'claude-sonnet-4.5',
				color: '#A78BFA'
			},
			{ id: 'inbox-triager', label: '📬 Inbox Triager', model: 'gpt-4o-mini', color: '#60A5FA' },
			{
				id: 'research-monitor',
				label: '🔬 Research Monitor',
				model: 'claude-sonnet-4.5',
				color: '#34D399'
			},
			{ id: 'deep-research', label: '🧬 Deep Research', model: 'gpt-4o', color: '#F472B6' }
		];

		const agentAngle = (2 * Math.PI) / agents.length;
		agents.forEach((a, i) => {
			const angle = i * agentAngle - Math.PI / 2;
			const r = 180;
			nodes.push({
				id: a.id,
				label: a.label,
				type: 'agent',
				size: 18,
				color: a.color,
				x: cx + r * Math.cos(angle),
				y: cy + r * Math.sin(angle),
				vx: 0,
				vy: 0,
				meta: `Model: ${a.model}`
			});
			edges.push({ source: 'center', target: a.id, strength: 0.8 });
		});

		// Model nodes (pinned models)
		const modelNodes = [
			{ id: 'm-haiku', label: 'Haiku 4.5', color: '#D97706' },
			{ id: 'm-sonnet', label: 'Sonnet 4.5', color: '#D97706' },
			{ id: 'm-gpt4o', label: 'GPT-4o', color: '#10A37F' },
			{ id: 'm-gpt41', label: 'GPT-4.1', color: '#10A37F' },
			{ id: 'm-gemini', label: 'Gemini 2.5 Pro', color: '#4285F4' },
			{ id: 'm-llama4', label: 'Llama 4', color: '#0082FB' }
		];
		const modelAngle = (2 * Math.PI) / modelNodes.length;
		modelNodes.forEach((m, i) => {
			const angle = i * modelAngle + Math.PI / 6;
			const r = 330;
			nodes.push({
				id: m.id,
				label: m.label,
				type: 'model',
				size: 14,
				color: m.color,
				x: cx + r * Math.cos(angle),
				y: cy + r * Math.sin(angle),
				vx: 0,
				vy: 0
			});
			edges.push({ source: 'center', target: m.id, strength: 0.3 });
		});

		// Connector nodes
		const connectors = [
			{ id: 'cn-openrouter', label: '🔌 OpenRouter', color: '#6366F1' },
			{ id: 'cn-anthropic', label: '🟠 Anthropic', color: '#D97706' },
			{ id: 'cn-openai', label: '🟢 OpenAI', color: '#10A37F' },
			{ id: 'cn-github', label: '🐙 GitHub', color: '#E5E7EB' },
			{ id: 'cn-icloud', label: '☁️ iCloud KB', color: '#60A5FA' }
		];
		connectors.forEach((c, i) => {
			nodes.push({
				id: c.id,
				label: c.label,
				type: 'connector',
				size: 12,
				color: c.color,
				x: cx - 380 + i * 60 + Math.random() * 40,
				y: cy + 280 + Math.random() * 60,
				vx: 0,
				vy: 0
			});
			edges.push({ source: 'center', target: c.id, strength: 0.2 });
		});

		// Live chat nodes from API
		try {
			const res = await fetch('/api/v1/chats/?page=1', {
				headers: { Authorization: `Bearer ${$user?.token ?? ''}` }
			});
			if (res.ok) {
				const data = await res.json();
				const chats = (Array.isArray(data) ? data : (data.items ?? [])).slice(0, 30);
				chatCount = chats.length;

				chats.forEach((chat: any, i: number) => {
					const angle = (i / chats.length) * 2 * Math.PI;
					const r = 260 + Math.random() * 60;
					const modelId = chat.models?.[0] ?? '';
					let agentId: string | undefined;
					if (modelId.includes('claude')) agentId = 'the-hawk';
					else if (modelId.includes('gpt-4o-mini')) agentId = 'inbox-triager';
					else if (modelId.includes('gpt-4o')) agentId = 'va-specialist';

					const nodeId = `chat-${chat.id?.slice(0, 8) ?? i}`;
					nodes.push({
						id: nodeId,
						label: (chat.title ?? 'Chat').slice(0, 28),
						type: 'chat',
						size: 9,
						color: COLORS.chat,
						x: cx + r * Math.cos(angle),
						y: cy + r * Math.sin(angle),
						vx: 0,
						vy: 0,
						meta: `Model: ${modelId.split('/').pop() ?? 'unknown'} · ${new Date(chat.updated_at * 1000).toLocaleDateString()}`,
						href: `/c/${chat.id}`
					});

					const srcId = agentId ?? 'center';
					edges.push({ source: srcId, target: nodeId, strength: 0.15 });
				});
			}
		} catch (_) {}

		loading = false;
		startSimulation();
	}

	// ── Force simulation ──────────────────────────────────────────────────────
	function startSimulation() {
		cancelAnimationFrame(animFrame);
		let tick = 0;

		function simulate() {
			tick++;
			const cooling = Math.max(0.01, 1 - tick / 300);

			// Repulsion between nodes
			for (let i = 0; i < nodes.length; i++) {
				for (let j = i + 1; j < nodes.length; j++) {
					const a = nodes[i];
					const b = nodes[j];
					if (a.pinned && b.pinned) continue;
					const dx = b.x - a.x;
					const dy = b.y - a.y;
					const dist = Math.sqrt(dx * dx + dy * dy) || 1;
					const minDist = (a.size + b.size) * 4;
					if (dist < minDist * 3) {
						const force = ((minDist * 3 - dist) / dist) * 0.4 * cooling;
						if (!a.pinned) {
							a.vx -= dx * force;
							a.vy -= dy * force;
						}
						if (!b.pinned) {
							b.vx += dx * force;
							b.vy += dy * force;
						}
					}
				}
			}

			// Attraction along edges
			const nodeMap = new Map(nodes.map((n) => [n.id, n]));
			for (const edge of edges) {
				const a = nodeMap.get(edge.source);
				const b = nodeMap.get(edge.target);
				if (!a || !b) continue;
				const dx = b.x - a.x;
				const dy = b.y - a.y;
				const dist = Math.sqrt(dx * dx + dy * dy) || 1;
				const idealDist = 120 / edge.strength;
				const force = ((dist - idealDist) / dist) * 0.03 * cooling;
				if (!a.pinned) {
					a.vx += dx * force;
					a.vy += dy * force;
				}
				if (!b.pinned) {
					b.vx -= dx * force;
					b.vy -= dy * force;
				}
			}

			// Gravity toward center
			for (const node of nodes) {
				if (node.pinned) continue;
				node.vx += (width / 2 - node.x) * 0.001 * cooling;
				node.vy += (height / 2 - node.y) * 0.001 * cooling;
				node.vx *= 0.85;
				node.vy *= 0.85;
				node.x += node.vx;
				node.y += node.vy;
			}

			draw();
			if (tick < 250 || cooling > 0.05) {
				animFrame = requestAnimationFrame(simulate);
			} else {
				// Keep drawing without physics
				const drawLoop = () => {
					draw();
					animFrame = requestAnimationFrame(drawLoop);
				};
				drawLoop();
			}
		}
		simulate();
	}

	// ── Canvas drawing ────────────────────────────────────────────────────────
	function draw() {
		if (!ctx) return;
		ctx.clearRect(0, 0, width, height);

		ctx.save();
		ctx.translate(panX, panY);
		ctx.scale(zoom, zoom);

		// Draw edges
		const nodeMap = new Map(nodes.map((n) => [n.id, n]));
		for (const edge of edges) {
			const a = nodeMap.get(edge.source);
			const b = nodeMap.get(edge.target);
			if (!a || !b) continue;
			ctx.beginPath();
			ctx.moveTo(a.x, a.y);
			ctx.lineTo(b.x, b.y);
			ctx.strokeStyle = `rgba(255,255,255,${edge.strength * 0.12})`;
			ctx.lineWidth = edge.strength * 1.5;
			ctx.stroke();
		}

		// Draw nodes
		for (const node of nodes) {
			const isHovered = hoveredNode?.id === node.id;
			const isSelected = selectedNode?.id === node.id;

			// Glow
			if (isHovered || isSelected) {
				ctx.beginPath();
				ctx.arc(node.x, node.y, node.size + 8, 0, Math.PI * 2);
				const grd = ctx.createRadialGradient(
					node.x,
					node.y,
					node.size,
					node.x,
					node.y,
					node.size + 8
				);
				grd.addColorStop(0, node.color + '60');
				grd.addColorStop(1, 'transparent');
				ctx.fillStyle = grd;
				ctx.fill();
			}

			// Node circle
			ctx.beginPath();
			ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
			ctx.fillStyle = node.color + (isHovered || isSelected ? 'FF' : 'CC');
			ctx.fill();

			if (isSelected) {
				ctx.strokeStyle = '#fff';
				ctx.lineWidth = 2;
				ctx.stroke();
			}

			// Label
			const minSizeForLabel = node.type === 'chat' ? 12 : 8;
			if (node.size >= minSizeForLabel || isHovered || isSelected) {
				ctx.fillStyle = isHovered || isSelected ? '#fff' : 'rgba(255,255,255,0.85)';
				ctx.font = `${isHovered ? 600 : 500} ${node.size < 12 ? 9 : 11}px "IBM Plex Mono", monospace`;
				ctx.textAlign = 'center';
				ctx.fillText(node.label, node.x, node.y + node.size + 14);
			}
		}

		ctx.restore();

		// Tooltip for selected node
		if (selectedNode?.meta) {
			ctx.fillStyle = 'rgba(0,0,0,0.85)';
			ctx.roundRect(12, height - 70, 380, 55, 8);
			ctx.fill();
			ctx.fillStyle = selectedNode.color;
			ctx.font = '600 12px "IBM Plex Mono", monospace';
			ctx.textAlign = 'left';
			ctx.fillText(selectedNode.label, 22, height - 48);
			ctx.fillStyle = 'rgba(255,255,255,0.6)';
			ctx.font = '400 10px "IBM Plex Mono", monospace';
			ctx.fillText(selectedNode.meta, 22, height - 30);
			if (selectedNode.href) {
				ctx.fillStyle = '#00D8FF';
				ctx.fillText('Click to open →', 22, height - 14);
			}
		}
	}

	// ── Mouse events ──────────────────────────────────────────────────────────
	function canvasToWorld(cx: number, cy: number) {
		return {
			x: (cx - panX) / zoom,
			y: (cy - panY) / zoom
		};
	}

	function getNodeAt(cx: number, cy: number): BrainNode | null {
		const { x, y } = canvasToWorld(cx, cy);
		for (let i = nodes.length - 1; i >= 0; i--) {
			const n = nodes[i];
			const dx = x - n.x;
			const dy = y - n.y;
			if (Math.sqrt(dx * dx + dy * dy) <= n.size + 6) return n;
		}
		return null;
	}

	function onMouseMove(e: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		const mx = e.clientX - rect.left;
		const my = e.clientY - rect.top;

		if (dragging) {
			const { x, y } = canvasToWorld(mx, my);
			dragging.x = x;
			dragging.y = y;
			dragging.vx = 0;
			dragging.vy = 0;
			return;
		}

		if (isPanning) {
			panX += mx - lastMouseX;
			panY += my - lastMouseY;
			lastMouseX = mx;
			lastMouseY = my;
			return;
		}

		const hit = getNodeAt(mx, my);
		hoveredNode = hit;
		canvas.style.cursor = hit ? 'pointer' : 'grab';
	}

	function onMouseDown(e: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		const mx = e.clientX - rect.left;
		const my = e.clientY - rect.top;
		const hit = getNodeAt(mx, my);
		if (hit) {
			dragging = hit;
			selectedNode = hit;
			canvas.style.cursor = 'grabbing';
		} else {
			isPanning = true;
			lastMouseX = mx;
			lastMouseY = my;
			canvas.style.cursor = 'grabbing';
		}
	}

	function onMouseUp(e: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		const mx = e.clientX - rect.left;
		const my = e.clientY - rect.top;

		if (dragging) {
			const wasDrag = Math.abs(dragging.vx) < 2 && Math.abs(dragging.vy) < 2;
			if (wasDrag && dragging.href) {
				goto(dragging.href);
			}
			dragging = null;
		}
		isPanning = false;
		canvas.style.cursor = 'grab';
	}

	function onWheel(e: WheelEvent) {
		e.preventDefault();
		const rect = canvas.getBoundingClientRect();
		const mx = e.clientX - rect.left;
		const my = e.clientY - rect.top;
		const delta = e.deltaY > 0 ? 0.9 : 1.1;
		const newZoom = Math.max(0.3, Math.min(3, zoom * delta));
		panX = mx - (mx - panX) * (newZoom / zoom);
		panY = my - (my - panY) * (newZoom / zoom);
		zoom = newZoom;
	}

	// ── Resize ────────────────────────────────────────────────────────────────
	function resize() {
		const container = canvas?.parentElement;
		if (!container) return;
		width = container.clientWidth;
		height = container.clientHeight;
		canvas.width = width;
		canvas.height = height;
	}

	// ── Lifecycle ─────────────────────────────────────────────────────────────
	onMount(async () => {
		ctx = canvas.getContext('2d')!;
		resize();
		window.addEventListener('resize', () => {
			resize();
			draw();
		});
		await buildGraph();
	});

	onDestroy(() => {
		cancelAnimationFrame(animFrame);
		window.removeEventListener('resize', resize);
	});

	// ── Legend items ──────────────────────────────────────────────────────────
	const legend = [
		{ color: COLORS.center, label: 'HaMm3r OS' },
		{ color: COLORS.agent, label: 'Agents' },
		{ color: COLORS.chat, label: 'Chats' },
		{ color: COLORS.model, label: 'Models' },
		{ color: COLORS.memory, label: 'Memory' },
		{ color: COLORS.connector, label: 'Connectors' }
	];
</script>

<svelte:head>
	<title>Brain Tree · HaMm3r OS</title>
</svelte:head>

<div class="bt-root">
	<!-- Header -->
	<header class="bt-header">
		<a href="/hammer" class="bt-back">← Command Center</a>
		<div class="bt-title-block">
			<span class="bt-title">🧠 Brain Tree</span>
			<span class="bt-subtitle">
				{#if loading}Building connections…{:else}{nodes.length} nodes · {edges.length} connections · {chatCount}
					chats{/if}
			</span>
		</div>
		<button class="bt-btn" on:click={buildGraph}>↺ Refresh</button>
	</header>

	<!-- Legend -->
	<div class="bt-legend">
		{#each legend as l}
			<span class="bt-legend-item">
				<span class="bt-legend-dot" style="background:{l.color}"></span>
				{l.label}
			</span>
		{/each}
		<span class="bt-legend-hint">Scroll to zoom · Drag to pan · Click node for details</span>
	</div>

	<!-- Canvas -->
	<div class="bt-canvas-wrap">
		{#if loading}
			<div class="bt-loading">
				<div class="bt-spinner"></div>
				<span>Loading your brain…</span>
			</div>
		{/if}
		<canvas
			bind:this={canvas}
			on:mousemove={onMouseMove}
			on:mousedown={onMouseDown}
			on:mouseup={onMouseUp}
			on:wheel={onWheel}
			style="cursor:grab"
		></canvas>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		overflow: hidden;
	}

	.bt-root {
		width: 100vw;
		height: 100vh;
		background: #0a0a0f;
		display: flex;
		flex-direction: column;
		font-family: 'IBM Plex Mono', monospace;
		color: #e2e8f0;
	}

	.bt-header {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 10px 20px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.08);
		background: rgba(0, 0, 0, 0.4);
		flex-shrink: 0;
	}
	.bt-back {
		color: #00d8ff;
		text-decoration: none;
		font-size: 0.75rem;
		opacity: 0.8;
		transition: opacity 0.15s;
	}
	.bt-back:hover {
		opacity: 1;
	}
	.bt-title-block {
		display: flex;
		flex-direction: column;
	}
	.bt-title {
		font-size: 1rem;
		font-weight: 700;
		letter-spacing: 0.05em;
	}
	.bt-subtitle {
		font-size: 0.65rem;
		color: rgba(255, 255, 255, 0.4);
		margin-top: 2px;
	}
	.bt-btn {
		margin-left: auto;
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.12);
		color: #e2e8f0;
		border-radius: 6px;
		padding: 5px 14px;
		font-size: 0.72rem;
		cursor: pointer;
		font-family: inherit;
		transition: background 0.15s;
	}
	.bt-btn:hover {
		background: rgba(255, 255, 255, 0.12);
	}

	.bt-legend {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 6px 20px;
		background: rgba(0, 0, 0, 0.3);
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		flex-shrink: 0;
		flex-wrap: wrap;
	}
	.bt-legend-item {
		display: flex;
		align-items: center;
		gap: 5px;
		font-size: 0.65rem;
		color: rgba(255, 255, 255, 0.5);
	}
	.bt-legend-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		flex-shrink: 0;
	}
	.bt-legend-hint {
		margin-left: auto;
		font-size: 0.6rem;
		color: rgba(255, 255, 255, 0.25);
		font-style: italic;
	}

	.bt-canvas-wrap {
		flex: 1;
		position: relative;
		overflow: hidden;
	}
	canvas {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
	}

	.bt-loading {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		font-size: 0.8rem;
		color: rgba(255, 255, 255, 0.4);
		z-index: 10;
		background: #0a0a0f;
	}
	.bt-spinner {
		width: 36px;
		height: 36px;
		border: 3px solid rgba(255, 255, 255, 0.1);
		border-top-color: #00d8ff;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}
	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}
</style>
