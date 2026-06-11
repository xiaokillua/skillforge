from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .analyzer import inspect_source
from .doctor import inspect_local_runtimes
from .generator import TARGETS
from .packager import build_packages
from .verifier import VERIFY_TARGETS, verify_build_outputs, verify_skill


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "inspect":
        return _inspect(args)
    if args.command == "build":
        return _build(args)
    if args.command == "doctor":
        return _doctor(args)
    if args.command == "verify":
        return _verify(args)
    if args.command == "version":
        print(__version__)
        return 0

    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillforge",
        description="Turn GitHub repositories into audited, portable agent skills.",
    )
    subparsers = parser.add_subparsers(dest="command")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a GitHub repo or local checkout.")
    inspect_parser.add_argument("source", help="GitHub URL, owner/repo, or local path")
    inspect_parser.add_argument("--name", help="Override the generated skill slug")
    inspect_parser.add_argument("--json", action="store_true", help="Print JSON instead of a human summary")

    build_parser = subparsers.add_parser("build", help="Generate a portable skill package.")
    build_parser.add_argument("source", help="GitHub URL, owner/repo, or local path")
    build_parser.add_argument("-o", "--output", default="dist", help="Output directory")
    build_parser.add_argument(
        "--target",
        choices=sorted(TARGETS),
        default="all",
        help="Packaging target",
    )
    build_parser.add_argument("--name", help="Override the generated skill slug")
    build_parser.add_argument(
        "--allow-risky",
        action="store_true",
        help="Allow packaging even when the audit finds high-risk patterns",
    )
    build_parser.add_argument(
        "--verify",
        action="store_true",
        help="Validate the generated layout immediately after packaging",
    )

    verify_parser = subparsers.add_parser("verify", help="Validate a generated skill bundle or layout.")
    verify_parser.add_argument("path", help="Path to a generated skill directory, build output directory, or .skill archive")
    verify_parser.add_argument(
        "--target",
        choices=sorted(VERIFY_TARGETS),
        default="auto",
        help="Verification target. Use auto to infer from the path.",
    )
    verify_parser.add_argument("--name", help="Select a specific skill name when the directory contains multiple skills")
    verify_parser.add_argument("--json", action="store_true", help="Print JSON instead of a human summary")

    doctor_parser = subparsers.add_parser("doctor", help="Inspect local runtime readiness for supported targets.")
    doctor_parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace path used to compute project-local install locations",
    )
    doctor_parser.add_argument("--json", action="store_true", help="Print JSON instead of a human summary")

    subparsers.add_parser("version", help="Print the SkillForge version")
    return parser


def _inspect(args: argparse.Namespace) -> int:
    try:
        profile = inspect_source(args.source, name_override=args.name)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))
        return 0

    print(f"Skill slug: {profile.slug}")
    print(f"Title: {profile.title}")
    print(f"Source: {profile.repo_url or profile.source}")
    print(f"Ecosystems: {', '.join(profile.ecosystems)}")
    print(f"Entrypoints: {', '.join(profile.entrypoints) if profile.entrypoints else 'none detected'}")
    print(f"Install commands: {len(profile.install_commands)}")
    print(f"Usage commands: {len(profile.usage_commands)}")
    print(f"Audit severity: {profile.audit.max_severity}")
    if profile.audit.findings:
        print("Audit findings:")
        for finding in profile.audit.findings[:5]:
            print(f"- [{finding.severity.upper()}] {finding.path}: {finding.title}")
    return 0


def _build(args: argparse.Namespace) -> int:
    try:
        profile = inspect_source(args.source, name_override=args.name)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        result = build_packages(
            profile=profile,
            output_dir=Path(args.output),
            target=args.target,
            allow_risky=args.allow_risky,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"Built skill '{result.profile.slug}'")
    print(f"Audit severity: {result.profile.audit.max_severity}")
    print("Outputs:")
    for item in result.outputs:
        print(f"- {item}")

    if not args.verify:
        return 0

    try:
        reports = verify_build_outputs(
            output_dir=Path(args.output),
            target=args.target,
            name=result.profile.slug,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 3

    print("Verification:")
    for report in reports:
        label = f"{report.target}{' archive' if report.archive else ''}"
        print(f"- [{report.status.upper()}] {label}: {report.path}")
        for finding in report.findings:
            print(f"  - [{finding.severity.upper()}] {finding.path}: {finding.message}")
    return 0 if all(not report.has_errors for report in reports) else 3


def _verify(args: argparse.Namespace) -> int:
    try:
        report = verify_skill(Path(args.path), target=args.target, name=args.name)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return 0 if not report.has_errors else 2

    print(f"Verified skill '{report.skill_name}'")
    print(f"Target: {report.target}{' (archive)' if report.archive else ''}")
    print(f"Status: {report.status}")
    print(f"Path: {report.path}")
    if report.findings:
        print("Findings:")
        for finding in report.findings:
            print(f"- [{finding.severity.upper()}] {finding.path}: {finding.message}")
    else:
        print("Findings: none")
    return 0 if not report.has_errors else 2


def _doctor(args: argparse.Namespace) -> int:
    try:
        report = inspect_local_runtimes(Path(args.workspace))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return 0

    print("SkillForge Doctor")
    print(f"SkillForge version: {report.skillforge_version}")
    print(f"Workspace: {report.workspace}")
    print(f"Home: {report.home}")
    print("Runtimes:")
    for entry in report.entries:
        print(f"- {entry.runtime}: {entry.status.upper()}")
        print(f"  - target: {entry.target}")
        print(f"  - cli: {entry.cli_path or 'not found'}")
        if entry.version:
            print(f"  - version: {entry.version}")
        print(f"  - install path: {entry.install_paths[0]}")
        for extra_path in entry.install_paths[1:]:
            print(f"  - alternate path: {extra_path}")
        for note in entry.notes:
            print(f"  - note: {note}")
    return 0
