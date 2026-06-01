# Security Policy

## Supported versions

TermDash is currently in early alpha. Security fixes will target the latest version on the `main` branch until formal releases are established.

## Reporting a vulnerability

Please do not open a public GitHub issue for sensitive security problems.

Instead, report the issue privately to the maintainer using the contact information on the GitHub profile, or open a minimal issue asking for a private contact path without disclosing exploit details.

Please include:

- Affected version or commit
- Description of the issue
- Steps to reproduce, if safe to share
- Potential impact
- Suggested mitigation, if known

## Sensitive data

TermDash should never require users to commit API keys, credentials, tokens, or private configuration to the repository.

Future API integrations should use local environment variables or local config files that are excluded from git.