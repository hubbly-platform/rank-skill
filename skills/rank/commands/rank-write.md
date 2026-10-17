# /rank-write

Propose a new page draft through Rank's existing write job.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-write <site-uuid> <payload.json>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Draft text must pass guardrails and fact checks. Preview and confirm through the gateway; do not bypass an unavailable route.
