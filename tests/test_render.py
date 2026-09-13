"""The principles in ``principles/`` are the single source; every copy must match."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import render  # noqa: E402

from agent_builder import scaffold  # noqa: E402


class RenderTests(unittest.TestCase):
    def test_committed_outputs_match_the_source(self) -> None:
        outputs = render.render_all(render.load_principles(), render.stencil_files())
        stale = render.stale_outputs(outputs)
        self.assertEqual(
            stale,
            [],
            "generated files are out of date — edit principles/ or scripts/stencils/ and run "
            "scripts/render.py: " + ", ".join(str(p.relative_to(ROOT)) for p, _ in stale),
        )

    def test_every_principle_has_id_title_full_and_short(self) -> None:
        for pid, principle in render.load_principles().items():
            with self.subTest(principle=pid):
                self.assertTrue(principle["title"])
                self.assertTrue(principle["full"])
                self.assertTrue(principle["short"], f"{pid} needs a '## Short form' section")

    def test_unknown_principle_id_fails_loudly(self) -> None:
        with self.assertRaises(render.RenderError):
            render.render_text(Path("stencil"), "{{principle:no-such-thing}}", {})

    def test_missing_short_form_fails_loudly(self) -> None:
        principles = {"p": {"title": "P", "full": "Full text.", "short": ""}}
        with self.assertRaises(render.RenderError):
            render.render_text(Path("stencil"), "{{principle:p|short}}", principles)

    def test_list_items_keep_continuation_lines_indented(self) -> None:
        principles = {"p": {"title": "P", "full": "line one\nline two", "short": ""}}
        rendered = render.render_text(Path("stencil"), "- {{principle:p}}\n", principles)
        self.assertEqual(rendered, "- line one\n  line two\n")

    def test_render_and_seed_tokens_do_not_overlap(self) -> None:
        # Render fills {{principle:...}} at build time; the scaffolder fills {{UPPER_CASE}}
        # at seed time. Neither may touch the other's tokens.
        self.assertIsNone(render.TOKEN.search("{{PROJECT_NAME}} {{GENERATED_DATE}}"))
        self.assertIsNone(scaffold._TOKEN.search("{{principle:phases}} {{principle:x|short}}"))

    def test_check_mode_reports_a_stale_output(self) -> None:
        principles = render.load_principles()
        with tempfile.TemporaryDirectory() as directory:
            stencil = Path(directory) / "note.md"
            stencil.write_text("{{principle:phases|short}}\n", encoding="utf-8")
            outputs = {Path(directory) / "out.md": render.render_text(stencil, "x", principles)}
            self.assertEqual(
                render.stale_outputs(outputs), [(Path(directory) / "out.md", "missing")]
            )


if __name__ == "__main__":
    unittest.main()
