# Contributing to SkillForge

Thanks for taking the time to improve SkillForge.

## Development Setup

```bash
git clone https://github.com/xiaokillua/skillforge.git
cd skillforge
python3 -m pip install -e ".[dev]"
python3 -m unittest discover -s tests -v
```

## What Good Contributions Look Like

- Keep changes aligned with the current product direction: audited, portable, multi-runtime agent skills.
- Prefer small, reviewable pull requests over broad refactors.
- Preserve English and Chinese docs when you change user-facing behavior.
- Add or update focused tests when a change touches CLI behavior, packaging, verification, or report output.

## Repo Areas

- `src/skillforge/`: core inspection, packaging, verification, doctor, and report logic
- `tests/`: focused unittest coverage for CLI and internal modules
- `examples/`: validated showcase material and sample outputs
- `docs/`: tutorials and compatibility notes
- `skills/`: the project's own reusable SkillForge skill

## Before Opening a Pull Request

Run the basics locally:

```bash
python3 -m unittest discover -s tests -v
python3 -m build
python3 -m twine check dist/*
```

If your change affects README examples or sample reports, regenerate them before opening the PR:

```bash
python3 scripts/generate_example_reports.py
```

## Documentation Expectations

If you change one of these, update both language tracks when the content is user-facing:

- `README.md`
- `README.zh-CN.md`
- `docs/TUTORIAL.md`
- `docs/TUTORIAL.zh-CN.md`
- any runtime showcase or compatibility docs that the behavior touches

## Showcase and Runtime Validation Changes

If you add a new runtime validation, try to include:

- the exact runtime version used
- the command or workflow that proved it
- a short evidence snippet in the relevant showcase doc

That keeps the repo honest about what is validated versus what is only packaged.
