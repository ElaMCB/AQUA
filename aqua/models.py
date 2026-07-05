from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

REPORT_VERSION = "0.1.0"


@dataclass
class Alternative:
    hypothesis: str
    probability: float
    evidence: str = ""


@dataclass
class Scenario:
    description: str
    confidence: float
    rationale: str
    impact: str
    status: str = "generated"
    id: str = field(default_factory=lambda: str(uuid4()))
    alternatives: list[Alternative] = field(default_factory=list)
    affected_paths: list[str] = field(default_factory=list)


@dataclass
class Recommendation:
    scenario_id: str
    action: str
    risk: str
    id: str = field(default_factory=lambda: str(uuid4()))
    auto_merge: bool = False


@dataclass
class DriftSignal:
    description: str
    severity: str
    id: str = field(default_factory=lambda: str(uuid4()))
    detected_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    confidence: float = 0.5


@dataclass
class Report:
    scenarios: list[Scenario]
    snapshot_id: str = field(default_factory=lambda: str(uuid4()))
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    version: str = REPORT_VERSION
    source: dict[str, Any] = field(default_factory=dict)
    production_drift: list[DriftSignal] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        def convert(obj: Any) -> Any:
            if hasattr(obj, "__dataclass_fields__"):
                return {k: convert(v) for k, v in asdict(obj).items()}
            if isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj

        return {"aqua_report": convert(self)}
