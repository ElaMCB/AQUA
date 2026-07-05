from __future__ import annotations

import re
import subprocess
from pathlib import Path

from aqua.models import Alternative, Recommendation, Report, Scenario

RISK_PATTERNS: list[tuple[str, str, str, float, str]] = [
    (
        r"(payment|checkout|billing|stripe|coupon)",
        "Payment path regression after refactor",
        "Changes touch payment or checkout logic where small validation gaps often cause revenue-impacting bugs",
        0.84,
        "high",
    ),
    (
        r"(auth|login|session|token|password|jwt)",
        "Authentication or session handling edge case",
        "Auth-related diffs frequently introduce session expiry, token refresh, or permission bypass issues",
        0.81,
        "high",
    ),
    (
        r"(async|await|promise|timeout|retry)",
        "Async timeout or silent failure under load",
        "New async paths without explicit timeout handling can fail silently in production",
        0.76,
        "medium",
    ),
    (
        r"(api|endpoint|route|handler|controller)",
        "API contract or validation mismatch",
        "Endpoint changes may break clients that rely on prior request/response validation",
        0.73,
        "medium",
    ),
    (
        r"(migrat|schema|database|sql|model)",
        "Data migration or schema compatibility issue",
        "Schema changes risk backward-incompatible reads or partial migration states",
        0.79,
        "high",
    ),
    (
        r"(config|env|secret|credential)",
        "Configuration or environment drift",
        "Config changes may pass locally but fail when required variables differ in staging or production",
        0.71,
        "medium",
    ),
]


def get_diff(repo: Path, base: str, head: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "diff", f"{base}...{head}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        result = subprocess.run(
            ["git", "-C", str(repo), "diff", base, head],
            capture_output=True,
            text=True,
            check=True,
        )
    return result.stdout


def changed_files(diff: str) -> list[str]:
    paths: list[str] = []
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:].strip()
            if path != "/dev/null":
                paths.append(path)
    return paths


def _alternatives_for(confidence: float, theme: str) -> list[Alternative]:
    remainder = max(0.0, 1.0 - confidence)
    alt_a = round(remainder * 0.65, 2)
    alt_b = round(remainder - alt_a, 2)
    return [
        Alternative(
            hypothesis=f"Test fixture does not cover production variant of {theme}",
            probability=alt_a,
            evidence="Diff lacks fixture updates for edge-case coverage",
        ),
        Alternative(
            hypothesis=f"Unrelated refactor masks observable failure in {theme}",
            probability=alt_b,
            evidence="Multiple files changed; failure signal may be indirect",
        ),
    ]


def generate_scenarios(diff: str, paths: list[str], max_scenarios: int = 5) -> list[Scenario]:
    haystack = f"{diff}\n{' '.join(paths)}".lower()
    scenarios: list[Scenario] = []
    seen: set[str] = set()

    for pattern, description, rationale, confidence, impact in RISK_PATTERNS:
        if len(scenarios) >= max_scenarios:
            break
        if not re.search(pattern, haystack, re.IGNORECASE):
            continue
        if description in seen:
            continue
        seen.add(description)
        affected = [p for p in paths if re.search(pattern, p, re.IGNORECASE)][:5]
        if not affected:
            affected = paths[:3]
        scenarios.append(
            Scenario(
                description=description,
                confidence=confidence,
                rationale=rationale,
                impact=impact,
                alternatives=_alternatives_for(confidence, description),
                affected_paths=affected,
            )
        )

    if not scenarios:
        scenarios.append(
            Scenario(
                description="Smoke regression on changed modules",
                confidence=0.62,
                rationale="No high-risk keyword match; baseline scenario covers general regression on touched files",
                impact="low",
                alternatives=_alternatives_for(0.62, "changed modules"),
                affected_paths=paths[:5],
            )
        )

    return scenarios[:max_scenarios]


def build_recommendations(scenarios: list[Scenario]) -> list[Recommendation]:
    recs: list[Recommendation] = []
    for scenario in scenarios:
        if scenario.confidence >= 0.75:
            action = f"Add targeted test for: {scenario.description}"
            risk = "medium" if scenario.impact != "high" else "high"
        else:
            action = f"Review manually before merge: {scenario.description}"
            risk = "low"
        recs.append(
            Recommendation(
                scenario_id=scenario.id,
                action=action,
                risk=risk,
            )
        )
    return recs


def analyze_diff(
    diff: str,
    *,
    repo: str | None = None,
    pr: int | None = None,
    base_ref: str | None = None,
    head_ref: str | None = None,
    base_sha: str | None = None,
    head_sha: str | None = None,
    max_scenarios: int = 5,
) -> Report:
    paths = changed_files(diff)
    scenarios = generate_scenarios(diff, paths, max_scenarios=max_scenarios)
    source: dict[str, str | int] = {}
    if repo:
        source["repo"] = repo
    if pr is not None:
        source["pr"] = pr
    if base_ref:
        source["base_ref"] = base_ref
    if head_ref:
        source["head_ref"] = head_ref
    if base_sha:
        source["base_sha"] = base_sha
    if head_sha:
        source["head_sha"] = head_sha

    return Report(
        scenarios=scenarios,
        source=source,
        recommendations=build_recommendations(scenarios),
    )


def analyze_repo(
    repo_path: Path,
    *,
    base: str,
    head: str = "HEAD",
    pr: int | None = None,
    max_scenarios: int = 5,
) -> Report:
    diff = get_diff(repo_path, base, head)
    return analyze_diff(
        diff,
        repo=str(repo_path),
        pr=pr,
        base_ref=base,
        head_ref=head,
        max_scenarios=max_scenarios,
    )
