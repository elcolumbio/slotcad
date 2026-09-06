"""Command-line interface for slotcad."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from slotcad import __version__
from slotcad.build import compile_topology
from slotcad.registry import find_profile, load_profile
from slotcad.sheet import write_build_sheet
from slotcad.topology import BoxShelf, Frame


def _cmd_measure(args: argparse.Namespace) -> int:
    from slotcad.measure import measure_and_emit, measure_step
    from slotcad.registry import canonical_json

    kwargs = {
        "profile_id": args.id,
        "vendor": args.vendor,
        "product_name": args.product_name or "",
        "product_url": args.product_url or "",
        "source_step_url": args.source_url or args.product_url or "",
        "fastener_family": args.family or "",
        "groove_nominal_mm": args.groove_nominal,
        "groove_depth_mm": args.groove_depth,
        "core_thread": args.core_thread or "",
    }
    # drop Nones
    kwargs = {k: v for k, v in kwargs.items() if v is not None and v != ""}

    if args.emit:
        out = Path(args.out) if args.out else None
        path = measure_and_emit(args.step, out, **kwargs)
        print(f"wrote {path}")
        # prove byte-identical re-run message
        record = measure_step(args.step, **kwargs)
        from slotcad.registry import canonical_json as cj

        again = cj(record.to_dict()).encode("utf-8")
        first = path.read_bytes()
        if again == first:
            print("re-emit byte-identical: OK")
        else:
            print("re-emit byte-identical: DIFFERED (check float rounding)", file=sys.stderr)
            return 1
        return 0

    record = measure_step(args.step, **kwargs)
    print(canonical_json(record.to_dict()))
    return 0


def _load_default_profile(profile_arg: str | None):
    if profile_arg:
        return find_profile(profile_arg) if "/" not in profile_arg and not profile_arg.endswith(".json") else load_profile(profile_arg)
    # default Nut 6 reference
    return find_profile("20x20-b-typ-nut-6")


def _cmd_build_shelf(args: argparse.Namespace) -> int:
    profile = _load_default_profile(args.profile)
    profile_b = find_profile(args.profile_b) if args.profile_b else None
    shelf = BoxShelf(
        width_mm=args.width,
        depth_mm=args.depth,
        height_mm=args.height,
        levels=args.levels,
        profile=profile,
        profile_b=profile_b,
        panel_thickness_mm=args.panel_thickness,
        panel_four_sides=args.panel_four_sides,
        force_overlap=args.force_overlap,
    )
    topo = shelf.build()
    result = compile_topology(topo, stock_mm=args.stock)
    _emit_build(result, profile, args)
    return 0 if result.ok else 2


def _cmd_build_frame(args: argparse.Namespace) -> int:
    profile = _load_default_profile(args.profile)
    profile_b = find_profile(args.profile_b) if args.profile_b else None
    frame = Frame(
        width_mm=args.width,
        height_mm=args.height,
        rungs=args.rungs,
        profile=profile,
        profile_b=profile_b,
        force_overlap=args.force_overlap,
    )
    topo = frame.build()
    result = compile_topology(topo, stock_mm=args.stock)
    _emit_build(result, profile, args)
    return 0 if result.ok else 2


def _emit_build(result, profile, args) -> None:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = result.to_dict()
    stem = getattr(args, "topology", None) or result.topology
    # normalize box-shelf → shelf for stable artefact names
    if stem in {"box-shelf", "shelf"}:
        stem = "shelf"
    json_path = out_dir / f"{stem}.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {json_path}")

    if args.sheet:
        html_path = Path(args.sheet)
    else:
        html_path = out_dir / f"{stem}.html"
    write_build_sheet(result, profile, html_path)
    print(f"wrote {html_path}")

    if result.cut_list is None:
        print("CUT LIST WITHHELD", file=sys.stderr)
        for e in result.errors:
            print(f"  error: {e}", file=sys.stderr)
    else:
        print("cut list:")
        for c in result.cut_list:
            print(f"  {c.qty}× {c.length_mm:g} mm {c.role} [{c.provenance}]")
    print(result.interference.summary())


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="slotcad", description="Measure T-slot profiles and compile topologies")
    p.add_argument("--version", action="version", version=f"slotcad {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    m = sub.add_parser("measure", help="measure a vendor STEP into a registry record")
    m.add_argument("step", help="path to .step/.stp (not committed)")
    m.add_argument("--emit", action="store_true", help="write registry JSON")
    m.add_argument("--out", help="output JSON path")
    m.add_argument("--id", help="profile id (filename stem)")
    m.add_argument("--vendor", default="motedis")
    m.add_argument("--product-name", dest="product_name")
    m.add_argument("--product-url", dest="product_url")
    m.add_argument("--source-url", dest="source_url")
    m.add_argument("--family", help="fastener family, e.g. nut-6")
    m.add_argument("--groove-nominal", dest="groove_nominal", type=float)
    m.add_argument("--groove-depth", dest="groove_depth", type=float)
    m.add_argument("--core-thread", dest="core_thread")
    m.set_defaults(func=_cmd_measure)

    b = sub.add_parser("build", help="compile a topology")
    bsub = b.add_subparsers(dest="topology", required=True)

    def add_common(sp):
        sp.add_argument("--profile", default="20x20-b-typ-nut-6")
        sp.add_argument("--profile-b", dest="profile_b", default=None, help="second profile (mix → hard error)")
        sp.add_argument("--out-dir", default="out")
        sp.add_argument("--sheet", help="HTML build sheet path")
        sp.add_argument("--stock", type=float, default=1980.0)
        sp.add_argument("--force-overlap", action="store_true", help="deliberate buried rail for tests")

    sh = bsub.add_parser("shelf", help="box shelf topology")
    add_common(sh)
    sh.add_argument("--width", type=float, default=800)
    sh.add_argument("--depth", type=float, default=300)
    sh.add_argument("--height", type=float, default=900)
    sh.add_argument("--levels", type=int, default=2)
    sh.add_argument("--panel-thickness", type=float, default=None)
    sh.add_argument("--panel-four-sides", action="store_true", help="engage all four slots (corners hit posts)")
    sh.set_defaults(func=_cmd_build_shelf)

    fr = bsub.add_parser("frame", help="two uprights + rungs")
    add_common(fr)
    fr.add_argument("--width", type=float, default=600)
    fr.add_argument("--height", type=float, default=1200)
    fr.add_argument("--rungs", type=int, default=3)
    fr.set_defaults(func=_cmd_build_frame)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
