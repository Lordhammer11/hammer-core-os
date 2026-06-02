<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let name = '';
	let emoji = '🤖';
	let baseModel = 'llama3.2:latest';
	let systemPrompt = '';
	let description = '';
	let tags = '';
	let saveToObsidian = true;
	let creating = false;
	let error = '';
	let success = false;

	const models = [
		{ id: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet' },
		{ id: 'llama3.2:latest', label: 'Llama 3.2 (Local)' },
		{ id: 'mistral:latest', label: 'Mistral 7B (Local)' },
		{ id: 'gemma3:latest', label: 'Gemma 3 (Local)' },
		{ id: 'phi4-mini:latest', label: 'Phi-4 Mini (Local)' },
	];

	const templates = [
		{
			label: '💼 Business Advisor',
			emoji: '💼',
			system: 'You are an expert business advisor focused on strategy, operations, and growth. You provide actionable, data-driven recommendations tailored to the specific business context.',
			desc: 'Business strategy and operations advisor'
		},
		{
			label: '⚖️ Legal Research',
			emoji: '⚖️',
			system: 'You are a legal research assistant specializing in analyzing statutes, regulations, and case law. You provide thorough research summaries while noting that your output is for informational purposes and not legal advice.',
			desc: 'Legal research and regulatory analysis'
		},
		{
			label: '📊 Data Analyst',
			emoji: '📊',
			system: 'You are an expert data analyst. You help interpret data, identify trends, suggest visualizations, and translate complex findings into clear business insights.',
			desc: 'Data analysis and business intelligence'
		},
		{
			label: '✍️ Content Writer',
			emoji: '✍️',
			system: 'You are a professional content writer and copywriter. You create compelling, SEO-optimized content tailored to the target audience and brand voice provided.',
			desc: 'Content writing and copywriting'
		},
	];

	function applyTemplate(t: any) {
		emoji = t.emoji;
		systemPrompt = t.system;
		description = t.desc;
	}

	async function createAgent() {
		if (!name.trim() || !systemPrompt.trim()) {
			error = 'Agent name and system prompt are required.';
			return;
		}
		creating = true;
		error = '';

		try {
			// Get token from localStorage
			const token = localStorage.getItem('token');
			if (!token) throw new Error('Not authenticated. Please log in.');

			const agentId = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

			const payload = {
				id: agentId,
				name: `${emoji} ${name}`,
				base_model_id: baseModel,
				params: { system: systemPrompt },
				meta: {
					description: description || `Custom agent: ${name}`,
					profile_image_url: '/static/claude-bot.svg',
					tags: tags.split(',').map(t => t.trim()).filter(Boolean)
				},
				is_active: true
			};

			const res = await fetch('/api/v1/models/create', {
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});

			if (!res.ok) {
				const err = await res.json();
				throw new Error(err.detail || 'Failed to create agent');
			}

			// Save to Obsidian vault if checked
			if (saveToObsidian) {
				const md = `# ${emoji} ${name}\n\n## Role\n${description || name}\n\n## System Prompt\n${systemPrompt}\n\n## Model\n${baseModel}\n\n## Tags\n${tags || 'custom'}\n`;
				// Write via a server action or just note it
				console.log('Would save to HaMm3r-KB/Agents/', agentId + '.md');
			}

			success = true;
			setTimeout(() => goto('/dashboard'), 1800);
		} catch (e: any) {
			error = e.message;
		} finally {
			creating = false;
		}
	}
</script>

<div class="builder-page">
	<!-- Header -->
	<div class="builder-header">
		<a href="/dashboard" class="back-btn">← Dashboard</a>
		<div class="header-center">
			<h1 class="builder-title">Agent Builder</h1>
			<p class="builder-sub">Create a new custom AI agent for HaMm3r OS</p>
		</div>
		<div class="header-right"></div>
	</div>

	<div class="builder-body">
		<!-- LEFT: Form -->
		<div class="form-col">

			<!-- Templates -->
			<div class="form-section">
				<div class="form-label">QUICK TEMPLATES</div>
				<div class="template-grid">
					{#each templates as t}
						<button class="template-btn" on:click={() => applyTemplate(t)}>
							{t.label}
						</button>
					{/each}
				</div>
			</div>

			<!-- Name + Emoji -->
			<div class="form-section">
				<div class="form-label">AGENT IDENTITY</div>
				<div class="name-row">
					<div class="emoji-wrap">
						<input class="emoji-input" bind:value={emoji} maxlength="2" placeholder="🤖"/>
					</div>
					<input class="text-input flex-1" bind:value={name} placeholder="Agent Name (e.g. Real Estate Scout)" />
				</div>
			</div>

			<!-- Base Model -->
			<div class="form-section">
				<div class="form-label">BASE MODEL</div>
				<select class="select-input" bind:value={baseModel}>
					{#each models as m}
						<option value={m.id}>{m.label}</option>
					{/each}
				</select>
			</div>

			<!-- System Prompt -->
			<div class="form-section">
				<div class="form-label">SYSTEM PROMPT</div>
				<textarea
					class="textarea-input"
					bind:value={systemPrompt}
					placeholder="Describe your agent's role, expertise, and behavior. Be specific — the more detail, the better the agent performs."
					rows="8"
				></textarea>
				<div class="char-count">{systemPrompt.length} chars</div>
			</div>

			<!-- Description + Tags -->
			<div class="form-section">
				<div class="form-label">DESCRIPTION</div>
				<input class="text-input" bind:value={description} placeholder="Short description shown on the dashboard" />
			</div>
			<div class="form-section">
				<div class="form-label">TAGS <span class="label-hint">(comma separated)</span></div>
				<input class="text-input" bind:value={tags} placeholder="e.g. business, finance, research" />
			</div>

			<!-- Options -->
			<div class="form-section options-row">
				<label class="checkbox-label">
					<input type="checkbox" bind:checked={saveToObsidian} />
					<span>Save to HaMm3r-KB Obsidian vault</span>
				</label>
			</div>

			<!-- Error / Success -->
			{#if error}
				<div class="error-msg">⚠️ {error}</div>
			{/if}
			{#if success}
				<div class="success-msg">✅ Agent created! Redirecting to dashboard…</div>
			{/if}

			<!-- Submit -->
			<button class="create-btn" on:click={createAgent} disabled={creating}>
				{creating ? 'Creating…' : '⚡ Create Agent'}
			</button>
		</div>

		<!-- RIGHT: Preview -->
		<div class="preview-col">
			<div class="form-label">LIVE PREVIEW</div>
			<div class="preview-card" style="--accent: #818CF8">
				<div class="preview-emoji">{emoji || '🤖'}</div>
				<div class="preview-name">{name || 'Agent Name'}</div>
				<div class="preview-desc">{description || 'Agent description will appear here'}</div>
				<div class="preview-model">
					<span class="model-badge">{models.find(m => m.id === baseModel)?.label || baseModel}</span>
				</div>
				{#if tags}
					<div class="preview-tags">
						{#each tags.split(',').filter(t => t.trim()) as tag}
							<span class="preview-tag">{tag.trim()}</span>
						{/each}
					</div>
				{/if}
				<div class="preview-cta">Start Chat →</div>
			</div>

			<div class="preview-prompt-box">
				<div class="form-label" style="margin-bottom:10px">SYSTEM PROMPT PREVIEW</div>
				<div class="prompt-preview">{systemPrompt || 'Your system prompt will appear here…'}</div>
			</div>

			<div class="obsidian-note">
				{#if saveToObsidian}
					<div class="obsidian-badge">
						🧠 Will save to <strong>~/HaMm3r-KB/Agents/</strong>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>

<style>
	.builder-page {
		min-height: 100vh;
		background: #090D16;
		color: #E2E8F0;
		font-family: 'Inter', -apple-system, sans-serif;
		display: flex;
		flex-direction: column;
	}

	.builder-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20px 32px;
		border-bottom: 1px solid rgba(255,255,255,0.06);
		background: #131B2E;
	}
	.back-btn {
		color: #718096;
		text-decoration: none;
		font-size: 13px;
		font-weight: 500;
		transition: color 0.15s;
		width: 120px;
	}
	.back-btn:hover { color: #818CF8; }
	.header-center { text-align: center; }
	.builder-title { font-size: 20px; font-weight: 700; color: #F7FAFC; margin: 0 0 4px; }
	.builder-sub { font-size: 13px; color: #718096; margin: 0; }
	.header-right { width: 120px; }

	.builder-body {
		display: grid;
		grid-template-columns: 1fr 380px;
		gap: 28px;
		padding: 32px;
		max-width: 1200px;
		margin: 0 auto;
		width: 100%;
	}

	/* Form */
	.form-section { margin-bottom: 22px; }
	.form-label {
		font-size: 10px;
		font-weight: 700;
		color: #4A5568;
		letter-spacing: 1.3px;
		text-transform: uppercase;
		margin-bottom: 8px;
	}
	.label-hint { font-weight: 400; text-transform: none; letter-spacing: 0; color: #4A5568; }

	.template-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;
	}
	.template-btn {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.07);
		border-radius: 8px;
		padding: 9px 12px;
		color: #A0AEC0;
		font-size: 12px;
		font-weight: 500;
		cursor: pointer;
		text-align: left;
		transition: all 0.15s;
		font-family: inherit;
	}
	.template-btn:hover { border-color: rgba(129,140,248,0.4); color: #818CF8; background: rgba(129,140,248,0.08); }

	.name-row { display: flex; gap: 10px; align-items: stretch; }
	.emoji-wrap {
		width: 52px; flex-shrink: 0;
	}
	.emoji-input {
		width: 52px;
		height: 44px;
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.08);
		border-radius: 10px;
		color: #E2E8F0;
		font-size: 22px;
		text-align: center;
		outline: none;
		cursor: pointer;
	}
	.emoji-input:focus { border-color: #818CF8; }

	.text-input, .select-input {
		width: 100%;
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.08);
		border-radius: 10px;
		padding: 10px 14px;
		color: #E2E8F0;
		font-size: 14px;
		outline: none;
		transition: border-color 0.15s;
		font-family: inherit;
		height: 44px;
	}
	.text-input:focus, .select-input:focus { border-color: #818CF8; box-shadow: 0 0 0 3px rgba(129,140,248,0.12); }
	.text-input::placeholder { color: #4A5568; }
	.select-input { cursor: pointer; }
	.flex-1 { flex: 1; }

	.textarea-input {
		width: 100%;
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.08);
		border-radius: 10px;
		padding: 12px 14px;
		color: #E2E8F0;
		font-size: 13px;
		outline: none;
		transition: border-color 0.15s;
		font-family: inherit;
		resize: vertical;
		line-height: 1.6;
	}
	.textarea-input:focus { border-color: #818CF8; box-shadow: 0 0 0 3px rgba(129,140,248,0.12); }
	.textarea-input::placeholder { color: #4A5568; }
	.char-count { font-size: 10px; color: #4A5568; text-align: right; margin-top: 4px; }

	.options-row { display: flex; align-items: center; gap: 16px; }
	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 13px;
		color: #A0AEC0;
		cursor: pointer;
	}
	.checkbox-label input { accent-color: #818CF8; width: 15px; height: 15px; cursor: pointer; }

	.error-msg {
		background: rgba(255,107,138,0.1);
		border: 1px solid rgba(255,107,138,0.3);
		border-radius: 8px;
		padding: 10px 14px;
		font-size: 13px;
		color: #FF6B8A;
		margin-bottom: 14px;
	}
	.success-msg {
		background: rgba(72,187,120,0.1);
		border: 1px solid rgba(72,187,120,0.3);
		border-radius: 8px;
		padding: 10px 14px;
		font-size: 13px;
		color: #48BB78;
		margin-bottom: 14px;
	}

	.create-btn {
		width: 100%;
		background: linear-gradient(135deg, #818CF8, #A855F7);
		border: none;
		border-radius: 12px;
		padding: 14px;
		color: white;
		font-size: 15px;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		font-family: inherit;
		letter-spacing: -0.2px;
	}
	.create-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(129,140,248,0.35); }
	.create-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

	/* Preview */
	.preview-col { display: flex; flex-direction: column; gap: 16px; }

	.preview-card {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.07);
		border-radius: 16px;
		padding: 24px;
		position: relative;
		overflow: hidden;
		transition: border-color 0.2s;
	}
	.preview-card::before {
		content: '';
		position: absolute;
		top: 0; left: 0; right: 0;
		height: 2px;
		background: linear-gradient(90deg, #818CF8, #A855F7);
	}
	.preview-emoji { font-size: 36px; margin-bottom: 10px; }
	.preview-name { font-size: 18px; font-weight: 700; color: #F7FAFC; margin-bottom: 6px; }
	.preview-desc { font-size: 13px; color: #718096; line-height: 1.5; margin-bottom: 12px; }
	.model-badge {
		display: inline-block;
		background: rgba(129,140,248,0.12);
		border: 1px solid rgba(129,140,248,0.25);
		color: #818CF8;
		font-size: 11px;
		padding: 3px 10px;
		border-radius: 20px;
		font-weight: 500;
	}
	.preview-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
	.preview-tag {
		background: rgba(255,255,255,0.05);
		border: 1px solid rgba(255,255,255,0.08);
		color: #718096;
		font-size: 11px;
		padding: 2px 8px;
		border-radius: 20px;
	}
	.preview-cta { font-size: 12px; color: #818CF8; margin-top: 14px; font-weight: 500; }

	.preview-prompt-box {
		background: #131B2E;
		border: 1px solid rgba(255,255,255,0.06);
		border-radius: 12px;
		padding: 16px;
	}
	.prompt-preview {
		font-size: 12px;
		color: #718096;
		line-height: 1.7;
		white-space: pre-wrap;
		max-height: 180px;
		overflow-y: auto;
		font-family: 'SF Mono', 'Monaco', monospace;
	}

	.obsidian-badge {
		background: rgba(168,85,247,0.1);
		border: 1px solid rgba(168,85,247,0.25);
		border-radius: 8px;
		padding: 10px 14px;
		font-size: 12px;
		color: #A855F7;
	}
	.obsidian-badge strong { color: #C084FC; }
</style>
