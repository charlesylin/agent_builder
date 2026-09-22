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
from check import phase_exit_issues, proposed_decisions, validate_project  # noqa: E402
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
        project = ProjectSpec.create(
            name="Plain Project", purpose="Check neutral kind.", kind="project"
        )
        self.assertEqual(project.kind, "project")
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

    def test_project_kind_seeds_a_neutral_valid_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "s3-watcher"
            spec = ProjectSpec.create(
                name="S3 Watcher",
                purpose="Notice new input files and start the approved process.",
                kind="project",
                adapters=("codex", "claude"),
            )
            create_project(target, spec, generated_at=GENERATED_AT)

            self.assertEqual(validate_project(target), ())
            manifest = json.loads((target / ".agent-builder.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["kind"], "project")
            self.assertNotIn("runtime_profile", manifest)
            self.assertNotIn("python_package", manifest)

            state = (target / "governance/project-state.yaml").read_text(encoding="utf-8")
            self.assertIn("  kind: project\n", state)
            self.assertIn("  current: define\n", state)
            self.assertNotIn("\nruntime:\n", state)
            self.assertNotIn("\ndeployment:\n", state)
            agreement = (target / "governance/operating-agreement.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("neutral project", agreement)
            self.assertNotIn("Docker Compose", agreement)

            for relative in ("contracts", "deployment", "src", "SKILL.md", ".claude-plugin"):
                self.assertFalse((target / relative).exists(), relative)
            ci = (target / ".github/workflows/ci.yml").read_text(encoding="utf-8")
            self.assertIn("unittest discover", ci)
            self.assertNotIn("compileall -q src", ci)
            dependabot = (target / ".github/dependabot.yml").read_text(encoding="utf-8")
            self.assertNotIn("package-ecosystem: pip", dependabot)

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
        for kind in ("agent", "skill", "project"):
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
            self.assertIn("Ran 2 tests" if kind == "project" else "Ran 3 tests", result.stderr)

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
            for kind in ("agent", "project"):
                with self.subTest(kind=kind):
                    target = Path(directory) / f"committed-{kind}"
                    spec = ProjectSpec.create(
                        name=f"Committed {kind}", purpose="Starts with history.", kind=kind
                    )
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
                        ["git", "status", "--porcelain"],
                        cwd=target,
                        capture_output=True,
                        text=True,
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

        # Structural, not tied to a particular release: whatever heading is newest, --since the
        # first release returns everything above it and nothing from it.
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        headings = re.findall(r"^## \[([^\]]+)\]", changelog, flags=re.MULTILINE)
        newest, oldest = headings[0], headings[-1]
        self.assertEqual(oldest, "0.1.0")

        newer = check.changes_since(oldest)
        self.assertIn(f"## [{newest}]", newer)
        self.assertNotIn(f"## [{oldest}]", newer)
        self.assertIn("Nothing newer", check.changes_since(newest))
        self.assertIn("No changelog heading for '9.9.9'", check.changes_since("9.9.9"))
        self.assertEqual(seed.TEMPLATE_VERSION, newest, "the released version heads the changelog")

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

    def test_principles_are_named_wherever_they_are_summarized(self) -> None:
        # F-005: asked "what is Nokkvi's law", a session that had only seen the short forms
        # truthfully said it had never heard of it, because no short form carried a title.
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for title in ("Phase control", "Nokkvi's law", "Security and authority"):
            with self.subTest(where="SKILL.md", title=title):
                self.assertIn(f"**{title}.**", skill)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "named"
            spec = ProjectSpec.create(
                name="Named", purpose="Name the principles.", adapters=["claude"]
            )
            create_project(target, spec, generated_at=GENERATED_AT)
            adapter = (target / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("**Nokkvi's law.**", adapter)

    def test_seeded_default_decisions_match_the_kind(self) -> None:
        # F-008: a skill project inherited "deploy the eventual agent as an OCI container".
        with tempfile.TemporaryDirectory() as directory:
            for kind, expect_oci in (("agent", True), ("skill", False), ("project", False)):
                with self.subTest(kind=kind):
                    target = Path(directory) / kind
                    spec = ProjectSpec.create(
                        name=f"Kind {kind}", purpose="Check defaults.", kind=kind
                    )
                    create_project(target, spec, generated_at=GENERATED_AT)
                    ledger = (target / "governance/decisions.yaml").read_text(encoding="utf-8")
                    self.assertEqual("OCI container" in ledger, expect_oci)
                    self.assertIn("-D001", ledger)
                    self.assertIn("-D002", ledger)

    def test_seeded_projects_start_active_and_reject_unknown_statuses(self) -> None:
        # AB-D031: a project's lifecycle is separate from its phase, so a colleague opening a
        # repository can tell "not started yet" from "nobody is doing this any more".
        with tempfile.TemporaryDirectory() as directory:
            for kind in ("agent", "skill", "project"):
                with self.subTest(kind=kind):
                    target = Path(directory) / kind
                    spec = ProjectSpec.create(name=f"S {kind}", purpose="Check status.", kind=kind)
                    create_project(target, spec, generated_at=GENERATED_AT)
                    state_path = target / "governance/project-state.yaml"
                    self.assertIn("  status: active\n", state_path.read_text(encoding="utf-8"))
                    self.assertEqual(validate_project(target), ())

                    for status, valid in (("paused", True), ("abandoned", True), ("zombie", False)):
                        state = state_path.read_text(encoding="utf-8")
                        state_path.write_text(
                            re.sub(
                                r"^  status: \w+$",
                                f"  status: {status}",
                                state,
                                count=1,
                                flags=re.M,
                            ),
                            encoding="utf-8",
                        )
                        codes = {issue.code for issue in validate_project(target)}
                        self.assertEqual("invalid-status" not in codes, valid, status)

    def test_a_project_predating_the_status_field_still_validates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "legacy"
            spec = ProjectSpec.create(name="Legacy", purpose="Predates project.status.")
            create_project(target, spec, generated_at=GENERATED_AT)
            state_path = target / "governance/project-state.yaml"
            state = state_path.read_text(encoding="utf-8").replace("  status: active\n", "", 1)
            state_path.write_text(state, encoding="utf-8")
            self.assertEqual(validate_project(target), ())

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


class ReviewFeedbackTests(unittest.TestCase):
    """0.2.1: Sean's review feedback (AB-D033..036) and the Nokkvi's-law amendment (AB-D037)."""

    def _seed(self, directory: str, **framing: str) -> Path:
        target = Path(directory) / "framed"
        spec = ProjectSpec.create(name="Framed", purpose="Answer the problem.", **framing)
        create_project(target, spec, generated_at=GENERATED_AT)
        return target

    def test_problem_answers_are_written_to_definition(self) -> None:
        # AB-D033: the four problem questions are recorded verbatim, before purpose.
        with tempfile.TemporaryDirectory() as directory:
            target = self._seed(
                directory,
                problem="Deals vanish  before anyone sees them.",
                current_approach="Three sites checked by hand.",
                value="One instrument a quarter at half price.",
                beneficiaries="The lab manager.",
            )
            definition = (target / "planning/definition.md").read_text(encoding="utf-8")
            self.assertLess(
                definition.index("## What problem does this solve?"),
                definition.index("## Purpose"),
            )
            self.assertIn("Deals vanish before anyone sees them.", definition)
            self.assertIn("The lab manager.", definition)
            self.assertTrue((target / "planning/later.md").is_file())
            self.assertFalse(validate_project(target), "seeding must still validate")

    def test_leaving_define_requires_every_answer_and_no_open_proposal(self) -> None:
        # AB-D033 + AB-D035: the gate names what is missing instead of failing vaguely.
        with tempfile.TemporaryDirectory() as directory:
            target = self._seed(directory, problem="Known.")
            issues = phase_exit_issues(target, "define")
            messages = "\n".join(f"{issue.code}: {issue.message}" for issue in issues)
            self.assertEqual({"unanswered", "proposed-decision"}, {issue.code for issue in issues})
            self.assertIn("'How is it solved today?' is still", messages)
            self.assertNotIn("'What problem does this solve?'", messages, "answered at seed time")
            self.assertIn("framed-D003 is still proposed", messages)

            definition = target / "planning/definition.md"
            definition.write_text(
                definition.read_text(encoding="utf-8").replace("(not yet answered)", "Answered."),
                encoding="utf-8",
            )
            ledger = target / "governance/decisions.yaml"
            ledger.write_text(
                ledger.read_text(encoding="utf-8").replace("status: proposed", "status: rejected"),
                encoding="utf-8",
            )
            self.assertEqual((), phase_exit_issues(target, "define"))

    def test_leaving_the_wrong_phase_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._seed(directory)
            codes = [issue.code for issue in phase_exit_issues(target, "build")]
            self.assertIn("wrong-phase", codes)
            self.assertEqual(
                ("unknown-phase",), tuple(i.code for i in phase_exit_issues(target, "ship"))
            )

    def test_proposed_decisions_are_read_per_entry(self) -> None:
        ledger = (
            "decisions:\n"
            "  - id: x-D001\n    status: confirmed\n    decision: a\n"
            "  - id: x-D002\n    status: proposed\n    decision: b\n"
            "  - id: x-D003\n    status: superseded\n    decision: c\n"
            "  - id: x-D004\n    status: proposed\n    decision: d\n"
        )
        self.assertEqual(("x-D002", "x-D004"), proposed_decisions(ledger))

    def test_leaving_cli_reports_and_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._seed(directory)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL / "scripts/check.py"),
                    str(target),
                    "--leaving",
                    "define",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("Cannot leave define yet", result.stderr)
            self.assertIn("unanswered", result.stderr)

    def test_skill_and_adapters_carry_the_review_rules(self) -> None:
        # AB-D033/035/036 must reach both the skill and the seeded project's own instructions,
        # because the seeded adapter does the work when the skill is not invoked (F-009).
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("What problem are you solving?", skill)
        self.assertLess(
            skill.index("**First, the problem.**"), skill.index("**Second, the kind.**")
        )
        self.assertIn("planning/later.md", skill)
        self.assertIn("**Approval is typed, never clicked.**", skill)
        self.assertIn("check.py . --leaving <old-phase>", skill)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "rules"
            spec = ProjectSpec.create(name="Rules", purpose="Carry the rules.", adapters=["claude"])
            create_project(target, spec, generated_at=GENERATED_AT)
            agreement = (target / "governance/operating-agreement.md").read_text(encoding="utf-8")
            self.assertIn("does not survive a phase close", agreement)
            self.assertIn("Do not use a menu pick or button as a substitute", agreement)
            self.assertIn("do not create a second approval round", agreement)
            self.assertIn("planning/later.md", agreement)
            adapter = (target / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("**Build only what you need.**", adapter)
            self.assertIn("planning/later.md", adapter)

    def test_nokkvis_law_encourages_a_stuck_person(self) -> None:
        # AB-D037: the law is about tone; a frustrated person gets encouragement, then help.
        for path in (SKILL / "SKILL.md", ROOT / "principles/03-nokkvis-law.md"):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("you got this!", text)
            self.assertIn("frustrat", text)


class BuildOrAdoptTests(unittest.TestCase):
    """The v0.3 gate distinguishes evidence, a confirmed decision, and archiving."""

    def _planned(self, directory: str, *, kind: str = "project") -> Path:
        target = Path(directory) / "candidate"
        spec = ProjectSpec.create(name="Candidate", purpose="Meet one need.", kind=kind)
        create_project(target, spec, generated_at=GENERATED_AT)
        state_path = target / "governance/project-state.yaml"
        state_path.write_text(
            state_path.read_text(encoding="utf-8").replace("  current: define\n", "  current: plan\n"),
            encoding="utf-8",
        )
        ledger_path = target / "governance/decisions.yaml"
        ledger_path.write_text(
            ledger_path.read_text(encoding="utf-8").replace("status: proposed", "status: rejected"),
            encoding="utf-8",
        )
        return target

    def _record(self, target: Path, outcome: str) -> None:
        path = target / "planning/solution-evaluation.md"
        text = path.read_text(encoding="utf-8")
        values = {
            "Need": "Read an existing dependency dataset.",
            "Search date": "2026-09-22",
            "Public sources searched": "Public skill registry and GitHub; links recorded in notes.",
            "User-provided codebases checked": "None offered by the author.",
            "Candidate fit": "A maintained skill covers the requested read-only workflow.",
            "Utilization and maintenance": "Releases this year and visible community usage.",
            "Tests and security history": "CI tests pass; security history reviewed.",
            "License obligations": "MIT; retain notice.",
            "Setup and operating burden": "Install one skill; no service to run.",
            "Evidence-backed reason": "Existing skill is a smaller path to the same outcome.",
            "Author confirmation": "The author typed approval of this recommendation.",
            "Decision record": "candidate-D003",
        }
        if outcome in {"adapt", "build"}:
            values.update(
                {
                    "Reused components and replaceable boundary": "Reuse the documented API behind one adapter.",
                    "Failure behavior and robustness": "Reject unavailable or malformed input clearly.",
                    "Why this is the simpler, maintainable option": "One small service beats a custom browser side-load.",
                }
            )
        for field, value in values.items():
            text = re.sub(rf"^- {re.escape(field)}: .*?$", f"- {field}: {value}", text, flags=re.M)
        text = text.replace("- Outcome: pending", f"- Outcome: {outcome}")
        if outcome == "adopt":
            text = text.replace(
                "- Adopted solution and version: not applicable",
                "- Adopted solution and version: Public Skill 1.2.0",
            )
        path.write_text(text, encoding="utf-8")
        if outcome in {"adapt", "build"}:
            state_path = target / "governance/project-state.yaml"
            state_path.write_text(
                state_path.read_text(encoding="utf-8")
                .replace("  target_version: null\n", '  target_version: "0.1.0"\n')
                .replace("  goal: null\n", '  goal: "Read one approved dataset reliably."\n'),
                encoding="utf-8",
            )
            definition_path = target / "planning/definition.md"
            definition_path.write_text(
                definition_path.read_text(encoding="utf-8").replace(
                    "(not yet answered)", "One documented read-only workflow.",
                ),
                encoding="utf-8",
            )
        ledger_path = target / "governance/decisions.yaml"
        ledger_path.write_text(
            ledger_path.read_text(encoding="utf-8")
            + "  - id: candidate-D003\n"
            + "    status: confirmed\n"
            + f"    decision: {outcome} the available solution.\n"
            + "    confirmed_by: author\n",
            encoding="utf-8",
        )

    def test_missing_evidence_blocks_plan_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._planned(directory)
            codes = {issue.code for issue in phase_exit_issues(target, "plan")}
            self.assertIn("missing-solution-evidence", codes)
            self.assertIn("missing-solution-decision", codes)
            self.assertIn("missing-decision-record", codes)
            self.assertEqual(validate_project(target), ())

    def test_adoption_requires_version_and_archived_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._planned(directory)
            self._record(target, "adopt")
            codes = {issue.code for issue in phase_exit_issues(target, "plan")}
            self.assertEqual(codes, {"adoption-not-archived"})
            state_path = target / "governance/project-state.yaml"
            state_path.write_text(
                state_path.read_text(encoding="utf-8").replace("  status: active\n", "  status: archived\n"),
                encoding="utf-8",
            )
            self.assertEqual(phase_exit_issues(target, "plan"), ())
            self.assertEqual(validate_project(target), ())
            self.assertIn("  current: plan\n", state_path.read_text(encoding="utf-8"))
            record = target / "planning/solution-evaluation.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace(
                    "Public Skill 1.2.0", "not applicable"
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "missing-adopted-version",
                {issue.code for issue in phase_exit_issues(target, "plan")},
            )

    def test_adapt_and_build_pass_with_a_completed_record(self) -> None:
        for outcome in ("adapt", "build"):
            with self.subTest(outcome=outcome), tempfile.TemporaryDirectory() as directory:
                target = self._planned(directory)
                self._record(target, outcome)
                self.assertEqual(phase_exit_issues(target, "plan"), ())

                ledger_path = target / "governance/decisions.yaml"
                ledger_path.write_text(
                    ledger_path.read_text(encoding="utf-8").replace(
                        "  - id: candidate-D003\n    status: confirmed",
                        "  - id: candidate-D003\n    status: rejected",
                    ),
                    encoding="utf-8",
                )
                self.assertIn(
                    "unconfirmed-solution-decision",
                    {issue.code for issue in phase_exit_issues(target, "plan")},
                )

    def test_version_and_quality_evidence_are_required_for_a_build(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._planned(directory)
            self._record(target, "build")
            state_path = target / "governance/project-state.yaml"
            state_path.write_text(
                state_path.read_text(encoding="utf-8").replace('"0.1.0"', '"01.0.0"'),
                encoding="utf-8",
            )
            record_path = target / "planning/solution-evaluation.md"
            record_path.write_text(
                record_path.read_text(encoding="utf-8").replace(
                    "One small service beats a custom browser side-load.", "(not yet recorded)"
                ),
                encoding="utf-8",
            )
            codes = {issue.code for issue in phase_exit_issues(target, "plan")}
            self.assertIn("invalid-deliverable-version", codes)
            self.assertIn("missing-technical-rationale", codes)

            state_path.write_text(
                state_path.read_text(encoding="utf-8").replace('"01.0.0"', '"0.1.0-rc.1"'),
                encoding="utf-8",
            )
            record_path.write_text(
                record_path.read_text(encoding="utf-8").replace(
                    "(not yet recorded)", "One adapter has a small, reviewable support cost.",
                ),
                encoding="utf-8",
            )
            self.assertEqual(phase_exit_issues(target, "plan"), ())

    def test_adoption_cannot_claim_a_new_project_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._planned(directory)
            self._record(target, "adopt")
            state_path = target / "governance/project-state.yaml"
            state_path.write_text(
                state_path.read_text(encoding="utf-8")
                .replace("  status: active\n", "  status: archived\n")
                .replace("  target_version: null\n", '  target_version: "0.1.0"\n'),
                encoding="utf-8",
            )
            self.assertIn(
                "adoption-has-project-release",
                {issue.code for issue in phase_exit_issues(target, "plan")},
            )

    def test_old_agent_projects_are_not_retroactively_gated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self._planned(directory, kind="agent")
            (target / "planning/solution-evaluation.md").unlink()
            self.assertEqual(phase_exit_issues(target, "plan"), ())
            self.assertEqual(validate_project(target), ())

            manifest_path = target / ".agent-builder.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["template_version"] = "0.3.0"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertIn(
                "missing-solution-evaluation",
                {issue.code for issue in phase_exit_issues(target, "plan")},
            )
            self.assertIn("missing-file", {issue.code for issue in validate_project(target)})


class PlainLanguageTests(unittest.TestCase):
    def test_human_briefings_do_not_require_internal_codes_or_empty_sections(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        guide = (SKILL / "references/closeout-template.md").read_text(encoding="utf-8")
        self.assertIn("the consequential decisions in plain words", skill)
        self.assertIn("do not make the\nperson learn local codes", skill)
        self.assertNotIn("four-section closeout", skill)
        self.assertNotIn("every decision, with ID and status", skill)
        self.assertNotIn("What should you be asking", guide)

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "plain"
            create_project(
                target,
                ProjectSpec.create(name="Plain", purpose="Show a clear status.", kind="project"),
                generated_at=GENERATED_AT,
            )
            agreement = (target / "governance/operating-agreement.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Do not make\nthe person decode local decision IDs", agreement)
            self.assertNotIn("Every human-facing closeout contains", agreement)
            ledger = (target / "governance/decisions.yaml").read_text(encoding="utf-8")
            self.assertIn("plain-D001", ledger, "stable IDs remain in the machine record")


if __name__ == "__main__":
    unittest.main()
