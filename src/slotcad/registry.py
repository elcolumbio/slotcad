"""Profile registry: load/save measurement records (never vendor STEP files)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

Provenance = Literal["measured", "vendor", "assumed"]

SCHEMA_VERSION = 1

# Default registry root: repo `registry/` next to installed package's parents, or CWD.
def default_registry_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "registry"
        if candidate.is_dir():
            return candidate
    return Path.cwd() / "registry"


@dataclass(frozen=True)
class SlotBand:
    depth_from_mm: float
    depth_to_mm: float
    width_mm: float


@dataclass
class ProfileRecord:
    """One vendor profile, measurements only."""

    id: str
    vendor: str
    product_name: str
    product_url: str
    source_step_url: str
    source_step_sha256: str
    source_step_filename: str
    outer_mm: list[float]
    fastener_family: str
    groove_nominal_mm: float
    groove_depth_mm: float
    core_thread: str
    area_mm2: float
    mass_per_m_kg: float
    density_used_kg_m3: float
    effective_density_kg_m3: float
    ixx_mm4: float
    iyy_mm4: float
    slot_scan: list[dict[str, float]]
    slot_bottom_mm: float
    neck_width_mm: float
    neck_depth_from_mm: float
    neck_depth_to_mm: float
    provenance: dict[str, Provenance]
    notes: str = ""
    schema_version: int = SCHEMA_VERSION
    aluminium_density_nominal_kg_m3: float = 2700.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProfileRecord:
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    def neck(self) -> float:
        return self.neck_width_mm

    def panel_max_thickness_mm(self, clearance_mm: float = 0.3) -> float:
        """Largest panel that still clears the measured neck."""
        return max(0.0, self.neck_width_mm - clearance_mm)


def canonical_json(data: dict[str, Any]) -> str:
    """Deterministic JSON for byte-identical re-emit."""
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def save_profile(record: ProfileRecord, path: Path | None = None) -> Path:
    if path is None:
        path = default_registry_root() / record.vendor.lower() / f"{record.id}.json"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json(record.to_dict())
    path.write_text(text, encoding="utf-8")
    return path


def load_profile(path: str | Path) -> ProfileRecord:
    path = Path(path)
    if not path.exists():
        # allow id like motedis/20x20-b-typ-nut-6
        alt = default_registry_root() / path
        if alt.exists():
            path = alt
        elif not str(path).endswith(".json"):
            alt = default_registry_root() / f"{path}.json"
            if alt.exists():
                path = alt
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return ProfileRecord.from_dict(data)


def find_profile(profile_id: str, root: Path | None = None) -> ProfileRecord:
    root = root or default_registry_root()
    matches = list(root.rglob(f"{profile_id}.json"))
    if not matches:
        # also try full relative path
        candidate = root / profile_id
        if candidate.exists():
            return load_profile(candidate)
        raise FileNotFoundError(f"profile not found: {profile_id} under {root}")
    return load_profile(matches[0])
