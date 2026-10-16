# /rank-questions

Propose changes to buyer questions tracked by the citation sampler.

Run `bash skills/rank/scripts/rank-command.sh rank-questions <site-uuid> <payload.json>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

This is a write. Obtain a gateway preview and payload-bound confirmation, then honor any awaiting_approval response.
