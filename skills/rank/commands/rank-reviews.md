# /rank-reviews

Read unanswered reviews and suggested replies.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-reviews <site-uuid>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Suggestions are for user copy-and-paste; this command must not post a reply.
