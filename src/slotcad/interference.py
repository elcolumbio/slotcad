"""Interference checks for axis-aligned bars and panels.

Prefer CadQuery boolean intersection when available; otherwise use honest
AABB / slab overlap that still catches buried rails and panel-corner/post hits.

Panel∩rail overlaps are *slot engagement* (the panel lives in the rail's void).
Our bar model is a solid AABB without a T-slot cutout, so those pairs are reported
as engagement notes, not hard failures. Panel∩post and bar∩bar remain hard errors.

Limitation (AABB path): does not detect non-axis-aligned or curved collisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Kind = Literal["bar", "panel"]


@dataclass(frozen=True)
class Box3:
    """Axis-aligned box in mm. xmin..xmax etc."""

    name: str
    kind: Kind
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float

    def volume(self) -> float:
        return max(0.0, self.xmax - self.xmin) * max(0.0, self.ymax - self.ymin) * max(
            0.0, self.zmax - self.zmin
        )

    def overlaps(self, other: Box3, tol: float = 0.05) -> bool:
        return not (
            self.xmax <= other.xmin + tol
            or other.xmax <= self.xmin + tol
            or self.ymax <= other.ymin + tol
            or other.ymax <= self.ymin + tol
            or self.zmax <= other.zmin + tol
            or other.zmax <= self.zmin + tol
        )

    def intersection_volume(self, other: Box3) -> float:
        dx = min(self.xmax, other.xmax) - max(self.xmin, other.xmin)
        dy = min(self.ymax, other.ymax) - max(self.ymin, other.ymin)
        dz = min(self.zmax, other.zmax) - max(self.zmin, other.zmin)
        if dx <= 0 or dy <= 0 or dz <= 0:
            return 0.0
        return dx * dy * dz


@dataclass
class InterferenceHit:
    a: str
    b: str
    volume_mm3: float
    note: str
    severity: str = "error"  # error | engagement


@dataclass
class InterferenceReport:
    ok: bool
    method: str
    hits: list[InterferenceHit] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[InterferenceHit]:
        return [h for h in self.hits if h.severity == "error"]

    def summary(self) -> str:
        errs = self.errors
        eng = [h for h in self.hits if h.severity == "engagement"]
        if not errs:
            msg = f"interference OK ({self.method}, 0 hard hits"
            if eng:
                msg += f", {len(eng)} panel/rail engagement note(s)"
            return msg + ")"
        lines = [f"interference FAILED ({self.method}, {len(errs)} hits):"]
        for h in errs:
            lines.append(f"  - {h.a} ∩ {h.b}: {h.volume_mm3:.1f} mm³ — {h.note}")
        return "\n".join(lines)


def _is_panel(box: Box3) -> bool:
    return box.kind == "panel" or "panel" in box.name.lower()


def _is_rail_like(box: Box3) -> bool:
    if box.kind != "bar":
        return False
    n = box.name.lower()
    return any(k in n for k in ("rail", "rung"))


def _is_post(box: Box3) -> bool:
    return "post" in box.name.lower() or "upright" in box.name.lower()


def _classify(a: Box3, b: Box3, vol: float) -> InterferenceHit:
    if (_is_panel(a) and _is_rail_like(b)) or (_is_panel(b) and _is_rail_like(a)):
        return InterferenceHit(
            a.name,
            b.name,
            vol,
            "panel engages rail slot (expected; bar AABB has no T-slot void)",
            severity="engagement",
        )
    if (_is_panel(a) and _is_post(b)) or (_is_panel(b) and _is_post(a)):
        return InterferenceHit(
            a.name,
            b.name,
            vol,
            "panel overlaps post — notch corners or hold panel front-and-back only",
            severity="error",
        )
    if a.kind == "bar" and b.kind == "bar":
        return InterferenceHit(
            a.name,
            b.name,
            vol,
            "bar/bar solid overlap (buried rail or crossing members)",
            severity="error",
        )
    return InterferenceHit(a.name, b.name, vol, "solid overlap", severity="error")


def check_aabb(boxes: list[Box3], *, min_volume_mm3: float = 1.0) -> InterferenceReport:
    hits: list[InterferenceHit] = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if not a.overlaps(b):
                continue
            vol = a.intersection_volume(b)
            if vol < min_volume_mm3:
                continue
            hits.append(_classify(a, b, vol))
    notes = [
        "AABB geometric overlap (axis-aligned bars/panels).",
        "Panel∩rail counted as slot engagement, not a hard failure "
        "(bar model has no T-slot cutout).",
        "Does not detect rotated or curved collisions.",
    ]
    errors = [h for h in hits if h.severity == "error"]
    return InterferenceReport(ok=len(errors) == 0, method="aabb", hits=hits, notes=notes)


def check_cadquery_boolean(boxes: list[Box3]) -> InterferenceReport | None:
    """Optional solid boolean; returns None if CadQuery unavailable."""
    try:
        import cadquery as cq
    except ImportError:
        return None

    solids = []
    for b in boxes:
        solid = (
            cq.Workplane("XY")
            .box(b.xmax - b.xmin, b.ymax - b.ymin, b.zmax - b.zmin, centered=False)
            .val()
            .moved(cq.Location(cq.Vector(b.xmin, b.ymin, b.zmin)))
        )
        solids.append(solid)

    hits: list[InterferenceHit] = []
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            try:
                inter = solids[i].intersect(solids[j])
                vol = float(inter.Volume()) if inter is not None else 0.0
            except Exception:
                vol = boxes[i].intersection_volume(boxes[j])
            if vol >= 1.0:
                hits.append(_classify(boxes[i], boxes[j], vol))
    errors = [h for h in hits if h.severity == "error"]
    return InterferenceReport(
        ok=len(errors) == 0,
        method="cadquery-boolean",
        hits=hits,
        notes=[
            "CadQuery Solid.intersect boolean volumes.",
            "Panel∩rail counted as slot engagement, not a hard failure.",
        ],
    )


def check_interference(boxes: list[Box3], *, prefer_boolean: bool = True) -> InterferenceReport:
    if prefer_boolean:
        report = check_cadquery_boolean(boxes)
        if report is not None:
            return report
    return check_aabb(boxes)
