# /rank-setup

Read connected sites and each site's Search Console connection state.

Resolve `<skill-directory>` from the installed `SKILL.md`, then run `bash <skill-directory>/scripts/rank-command.sh rank-setup` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Never request a site password or OAuth token in chat. This read-only route does not start OAuth; direct the user to the official Hubbly dashboard for connection changes.
