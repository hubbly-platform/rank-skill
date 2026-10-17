# Hubbly Rank Skill

Original, clean-room client instructions for the governed Hubbly Rank agent gateway. Install with `npx skills add hubbly-platform/rank-skill` once this repository is published. The installable skill lives at `skills/rank/`.

The private API remains the sole authorization and execution boundary. At this release stage it may report every Rank command unavailable; the client must fail closed. See `skills/rank/SKILL.md` and the command files for usage and limitations.

Local checks: `python3 -m unittest discover -s tests -v` and `bash -n skills/rank/scripts/rank-command.sh`. No API keys or proprietary server code belong in this repository.

The CI workflow template is in `docs/ci-workflow-template.yml`. It is not active because the publishing credential lacks GitHub's `workflow` scope; a maintainer must move it to `.github/workflows/ci.yml` with an authorized credential.
