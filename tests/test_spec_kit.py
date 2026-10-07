"""The pinned Spec Kit bundle is complete, filtered, and seeded without a member CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/agent-builder"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))

import refresh_spec_kit  # noqa: E402
from check import phase_exit_issues, validate_project  # noqa: E402
from seed import ProjectSpec, create_project  # noqa: E402


def _git(cwd: Path, *args: str) -> None:
    result = subprocess.run(
        [
            "git",
            "-c",
            "core.autocrlf=true",
            "-c",
            "user.name=Agent Builder Test",
            "-c",
            "user.email=test@example.invalid",
            *args,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr.strip()}")


class SpecKitBundleTests(unittest.TestCase):
    def test_committed_payload_is_exact_and_has_no_excluded_workflows(self) -> None:
        refresh_spec_kit.verify()
        names = set(json.loads((refresh_spec_kit.DEST / "manifest.json").read_text())["files"])
        self.assertEqual(len(names), 25)
        self.assertFalse(any("speckit-implement" in name for name in names))
        self.assertFalse(any("speckit-converge" in name for name in names))
        self.assertFalse(any("constitution-template" in name for name in names))
        self.assertEqual(list(SKILL.rglob("SKILL.md")), [SKILL / "SKILL.md"])
        for host in ("claude", "codex"):
            for step in refresh_spec_kit.STEPS:
                with self.subTest(host=host, step=step):
                    path = f"{host}/speckit-{step}/instructions.md"
                    self.assertIn(path, names)
                    self.assertTrue((refresh_spec_kit.DEST / path).is_file())

    def test_payload_drift_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "spec-kit"
            shutil.copytree(refresh_spec_kit.DEST, copy)
            with patch.object(refresh_spec_kit, "DEST", copy):
                refresh_spec_kit.verify()
                (copy / "project/.specify/templates/spec-template.md").write_text("changed")
                with self.assertRaisesRegex(ValueError, "asset drift"):
                    refresh_spec_kit.verify()

    @unittest.skipUnless(shutil.which("git"), "Git is needed for the checkout regression")
    def test_bundle_survives_autocrlf_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            bundle = source / "skills/agent-builder/vendor/spec-kit"
            bundle.parent.mkdir(parents=True)
            shutil.copytree(refresh_spec_kit.DEST, bundle)
            shutil.copy2(ROOT / ".gitattributes", source / ".gitattributes")
            _git(source, "init", "-q")
            _git(source, "add", "-A")
            _git(source, "commit", "-qm", "test pinned bundle")

            checkout = Path(directory) / "checkout"
            _git(Path(directory), "clone", "-q", str(source), str(checkout))
            with patch.object(
                refresh_spec_kit,
                "DEST",
                checkout / "skills/agent-builder/vendor/spec-kit",
            ):
                refresh_spec_kit.verify()

    def test_payload_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "spec-kit"
            shutil.copytree(refresh_spec_kit.DEST, copy)
            asset = copy / "project/.specify/templates/spec-template.md"
            asset.unlink()
            asset.symlink_to(refresh_spec_kit.DEST / "project/.specify/templates/spec-template.md")
            with (
                patch.object(refresh_spec_kit, "DEST", copy),
                self.assertRaisesRegex(ValueError, "must not be a symlink"),
            ):
                refresh_spec_kit.verify()

    def test_nested_skill_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "spec-kit"
            shutil.copytree(refresh_spec_kit.DEST, copy)
            (copy / "codex/speckit-plan/SKILL.md").write_text("unexpected skill")
            with (
                patch.object(refresh_spec_kit, "DEST", copy),
                self.assertRaisesRegex(ValueError, "must not be discoverable"),
            ):
                refresh_spec_kit.verify()


class SpecKitSeedTests(unittest.TestCase):
    def test_all_three_kinds_seed_for_each_target_host(self) -> None:
        for kind in ("agent", "skill", "project"):
            for host in ("claude", "codex"):
                with self.subTest(kind=kind, host=host), tempfile.TemporaryDirectory() as directory:
                    target = Path(directory) / "seeded"
                    spec = ProjectSpec.create(
                        name="Seeded",
                        purpose="Test bundled dependency.",
                        kind=kind,
                        adapters=(host,),
                    )
                    create_project(target, spec)
                    self.assertEqual(validate_project(target), ())
                    manifest = json.loads((target / ".agent-builder.json").read_text())
                    provenance = json.loads(
                        (target / ".specify/spec-kit-provenance.json").read_text()
                    )
                    self.assertEqual(manifest["template_version"], "0.4.1")
                    self.assertEqual(provenance["upstream"]["version"], "1.1.0")
                    self.assertEqual(
                        (target / ".specify/memory/constitution.md").read_bytes(),
                        (target / "governance/operating-agreement.md").read_bytes(),
                    )
                    self.assertFalse((target / ".agents/skills/speckit-implement").exists())
                    self.assertFalse((target / ".claude/skills/speckit-implement").exists())

    def test_gemini_only_retains_previous_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "gemini-only"
            spec = ProjectSpec.create(
                name="Gemini Only",
                purpose="Keep existing behavior.",
                kind="project",
                adapters=("gemini",),
            )
            create_project(target, spec)
            self.assertEqual(validate_project(target), ())
            self.assertFalse((target / ".specify").exists())
            self.assertFalse((target / ".gitattributes").exists())

    @unittest.skipUnless(shutil.which("git"), "Git is needed for the checkout regression")
    def test_seeded_project_survives_autocrlf_checkout(self) -> None:
        for host in ("claude", "codex"):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "source"
                spec = ProjectSpec.create(
                    name="Windows Git checkout",
                    purpose="Preserve pinned assets.",
                    kind="project",
                    adapters=(host,),
                )
                create_project(source, spec)
                self.assertTrue((source / ".gitattributes").is_file())
                _git(source, "init", "-q")
                _git(source, "add", "-A")
                _git(source, "commit", "-qm", "test seeded project")

                checkout = Path(directory) / "checkout"
                _git(Path(directory), "clone", "-q", str(source), str(checkout))
                self.assertEqual(validate_project(checkout), ())
                asset = checkout / ".specify/scripts/bash/check-prerequisites.sh"
                asset.write_bytes(asset.read_bytes() + b"# changed\n")
                self.assertIn(
                    "spec-kit-asset-drift", {issue.code for issue in validate_project(checkout)}
                )

    def test_checker_catches_missing_and_divergent_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "seeded"
            spec = ProjectSpec.create(name="Seeded", purpose="Check drift.", kind="project")
            create_project(target, spec)
            (target / ".specify/scripts/bash/setup-plan.sh").unlink()
            self.assertIn(
                "missing-spec-kit-asset", {item.code for item in validate_project(target)}
            )
            (target / ".specify/memory/constitution.md").write_text("stale")
            self.assertIn(
                "stale-constitution-view", {item.code for item in validate_project(target)}
            )

    def test_older_manifest_remains_valid_without_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "older"
            spec = ProjectSpec.create(name="Older", purpose="Stay valid.", kind="project")
            create_project(target, spec)
            shutil.rmtree(target / ".specify")
            shutil.rmtree(target / "third_party")
            manifest_path = target / ".agent-builder.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["template_version"] = "0.3.0"
            manifest_path.write_text(json.dumps(manifest) + "\n")
            self.assertEqual(validate_project(target), ())

    def test_plan_exit_requires_upstream_research_and_build_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "planned"
            spec = ProjectSpec.create(name="Planned", purpose="Check Plan gates.", kind="project")
            create_project(target, spec)
            state = target / "governance/project-state.yaml"
            state.write_text(state.read_text().replace("  current: define\n", "  current: plan\n"))
            record = target / "planning/solution-evaluation.md"
            record.write_text(record.read_text().replace("- Outcome: pending", "- Outcome: build"))
            codes = {issue.code for issue in phase_exit_issues(target, "plan")}
            self.assertIn("missing-spec-kit-research", codes)
            self.assertIn("missing-spec-kit-feature", codes)

    def test_archived_adoption_requires_research_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "adopted"
            spec = ProjectSpec.create(name="Adopted", purpose="Check adoption.", kind="project")
            create_project(target, spec)
            state = target / "governance/project-state.yaml"
            state.write_text(
                state.read_text().replace("  status: active\n", "  status: archived\n")
            )
            record = target / "planning/solution-evaluation.md"
            record.write_text(record.read_text().replace("- Outcome: pending", "- Outcome: adopt"))
            self.assertIn(
                "missing-spec-kit-research", {issue.code for issue in validate_project(target)}
            )

    def test_copied_skill_is_self_contained(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_copy = Path(directory) / "agent-builder"
            shutil.copytree(SKILL, skill_copy)
            for kind in ("agent", "skill", "project"):
                for host in ("claude", "codex"):
                    with self.subTest(kind=kind, host=host):
                        target = Path(directory) / f"{kind}-{host}"
                        result = subprocess.run(
                            [
                                sys.executable,
                                str(skill_copy / "scripts/seed.py"),
                                str(target),
                                "--name",
                                f"{kind} {host}",
                                "--purpose",
                                "Test a copied skill.",
                                "--kind",
                                kind,
                                "--adapter",
                                host,
                                "--no-git",
                            ],
                            text=True,
                            capture_output=True,
                            check=False,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(validate_project(target), ())
