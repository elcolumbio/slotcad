from pathlib import Path

from slotcad.registry import canonical_json, load_profile, save_profile

ROOT = Path(__file__).resolve().parents[1]
NUT6 = ROOT / "registry/motedis/20x20-b-typ-nut-6.json"
NUT5 = ROOT / "registry/motedis/20x20-i-typ-nut-5.json"


def test_load_reference_profiles():
    p6 = load_profile(NUT6)
    p5 = load_profile(NUT5)
    assert p6.fastener_family == "nut-6"
    assert p5.fastener_family == "nut-5"
    assert p6.neck_width_mm == 6.2
    assert abs(p5.mass_per_m_kg - 0.4912) < 1e-6
    assert abs(p5.effective_density_kg_m3 - 1228.0) < 1e-6


def test_save_roundtrip_byte_identical(tmp_path):
    p6 = load_profile(NUT6)
    out = tmp_path / "round.json"
    save_profile(p6, out)
    assert out.read_text(encoding="utf-8") == canonical_json(p6.to_dict())
    assert load_profile(out).to_dict() == p6.to_dict()


def test_nut6_slot_scan_matches_brief_shape():
    p6 = load_profile(NUT6)
    assert p6.slot_bottom_mm == 5.5
    # entry wider than neck; chamber wider still
    widths = [b["width_mm"] for b in p6.slot_scan]
    assert widths[0] > p6.neck_width_mm
    assert max(widths) >= 11.0
