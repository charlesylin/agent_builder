# Agent Builder v0.6.2 — Define

Working patch target, 2026-10-26. Restore reliable seeding from the installed Claude plugin
without repeated investigation or fetching a source checkout to replace a missing template.

A local Desktop payload (v0.6.0) lacks only .env.example.tmpl among the templates; seeding
with those templates fails validation, while repository templates succeed. The specific
v0.6.1 installation mentioned by the author and the omission stage remain unverified.

Success: the actual published/installed Claude plugin seeds a new project containing the
names-only .env.example, with normal validation and no remote-source recovery needed.
Keep the correction small; no updater, retry layer, packaging framework or v0.7 features.
No Plan or Build approved. Detailed diagnostic evidence stays local.
