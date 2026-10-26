# Agent Builder v0.6.2 — Define

Working patch target, 2026-10-26. Author confirms the failure occurs in Claude Code:
new-project seeding is delayed while Claude recovers a missing .env.example template.

The local registered Claude Code plugin is v0.6.0 and contains every template, including
.env.example.tmpl. A separate Desktop payload lacks that template, but its reproduced
failure does not establish the cause of the reported Claude Code problem. Identify the
failing machine, plugin path and version before choosing a fix; filename filtering is unproven.

Success: the affected Claude Code installation seeds a project with the names-only
.env.example and normal validation, without remote-source recovery. Keep the correction
small; no updater, retry layer, packaging framework or v0.7 features. No Plan or Build approved.
