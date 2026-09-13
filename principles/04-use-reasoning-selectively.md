---
id: use-reasoning-selectively
title: Use reasoning selectively
---
Models decide, prioritize, interpret ambiguity, and orchestrate. Deterministic code retrieves,
validates, transforms, calculates, enforces policy, and executes repeatable actions. A model
must not be used where a small testable function can produce the required result reliably.
Prefer Python for that code; explain any material departure.

## Short form

Reserve model reasoning for orchestration and judgment. Put repeatable retrieval, validation,
transformation, calculation, policy enforcement, and execution in deterministic, tested Python.
