# /rank-health

Read current technical health findings for a connected site.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-health <site-uuid>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Preserve severity, freshness, and provenance labels. An incomplete crawl is not a clean bill of health.
