"""Compile a topology into solids metadata, cut list, fasteners, checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from slotcad.deflection import DeflectionResult, uniformly_distributed
from slotcad.fasteners import FastenerFamilyError, assert_single_family
from slotcad.interference import Box3, InterferenceReport, check_interference
from slotcad.nesting import compare_nesting
from slotcad.registry import ProfileRecord
from slotcad.topology import Member, Topology


@dataclass
class CutItem:
    name: str
    length_mm: float
    qty: int
    profile_id: str
    role: str
    provenance: str


@dataclass
class PanelItem:
    name: str
    width_mm: float
    depth_mm: float
    thickness_mm: float
    thickness_band_mm: tuple[float, float]
    provenance: str
    notes: str


@dataclass
class FastenerCount:
    name: str
    qty: int
    family: str
    provenance: str
    notes: str = ""


@dataclass
class BuildResult:
    topology: str
    params: dict
    family: str
    cut_list: list[CutItem] | None
    panels: list[PanelItem]
    fasteners: list[FastenerCount]
    interference: InterferenceReport
    deflection: list[DeflectionResult]
    nesting: dict | None
    assembly_order: list[str]
    notes: list[str]
    solids: list[dict]  # AABB descriptors (STEP export optional)
    ok: bool
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "topology": self.topology,
            "params": self.params,
            "family": self.family,
            "ok": self.ok,
            "errors": self.errors,
            "cut_list": None
            if self.cut_list is None
            else [
                {
                    "name": c.name,
                    "length_mm": c.length_mm,
                    "qty": c.qty,
                    "profile_id": c.profile_id,
                    "role": c.role,
                    "provenance": c.provenance,
                }
                for c in self.cut_list
            ],
            "panels": [
                {
                    "name": p.name,
                    "width_mm": p.width_mm,
                    "depth_mm": p.depth_mm,
                    "thickness_mm": p.thickness_mm,
                    "thickness_band_mm": list(p.thickness_band_mm),
                    "provenance": p.provenance,
                    "notes": p.notes,
                }
                for p in self.panels
            ],
            "fasteners": [
                {
                    "name": f.name,
                    "qty": f.qty,
                    "family": f.family,
                    "provenance": f.provenance,
                    "notes": f.notes,
                }
                for f in self.fasteners
            ],
            "interference": {
                "ok": self.interference.ok,
                "method": self.interference.method,
                "hits": [
                    {"a": h.a, "b": h.b, "volume_mm3": h.volume_mm3, "note": h.note, "severity": h.severity}
                    for h in self.interference.hits
                ],
                "notes": self.interference.notes,
            },
            "deflection": [
                {
                    "span_mm": d.span_mm,
                    "load_n": d.load_n,
                    "i_mm4": d.i_mm4,
                    "delta_mm": d.delta_mm,
                    "formula": d.formula,
                    "provenance_i": d.provenance_i,
                    "provenance_e": d.provenance_e,
                    "assumptions": d.assumptions,
                }
                for d in self.deflection
            ],
            "nesting": self.nesting,
            "assembly_order": self.assembly_order,
            "notes": self.notes,
            "solids": self.solids,
        }


def _boxes(topo: Topology) -> list[Box3]:
    out = []
    for m in topo.members:
        kind = "panel" if m.role == "panel" else "bar"
        out.append(
            Box3(m.name, kind, m.xmin, m.xmax, m.ymin, m.ymax, m.zmin, m.zmax)
        )
    return out


def _cut_list(topo: Topology) -> list[CutItem]:
    # Aggregate identical lengths/roles
    key_map: dict[tuple, CutItem] = {}
    for m in topo.members:
        if m.role == "panel":
            continue
        key = (round(m.length_mm, 2), m.role, m.profile_id)
        if key not in key_map:
            key_map[key] = CutItem(
                name=f"{m.role} {m.length_mm:g} mm",
                length_mm=round(m.length_mm, 2),
                qty=1,
                profile_id=m.profile_id,
                role=m.role,
                provenance=m.provenance,
            )
        else:
            key_map[key].qty += 1
    return sorted(key_map.values(), key=lambda c: (-c.length_mm, c.role, c.name))


def _panels(topo: Topology) -> list[PanelItem]:
    profile = topo.primary_profile
    items = []
    t = float(topo.params.get("panel_thickness_mm") or profile.panel_max_thickness_mm())
    # tolerance band: ±0.2 mm assumed sheet tolerance
    band = (round(t - 0.2, 2), round(t + 0.2, 2))
    size = topo.params.get("panel_size_mm")
    for m in topo.members:
        if m.role != "panel":
            continue
        w = round(m.xmax - m.xmin, 2)
        d = round(m.ymax - m.ymin, 2)
        if size:
            w, d = float(size[0]), float(size[1])
        neck = profile.neck_width_mm
        note = (
            f"neck {neck:g} mm [measured]; thickness must stay ≤ "
            f"{profile.panel_max_thickness_mm():.2f} mm with clearance"
        )
        if band[1] > neck:
            note += (
                f" — WARNING: top of tolerance band {band[1]:g} mm exceeds neck "
                f"{neck:g} mm (will jam)"
            )
        items.append(
            PanelItem(
                name=m.name,
                width_mm=w,
                depth_mm=d,
                thickness_mm=t,
                thickness_band_mm=band,
                provenance="assumed" if "panel_thickness_mm" in topo.params else "measured",
                notes=note,
            )
        )
    return items


def _fasteners(topo: Topology, family: str) -> list[FastenerCount]:
    """Count brackets/screws for reference topologies (assumed kit)."""
    n_posts = sum(1 for m in topo.members if m.role == "post")
    n_rails = sum(1 for m in topo.members if m.role in {"rail", "rung"})
    # each rail/rung end gets one bracket + T-nut + screw (assumed)
    joints = n_rails * 2
    if topo.name == "box-shelf":
        # corner brackets per rail end
        brackets = joints
    else:
        brackets = joints
    return [
        FastenerCount(
            name=f"corner bracket ({family})",
            qty=brackets,
            family=family,
            provenance="assumed",
            notes="one bracket per rail/rung end",
        ),
        FastenerCount(
            name=f"T-nut ({family})",
            qty=brackets * 2,
            family=family,
            provenance="assumed",
            notes="two T-nuts per bracket",
        ),
        FastenerCount(
            name=f"machine screw ({family})",
            qty=brackets * 2,
            family=family,
            provenance="assumed",
            notes="matched to family thread (M5 for nut-5, M6 for nut-6)",
        ),
        FastenerCount(
            name="end cap",
            qty=n_posts * 2,
            family=family,
            provenance="assumed",
            notes="optional cosmetic",
        ),
    ]


def _deflection(topo: Topology) -> list[DeflectionResult]:
    profile = topo.primary_profile
    i = min(profile.ixx_mm4, profile.iyy_mm4)
    prov = profile.provenance.get("ixx_mm4", "measured")
    results = []
    # loaded spans = horizontal rails/rungs
    seen = set()
    for m in topo.members:
        if m.role not in {"rail", "rung"}:
            continue
        span = round(m.length_mm, 2)
        if span in seen:
            continue
        seen.add(span)
        # 200 N assumed shelf load per span
        results.append(
            uniformly_distributed(span, 200.0, i, provenance_i=prov)
        )
    return results


def compile_topology(
    topo: Topology,
    *,
    stock_mm: float = 1980.0,
    min_cut_mm: float = 50.0,
    load_n_per_span: float = 200.0,
) -> BuildResult:
    errors: list[str] = []
    notes = list(topo.notes)

    try:
        family = assert_single_family(topo.profiles)
    except FastenerFamilyError as exc:
        # Hard error: no cut list
        boxes = _boxes(topo)
        report = check_interference(boxes)
        return BuildResult(
            topology=topo.name,
            params=topo.params,
            family="MIXED",
            cut_list=None,
            panels=[],
            fasteners=[],
            interference=report,
            deflection=[],
            nesting=None,
            assembly_order=topo.assembly_order,
            notes=notes,
            solids=[{"name": m.name, "bbox": [m.xmin, m.ymin, m.zmin, m.xmax, m.ymax, m.zmax]} for m in topo.members],
            ok=False,
            errors=[str(exc)],
        )

    boxes = _boxes(topo)
    report = check_interference(boxes)
    panels = _panels(topo)
    fasteners = _fasteners(topo, family)
    deflection = _deflection(topo)

    # Panel four-side trade-off note
    if topo.name == "box-shelf" and topo.params.get("panel_four_sides"):
        corner_hits = [h for h in report.hits if h.severity == "error" and ("post" in h.a or "post" in h.b)]
        if corner_hits:
            notes.append(
                "panel corners hit posts (~5×5 mm class overlap). "
                "Choice: notch all four corners, or hold panel front-and-back only "
                "(--panel-two-sides). Measured trade-off in the brief: notches bought "
                "only 0.80 → 0.65 mm of sag — often not worth the work. "
                "Report the trade-off; do not silently pick."
            )

    if not report.ok:
        errors.append("interference check failed — cut list withheld")
        cut_list = None
        nesting = None
        ok = False
    else:
        cut_list = _cut_list(topo)
        lengths = []
        for c in cut_list:
            lengths.extend([c.length_mm] * c.qty)
        nesting = compare_nesting(lengths, stock_mm=stock_mm, min_cut_mm=min_cut_mm)
        ok = True
        # flag assumed provenance on cut list
        if any(c.provenance == "assumed" for c in cut_list):
            notes.append(
                "WARNING: cut list lengths are derived from topology params "
                "(provenance=assumed until you verify with a caliper)"
            )

    solids = [
        {
            "name": m.name,
            "role": m.role,
            "bbox_mm": [m.xmin, m.ymin, m.zmin, m.xmax, m.ymax, m.zmax],
            "length_mm": m.length_mm,
        }
        for m in topo.members
    ]

    return BuildResult(
        topology=topo.name,
        params=topo.params,
        family=family,
        cut_list=cut_list,
        panels=panels,
        fasteners=fasteners,
        interference=report,
        deflection=deflection,
        nesting=nesting,
        assembly_order=topo.assembly_order,
        notes=notes,
        solids=solids,
        ok=ok,
        errors=errors,
    )
