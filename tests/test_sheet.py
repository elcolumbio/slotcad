from pathlib import Path

from slotcad.build import compile_topology
from slotcad.registry import load_profile
from slotcad.sheet import render_build_sheet
from slotcad.topology import BoxShelf

ROOT = Path(__file__).resolve().parents[1]
NUT6 = load_profile(ROOT / "registry/motedis/20x20-b-typ-nut-6.json")


def test_html_contains_provenance_tags():
    result = compile_topology(BoxShelf(800, 300, 900, levels=2, profile=NUT6).build())
    html = render_build_sheet(result, NUT6)
    assert "prov-m" in html or "measured" in html
    assert "assumed" in html
    assert "slotcad" in html.lower()
    assert NUT6.neck_width_mm.__str__() in html or "6.2" in html
