# /rank-scan

Scan a public HTTPS URL for SEO and AEO findings.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-scan https://example.com` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

The gateway must advertise scanning. Treat this as a public scan, not site ownership or connected-site access.
