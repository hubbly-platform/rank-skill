# /rank

Read account, connected sites, autonomy mode, and waiting approvals.

Run `bash skills/rank/scripts/rank-command.sh rank` only after the user has configured `RANK_API_KEY` and `RANK_API_URL`. The wrapper checks the exact command, method, and route in the authenticated capability catalog before calling it. If unavailable, explain the missing gateway capability and stop.

No site argument. Report only the returned status; do not infer unmeasured values.
