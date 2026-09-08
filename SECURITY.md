# Security policy

Do not report a credential, token, private key, personal record, or exploitable detail in a
public issue. Revoke or rotate exposed credentials immediately; deleting a file or commit
does not invalidate a copied secret.

## Repository rules

- Commit only secret **names** and documented injection instructions, never values.
- Keep `.env`, private-key formats, credential exports, and local secret directories ignored.
- Do not pass secrets through model prompts, command-line arguments, Docker build arguments,
  generated handoffs, fixtures, screenshots, or telemetry.
- Grant each agent and container only the files, network destinations, tools, and credentials
  required for its current responsibility.
- Redact sensitive fields before logging. Test redaction with synthetic values.
- Use runtime secret injection. Docker Compose secrets or an external secret manager are
  preferred once a runtime exists.

## Incident response

If exposure is suspected: stop the affected workflow, avoid repeating the value, revoke or
rotate it, inspect repository history and logs, remove recoverable copies, and document the
incident without reproducing the secret.
