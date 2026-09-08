"""Behavioral tests for the v0.1 scaffold contract."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from contextlib import redirect_stderr
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent_builder import ProjectSpec, ScaffoldError, create_project, validate_project  # noqa: E402
from agent_builder.cli import main  # noqa: E402

GENERATED_AT = datetime(2026, 9, 8, 12, 0, tzinfo=UTC)


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
            self.assertEqual(metadata["template_version"], "0.1.0")
            self.assertEqual(metadata["coding_agent_adapters"], ["codex", "gemini"])
            self.assertIsNone(metadata["runtime_profile"])

            project_metadata = tomllib.loads(
                (target / "pyproject.toml").read_text(encoding="utf-8")
            )
            self.assertEqual(project_metadata["project"]["name"], "generated-agent")

    def test_generated_project_runs_its_own_tests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "self-test-agent"
            spec = ProjectSpec.create(name="Self Test Agent", purpose="Exercise its scaffold.")
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

    def test_cli_returns_nonzero_for_an_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "existing"
            target.mkdir()

            error_output = StringIO()
            with redirect_stderr(error_output):
                result = main(
                    (
                        "init",
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
