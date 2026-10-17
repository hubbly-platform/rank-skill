# /rank-visibility

Read per-engine AI citation visibility for a connected site.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-visibility <site-uuid>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Separate measured ChatGPT, AI Overview, Perplexity, and Gemini results. Unmeasured means measuring, not zero.
