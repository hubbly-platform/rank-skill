# /rank-questions

Propose changes to buyer questions tracked by the citation sampler.

This command is disabled in the current read-only phase. Do not run it or call `PUT /v1/agent/sites/{id}/questions` directly. The wrapper exits with code 3 before any network request, even if a malformed capability response advertises the route.

A future client must first implement a gateway preview and payload-bound confirmation, then honor any `awaiting_approval` response. Until that flow exists and the gateway advertises the exact contract, make question changes in the Hubbly dashboard.
