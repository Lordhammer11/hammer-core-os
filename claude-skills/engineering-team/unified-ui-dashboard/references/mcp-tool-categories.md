# MCP Tool Categories Reference

Complete reference for the 11 connected MCP tool categories shown in HaMm3r's Unified Tool Hub.

## Gmail — Email & Messaging

Gmail MCP provides full read/write access to Gmail via the Gmail API.

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `search_threads` | `query` (Gmail syntax) | Supports `from:`, `to:`, `subject:`, `label:`, `after:`, `before:` |
| `create_draft` | `to`, `subject`, `body`, `cc?`, `bcc?` | Creates draft only — does not send |
| `label_message` | `messageId`, `labelName` | Apply existing label; create first with `create_label` |
| `get_thread` | `threadId` | Returns full thread with all messages |
| `unlabel_thread` | `threadId`, `labelName` | Removes label from every message in thread |
| `list_labels` | — | Returns all user and system labels |
| `list_drafts` | `maxResults?` | Lists saved drafts |

**Best for:** Email triage, draft creation, organizing threads.

---

## Google Drive — File Storage & Docs

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `list_recent_files` | `maxResults?` | Sorted by `modifiedTime` descending |
| `search_files` | `query` (Drive query syntax) | Supports `name contains`, `mimeType=`, `trashed=false` |
| `create_file` | `name`, `mimeType`, `content?` | Use `application/vnd.google-apps.document` for Docs |
| `download_file_content` | `fileId` | Returns raw file bytes or text |
| `get_file_metadata` | `fileId` | Returns name, mimeType, modifiedTime, owners |
| `get_file_permissions` | `fileId` | Returns permission list with roles |
| `read_file_content` | `fileId` | Extracts text from Google Docs/Sheets |

**Best for:** Document retrieval, file organization, content extraction.

---

## Google Calendar — Scheduling & Events

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `list_events` | `calendarId`, `timeMin`, `timeMax` | ISO 8601 timestamps |
| `create_event` | `summary`, `start`, `end`, `attendees?` | Sends invites to attendees |
| `suggest_time` | `attendees`, `duration` | Finds mutual free slots |
| `respond_to_event` | `eventId`, `response` | Values: `accepted`, `declined`, `tentative` |
| `update_event` | `eventId`, `fields...` | Partial update — only changed fields required |
| `delete_event` | `eventId` | Cancels and removes event |
| `get_event` | `eventId` | Full event with attendee status |

**Best for:** Meeting scheduling, availability checking, calendar management.

---

## Zoom — Video Meetings

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `recordings_list` | `from?`, `to?` | Date range in `YYYY-MM-DD` format |
| `search_meetings` | `query` | Searches by topic, host, or ID |
| `get_meeting_assets` | `meetingId` | Returns recording URLs and transcript link |
| `get_file_content` | `fileUrl` | Downloads transcript or recording |
| `search_zoom` | `query` | Full-text search across all Zoom content |

**Best for:** Retrieving meeting recordings, accessing transcripts, meeting search.

---

## GitHub — Code & Collaboration

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `list_pull_requests` | `owner`, `repo`, `state?` | State: `open`, `closed`, `all` |
| `list_issues` | `owner`, `repo`, `labels?`, `state?` | Filter by label arrays |
| `search_code` | `query` | GitHub code search syntax |
| `push_files` | `owner`, `repo`, `branch`, `files[]` | Multi-file atomic push |
| `create_branch` | `owner`, `repo`, `branch`, `sha` | Branch from specific commit |
| `create_pull_request` | `owner`, `repo`, `title`, `head`, `base` | Opens PR with optional body |
| `get_file_contents` | `owner`, `repo`, `path`, `ref?` | Read file at any branch/tag |

**Best for:** Code review automation, PR management, file operations.

---

## Shopify — E-Commerce

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `get_product` | `productId` | Returns product with variants and images |
| `list_orders` | `status?`, `limit?` | Status: `open`, `closed`, `cancelled` |
| `run_analytics_query` | `query` (ShopifyQL) | SQL-like analytics over orders/products |
| `create_product` | `title`, `bodyHtml`, `vendor`, `variants[]` | Full product creation |
| `search_products` | `query` | Search by title, SKU, or tag |
| `list_customers` | `limit?`, `since_id?` | Paginated customer list |
| `get_inventory_levels` | `locationId`, `inventoryItemId` | Stock at specific location |

**Best for:** Store analytics, inventory management, product catalog operations.

---

## Adobe Creative Cloud — Image & Design

Powered by Adobe Firefly and Photoshop APIs.

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `image_remove_background` | `imageUrl` | Returns PNG with transparent background |
| `image_crop_and_resize` | `imageUrl`, `width`, `height` | Smart crop preserving subject |
| `image_fill_area` | `imageUrl`, `mask`, `prompt` | Generative fill with Firefly |
| `image_vectorize` | `imageUrl` | Outputs SVG vector |
| `image_generate` | `prompt`, `style?` | Firefly AI image generation |
| `image_generative_expand` | `imageUrl`, `direction`, `size` | Outpaint canvas extension |
| `asset_search` | `query` | Search Creative Cloud library |

**Best for:** Image editing, AI generation, background removal, vectorization.

---

## Canva — Graphic Design

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `generate_design` | `prompt`, `type?` | Type: `presentation`, `social`, `poster` |
| `search_designs` | `query` | Searches your Canva library |
| `export_design` | `designId`, `format` | Format: `png`, `pdf`, `svg`, `mp4` |
| `list_brand_kits` | — | Returns brand colors, fonts, logos |
| `get_design` | `designId` | Returns design metadata and thumbnail |
| `copy_design` | `designId` | Duplicates with new ID |
| `resize_design` | `designId`, `width`, `height` | Resize to new dimensions |

**Best for:** Marketing materials, presentations, branded content creation.

---

## DocuSign — e-Signatures & Contracts

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `getEnvelopes` | `status?`, `fromDate?` | Status: `sent`, `delivered`, `completed` |
| `createEnvelope` | `emailSubject`, `documents[]`, `recipients[]` | Sends for signature |
| `getTemplates` | — | Lists available document templates |
| `triggerWorkflow` | `workflowId`, `payload` | Starts a DocuSign workflow |
| `listRecipients` | `envelopeId` | Returns signer list with status |
| `getEnvelope` | `envelopeId` | Full envelope details |
| `sendReminder` | `envelopeId` | Sends reminder to pending signers |

**Best for:** Contract management, signature collection, workflow automation.

---

## Hugging Face — AI Models & Research

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `hub_repo_search` | `query`, `type?` | Type: `model`, `dataset`, `space` |
| `paper_search` | `query` | Searches arXiv papers linked to HF |
| `space_search` | `query` | Finds HF Spaces by topic |
| `hf_doc_search` | `query` | Searches HF documentation |
| `hf_whoami` | — | Returns authenticated user profile |
| `hub_repo_details` | `repoId` | Full repo metadata, files, and card |
| `hf_doc_fetch` | `url` | Fetches a docs page by URL |

**Best for:** Model discovery, research paper search, AI documentation lookup.

---

## Ideabrowser — Startup Ideas & Market Research

| Capability | Parameters | Notes |
|-----------|-----------|-------|
| `browse_ideas` | `filters?` | Filter by budget, difficulty, category |
| `list_trends` | `category?` | Current market trend categories |
| `get_market_insight_detail` | `insightId` | Full market analysis with sources |
| `list_projects` | — | Your saved startup projects |
| `get_founder_profile` | — | Skills, budget, goals from your profile |
| `save_idea` | `ideaId` | Save to your idea collection |
| `start_idea_research` | `ideaId` | Triggers AI market research |

**Best for:** Startup ideation, market validation, competitive analysis.
