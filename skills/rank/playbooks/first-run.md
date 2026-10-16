# First run

1. Have the user create a workspace Rank API key in Hubbly when Settings supports it. Keep the key only in `RANK_API_KEY`, and point `RANK_API_URL` at the official HTTPS API origin.
2. Run `/rank` through the wrapper to check the authenticated capability catalog. If the status route is not advertised, report the integration as unavailable; do not call dashboard internals.
3. If `/rank-setup` is advertised, list connected sites and return only official connection links. The user completes OAuth in the browser. Never collect passwords or refresh tokens.
4. Choose a site UUID returned by the gateway and run read-only health and visibility commands. Preserve provenance, freshness, and unmeasured states.
5. Before any proposed write, read `safe-autonomy.md` and obtain the user's direction. The current client does not implement preview/confirm, so writes remain disabled.
