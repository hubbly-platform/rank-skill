---
name: rank
description: Use the Hubbly Rank gateway to inspect a connected site's SEO and AI visibility, or to propose governed Rank changes when the gateway advertises those capabilities.
---

# Hubbly Rank

Rank is a client for your own Hubbly account, not an independent publisher. The private Hubbly API is the sole authority for site access, plan entitlement, approval, and execution.

## Setup and preflight

Ask the user for a workspace-scoped Rank API key created in Hubbly Settings. Keep it in `RANK_API_KEY`; never paste it into chat, command arguments, logs, or files. Set `RANK_API_URL` to the official HTTPS API origin. The wrapper requires `curl` and `jq`. Run `bash skills/rank/scripts/rank-command.sh rank` to discover whether status is enabled. Every command checks `/v1/agent/capabilities` first and refuses unavailable routes; an unavailable capability is not a reason to call a legacy dashboard route directly.

Never infer that a successful key check grants write permission. Read keys cannot write. A revoked key, expired approval, kill switch, missing entitlement, or site mismatch must stop the action. Do not work around a gateway denial.

## Commands

Read the matching file in `commands/` before running one of the twelve commands. Read `playbooks/first-run.md` for onboarding, `playbooks/weekly-loop.md` for recurring work, or `playbooks/safe-autonomy.md` before any write.

| Command | Purpose |
| --- | --- |
| `/rank` | Account/site status |
| `/rank-setup` | Connection status and connect links |
| `/rank-scan <url>` | Public SEO/AEO scan |
| `/rank-health <site-uuid>` | Technical health |
| `/rank-opportunities <site-uuid>` | Search Console opportunities |
| `/rank-visibility <site-uuid>` | Measured AI citations |
| `/rank-questions <site-uuid>` | Propose buyer-question changes |
| `/rank-plan <site-uuid>` | Proposed next actions |
| `/rank-write <site-uuid> <payload.json>` | Propose a draft |
| `/rank-publish <draft-uuid> <payload.json>` | Propose publication |
| `/rank-reviews <site-uuid>` | Review suggestions for manual use |
| `/rank-report <site-uuid>` | Weekly report |

## Safety boundary

Read-only work may proceed on an authorized site. Treat metrics with their API provenance; missing or unmeasured is not zero. Questions, drafts, and publishing require a gateway preview, exact payload-bound confirmation, and whatever server-side approvals the site requires. The current wrapper does not implement this exchange and disables those three commands. An agent's confirmation is not human approval. Do not publish to Goldworth; Goldworth validation is read-only. Only use an explicitly authorized throwaway site for draft-to-rollback tests. Never claim a page was published, verified, or rolled back without the gateway receipts and a public check.

The current gateway may advertise no catalog capabilities. If so, report that honestly and stop; never fabricate a result or use private dashboard routes as a substitute. Reviews are copy-and-paste suggestions, not reply-posting. `/rank-update`, agency switching, and unsupported CMS actions are not part of this skill.
