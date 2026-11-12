# /rank-scan

Read a public HTTPS homepage's title, meta description, headings, internal and social links, and word count.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-scan https://example.com` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

The gateway must advertise scanning. Treat this as a public homepage fetch, not site ownership or connected-site access. URLs with embedded credentials are rejected. Competitor comparison is unavailable in this phase; do not invent competitors or additional page crawls.
