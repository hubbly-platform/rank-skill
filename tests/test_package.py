"""Keep the public skill surface aligned with the twelve-command catalog."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "rank"
COMMANDS = {
    "rank", "rank-setup", "rank-scan", "rank-health", "rank-opportunities",
    "rank-visibility", "rank-questions", "rank-plan", "rank-write",
    "rank-publish", "rank-reviews", "rank-report",
}
PLAYBOOKS = {"first-run", "weekly-loop", "safe-autonomy"}


class PackageTests(unittest.TestCase):
    def test_catalog_files_are_complete_without_extra_commands(self):
        self.assertEqual({p.stem for p in (SKILL / "commands").glob("*.md")}, COMMANDS)
        self.assertEqual({p.stem for p in (SKILL / "playbooks").glob("*.md")}, PLAYBOOKS)

    def test_skill_is_installable_and_fail_closed(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("name: rank", text)
        self.assertIn("/v1/agent/capabilities", text)
        self.assertIn("disables those three commands", text)
        self.assertNotIn("gho_", text)


if __name__ == "__main__":
    unittest.main()
