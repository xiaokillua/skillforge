# Security Policy

SkillForge handles untrusted upstream repositories, so security matters in two places:

1. vulnerabilities in SkillForge itself
2. risky behavior detected in repositories that SkillForge inspects

## Reporting a Vulnerability in SkillForge

Please do not post sensitive vulnerability details in a public issue.

Use GitHub's private vulnerability reporting flow if it is available for this repository. If private reporting is not available in your interface, open a minimal public issue without exploit details and ask for a secure contact path.

Include:

- affected version
- reproduction steps
- expected impact
- whether the issue requires a malicious upstream repository, a crafted local path, or a normal user workflow

## What SkillForge Tries to Catch

SkillForge includes a lightweight upstream audit that flags common risky patterns such as:

- `curl` piped to a shell
- inline PowerShell execution
- suspicious base64 pipelines
- upstream AI instruction files that deserve manual review

This audit is a first-pass safety check, not a full malware scanner or sandbox.

## Supported Versions

The latest minor release on `main` is the supported line for fixes.

## Hardening Guidance

Even with SkillForge:

- review `references/SECURITY-AUDIT.md`
- review extracted install commands before running them
- prefer isolated environments for first-time upstream installs
- avoid trusting generated skills from repositories you would not trust manually
