# Changelog

## Unreleased

- Add `build --verify` so packaging can validate generated layouts immediately in the same command.
- Add runtime compatibility documentation and a concrete Codex showcase.
- Add `doctor` for local runtime readiness checks across Codex, Claude, Copilot, OpenClaw, and Hermes.
- Add `doctor --markdown` for shareable environment reports.
- Add `report` to generate a combined markdown artifact from inspect, build, verify, and doctor.

## 0.2.0 - 2026-06-12

- Align Claude packaging with the official `.claude/skills/<name>` layout.
- Keep `.skill` archives as an optional sharing artifact instead of the primary Claude install path.
- Add Claude showcase documentation in English and Chinese.
- Add a `verify` command for validating generated skill layouts and Claude archives.
- Add packaging and release automation for wheels, sdists, GitHub Releases, and optional PyPI trusted publishing.

## 0.1.0

- Initial public release.
- Added repository inspection, security audit, and portable Agent Skills generation.
- Added target packaging for Claude, Codex, Copilot, OpenClaw, and Hermes.
- Added English and Chinese documentation plus a reusable SkillForge skill.
