"""Optional live STEP re-measure — skipped when the vendor file is absent."""

from pathlib import Path

import pytest

STEP = Path("/tmp/slotcad-dl/Motedis Profile 20x20 B-Type slot 6.stp")
ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(not STEP.exists(), reason="vendor STEP not present locally")
def test_measure_emit_byte_identical(tmp_path):
    from slotcad.measure import measure_step
    from slotcad.registry import canonical_json, save_profile

    rec = measure_step(
        STEP,
        profile_id="20x20-b-typ-nut-6",
        vendor="motedis",
        product_name="20x20 B-Typ Nut 6",
        product_url="https://www.motedis.com/en/Profile-20x20-B-type-slot-6",
        source_step_url="https://www.motedis.com/shop/products_files/motedis-profile-20x20-b-type-slot-6.zip",
        fastener_family="nut-6",
        groove_nominal_mm=6.0,
        groove_depth_mm=5.5,
        core_thread="M6",
    )
    out = tmp_path / "out.json"
    save_profile(rec, out)
    again = canonical_json(measure_step(
        STEP,
        profile_id="20x20-b-typ-nut-6",
        vendor="motedis",
        product_name="20x20 B-Typ Nut 6",
        product_url="https://www.motedis.com/en/Profile-20x20-B-type-slot-6",
        source_step_url="https://www.motedis.com/shop/products_files/motedis-profile-20x20-b-type-slot-6.zip",
        fastener_family="nut-6",
        groove_nominal_mm=6.0,
        groove_depth_mm=5.5,
        core_thread="M6",
    ).to_dict()).encode()
    assert out.read_bytes() == again
    # neck matches committed registry
    committed = (ROOT / "registry/motedis/20x20-b-typ-nut-6.json").read_bytes()
    assert out.read_bytes() == committed
