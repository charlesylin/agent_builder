#!/usr/bin/env python3
"""Offer the agent-builder skill when someone starts building something new.

A `UserPromptSubmit` hook. Claude Code runs it before every prompt, hands it JSON on stdin,
and adds anything in ``additionalContext`` to the model's context. Hooks cannot ask a person
anything, so this one asks *Claude* to make the offer, and Claude does the asking.

Silence is the default. It prints nothing at all unless every one of these is true:

- the prompt looks like the start of something new (see ``looks_like_new_work``);
- the working directory is not already a seeded project (those carry an adapter file that
  points at the skill, so an offer would be noise);
- nothing has muted this session.

Muting: the marker is written **when the offer is made**, so a session is asked exactly once
whether the person accepts, declines, or ignores it. Waiting for a decline to arrive as a
command was worse: on 2026-09-14 a person answered "build directly without agent-builder" and
was offered again, because that sentence also reads as starting something. ``--mute
<session-id>`` remains for Claude to call explicitly; it is idempotent and harmless.

Exit status is always 0 and a failure prints nothing: a hook that breaks a person's prompt is
worse than a hook that misses one.

Debugging: set ``AGENT_BUILDER_HOOK_LOG`` to a file path and every invocation appends one line
saying what it decided and why. If that file never appears, the hook is not being run at all —
plugin hooks load only from an installed plugin, not from ``--plugin-dir``. ``--selftest``
exercises the matcher with no stdin, so you can prove the script itself works on a machine.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SKILL = "agent-builder"
MARKER_PREFIX = "agent-builder-offer-muted-"

# Claude Code 2.1.270 sends: cwd, hook_event_name, permission_mode, prompt, prompt_id,
# scratchpad_dir, session_id, transcript_path. "prompt" is the typed text — confirmed by trace
# on 2026-09-14, after an earlier guess of "user_prompt" made the hook silent forever. The rest
# are fallbacks so a schema change degrades into silence rather than a wrong read.
PROMPT_KEYS = ("prompt", "user_prompt", "user_prompt_raw", "message", "input", "text")

# Something is being created that does not exist yet. Deliberately conservative: a false
# positive costs one question, and the negative patterns below take precedence.
_CREATE = (
    r"(?:build|make|create|write|set\s+up|start|stand\s+up|spin\s+up|scaffold|bootstrap|automate)"
)
_THING = (
    r"(?:agent|skill|tool|script|service|app|application|bot|project|repo|repository|pipeline|"
    r"workflow|dashboard|cli|api|integration|connector|mcp|server|thing|something|utility)"
)
POSITIVE = [
    # "build an agent that…", "make a thing that…", "create a tool for…"
    re.compile(rf"\b{_CREATE}\b[^.?!]{{0,40}}\b{_THING}\b", re.I),
    # "i want to build…", "we need an internal tool…", "help me build…"
    re.compile(rf"\b(?:i|we)\s+(?:want|need|would\s+like)\b[^.?!]{{0,60}}\b{_THING}\b", re.I),
    re.compile(rf"\bhelp\s+me\b[^.?!]{{0,30}}\b{_CREATE}\b", re.I),
    # "starting a new project", "new agent for…"
    re.compile(rf"\bnew\s+{_THING}\b", re.I),
    # "can we automate that?", "is there a way to automate…"
    re.compile(r"\b(?:can|could|should)\s+(?:we|i|you)\b[^.?!]{0,40}\bautomate\b", re.I),
    # "where do I start", "what's the right way to set this up"
    re.compile(r"\b(?:where\s+do\s+(?:i|we)\s+start|right\s+way\s+to\s+(?:set|start))\b", re.I),
]
# Work on something that already exists, or a question about code. These win over POSITIVE.
NEGATIVE = [
    re.compile(
        r"\b(?:fix|debug|refactor|rename|review|explain|why\s+(?:is|does|did)|what(?:'s|\s+is)\s+the\s+"
        r"difference|how\s+does|what\s+does|translate|summariz|read|open|run\s+the\s+tests?)\b",
        re.I,
    ),
    re.compile(r"\b(?:this|that|the)\s+(?:bug|error|failure|test|traceback|stack\s*trace)\b", re.I),
]

OFFER = (
    "A hook noticed that this message may be the start of something new — an agent, a skill, a "
    f"tool, or a project. The `{SKILL}` skill exists for exactly this: it runs a short Define "
    "conversation, then seeds a governed repository with one script instead of writing files by "
    "hand.\n\n"
    "Before doing substantive work, ask the person once, in one short sentence, whether they want "
    f"to use `{SKILL}` for this. Do not describe the skill at length and do not start the work "
    "while asking.\n\n"
    f"- If they say yes, invoke the `{SKILL}` skill and follow it.\n"
    "- If they say no, or say this is a quick or throwaway task, drop it and continue with what "
    "they actually asked for. They will not be asked again this session.\n\n"
    "If this message is plainly not about creating something new, skip the question entirely and "
    "just help. The hook matches text, not intent."
)


def marker_path(session_id: str) -> Path:
    """Where this session's mute marker lives. Keyed by session, cleaned up with the temp dir."""

    safe = re.sub(r"[^A-Za-z0-9_-]", "", session_id)[:64] or "unknown"
    return Path(tempfile.gettempdir()) / f"{MARKER_PREFIX}{safe}"


def extract_prompt(payload: dict) -> str:
    """The text the person typed, from whichever key this Claude Code version uses."""

    for key in PROMPT_KEYS:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def looks_like_new_work(prompt: str) -> bool:
    """True when the text reads as creating something that does not exist yet."""

    if not prompt or len(prompt) > 2000:
        return False
    if any(pattern.search(prompt) for pattern in NEGATIVE):
        return False
    return any(pattern.search(prompt) for pattern in POSITIVE)


def is_seeded_project(cwd: str) -> bool:
    """True when the directory already has an Agent Builder project in it."""

    try:
        root = Path(cwd)
    except (TypeError, ValueError):
        return False
    return (root / ".agent-builder.json").is_file() or (
        root / "governance/project-state.yaml"
    ).is_file()


def should_offer(payload: dict) -> bool:
    session_id = str(payload.get("session_id") or "")
    if session_id and marker_path(session_id).exists():
        return False
    if is_seeded_project(str(payload.get("cwd") or "")):
        return False
    return looks_like_new_work(extract_prompt(payload))


def trace(message: str) -> None:
    """Append one line to AGENT_BUILDER_HOOK_LOG, when it is set. Never raises."""

    path = os.environ.get("AGENT_BUILDER_HOOK_LOG")
    if not path:
        return
    with contextlib.suppress(OSError), open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{datetime.now().isoformat(timespec='seconds')} {message}\n")


def decide(payload: dict) -> tuple[bool, str]:
    """Return (offer?, why) so the reason can be traced."""

    session_id = str(payload.get("session_id") or "")
    prompt = extract_prompt(payload)
    if session_id and marker_path(session_id).exists():
        return False, "already offered or muted this session"
    if is_seeded_project(str(payload.get("cwd") or "")):
        return False, "already a seeded project"
    if not looks_like_new_work(prompt):
        return False, f"prompt did not match: {prompt[:60]!r}"
    return True, f"offering for: {prompt[:60]!r}"


def selftest() -> int:
    """Run the matcher over known prompts without stdin, and report."""

    checks = [
        ("help me build a little service that watches our S3 bucket", True),
        ("we need an internal tool that summarizes QC reports. where do I start?", True),
        ("i want to make a thing that retrieves depmap data", True),
        ("fix the failing test in test_parser.py", False),
        ("what's the difference between a dataclass and a NamedTuple?", False),
    ]
    bad = 0
    for prompt, want in checks:
        got = looks_like_new_work(prompt)
        bad += got != want
        print(f"{'ok  ' if got == want else 'MISS'} {'offer ' if got else 'silent'}  {prompt[:60]}")
    print(f"{len(checks) - bad}/{len(checks)} correct; python {sys.version.split()[0]}")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--selftest":
        return selftest()
    if argv and argv[0] == "--mute":
        if len(argv) > 1:
            with contextlib.suppress(OSError):
                marker_path(argv[1]).touch()
            trace(f"muted session {argv[1]}")
        return 0

    try:
        payload = json.loads(sys.stdin.read() or "{}")
        if not isinstance(payload, dict):
            trace("input was not a JSON object")
            return 0
        offer, why = decide(payload)
        trace(f"keys={sorted(payload)} :: " + ("OFFER  " if offer else "silent ") + why)
        if not offer:
            return 0
        # Mark before printing: one offer per session, whatever the person does with it.
        session_id = str(payload.get("session_id") or "")
        if session_id:
            with contextlib.suppress(OSError):
                marker_path(session_id).touch()
        offer = OFFER
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": offer,
                }
            },
            sys.stdout,
        )
    except Exception:  # noqa: BLE001 - a broken hook must never break a prompt
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
