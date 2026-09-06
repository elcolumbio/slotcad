"""Measure a vendor STEP solid into a registry ProfileRecord."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

from slotcad.registry import ProfileRecord, canonical_json, save_profile

ALUMINIUM_DENSITY_KG_M3 = 2700.0


def _require_cadquery():
    try:
        import cadquery as cq  # noqa: F401
        from OCP.BRep import BRep_Tool  # noqa: F401
        from OCP.BRepMesh import BRepMesh_IncrementalMesh  # noqa: F401
        from OCP.GCPnts import GCPnts_QuasiUniformDeflection  # noqa: F401
        from OCP.TopAbs import TopAbs_EDGE  # noqa: F401
        from OCP.TopExp import TopExp_Explorer  # noqa: F401
        from OCP.TopoDS import TopoDS  # noqa: F401
        from OCP.TopLoc import TopLoc_Location  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "CadQuery/OCP is required for `slotcad measure`. "
            "Install with: uv sync && uv add cadquery"
        ) from exc


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _end_face(solid):
    """Largest planar face whose normal is along the longest bbox axis (extrusion)."""
    bb = solid.BoundingBox()
    dims = [("x", bb.xlen), ("y", bb.ylen), ("z", bb.zlen)]
    axis = max(dims, key=lambda t: t[1])[0]

    def normal_component(n):
        return {"x": n.x, "y": n.y, "z": n.z}[axis]

    cands = []
    for face in solid.Faces():
        try:
            n = face.normalAt()
        except Exception:
            continue
        if abs(abs(normal_component(n)) - 1.0) < 1e-5:
            cands.append(face)
    if not cands:
        raise RuntimeError("no end face found on STEP solid")
    return max(cands, key=lambda f: f.Area()), axis, bb


def _face_polylines(face, deflection: float = 0.05):
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    from OCP.GCPnts import GCPnts_QuasiUniformDeflection
    from OCP.TopAbs import TopAbs_EDGE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopoDS import TopoDS

    polys: list[list[tuple[float, float]]] = []
    for wire in face.Wires():
        pts: list[tuple[float, float]] = []
        exp = TopExp_Explorer(wire.wrapped, TopAbs_EDGE)
        while exp.More():
            edge = TopoDS.Edge_s(exp.Current())
            adaptor = BRepAdaptor_Curve(edge)
            disc = GCPnts_QuasiUniformDeflection(adaptor, deflection)
            if disc.IsDone():
                for i in range(1, disc.NbPoints() + 1):
                    p = disc.Value(i)
                    pts.append((p.X(), p.Y()))
            exp.Next()
        if len(pts) >= 3:
            polys.append(pts)
    return polys


def _point_in_poly(x: float, y: float, poly: list[tuple[float, float]]) -> bool:
    n = len(poly)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        denom = (yj - yi) if abs(yj - yi) > 1e-30 else 1e-30
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / denom + xi):
            inside = not inside
        j = i
    return inside


def _classify_polys(polys):
    scored = []
    for poly in polys:
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        scored.append(((max(xs) - min(xs)) * (max(ys) - min(ys)), poly))
    scored.sort(key=lambda t: -t[0])
    return scored[0][1], [p for _, p in scored[1:]]


def _in_material(x, y, outer, holes) -> bool:
    if not _point_in_poly(x, y, outer):
        return False
    for hole in holes:
        if _point_in_poly(x, y, hole):
            return False
    return True


def _build_grid(outer, holes, xmin, xmax, ymin, ymax, step: float = 0.1):
    """Occupancy grid over the cross-section AABB."""
    nx = max(1, int(math.ceil((xmax - xmin) / step)))
    ny = max(1, int(math.ceil((ymax - ymin) / step)))
    grid = [[False] * ny for _ in range(nx)]
    for ix in range(nx):
        x = xmin + (ix + 0.5) * step
        for iy in range(ny):
            y = ymin + (iy + 0.5) * step
            grid[ix][iy] = _in_material(x, y, outer, holes)
    return grid, step, xmin, ymin, nx, ny


def _gaps_on_row(occupied: list[bool], origin: float, step: float, lo: float, hi: float):
    gaps = []
    in_gap = False
    start = None
    for i, occ in enumerate(occupied):
        t = origin + (i + 0.5) * step
        if not occ and not in_gap:
            in_gap = True
            start = t - step * 0.5
        elif occ and in_gap:
            in_gap = False
            end = t - step * 0.5
            gaps.append((start, end, end - start))
    if in_gap:
        end = origin + len(occupied) * step
        gaps.append((start, end, end - start))
    cands = []
    for a, b, w in gaps:
        mid = (a + b) / 2
        if 1.5 < w < 16 and lo + 0.3 < mid < hi - 0.3 and a >= lo - 0.5 and b <= hi + 0.5:
            cands.append(w)
    return max(cands) if cands else 0.0


def _slot_scan_grid(grid, step, xmin, ymin, nx, ny, face, max_depth_mm: float = 8.0):
    """Scan slot opening vs depth from one outer face. face in {+x,-x,+y,-y}."""
    rows: list[tuple[float, float]] = []
    depth = 0.0
    while depth <= max_depth_mm + 1e-9:
        if face == "+y":
            iy = int((depth) / step)
            if iy >= ny:
                break
            occupied = [grid[ix][iy] for ix in range(nx)]
            width = _gaps_on_row(occupied, xmin, step, xmin, xmin + nx * step)
        elif face == "-y":
            iy = ny - 1 - int(depth / step)
            if iy < 0:
                break
            occupied = [grid[ix][iy] for ix in range(nx)]
            width = _gaps_on_row(occupied, xmin, step, xmin, xmin + nx * step)
        elif face == "+x":
            ix = int(depth / step)
            if ix >= nx:
                break
            occupied = [grid[ix][iy] for iy in range(ny)]
            width = _gaps_on_row(occupied, ymin, step, ymin, ymin + ny * step)
        else:  # -x
            ix = nx - 1 - int(depth / step)
            if ix < 0:
                break
            occupied = [grid[ix][iy] for iy in range(ny)]
            width = _gaps_on_row(occupied, ymin, step, ymin, ymin + ny * step)
        rows.append((round(depth, 2), round(width, 2)))
        depth = round(depth + 0.25, 2)
    return rows


def _bin_slot_scan(rows: list[tuple[float, float]]) -> tuple[list[dict[str, float]], float, float, float, float]:
    """Collapse fine rows into bands; return bands, bottom, neck_w, neck_from, neck_to."""
    bottom = None
    saw_chamber = False
    for d, w in rows:
        if w >= 9.0:
            saw_chamber = True
        if saw_chamber and 0 < w < 4.0:
            bottom = d
            break
        if saw_chamber and w == 0.0:
            bottom = d
            break
    if bottom is None:
        # last depth with width > 3 before collapse
        for d, w in reversed(rows):
            if w >= 3.0:
                bottom = d
                break
    if bottom is None:
        bottom = rows[-1][0] if rows else 0.0

    useful = [(d, w) for d, w in rows if d <= bottom + 1e-9 and w > 0]
    bands: list[dict[str, float]] = []
    i = 0
    while i < len(useful):
        d0, w0 = useful[i]
        widths = [w0]
        j = i
        while j + 1 < len(useful):
            _, w1 = useful[j + 1]
            ref = sum(widths) / len(widths)
            if abs(w1 - ref) <= max(0.85, 0.12 * ref):
                widths.append(w1)
                j += 1
            else:
                break
        if j + 1 < len(useful):
            d_end = round((useful[j][0] + useful[j + 1][0]) / 2, 2)
        else:
            d_end = useful[j][0]
        d_from = 0.0 if not bands else bands[-1]["depth_to_mm"]
        bands.append(
            {
                "depth_from_mm": d_from,
                "depth_to_mm": d_end,
                "width_mm": round(sum(widths) / len(widths), 2),
            }
        )
        i = j + 1

    # neck = minimum width in the first ~2 mm among bands/rows with w>4
    neck_rows = [(d, w) for d, w in rows if 0.25 <= d <= 2.0 and w >= 4.0]
    if neck_rows:
        neck_w = min(w for _, w in neck_rows)
        neck_ds = [d for d, w in neck_rows if abs(w - neck_w) < 0.35]
        neck_from = min(neck_ds)
        neck_to = max(neck_ds)
    else:
        neck_w = bands[0]["width_mm"] if bands else 0.0
        neck_from, neck_to = 0.0, 0.0

    return bands, float(bottom), float(neck_w), float(neck_from), float(neck_to)


def _second_moments(face) -> tuple[float, float, float]:
    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopLoc import TopLoc_Location

    BRepMesh_IncrementalMesh(face.wrapped, 0.05)
    loc = TopLoc_Location()
    tri = BRep_Tool.Triangulation_s(face.wrapped, loc)
    if tri is None:
        raise RuntimeError("failed to triangulate end face")
    trsf = loc.Transformation()
    nodes: list[tuple[float, float]] = []
    for i in range(1, tri.NbNodes() + 1):
        p = tri.Node(i)
        p.Transform(trsf)
        nodes.append((p.X(), p.Y()))
    area = 0.0
    cx = cy = 0.0
    tris: list[tuple[float, float, float, float, float, float, float]] = []
    for i in range(1, tri.NbTriangles() + 1):
        i1, i2, i3 = tri.Triangle(i).Get()
        x1, y1 = nodes[i1 - 1]
        x2, y2 = nodes[i2 - 1]
        x3, y3 = nodes[i3 - 1]
        a = 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        area += a
        cx += a * (x1 + x2 + x3) / 3.0
        cy += a * (y1 + y2 + y3) / 3.0
        tris.append((x1, y1, x2, y2, x3, y3, a))
    if abs(area) < 1e-9:
        raise RuntimeError("zero-area end face")
    cx /= area
    cy /= area
    ixx = iyy = 0.0
    abs_area = 0.0
    for x1, y1, x2, y2, x3, y3, a in tris:
        x1c, y1c = x1 - cx, y1 - cy
        x2c, y2c = x2 - cx, y2 - cy
        x3c, y3c = x3 - cx, y3 - cy
        aa = abs(a)
        ixx += aa / 6.0 * (y1c * y1c + y2c * y2c + y3c * y3c + y1c * y2c + y1c * y3c + y2c * y3c)
        iyy += aa / 6.0 * (x1c * x1c + x2c * x2c + x3c * x3c + x1c * x2c + x1c * x3c + x2c * x3c)
        abs_area += aa
    return abs_area, ixx, iyy


def measure_step(
    step_path: str | Path,
    *,
    profile_id: str | None = None,
    vendor: str = "motedis",
    product_name: str = "",
    product_url: str = "",
    source_step_url: str = "",
    fastener_family: str = "",
    groove_nominal_mm: float | None = None,
    groove_depth_mm: float | None = None,
    core_thread: str = "",
    grid_step_mm: float = 0.1,
) -> ProfileRecord:
    """Import STEP, measure section properties + slot scan, return a ProfileRecord."""
    _require_cadquery()
    import cadquery as cq

    path = Path(step_path)
    if not path.exists():
        raise FileNotFoundError(path)

    solid = cq.importers.importStep(str(path)).val()
    end, axis, bb = _end_face(solid)
    length = {"x": bb.xlen, "y": bb.ylen, "z": bb.zlen}[axis]
    area_from_volume = solid.Volume() / length
    area_tri, ixx, iyy = _second_moments(end)
    # Prefer volume-derived area (exact); keep I from triangulation.
    area = round(area_from_volume, 4)
    mass = round(area * 1e-6 * ALUMINIUM_DENSITY_KG_M3, 4)
    effective_density = round(mass / ((bb.xlen * bb.ylen) * 1e-9) , 1) if axis == "z" else round(
        mass / (area * 1e-6), 1
    )
    # Effective density of the envelope: mass / (outer_x * outer_y * 1 m)
    outer_x = round(min(bb.xlen, bb.ylen) if axis == "z" else (bb.ylen if axis == "x" else bb.xlen), 3)
    # Actually outer is the two short bbox dims
    dims = sorted([bb.xlen, bb.ylen, bb.zlen])
    outer = [round(dims[0], 3), round(dims[1], 3)]
    envelope_m2 = (outer[0] * 1e-3) * (outer[1] * 1e-3)
    effective_density = round(mass / envelope_m2, 1)

    polys = _face_polylines(end)
    outer_poly, holes = _classify_polys(polys)
    xs = [p[0] for p in outer_poly]
    ys = [p[1] for p in outer_poly]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    grid, step, gx0, gy0, nx, ny = _build_grid(
        outer_poly, holes, xmin, xmax, ymin, ymax, step=grid_step_mm
    )

    best_rows = None
    best_score = -1
    for face in ("+y", "-y", "+x", "-x"):
        rows = _slot_scan_grid(grid, step, gx0, gy0, nx, ny, face)
        widths = [w for _, w in rows]
        score = 0
        if any(5.0 <= w <= 8.0 for w in widths):
            score += 2
        if any(w >= 9.0 for w in widths):
            score += 2
        if any(4.5 <= d <= 7.5 and 0 < w < 4 for d, w in rows):
            score += 2
        if score > best_score:
            best_score = score
            best_rows = rows

    assert best_rows is not None
    bands, bottom, neck_w, neck_from, neck_to = _bin_slot_scan(best_rows)

    # Guess family from neck if not provided
    if not fastener_family:
        if neck_w < 5.6:
            fastener_family = "nut-5"
            groove_nominal_mm = groove_nominal_mm or 5.0
            core_thread = core_thread or "M5"
        else:
            fastener_family = "nut-6"
            groove_nominal_mm = groove_nominal_mm or 6.0
            core_thread = core_thread or "M6"
    groove_nominal_mm = float(groove_nominal_mm or round(neck_w))
    groove_depth_mm = float(groove_depth_mm or bottom)

    if not profile_id:
        profile_id = f"{int(outer[0])}x{int(outer[1])}-{fastener_family}"
    if not product_name:
        product_name = path.stem

    provenance = {
        "area_mm2": "measured",
        "mass_per_m_kg": "measured",
        "ixx_mm4": "measured",
        "iyy_mm4": "measured",
        "slot_scan": "measured",
        "slot_bottom_mm": "measured",
        "neck_width_mm": "measured",
        "outer_mm": "measured",
        "groove_nominal_mm": "vendor" if groove_nominal_mm else "assumed",
        "groove_depth_mm": "vendor" if groove_depth_mm else "measured",
        "core_thread": "vendor" if core_thread else "assumed",
        "fastener_family": "vendor" if fastener_family else "assumed",
    }

    return ProfileRecord(
        id=profile_id,
        vendor=vendor,
        product_name=product_name,
        product_url=product_url,
        source_step_url=source_step_url or product_url,
        source_step_sha256=file_sha256(path),
        source_step_filename=path.name,
        outer_mm=outer,
        fastener_family=fastener_family,
        groove_nominal_mm=groove_nominal_mm,
        groove_depth_mm=groove_depth_mm,
        core_thread=core_thread,
        area_mm2=area,
        mass_per_m_kg=mass,
        density_used_kg_m3=ALUMINIUM_DENSITY_KG_M3,
        effective_density_kg_m3=effective_density,
        ixx_mm4=round(ixx, 2),
        iyy_mm4=round(iyy, 2),
        slot_scan=bands,
        slot_bottom_mm=bottom,
        neck_width_mm=round(neck_w, 2),
        neck_depth_from_mm=round(neck_from, 2),
        neck_depth_to_mm=round(neck_to, 2),
        provenance=provenance,  # type: ignore[arg-type]
        notes=(
            "Measured from vendor STEP. Mass uses aluminium density "
            f"{ALUMINIUM_DENSITY_KG_M3:g} kg/m³ on the measured cross-section "
            "(effective density is for the outer envelope, not solid bar)."
        ),
    )


def emit_record(record: ProfileRecord, out_path: Path | None = None) -> Path:
    return save_profile(record, out_path)


def measure_and_emit(step_path: str | Path, out_path: Path | None = None, **kwargs: Any) -> Path:
    record = measure_step(step_path, **kwargs)
    return emit_record(record, out_path)
