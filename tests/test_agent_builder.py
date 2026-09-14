"""Behavioral tests for the seeder and checker shipped inside the agent-builder skill."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "agent-builder"
sys.path.insert(0, str(SKILL / "scripts"))

import seed  # noqa: E402
from check import validate_project  # noqa: E402
from seed import ProjectSpec, ScaffoldError, create_project  # noqa: E402

GENERATED_AT = datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)


class ProjectSpecTests(unittest.TestCase):
    def test_defaults_to_codex_and_derives_identifiers(self) -> None:
        spec = ProjectSpec.create(name="Example Travel Agent", purpose="Review trip options.")

        self.assertEqual(spec.slug, "example-travel-agent")
        self.assertEqual(spec.python_package, "example_travel_agent")
        self.assertEqual(spec.adapters, ("codex",))

    def test_adapters_are_deduplicated_in_canonical_order(self) -> None:
        spec = ProjectSpec.create(
            name="Example",
            purpose="Exercise adapter selection.",
            adapters=("gemini", "codex", "gemini", "claude"),
        )

        self.assertEqual(spec.adapters, ("codex", "claude", "gemini"))

    def test_invalid_inputs_fail_loudly(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            ProjectSpec.create(name=" ", purpose="Valid purpose.")
        with self.assertRaisesRegex(ValueError, "unsupported adapter"):
            ProjectSpec.create(name="Example", purpose="Valid purpose.", adapters=("other",))
        with self.assertRaisesRegex(ValueError, "select at least one"):
            ProjectSpec.create(name="Example", purpose="Valid purpose.", adapters=())


class ScaffoldTests(unittest.TestCase):
    def test_generates_and_validates_selected_adapters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "generated-agent"
            spec = ProjectSpec.create(
                name="Generated Agent",
                purpose="Produce one deterministic review.",
                adapters=("codex", "gemini"),
            )

            files = create_project(target, spec, generated_at=GENERATED_AT)

            self.assertGreater(len(files), 20)
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / "GEMINI.md").is_file())
            self.assertFalse((target / "CLAUDE.md").exists())
            self.assertTrue((target / ".env.example").is_file())
            self.assertTrue((target / "src/generated_agent/__init__.py").is_file())
            self.assertEqual(validate_project(target), ())

            metadata = json.loads((target / ".agent-builder.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["template_version"], seed.TEMPLATE_VERSION)
            self.assertEqual(metadata["coding_agent_adapters"], ["codex", "gemini"])
            self.assertIsNone(metadata["runtime_profile"])

            pyproject = (target / "pyproject.toml").read_text(encoding="utf-8")
            name_line = re.search(r'^name = "([^"]+)"$', pyproject, flags=re.MULTILINE)
            self.assertIsNotNone(name_line)
            self.assertEqual(name_line.group(1), "generated-agent")

    def test_kind_defaults_to_agent_and_rejects_unknown_kinds(self) -> None:
        spec = ProjectSpec.create(name="Kind Test", purpose="Check kind handling.")
        self.assertEqual(spec.kind, "agent")
        with self.assertRaises(ValueError):
            ProjectSpec.create(name="Kind Test", purpose="Check kind handling.", kind="mcp")

    def test_agent_kind_files_come_from_the_kind_layer(self) -> None:
        # contracts/ and src/ live in templates/kinds/agent, not templates/base.
        self.assertTrue((SKILL / "templates/kinds/agent/contracts").is_dir())
        self.assertFalse((SKILL / "templates/base/contracts").exists())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "kind-layer-agent"
            spec = ProjectSpec.create(name="Kind Layer Agent", purpose="Check the layers.")
            create_project(target, spec, generated_at=GENERATED_AT)
            self.assertTrue((target / "contracts/schemas/agent-handoff.schema.json").is_file())
            self.assertTrue((target / "governance/project-state.yaml").is_file())

    def test_skill_kind_seeds_a_loadable_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "note-taker"
            spec = ProjectSpec.create(
                name="Note Taker", purpose="Turn rough notes into a checklist.", kind="skill"
            )
            create_project(target, spec, generated_at=GENERATED_AT)
            self.assertEqual(validate_project(target), ())

            skill = (target / "SKILL.md").read_text(encoding="utf-8")
            front_matter = re.match(r"\A---\n(.*?)\n---\n", skill, flags=re.DOTALL)
            self.assertIsNotNone(front_matter)
            self.assertIn('name: "note-taker"', front_matter.group(1))
            self.assertIn("description: ", front_matter.group(1))

            manifest = json.loads((target / ".agent-builder.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["kind"], "skill")
            plugin = json.loads((target / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(plugin["name"], "note-taker")

            # Kind overrides replaced agent-flavored base files; agent-only files are absent.
            self.assertIn("SKILL.md", (target / "README.md").read_text(encoding="utf-8"))
            self.assertFalse((target / "contracts").exists())
            self.assertFalse((target / "src").exists())
            self.assertFalse((target / ".dockerignore").exists())

    def test_validator_requires_kind_specific_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "broken-skill"
            spec = ProjectSpec.create(name="Broken Skill", purpose="Lose SKILL.md.", kind="skill")
            create_project(target, spec, generated_at=GENERATED_AT)
            (target / "SKILL.md").unlink()
            codes = {issue.code for issue in validate_project(target)}
            self.assertIn("missing-file", codes)

    def test_manifest_without_kind_validates_as_an_agent(self) -> None:
        # Projects generated by v0.1 have no "kind"; they must keep validating unchanged.
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "legacy-agent"
            spec = ProjectSpec.create(name="Legacy Agent", purpose="Predates kinds.")
            create_project(target, spec, generated_at=GENERATED_AT)
            manifest_path = target / ".agent-builder.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["kind"]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            self.assertEqual(validate_project(target), ())

    def test_generated_project_runs_its_own_tests(self) -> None:
        for kind in ("agent", "skill"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / f"self-test-{kind}"
                spec = ProjectSpec.create(
                    name=f"Self Test {kind}", purpose="Exercise its scaffold.", kind=kind
                )
                create_project(target, spec, generated_at=GENERATED_AT)

                result = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                    cwd=target,
                    check=False,
                    capture_output=True,
                    text=True,
                )

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Ran 3 tests", result.stderr)

    def test_refuses_to_overwrite_an_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "existing"
            target.mkdir()
            marker = target / "keep.txt"
            marker.write_text("user-owned", encoding="utf-8")
            spec = ProjectSpec.create(name="Example", purpose="Do not overwrite files.")

            with self.assertRaisesRegex(ScaffoldError, "refusing to overwrite"):
                create_project(target, spec, generated_at=GENERATED_AT)

            self.assertEqual(marker.read_text(encoding="utf-8"), "user-owned")

    def test_validator_detects_a_secret_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "secret-check-agent"
            spec = ProjectSpec.create(name="Secret Check Agent", purpose="Check generated files.")
            create_project(target, spec, generated_at=GENERATED_AT)
            (target / "bad.txt").write_text(
                "-----BEGIN PRIVATE KEY-----\nsynthetic-not-a-real-key\n",
                encoding="utf-8",
            )

            issues = validate_project(target)

            self.assertIn("possible-secret", {issue.code for issue in issues})

    def test_owner_is_recorded_when_given(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "owned"
            spec = ProjectSpec.create(name="Owned", purpose="Has an owner.", owner="  sean ")
            create_project(target, spec, generated_at=GENERATED_AT)
            manifest = json.loads((target / ".agent-builder.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["owner"], "sean")
            state = (target / "governance/project-state.yaml").read_text(encoding="utf-8")
            self.assertIn('  owner: "sean"\n', state)

    def test_seed_makes_the_first_commit_on_main(self) -> None:
        import os
        import shutil

        if shutil.which("git") is None:
            self.skipTest("git is not installed")
        identity = {
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        }
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "committed"
            spec = ProjectSpec.create(name="Committed", purpose="Starts with history.")
            create_project(target, spec, generated_at=GENERATED_AT)
            previous = {key: os.environ.get(key) for key in identity}
            os.environ.update(identity)
            try:
                status = seed.initialize_git(target, spec)
            finally:
                for key, value in previous.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
            self.assertIn("first commit", status)
            branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=target,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            self.assertEqual(branch, "main")
            dirty = subprocess.run(
                ["git", "status", "--porcelain"], cwd=target, capture_output=True, text=True
            ).stdout
            self.assertEqual(dirty, "")

    def test_template_version_matches_the_plugin_manifest(self) -> None:
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(seed.TEMPLATE_VERSION, plugin["version"])

    def test_agent_builder_skill_front_matter_is_well_formed(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md must begin with front matter")
        lines = match.group(1).splitlines()
        self.assertEqual(lines[0], "name: agent-builder")
        self.assertTrue(lines[1].startswith("description: '") and lines[1].endswith("'"))
        self.assertLessEqual(len(lines[1]) - len("description: ''"), 1024)
        self.assertEqual(len(lines), 2, "front matter carries only name and description")

    def test_adapters_point_at_the_skill_and_ask_for_a_briefing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "adapters"
            spec = ProjectSpec.create(
                name="Adapters",
                purpose="Check adapter text.",
                adapters=["codex", "claude", "gemini"],
            )
            create_project(target, spec, generated_at=GENERATED_AT)
            for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
                with self.subTest(adapter=name):
                    text = (target / name).read_text(encoding="utf-8")
                    self.assertIn("If the `agent-builder` skill is available, invoke it", text)
                    self.assertIn("give a briefing", text)
                    self.assertIn("governance/operating-agreement.md", text)

    def test_manifest_records_source_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "commit"
            spec = ProjectSpec.create(name="Commit", purpose="Record provenance.")
            create_project(target, spec, generated_at=GENERATED_AT)
            manifest = json.loads((target / ".agent-builder.json").read_text(encoding="utf-8"))
            self.assertIn("source_commit", manifest)
            commit = manifest["source_commit"]
            self.assertTrue(commit is None or re.fullmatch(r"[0-9a-f]{40}", commit), commit)

    def test_since_reports_changelog_sections_newer_than_a_version(self) -> None:
        import check

        newer = check.changes_since("0.1.0")
        self.assertIn("## [Unreleased]", newer)
        self.assertNotIn("## [0.1.0]", newer)
        unknown = check.changes_since("9.9.9")
        self.assertIn("No changelog heading for '9.9.9'", unknown)

    def test_skill_description_covers_start_and_resume(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        description = re.search(r"^description: '(.*)'$", text, flags=re.MULTILINE).group(1)
        for phrase in (
            "build an agent",
            "status here",
            "where did we leave off",
            "what phase are we in",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, description)

    def test_cli_returns_nonzero_for_an_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "existing"
            target.mkdir()

            error_output = StringIO()
            with redirect_stderr(error_output):
                result = seed.main(
                    (
                        str(target),
                        "--name",
                        "Example",
                        "--purpose",
                        "Exercise the command line.",
                    )
                )

            self.assertEqual(result, 2)
            self.assertIn("refusing to overwrite", error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
