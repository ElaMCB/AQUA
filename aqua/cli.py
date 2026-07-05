from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from aqua import __version__
from aqua.analyze import analyze_repo
from aqua.render import render_markdown, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aqua",
        description="AQUA — autonomous testing with explicit uncertainty",
    )
    parser.add_argument("--version", action="version", version=f"aqua {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analyze a PR or diff and generate aqua-report.json")
    analyze.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository path")
    analyze.add_argument("--pr", type=int, help="Pull request number (metadata only in MVP)")
    analyze.add_argument("--base", default="main", help="Base git ref for diff")
    analyze.add_argument("--head", default="HEAD", help="Head git ref for diff")
    analyze.add_argument("--output", type=Path, default=Path("aqua-report.json"))
    analyze.add_argument("--max-scenarios", type=int, default=5)

    render = sub.add_parser("render", help="Render aqua-report.json")
    render.add_argument("--input", type=Path, default=Path("aqua-report.json"))
    render.add_argument("--format", choices=["markdown", "json"], default="markdown")
    render.add_argument("--alert-threshold", type=float, default=0.75)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "analyze":
        report = analyze_repo(
            args.repo.resolve(),
            base=args.base,
            head=args.head,
            pr=args.pr,
            max_scenarios=args.max_scenarios,
        )
        payload = report.to_dict()
        write_report(payload, args.output)
        print(f"Wrote {args.output} ({len(report.scenarios)} scenarios)")
        return 0

    if args.command == "render":
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if args.format == "json":
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        else:
            sys.stdout.write(
                render_markdown(payload, alert_threshold=args.alert_threshold)
            )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
