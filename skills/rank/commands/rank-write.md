# /rank-write

Propose a new page draft through Rank's existing write job.

This command is disabled in the current read-only phase. Do not run it or call `POST /v1/agent/sites/{id}/drafts` directly. The wrapper exits with code 3 before any network request, even if a malformed capability response advertises the route.

A future client must implement preview and exact payload-bound confirmation. Draft text must still pass Rank's guardrails and fact checks, and server-side approval remains mandatory where required. Until then, use the Hubbly dashboard.
