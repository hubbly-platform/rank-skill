# First run

1. Have the user create a workspace Rank API key in Hubbly Settings → API keys. Copy the one-time token directly into the client's secret configuration as `RANK_API_KEY`, and point `RANK_API_URL` at the official HTTPS API origin. Never ask for the token in chat.
2. Run `/rank` through the wrapper to check the authenticated capability catalog. If the status route is not advertised, report the integration as unavailable; do not call dashboard internals.
3. If `/rank-setup` is advertised, list connected sites and their Search Console state. Direct the user to the official Hubbly dashboard to connect a site or complete OAuth. Never collect passwords or refresh tokens.
4. Choose a site UUID returned by the gateway and run read-only health and visibility commands. Preserve provenance, freshness, and unmeasured states. `/rank-scan` is a public homepage-only fetch and does not compare competitors.
5. Before any proposed write, read `safe-autonomy.md` and obtain the user's direction. The current client does not implement preview/confirm, so all three write commands remain disabled and make no network request.
