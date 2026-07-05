from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _pct(value: float) -> str:
    return f"{round(value * 100)}%"


def render_markdown(report: dict[str, Any], *, alert_threshold: float = 0.75) -> str:
    aqua = report["aqua_report"]
    lines = [
        "## A.Q.U.A Report",
        "",
        f"**Snapshot:** `{aqua['snapshot_id']}`  ",
        f"**Generated:** {aqua['generated_at']}  ",
        f"**Version:** {aqua['version']}",
        "",
        "### Scenarios",
        "",
    ]

    for index, scenario in enumerate(aqua.get("scenarios", []), start=1):
        flag = " [review]" if scenario["confidence"] < alert_threshold else ""
        lines.extend(
            [
                f"#### {index}. {scenario['description']}{flag}",
                f"- **Confidence:** {_pct(scenario['confidence'])}",
                f"- **Impact:** {scenario['impact']}",
                f"- **Status:** {scenario['status']}",
                f"- **Rationale:** {scenario['rationale']}",
            ]
        )
        if scenario.get("alternatives"):
            lines.append("- **Alternatives:**")
            for alt in scenario["alternatives"]:
                lines.append(
                    f"  - {alt['hypothesis']} ({_pct(alt['probability'])})"
                )
        lines.append("")

    recommendations = aqua.get("recommendations", [])
    if recommendations:
        lines.extend(["### Recommendations", ""])
        for rec in recommendations:
            lines.append(f"- [{rec['risk'].upper()}] {rec['action']}")

    low = [
        s for s in aqua.get("scenarios", [])
        if s["confidence"] < alert_threshold
    ]
    if low:
        lines.extend(
            [
                "",
                f"> **{len(low)} scenario(s) below { _pct(alert_threshold) } confidence** — manager review recommended.",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def write_report(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
