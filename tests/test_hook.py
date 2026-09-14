"""The UserPromptSubmit hook: offers agent-builder on new work, silent otherwise."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "agent_builder_offer.py"
sys.path.insert(0, str(ROOT / "hooks"))

import agent_builder_offer as hook  # noqa: E402

# The seven eval prompts. The three marked False scored 0/3 on the skill description alone
# (docs/v0-2-skill-test.md, eval run 2); the hook is what catches them.
EVAL_PROMPTS = [
    "I want to build something that finds secondhand lab equipment listings and flags good deals.",
    "starting a new project today — a CLI that our scientists can use to look up internal"
    " compound IDs. what's the right way to set it up?",
    "can you help me make a skill that turns my rough experiment notes into a structured lab"
    " notebook entry with a checklist of what's missing",
    "i want to make a thing that can quickly retrieve depmap data and deploy it org wide with"
    " a few consistent ways of presenting the output",
    "i keep manually reformatting our assay results into the same report every week. can we"
    " automate that?",
    "help me build a little service that watches our S3 bucket for new FASTQs and kicks off"
    " the pipeline",
    "we need an internal tool that summarizes our weekly sequencing QC reports for the team."
    " where do I start?",
]
NOT_NEW_WORK = [
    "what's the difference between a dataclass and a NamedTuple in Python, and when would I"
    " pick one?",
    "fix the failing test in test_parser.py",
    "why is this build failing?",
    "explain how the retry logic works",
    "refactor the auth module to use async/await",
    "rename getUser to fetchUser across the repo",
    "summarize this document for me",
    "run the tests",
    "",
]


def invoke(payload: dict) -> str:
    """Run the hook as Claude Code does and return its stdout."""

    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


class MatcherTests(unittest.TestCase):
    def test_every_eval_prompt_is_recognized_as_new_work(self) -> None:
        for prompt in EVAL_PROMPTS:
            with self.subTest(prompt=prompt[:48]):
                self.assertTrue(hook.looks_like_new_work(prompt))

    def test_existing_work_and_questions_are_not(self) -> None:
        for prompt in NOT_NEW_WORK:
            with self.subTest(prompt=prompt[:48]):
                self.assertFalse(hook.looks_like_new_work(prompt))

    def test_negative_patterns_win_over_positive_ones(self) -> None:
        # Mentions building, but is plainly about code that already exists.
        self.assertFalse(
            hook.looks_like_new_work("why does the build script create a stale agent?")
        )

    def test_very_long_prompts_are_ignored(self) -> None:
        self.assertFalse(hook.looks_like_new_work("build an agent that " + "x" * 2000))


class HookProcessTests(unittest.TestCase):
    def test_offer_names_the_skill_and_the_mute_command(self) -> None:
        out = invoke({"user_prompt": EVAL_PROMPTS[0], "cwd": "/", "session_id": "abc"})
        payload = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(payload["hookEventName"], "UserPromptSubmit")
        self.assertIn("agent-builder", payload["additionalContext"])
        self.assertIn("--mute abc", payload["additionalContext"])

    def test_silent_on_unrelated_prompts(self) -> None:
        self.assertEqual(
            invoke({"user_prompt": NOT_NEW_WORK[0], "cwd": "/", "session_id": "a"}), ""
        )

    def test_silent_inside_a_seeded_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / ".agent-builder.json").write_text("{}", encoding="utf-8")
            out = invoke({"user_prompt": EVAL_PROMPTS[0], "cwd": directory, "session_id": "b"})
            self.assertEqual(out, "", "a seeded project carries an adapter; the offer is noise")

    def test_mute_silences_that_session_only(self) -> None:
        session = "mute-test-session"
        marker = hook.marker_path(session)
        marker.unlink(missing_ok=True)
        try:
            self.assertNotEqual(
                invoke({"user_prompt": EVAL_PROMPTS[0], "cwd": "/", "session_id": session}), ""
            )
            subprocess.run([sys.executable, str(HOOK), "--mute", session], check=True)
            self.assertEqual(
                invoke({"user_prompt": EVAL_PROMPTS[0], "cwd": "/", "session_id": session}), ""
            )
            other = invoke({"user_prompt": EVAL_PROMPTS[0], "cwd": "/", "session_id": "another"})
            self.assertNotEqual(other, "", "muting one session must not mute the next")
        finally:
            marker.unlink(missing_ok=True)

    def test_malformed_input_never_breaks_a_prompt(self) -> None:
        for bad in ("", "not json", "[]", "null"):
            with self.subTest(payload=bad):
                result = subprocess.run(
                    [sys.executable, str(HOOK)],
                    input=bad,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")


class ManifestTests(unittest.TestCase):
    def test_hooks_json_points_at_the_script(self) -> None:
        manifest = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        entries = manifest["hooks"]["UserPromptSubmit"]
        command = entries[0]["hooks"][0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/agent_builder_offer.py", command)
        self.assertTrue(HOOK.is_file())


if __name__ == "__main__":
    unittest.main()
