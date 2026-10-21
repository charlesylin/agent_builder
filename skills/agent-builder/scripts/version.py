#!/usr/bin/env python3
"""Describe artifact metadata and remote freshness without fetching or updating code."""

import argparse
import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

STABLE = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")

PRE = r"(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = STABLE.pattern + rf"(?:-{PRE}(?:\.{PRE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        timeout=8,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    if result.returncode:
        raise ValueError("Git unavailable")
    return result.stdout.strip()


def repository(value):
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        raise ValueError("invalid repository")
    if "://" not in value:
        match = re.fullmatch(r"git@([^:]+):(.+)", value)
        if not match:
            raise ValueError("invalid repository")
        return (match[1].lower(), match[2].removesuffix(".git").rstrip("/"))
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "ssh"} or not parsed.hostname or parsed.password:
        raise ValueError("invalid repository")
    if parsed.query or parsed.fragment or (parsed.username and parsed.username != "git"):
        raise ValueError("credential-bearing repository")
    return (
        parsed.hostname.lower()
        + (
            f":{parsed.port}"
            if parsed.port not in {None, 443 if parsed.scheme == "https" else 22}
            else ""
        ),
        parsed.path.strip("/").removesuffix(".git"),
    )


def notice(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        name, version, updated = data["name"], data["version"], data["updated"]
        if data["schema_version"] != 1 or not isinstance(name, str) or not name.strip():
            raise ValueError("invalid metadata")
        if any(ord(c) < 32 for c in name) or not isinstance(updated, str):
            raise ValueError("invalid metadata")
        date.fromisoformat(updated)
        if version is not None and (
            not isinstance(version, str) or not re.fullmatch(SEMVER, version)
        ):
            raise ValueError("invalid version")
        branch = data.get("branch")
        if branch is not None and (
            not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/_.-]*", branch)
        ):
            raise ValueError("invalid branch")
        source = data.get("repository")
        identity = repository(source) if source else None
    except (OSError, ValueError, TypeError, KeyError):
        return "Version metadata invalid or unavailable; freshness unknown."
    prefix = f"{name} version {version or 'unversioned'}, last updated {updated}"
    root = Path(path).resolve().parent
    details = []
    checkout = False
    try:
        checkout = (
            identity is not None
            and repository(git(root, "remote", "get-url", "origin")) == identity
        )
        if checkout and git(root, "status", "--porcelain"):
            details.append("local modifications; unreleased work")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        pass
    if not source:
        return prefix + " — remote unavailable; freshness unknown."
    try:
        refs = dict(
            line.split()[::-1]
            for line in git(
                root,
                "ls-remote",
                source,
                "refs/tags/v*",
                *([f"refs/heads/{branch}"] if branch else []),
            ).splitlines()
        )
        tags = [
            tuple(map(int, match.groups()))
            for ref in refs
            if (match := STABLE.fullmatch(ref.removeprefix("refs/tags/v")))
            and ref.startswith("refs/tags/v")
        ]
        latest = max(tags) if tags else None
        current = STABLE.fullmatch(version or "")
        if latest is None:
            details.append("no stable remote tags; release freshness unknown")
        elif current:
            local = tuple(map(int, current.groups()))
            label = (
                "matches latest published version (metadata only)"
                if local == latest
                else (
                    "behind latest published version"
                    if local < latest
                    else "unreleased; newer than latest published version"
                )
            )
            details.append(f"{label} {'.'.join(map(str, latest))}")
        else:
            details.append("unversioned/prerelease; latest published " + ".".join(map(str, latest)))
        if checkout and branch:
            remote = refs.get(f"refs/heads/{branch}")
            head = git(root, "rev-parse", "HEAD")
            release_ref = f"refs/tags/v{version}"
            if head != refs.get(release_ref + "^{}", refs.get(release_ref)):
                details.append("checkout is not the named release; unreleased work")
            if remote == head:
                details.append("checkout matches remote branch tip")
            elif remote:
                try:
                    ahead, behind = git(
                        root, "rev-list", "--left-right", "--count", f"{head}...{remote}"
                    ).split()
                    details.append(f"checkout ahead {ahead}, behind {behind} commits")
                except ValueError:
                    details.append("remote branch differs; distance unknown")
            else:
                details.append("remote branch unavailable")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        details.append("remote unavailable; freshness unknown")
    return prefix + " — " + "; ".join(details) + "."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "metadata",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parents[1] / "version.json",
    )
    print(notice(parser.parse_args().metadata))


if __name__ == "__main__":
    main()
