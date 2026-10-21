#!/usr/bin/env python3
"""Report physical-line changes against a fixed commit; enforce an approved JSON budget."""

import argparse
import fnmatch
import json
import os
import subprocess
from pathlib import Path


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=30)
    if result.returncode:
        raise ValueError("Git operation failed; check repository and baseline")
    return result.stdout


def category(name, overrides):
    for pattern, label in overrides.items():
        if fnmatch.fnmatchcase(name, pattern):
            return label
    path = Path(name.removesuffix(".tmpl"))
    suffix = path.suffix.lower()
    languages = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".jsx": "JavaScript",
        ".sh": "Shell",
        ".bash": "Shell",
        ".rs": "Rust",
        ".go": "Go",
        ".css": "CSS",
        ".html": "HTML",
    }
    if suffix in languages:
        role = "tests" if any(p in {"tests", "test", "evals"} for p in path.parts) else "code"
        return f"{languages[suffix]} {role}"
    if suffix == ".md":
        instruction = (
            path.name
            in {"SKILL.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "operating-agreement.md"}
            or "principles" in path.parts
        )
        return "Instruction Markdown" if instruction else "Documentation"
    if path.name.upper().startswith(("LICENSE", "COPYING")):
        return "Misc: license"
    if suffix in {".json", ".yaml", ".yml", ".toml"} or path.name.startswith("."):
        return "Misc: configuration/metadata"
    return f"Misc: {suffix or path.name} files"


def measure(root, base, overrides=None):
    root = Path(root).resolve()
    if Path(os.fsdecode(git(root, "rev-parse", "--show-toplevel")).strip()).resolve() != root:
        raise ValueError("root must be the repository root")
    base = (
        git(root, "rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
    )
    overrides = overrides or {}
    tree = {}
    for entry in git(root, "ls-tree", "-rz", base).split(b"\0"):
        if entry:
            info, name = entry.split(b"\t", 1)
            tree[os.fsdecode(name)] = info.split()[0]
    tracked = set(map(os.fsdecode, git(root, "ls-files", "-z").split(b"\0")))
    rows, paths = {}, set()

    def content(name, old=False):
        if old:
            return git(root, "show", f"{base}:{name}") if name in tree else b""
        path = root / name
        if name not in tracked or not path.exists() or not path.resolve().is_relative_to(root):
            return b""
        return path.read_bytes()

    def special(name, old=False):
        if old:
            return tree.get(name) in {b"120000", b"160000"}
        return (root / name).is_symlink() or (root / name).is_dir()

    def row(name, unit):
        label = category(name, overrides) + (f" ({unit})" if unit != "lines" else "")
        return rows.setdefault(
            label, dict(baseline=0, added=0, removed=0, files=0, generated=0, vendor=0, unit=unit)
        )

    for name in tree:
        if special(name, True):
            row(name, "links")["baseline"] += 1
        else:
            data = content(name, True)
            row(name, "bytes" if b"\0" in data else "lines")["baseline"] += (
                len(data)
                if b"\0" in data
                else data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))
            )

    entries = iter(
        git(
            root,
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--numstat",
            "-z",
            "--find-renames",
            base,
            "--",
        ).split(b"\0")
    )
    changes = []
    for entry in entries:
        if not entry:
            continue
        added, removed, name = entry.split(b"\t", 2)
        old = name
        if not name:
            old, name = next(entries), next(entries)
        changes.append((os.fsdecode(old), os.fsdecode(name), added, removed))
    for raw in git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
        if raw:
            name = os.fsdecode(raw)
            tracked.add(name)
            data = b"" if special(name) else content(name)
            count = (
                b"-"
                if b"\0" in data
                else str(data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))).encode()
            )
            changes.append((name, name, count, b"0"))
    for old, name, added, removed in changes:
        paths.update((old, name))
        is_link = special(old, True) or special(name)
        unit = "links" if is_link else ("bytes" if added == b"-" else "lines")
        item = row(name, unit)
        if is_link:
            plus, minus = int(name in tracked and special(name)), int(special(old, True))
            for path, before, key in ((old, True, "removed"), (name, False, "added")):
                if not special(path, before):
                    data = content(path, before)
                    if data:
                        binary = b"\0" in data
                        ordinary = row(path, "bytes" if binary else "lines")
                        ordinary[key] += (
                            len(data)
                            if binary
                            else (data.count(b"\n") + int(not data.endswith(b"\n")))
                        )
                        ordinary["files"] += 1
        elif unit == "bytes":
            plus, minus = len(content(name)), len(content(old, True))
        else:
            plus, minus = int(added), int(removed)
        item["added"] += plus
        item["removed"] += minus
        item["files"] += 1
        item["vendor"] += int(any(p in {"vendor", "third_party"} for p in Path(name).parts))
        item["generated"] += int(
            "templates/" in name
            or "stencils/" in name
            or (
                not is_link
                and any(
                    line.startswith(b"<!-- Generated by") for line in content(name).splitlines()[:8]
                )
            )
        )
    for item in rows.values():
        item["net"] = item["added"] - item["removed"]
        item["percent"] = 100 * item["net"] / item["baseline"] if item["baseline"] else None
    return {"baseline": base, "rows": rows, "paths": sorted(paths)}


def check_budget(report, budget):
    if budget.get("schema_version") != 1 or not isinstance(budget.get("paths"), list):
        raise ValueError("budget needs schema_version 1, paths and row limits")
    issues = [
        f"unapproved path: {p}"
        for p in report["paths"]
        if not any(fnmatch.fnmatchcase(p, pattern) for pattern in budget["paths"])
    ]
    limits = budget["limits"]
    for label, row in report["rows"].items():
        if row["files"]:
            for key in ("added", "removed"):
                limit = limits.get(label, {}).get(key)
                if type(limit) is not int or limit < 0:
                    issues.append(f"{label}: missing/invalid {key} limit")
                elif row[key] > limit:
                    issues.append(f"{label}: {key} {row[key]} exceeds {limit}")
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path.cwd())
    parser.add_argument("--base", help="fixed clean commit for an estimate without a budget")
    parser.add_argument(
        "--budget", type=Path, help="defaults to ROOT/governance/change-budget.json"
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        budget = (
            None
            if args.base
            else json.loads(
                (args.budget or (args.root / "governance/change-budget.json")).read_text()
            )
        )
        report = measure(
            args.root,
            args.base or budget["baseline"],
            budget.get("categories", {}) if budget else {},
        )
        issues = check_budget(report, budget) if budget else []
        if args.json:
            print(json.dumps({**report, "issues": issues}, indent=2))
        else:
            print("Category | Baseline | Added | Removed | Net | Net % | Files/generated/vendor")
            for label, row in sorted(report["rows"].items()):
                pct = f"{row['percent']:+.1f}%" if row["percent"] is not None else "N/A"
                print(
                    f"{label} | {row['baseline']} | +{row['added']} | -{row['removed']} | "
                    f"{row['net']:+} | {pct} | {row['files']}/{row['generated']}/{row['vendor']}"
                )
            lines = [row for row in report["rows"].values() if row["unit"] == "lines"]
            baseline, added, removed = (
                sum(row[k] for row in lines) for k in ("baseline", "added", "removed")
            )
            pct = f"{100 * (added - removed) / baseline:+.1f}%" if baseline else "N/A"
            print(f"Total text | {baseline} | +{added} | -{removed} | {added - removed:+} | {pct}")
            for issue in issues:
                print(issue)
        return int(bool(issues))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.TimeoutExpired):
        print("Invalid/unavailable repository or budget; verify baseline, paths and row limits.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
