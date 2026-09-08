# v0.1 validation

**Build validation date:** 2026-09-08

**Status:** Mechanical validation passed; realistic author acceptance pending.

## Automated evidence

- 8 Agent Builder unit and behavioral tests passed.
- A wheel was built, installed in a clean virtual environment, and invoked through its
  installed `agent-builder` command.
- The installed command generated a 25-file acceptance fixture with Codex, Claude Code, and
  Gemini CLI adapters.
- The generated project passed Agent Builder validation and its own 3 dependency-free tests.
- Python compilation, Ruff 0.16.6 lint, Ruff formatting, Git whitespace checks, JSON parsing,
  TOML parsing, and generated YAML parsing passed.
- The final wheel SHA-256 is
  `dfc74fbe143cf1dc03e86cb6357ee9328462b3ba6c2f97b7ccfb28d6f5ae7423`.

The ignored local fixture is at `.generated/v0-1-acceptance-agent`. It is evidence for this
build, not part of the reusable repository.

## Behaviors covered

- default and multi-host adapter selection;
- canonical ordering and deduplication;
- invalid and explicitly empty adapter rejection;
- safe refusal to overwrite an existing target;
- temporary generation followed by validation and atomic placement;
- template-version and runtime-selection metadata;
- required scaffold files, adapter declarations, and initial Define phase;
- compact handoff schema/example consistency;
- ignored secret-file patterns and common credential-pattern detection; and
- generated-project self-tests with no agent runtime.

## Deliberate limits

The built-in validator performs fast structural checks. It does not fully evaluate arbitrary
edited YAML, prove JSON Schema semantics, detect every possible secret format, or assess agent
behavior. Those limits are explicit rather than hidden behind a broad correctness claim.

Practical acceptance will come from creating one real agent, following the workflow through
its phases, and recording friction, missing instructions, unnecessary files, and inconsistent
behavior. That feedback will define the next acceptance suite.
