#!/usr/bin/env python3
"""Regenerate or verify Agent Builder's pinned, filtered Spec Kit asset bundle.

Refresh needs Python 3.11+, Spec Kit's release-build dependencies, and an isolated
checkout of the pinned upstream commit. Verification uses only the standard library.
Member machines never run this script or the Spec Kit CLI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "skills/agent-builder/vendor/spec-kit"
UPSTREAM_URL = "https://github.com/github/spec-kit.git"
UPSTREAM_VERSION = "1.1.0"
UPSTREAM_COMMIT = "f1d3a4f8337ebbd3ae22760a9c12e3352b93a175"
STEPS = ("assess-research", "specify", "clarify", "checklist", "plan", "tasks", "analyze")
SCRIPTS = (
    "check-prerequisites.sh",
    "common.sh",
    "create-new-feature.sh",
    "resolve-template.sh",
    "setup-plan.sh",
    "setup-tasks.sh",
)
TEMPLATES = ("spec-template.md", "plan-template.md", "tasks-template.md", "checklist-template.md")
HOST_DIR = {"claude": ".claude/skills", "codex": ".agents/skills"}
CLI_EXPR = "import sys; sys.path.insert(0, 'src'); from specify_cli import main; main()"


def expected_paths() -> tuple[Path, ...]:
    paths = [Path("LICENSE")]
    for host in HOST_DIR:
        paths.extend(Path(host, f"speckit-{step}", "SKILL.md") for step in STEPS)
    paths.extend(Path("project/.specify/scripts/bash") / name for name in SCRIPTS)
    paths.extend(Path("project/.specify/templates") / name for name in TEMPLATES)
    return tuple(paths)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> None:
    manifest_path = DEST / "manifest.json"
    if manifest_path.is_symlink():
        raise ValueError("Spec Kit manifest must not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    upstream = manifest.get("upstream", {})
    if upstream.get("version") != UPSTREAM_VERSION or upstream.get("commit") != UPSTREAM_COMMIT:
        raise ValueError("Spec Kit manifest version/commit differs from the approved pin")
    listed = manifest.get("files")
    expected = {path.as_posix() for path in expected_paths()}
    if not isinstance(listed, dict) or set(listed) != expected:
        raise ValueError("Spec Kit manifest does not contain exactly the approved asset allowlist")
    actual = {
        path.relative_to(DEST).as_posix()
        for path in DEST.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    if actual != expected:
        raise ValueError(f"Spec Kit bundle has missing or extra files: {sorted(actual ^ expected)}")
    for relative, digest in listed.items():
        asset = DEST / relative
        if asset.is_symlink():
            raise ValueError(f"Spec Kit asset must not be a symlink: {relative}")
        if sha256(asset) != digest:
            raise ValueError(f"Spec Kit asset drift: {relative}")


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def source_checkout(source: Path | None, temporary: Path) -> Path:
    if source is None:
        source = temporary / "spec-kit"
        run("git", "clone", "--quiet", UPSTREAM_URL, str(source))
        run("git", "checkout", "--quiet", "--detach", UPSTREAM_COMMIT, cwd=source)
    source = source.resolve()
    commit = subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=source, text=True).strip()
    if commit != UPSTREAM_COMMIT:
        raise ValueError(f"Spec Kit checkout is {commit}, expected {UPSTREAM_COMMIT}")
    changes = subprocess.check_output(
        ("git", "status", "--porcelain", "--untracked-files=all"), cwd=source, text=True
    ).strip()
    if changes:
        raise ValueError("Spec Kit checkout has local changes; use a clean pinned checkout")
    if not (source / "src/specify_cli").is_dir() or not (source / "LICENSE").is_file():
        raise ValueError("pinned Spec Kit checkout is incomplete")
    return source


def refresh(source: Path | None, python: str) -> None:
    if sys.version_info < (3, 11):
        raise ValueError("refresh needs Python 3.11+; verify mode supports older Python")
    with tempfile.TemporaryDirectory(prefix="agent-builder-spec-kit-") as name:
        temporary = Path(name)
        checkout = source_checkout(source, temporary)
        output = {}
        for host in HOST_DIR:
            target = temporary / host
            run(
                python,
                "-c",
                CLI_EXPR,
                "init",
                str(target),
                "--integration",
                host,
                "--script",
                "sh",
                "--extension",
                "assess",
                "--non-interactive",
                cwd=checkout,
            )
            output[host] = target

        sources = {Path("LICENSE"): checkout / "LICENSE"}
        for host, directory in HOST_DIR.items():
            for step in STEPS:
                sources[Path(host, f"speckit-{step}", "SKILL.md")] = (
                    output[host] / directory / f"speckit-{step}" / "SKILL.md"
                )
        for script in SCRIPTS:
            sources[Path("project/.specify/scripts/bash") / script] = (
                output["claude"] / ".specify/scripts/bash" / script
            )
        for template in TEMPLATES:
            sources[Path("project/.specify/templates") / template] = (
                output["claude"] / ".specify/templates" / template
            )
        if set(sources) != set(expected_paths()):
            raise ValueError("internal asset allowlist mismatch")
        existing = (
            {
                path.relative_to(DEST)
                for path in DEST.rglob("*")
                if path.is_file() and path.name != "manifest.json"
            }
            if DEST.exists()
            else set()
        )
        if existing - set(sources):
            raise ValueError(
                f"unexpected existing vendor assets: {sorted(existing - set(sources))}"
            )
        for relative, upstream_path in sources.items():
            if not upstream_path.is_file():
                raise ValueError(f"pinned Spec Kit CLI omitted {relative}")
            target = DEST / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(upstream_path, target)
        manifest = {
            "schema_version": 1,
            "upstream": {
                "name": "github/spec-kit",
                "version": UPSTREAM_VERSION,
                "commit": UPSTREAM_COMMIT,
                "license": "MIT",
                "repository": UPSTREAM_URL,
            },
            "generation": {
                host: [
                    "python",
                    "-c",
                    CLI_EXPR,
                    "init",
                    "<temporary-output>",
                    "--integration",
                    host,
                    "--script",
                    "sh",
                    "--extension",
                    "assess",
                    "--non-interactive",
                ]
                for host in HOST_DIR
            },
            "files": {path.as_posix(): sha256(DEST / path) for path in expected_paths()},
        }
        (DEST / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    verify()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify the committed payload offline")
    parser.add_argument("--source", type=Path, help="existing pinned upstream checkout")
    parser.add_argument(
        "--python", default=sys.executable, help="Python with Spec Kit release dependencies"
    )
    args = parser.parse_args()
    try:
        if args.check:
            verify()
        else:
            refresh(args.source, args.python)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"Spec Kit payload error: {error}", file=sys.stderr)
        return 1
    print(f"Spec Kit {UPSTREAM_VERSION} payload verified at {UPSTREAM_COMMIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
