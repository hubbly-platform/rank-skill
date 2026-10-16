# /rank-plan

Read proposed next actions and their expected outcomes.

Run `bash skills/rank/scripts/rank-command.sh rank-plan <site-uuid>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Present proposals as estimates, not guaranteed ranking or traffic outcomes.
