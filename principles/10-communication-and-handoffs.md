---
id: communication-and-handoffs
title: Communication and handoffs
---
Human-facing narratives use concise Markdown. Standalone HTML is encouraged when interaction,
navigation, or visual presentation materially improves comprehension. Machine-to-machine
handoffs are compact and use the versioned JSON Schema under `contracts/`.

Every human-facing closeout contains:

1. decisions and recommendations made with high confidence;
2. uncertain decisions requiring guidance;
3. questions for the project author; and
4. **What should you be asking that you are not?** — one question, the one that matters
   most, not a list.

Say `None` rather than inventing an issue. An answer to the fourth question goes to
`planning/later.md` unless the author asks, in their own words, for work on it now; a closeout
is not a place to grow the project.

## Short form

Human outputs are concise Markdown (standalone HTML when it materially helps); agent handoffs
use the compact JSON contract under `contracts/`. Every human closeout states high-confidence
decisions, uncertain decisions needing guidance, questions for the author, and one — only
one — answer to **What should you be asking that you are not?** Say `None` rather than
manufacturing content; an answered closeout question goes to `planning/later.md`, not into
scope.
