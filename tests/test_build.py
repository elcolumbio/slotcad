from pathlib import Path

import pytest

from slotcad.build import compile_topology
from slotcad.fasteners import FastenerFamilyError, assert_single_family
from slotcad.registry import load_profile
from slotcad.topology import BoxShelf, Frame

ROOT = Path(__file__).resolve().parents[1]
NUT6 = load_profile(ROOT / "registry/motedis/20x20-b-typ-nut-6.json")
NUT5 = load_profile(ROOT / "registry/motedis/20x20-i-typ-nut-5.json")


def test_shelf_emits_cut_list_and_checks():
    topo = BoxShelf(800, 300, 900, levels=2, profile=NUT6).build()
    result = compile_topology(topo)
    assert result.ok
    assert result.cut_list is not None
    assert len(result.cut_list) >= 2
    assert result.panels
    assert result.fasteners
    assert result.interference.ok
    assert result.deflection
    assert result.nesting is not None
    assert result.assembly_order


def test_frame_rung_length_subtracts_faces():
    topo = Frame(600, 1200, rungs=3, profile=NUT6).build()
    assert topo.params["rung_length_mm"] == 600 - 2 * 20
    result = compile_topology(topo)
    assert result.ok
    assert result.cut_list is not None


def test_changing_parameter_changes_cut_list():
    a = compile_topology(BoxShelf(800, 300, 900, levels=2, profile=NUT6).build())
    b = compile_topology(BoxShelf(900, 300, 900, levels=2, profile=NUT6).build())
    assert a.cut_list is not None and b.cut_list is not None
    lengths_a = sorted((c.length_mm, c.qty, c.role) for c in a.cut_list)
    lengths_b = sorted((c.length_mm, c.qty, c.role) for c in b.cut_list)
    assert lengths_a != lengths_b


def test_mix_nut5_nut6_hard_error():
    with pytest.raises(FastenerFamilyError) as ei:
        assert_single_family([NUT5, NUT6])
    msg = str(ei.value)
    assert "Nut 5" in msg or "nut-5" in msg.lower() or "I-Typ" in msg
    assert "Nut 6" in msg or "nut-6" in msg.lower() or "B-Typ" in msg

    topo = BoxShelf(800, 300, 900, levels=2, profile=NUT6, profile_b=NUT5).build()
    result = compile_topology(topo)
    assert not result.ok
    assert result.cut_list is None
    assert any("fastener" in e.lower() or "mix" in e.lower() for e in result.errors)
    assert "Nut 5" in result.errors[0] or "nut-5" in result.errors[0].lower() or "I-Typ" in result.errors[0]
    assert "Nut 6" in result.errors[0] or "nut-6" in result.errors[0].lower() or "B-Typ" in result.errors[0]


def test_deliberate_overlap_withholds_cut_list():
    topo = BoxShelf(800, 300, 900, levels=2, profile=NUT6, force_overlap=True).build()
    result = compile_topology(topo)
    assert not result.interference.ok
    assert result.cut_list is None
    assert not result.ok


def test_four_side_panel_reports_corner_hits():
    topo = BoxShelf(800, 300, 900, levels=1, profile=NUT6, panel_four_sides=True).build()
    result = compile_topology(topo)
    assert not result.interference.ok
    assert result.cut_list is None
    assert any("notch" in n.lower() or "corner" in n.lower() for n in result.notes)
