# /rank-publish

Propose publishing an existing draft.

This command is disabled in the current read-only phase. Do not run it or call `POST /v1/agent/drafts/{id}/publish` directly. The wrapper exits with code 3 before any network request, even if a malformed capability response advertises the route.

A future client must implement preview and exact payload-bound confirmation on an authorized site, then require public verification and a rollback handle before claiming success. Until then, use the Hubbly dashboard.
