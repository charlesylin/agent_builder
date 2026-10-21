# Change budgets and local records

Use `python3 scripts/changes.py . --base <commit>` before agreeing the budget (from
an installed skill, use its script path). Count physical lines, including blanks/comments;
zero baselines report N/A. Copies under templates and generated outputs still count.
Inspect pre-existing dirty work and agree its handling before fixing the cycle baseline.
After approval run `python3 scripts/changes.py .` after coherent edits and before commits.
An overrun or unapproved path exits 1; unavailable/invalid input exits 2. Re-estimate with
the author rather than widening the budget. Scope approval still applies below the limits.

`governance/change-budget.json` example (replace estimates with the approved numbers):

```json
{
  "schema_version": 1,
  "baseline": "<full clean commit SHA>",
  "paths": ["src/example.py", "tests/test_example.py", "governance/*"],
  "categories": {"src/*.py": "Python code"},
  "limits": {
    "Python code": {"added": 25, "removed": 15},
    "Python tests": {"added": 15, "removed": 5},
    "Misc: configuration/metadata": {"added": 10, "removed": 10}
  }
}
```

Paths/categories use case-sensitive shell patterns; first matching category wins.
Unrecognized types are named. Rows report baseline/added/removed/net/percent and changed
file counts, with generated/vendor flags. Binary rows use bytes; symlink/submodule rows
use link counts and never follow their contents. Renames use Git's detection heuristic;
otherwise delete/add counts apply. Review classification and allow only intended paths.

New v0.6 projects ignore working planning notes, specs and assessments while retaining
concise definition/reuse evidence and authority. Older projects are not migrated.
To opt in: agree the cleanup inventory, preserve copies, add only those ignore patterns,
then `git rm --cached -- <approved paths>`. Preserve pinned Spec Kit assets/constitution,
repair links, and add the canonical helpers plus project-owned `version.json`; never use
the template version as the project's version. Set manifest template_version only after
adopting and validating the full v0.6 contract; preserve original generated_by provenance.
Before Build on a fresh clone, reconstruct local working detail from shared approval and
rerun applicable Spec Kit checks. Compacted history needs a pinned commit/path reference.
