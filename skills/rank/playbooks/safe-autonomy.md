# Safe autonomy

The gateway is the sole decision maker for plan entitlement, site ownership, workspace scope, onboarding window, autonomy mode, always-ask items, kill switch, approval, job dispatch, and audit. The client must not downgrade a denial or pending approval into success.

The current wrapper has no implemented preview/confirm exchange; its write commands are intentionally disabled even if a gateway accidentally advertises them. To enable a write later, first add a tested two-phase flow that previews the exact payload, binds a short-lived token to that payload and actor, confirms it, and handles `awaiting_approval` as pending. A changed payload needs a new preview. Confirming as an agent is not human approval.

Goldworth is read-only. For publish tests, use an explicitly authorized throwaway site and demand receipts for draft, publish, public verification, and rollback. Do not add `/rank-update` or unsupported CMS adapters by inference.
