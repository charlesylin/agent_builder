"""Budget enforcement, truthful freshness, and portable fresh-clone behavior."""

import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, suppress
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/agent-builder/scripts"))
import changes  # noqa: E402
import seed  # noqa: E402
import version  # noqa: E402
from check import validate_project  # noqa: E402


def git(root, *args):
    return subprocess.check_output(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            *args,
        ],
        text=True,
    ).strip()


def commit(root):
    git(root, "add", "-A")
    git(root, "commit", "-qm", "fixture")
    return git(root, "rev-parse", "HEAD")


class ChangesTests(unittest.TestCase):
    def test_counts_rename_binary_untracked_and_budget_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git(root, "init", "-q")
            (root / "old name.py").write_text("".join(f"x={i}\n" for i in range(30)))
            (root / "image.bin").write_bytes(b"\0old")
            (root / ".gitignore").write_text("ignored/\n")
            base = commit(root)
            git(root, "mv", "old name.py", "new name.py")
            with (root / "new name.py").open("a") as f:
                f.write("extra=1\n")
            (root / "image.bin").write_bytes(b"\0newer")
            (root / "notes.md").write_text("note\n")
            (root / "ignored").mkdir()
            (root / "ignored/no.py").write_text("excluded\n")
            report = changes.measure(root, base)
            self.assertEqual(report["rows"]["Python code"]["added"], 1)
            self.assertEqual(report["rows"]["Python code"]["baseline"], 30)
            binary = report["rows"]["Misc: .bin files (bytes)"]
            self.assertEqual((binary["added"], binary["removed"]), (6, 4))
            self.assertNotIn("ignored/no.py", report["paths"])
            self.assertIsNone(report["rows"]["Documentation"]["percent"])
            budget = {
                "schema_version": 1,
                "baseline": base,
                "paths": ["*"],
                "limits": {
                    label: {k: r[k] for k in ("added", "removed")}
                    for label, r in report["rows"].items()
                },
            }
            self.assertFalse(changes.check_budget(report, budget))
            budget["limits"]["Python code"]["added"] = 0
            self.assertTrue(changes.check_budget(report, budget))
            budget["paths"] = ["*.py"]
            self.assertTrue(any("notes.md" in x for x in changes.check_budget(report, budget)))
            budget_path = root / "ignored/budget.json"
            budget_path.write_text(json.dumps(budget))
            with redirect_stdout(StringIO()):
                self.assertEqual(changes.main([str(root), "--budget", str(budget_path)]), 1)
                self.assertEqual(changes.main([str(root), "--base", "not-a-commit"]), 2)

    def test_staged_deletion_keeps_ignored_copy_and_never_reads_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git(root, "init", "-q")
            (root / "local.md").write_text("local\nnotes\n")
            (root / "external").write_text("replaced\n")
            base = commit(root)
            git(root, "rm", "--cached", "local.md")
            (root / ".gitignore").write_text("local.md\n")
            (root / "external").unlink()
            with suppress(OSError):  # Windows may lack symlink privilege.
                (root / "external").symlink_to(root / "missing")
            report = changes.measure(root, base)
            self.assertEqual(report["rows"]["Documentation"]["removed"], 2)
            self.assertEqual(report["rows"]["Documentation"]["added"], 0)
            if (root / "external").is_symlink():
                self.assertEqual(report["rows"]["Misc: external files (links)"]["added"], 1)
            self.assertEqual(report["rows"]["Misc: external files"]["removed"], 1)
            self.assertTrue((root / "local.md").is_file())
            self.assertEqual(changes.category("src/a.ts", {}), "TypeScript code")
            self.assertEqual(changes.category("a.py", {"a.py": "override"}), "override")


class VersionTests(unittest.TestCase):
    def test_remote_status_and_unavailable_states_never_guess(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "version.json"
            data = {
                "schema_version": 1,
                "name": "Example",
                "version": "1.0.0",
                "updated": "2026-10-21",
                "repository": "https://example.com/repo.git",
                "branch": "main",
            }
            path.write_text(json.dumps(data))

            def fake_git(root, *args):
                if args[0] == "remote":
                    return data["repository"]
                if args[0] == "status":
                    return " M file.py"
                if args[0] == "ls-remote":
                    return "abc refs/tags/v1.0.0\ndef refs/heads/main\nzzz refs/tags/v9.0.0-beta"
                if args[0] == "rev-parse":
                    return "abc"
                return "0 2"

            with patch.object(version, "git", side_effect=fake_git):
                text = version.notice(path)
                self.assertIn("matches latest published version", text)
                self.assertIn("local modifications", text)
                self.assertIn("behind 2 commits", text)
                data["version"] = "0.9.0"
                path.write_text(json.dumps(data))
                self.assertIn("behind latest published version", version.notice(path))
            with patch.object(version, "git", side_effect=ValueError("private auth detail")):
                text = version.notice(path)
                self.assertIn("freshness unknown", text)
                self.assertNotIn("private auth detail", text)
            data.update(version=None, repository=None)
            path.write_text(json.dumps(data))
            self.assertIn("unversioned", version.notice(path))
            for bad in (
                "{}",
                "[]",
                "{",
                json.dumps({**data, "updated": "yesterday"}),
                json.dumps({**data, "version": "1.0.0-01"}),
                json.dumps({**data, "repository": "https://user:password@example.com/repo"}),
            ):
                path.write_text(bad)
                self.assertIn("invalid or unavailable", version.notice(path))
                self.assertNotIn("password", version.notice(path))

    def test_no_tags_and_missing_commit_distance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "version.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "name": "X",
                        "version": "1.0.0",
                        "updated": "2026-10-21",
                        "repository": "https://example.com/r",
                        "branch": "main",
                    }
                )
            )
            with patch.object(
                version,
                "git",
                side_effect=[
                    "https://example.com/r",
                    "",
                    "remote refs/heads/main",
                    "local",
                    ValueError(),
                ],
            ):
                text = version.notice(path)
                self.assertIn("no stable remote tags", text)
                self.assertIn("distance unknown", text)


class FreshCloneTests(unittest.TestCase):
    def test_all_kinds_keep_helpers_and_validate_without_local_notes(self):
        with tempfile.TemporaryDirectory() as directory:
            for kind in seed.SUPPORTED_KINDS:
                root = Path(directory) / kind
                seed.create_project(
                    root, seed.ProjectSpec.create(name=kind, purpose="One result.", kind=kind)
                )
                git(root, "init", "-q")
                commit(root)
                clone = Path(directory) / (kind + "-clone")
                git(Path(directory), "clone", "-q", str(root), str(clone))
                self.assertFalse((clone / "planning/open-questions.md").exists())
                self.assertFalse((clone / "planning/later.md").exists())
                self.assertEqual(validate_project(clone), ())
                for helper in ("version.py", "changes.py"):
                    self.assertEqual(
                        (clone / "scripts" / helper).read_bytes(),
                        (ROOT / "skills/agent-builder/scripts" / helper).read_bytes(),
                    )
                self.assertIsNone(json.loads((clone / "version.json").read_text())["version"])
                result = subprocess.run(
                    [sys.executable, str(clone / "scripts/version.py")],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertIn("unversioned", result.stdout)
                marker = clone / ".agent-builder.json"
                data = json.loads(marker.read_text())
                data["template_version"] = "0.5.0"
                marker.write_text(json.dumps(data))
                self.assertTrue(
                    any(
                        i.path == Path("planning/open-questions.md")
                        for i in validate_project(clone)
                    )
                )


if __name__ == "__main__":
    unittest.main()
