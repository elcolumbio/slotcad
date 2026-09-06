"""Self-contained HTML build sheets (f-strings, html.escape, inline CSS)."""

from __future__ import annotations

import html as html_lib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from slotcad.build import BuildResult
from slotcad.registry import ProfileRecord


def _esc(value: Any) -> str:
    return html_lib.escape(str(value), quote=True)


def _prov_tag(prov: str) -> str:
    cls = {"measured": "prov-m", "vendor": "prov-v", "assumed": "prov-a"}.get(prov, "prov-a")
    return f'<span class="prov {cls}">{_esc(prov)}</span>'


def render_build_sheet(
    result: BuildResult,
    profile: ProfileRecord,
    *,
    title: str | None = None,
) -> str:
    title = title or f"slotcad build sheet — {result.topology}"
    generated = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")

    scan_rows = "".join(
        f"<tr><td>{_esc(b['depth_from_mm'])}–{_esc(b['depth_to_mm'])}</td>"
        f"<td>{_esc(b['width_mm'])}</td></tr>"
        for b in profile.slot_scan
    )

    cut_html = ""
    if result.cut_list is None:
        cut_html = (
            "<p class='fail'><strong>No cut list.</strong> "
            "Interference failed or fastener families were mixed — "
            "a missing cut list is cheaper than a wrong delivery.</p>"
        )
        if result.errors:
            cut_html += "<ul>" + "".join(f"<li>{_esc(e)}</li>" for e in result.errors) + "</ul>"
    else:
        rows = "".join(
            "<tr>"
            f"<td>{_esc(c.name)}</td>"
            f"<td>{_esc(c.qty)}</td>"
            f"<td>{_esc(c.length_mm)}</td>"
            f"<td>{_esc(c.role)}</td>"
            f"<td>{_prov_tag(c.provenance)}</td>"
            "</tr>"
            for c in result.cut_list
        )
        cut_html = f"""
        <table>
          <thead><tr><th>Item</th><th>Qty</th><th>Length (mm)</th><th>Role</th><th>Provenance</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        """

    panel_rows = "".join(
        "<tr>"
        f"<td>{_esc(p.name)}</td>"
        f"<td>{_esc(p.width_mm)} × {_esc(p.depth_mm)}</td>"
        f"<td>{_esc(p.thickness_mm)} (band {_esc(p.thickness_band_mm[0])}–{_esc(p.thickness_band_mm[1])})</td>"
        f"<td>{_prov_tag(p.provenance)}</td>"
        f"<td>{_esc(p.notes)}</td>"
        "</tr>"
        for p in result.panels
    )

    fast_rows = "".join(
        "<tr>"
        f"<td>{_esc(f.name)}</td>"
        f"<td>{_esc(f.qty)}</td>"
        f"<td>{_esc(f.family)}</td>"
        f"<td>{_prov_tag(f.provenance)}</td>"
        f"<td>{_esc(f.notes)}</td>"
        "</tr>"
        for f in result.fasteners
    )

    hit_rows = "".join(
        f"<tr><td>{_esc(h.a)}</td><td>{_esc(h.b)}</td>"
        f"<td>{_esc(round(h.volume_mm3,1))}</td><td>{_esc(h.note)}</td></tr>"
        for h in result.interference.hits
    ) or "<tr><td colspan='4'>none</td></tr>"

    defl_rows = "".join(
        "<tr>"
        f"<td>{_esc(d.span_mm)}</td>"
        f"<td>{_esc(d.load_n)}</td>"
        f"<td>{_esc(d.i_mm4)} {_prov_tag(d.provenance_i)}</td>"
        f"<td>{_esc(d.delta_mm)}</td>"
        f"<td>{_esc(d.formula)}</td>"
        "</tr>"
        for d in result.deflection
    )

    nest = result.nesting or {}
    nest_html = "<p>n/a</p>"
    if nest:
        nest_html = f"""
        <p>Stock {_esc(nest.get('stock_mm'))} mm; min cut {_esc(nest.get('min_cut_mm'))} mm.</p>
        <p>FFD bars: <strong>{_esc(nest.get('first_fit_decreasing_bars'))}</strong>;
           interleaved bars: <strong>{_esc(nest.get('interleaved_bars'))}</strong>.</p>
        <p class="note">{_esc(nest.get('cut_to_length_note',''))}</p>
        """

    order = "".join(f"<li>{_esc(s)}</li>" for s in result.assembly_order)
    notes = "".join(f"<li>{_esc(n)}</li>" for n in result.notes)
    params = "".join(
        f"<tr><td>{_esc(k)}</td><td>{_esc(v)}</td></tr>" for k, v in sorted(result.params.items(), key=lambda kv: kv[0])
    )

    status = "OK" if result.ok else "FAILED"
    status_cls = "ok" if result.ok else "fail"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{_esc(title)}</title>
<style>
  body {{ font-family: Georgia, serif; margin: 2rem; color: #122; background: #faf9f6; }}
  h1,h2 {{ font-family: system-ui, sans-serif; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0.75rem 0 1.5rem; }}
  th, td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; }}
  th {{ background: #eee; }}
  .prov {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
           padding: 0.1rem 0.35rem; border-radius: 3px; }}
  .prov-m {{ background: #c8f7c5; }}
  .prov-v {{ background: #cde4ff; }}
  .prov-a {{ background: #ffe6a7; }}
  .ok {{ color: #0a0; font-weight: 700; }}
  .fail {{ color: #a00; font-weight: 700; }}
  .banner {{ background: #fff3cd; border: 1px solid #e0c36a; padding: 0.75rem 1rem; margin-bottom: 1.5rem; }}
  .note {{ color: #555; font-size: 0.95rem; }}
  code {{ background: #eee; padding: 0.1rem 0.3rem; }}
</style>
</head>
<body>
  <h1>{_esc(title)}</h1>
  <p class="note">Generated { _esc(generated) }. No relationship with any vendor.
  This tool sizes parts; it does not certify a structure.</p>

  <div class="banner">
    <strong>Honesty header:</strong> every dimension carries
    {_prov_tag("measured")} / {_prov_tag("vendor")} / {_prov_tag("assumed")}.
    Assumed values are placeholders until someone reaches for a caliper.
    Status: <span class="{status_cls}">{_esc(status)}</span>
    — family <code>{_esc(result.family)}</code>
  </div>

  <h2>Profile</h2>
  <table>
    <tr><th>Product</th><td>{_esc(profile.product_name)} (<code>{_esc(profile.id)}</code>)</td></tr>
    <tr><th>Vendor</th><td>{_esc(profile.vendor)} — <a href="{_esc(profile.product_url)}">{_esc(profile.product_url)}</a></td></tr>
    <tr><th>Outer</th><td>{_esc(profile.outer_mm)} mm {_prov_tag(profile.provenance.get('outer_mm','measured'))}</td></tr>
    <tr><th>Area</th><td>{_esc(profile.area_mm2)} mm² {_prov_tag(profile.provenance.get('area_mm2','measured'))}</td></tr>
    <tr><th>Mass / m</th><td>{_esc(profile.mass_per_m_kg)} kg/m {_prov_tag(profile.provenance.get('mass_per_m_kg','measured'))}</td></tr>
    <tr><th>Ixx / Iyy</th><td>{_esc(profile.ixx_mm4)} / {_esc(profile.iyy_mm4)} mm⁴ {_prov_tag(profile.provenance.get('ixx_mm4','measured'))}</td></tr>
    <tr><th>Neck</th><td>{_esc(profile.neck_width_mm)} mm @ {_esc(profile.neck_depth_from_mm)}–{_esc(profile.neck_depth_to_mm)} mm {_prov_tag(profile.provenance.get('neck_width_mm','measured'))}</td></tr>
    <tr><th>Slot bottom</th><td>{_esc(profile.slot_bottom_mm)} mm {_prov_tag(profile.provenance.get('slot_bottom_mm','measured'))}</td></tr>
    <tr><th>STEP sha256</th><td><code>{_esc(profile.source_step_sha256)}</code></td></tr>
  </table>

  <h2>Slot scan (depth from outer face → opening width)</h2>
  <table>
    <thead><tr><th>Depth (mm)</th><th>Width (mm)</th></tr></thead>
    <tbody>{scan_rows}</tbody>
  </table>

  <h2>Topology parameters</h2>
  <table>
    <thead><tr><th>Parameter</th><th>Value</th></tr></thead>
    <tbody>{params}</tbody>
  </table>

  <h2>Cut list</h2>
  {cut_html}

  <h2>Panels</h2>
  <table>
    <thead><tr><th>Name</th><th>Size (mm)</th><th>Thickness (mm)</th><th>Provenance</th><th>Notes</th></tr></thead>
    <tbody>{panel_rows or "<tr><td colspan='5'>none</td></tr>"}</tbody>
  </table>

  <h2>Fasteners</h2>
  <table>
    <thead><tr><th>Item</th><th>Qty</th><th>Family</th><th>Provenance</th><th>Notes</th></tr></thead>
    <tbody>{fast_rows or "<tr><td colspan='5'>none</td></tr>"}</tbody>
  </table>

  <h2>Interference ({_esc(result.interference.method)})</h2>
  <p class="{ 'ok' if result.interference.ok else 'fail' }">{_esc(result.interference.summary())}</p>
  <table>
    <thead><tr><th>A</th><th>B</th><th>Volume (mm³)</th><th>Note</th></tr></thead>
    <tbody>{hit_rows}</tbody>
  </table>

  <h2>Deflection</h2>
  <table>
    <thead><tr><th>Span (mm)</th><th>Load (N)</th><th>I (mm⁴)</th><th>δ (mm)</th><th>Formula</th></tr></thead>
    <tbody>{defl_rows or "<tr><td colspan='5'>none</td></tr>"}</tbody>
  </table>

  <h2>Nesting</h2>
  {nest_html}

  <h2>Assembly order</h2>
  <ol>{order}</ol>

  <h2>Notes</h2>
  <ul>{notes}</ul>
</body>
</html>
"""


def write_build_sheet(result: BuildResult, profile: ProfileRecord, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_build_sheet(result, profile), encoding="utf-8")
    return path
