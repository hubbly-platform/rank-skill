# /rank-publish

Propose publishing an existing draft.

Run `bash skills/rank/scripts/rank-command.sh rank-publish <draft-uuid> <payload.json>` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

Only use an authorized site and gateway confirmation. Require public verification and a rollback handle before claiming success.
