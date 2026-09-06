# slotcad

Measured on a real Motedis **20×20 B-Typ Nut 6** STEP (sha256 `af8c0578…`):

```
 0.0 – 0.38 mm    7.30 mm   chamfered entry
 0.38 – 1.38 mm   6.35 mm   → neck min 6.20 mm (the only part that grips a panel)
 1.62 – 3.88 mm  ~11.3 mm   T-nut chamber; a panel just floats here
 5.5 mm                    bottom
```

**The catalogue number is not the dimension that holds your panel.** “Nut 6” is a
**6.20 mm neck roughly 1 mm long**. A panel must be ≤ ~5.9 mm; a nominal 6 mm sheet at
the top of its tolerance band jams partway down a long slide. 5 mm acrylic goes in with
play. No catalogue page tells you that.

`slotcad` takes the **vendor’s own solid**, measures what the profile really is, and
compiles a declared *topology* (posts, rails, panels) into a cut list, panel sizes,
fastener counts, interference check, deflection estimate and nesting plan — from one
object, so the bill of materials cannot drift from the geometry.

There is **no relationship** with Motedis or any other vendor. We link to product pages
and publish measurements derived from their CAD; we do not redistribute STEP files,
catalogue data, or prices.

## Why it exists

Builders keep ordering the wrong T-nuts for “series 20 / 2020” and sizing panels without
a real slot neck. Two linked failures this library is built to catch:

1. Amazon “series 20” T-nuts jammed in an 80/20 Series 20 opening that was actually
   ~5.26 mm — [OpenBuilds thread](https://builds.openbuilds.com/threads/watch-out-for-this-detail-when-buying-extrusion-from-certain-suppliers.14970/).
2. “2020” is not one slot — local stock vs catalogue T-nuts —
   [Engineering Stack Exchange](https://engineering.stackexchange.com/questions/13471/will-standard-m5-t-slot-nuts-fit-these-different-2020-aluminium-extrusions).

See `research/PAINPOINTS.md` for six documented cases. Mixing **Nut 5** and **Nut 6** on
the same 20×20 outer size is a **hard error** (they share no T-nut, bracket, or screw).

## Quick start

```bash
uv sync --extra dev
make test
make build-shelf    # → out/shelf.json + out/shelf.html
make sheet          # same HTML build sheet
make build-frame
```

CLI (every command has a Make target):

```bash
uv run python -m slotcad build shelf --width 800 --depth 300 --height 900 --levels 2
uv run python -m slotcad build frame --width 600 --height 1200 --rungs 3
uv run python -m slotcad measure path/to/vendor.step --emit   # local STEP only
```

## Registry (the durable asset)

Vendor STEP files are **not** redistributable (Motedis terms forbid handing drawings to
third parties). What ships is `registry/` — one JSON per profile with area, mass/m,
Ixx/Iyy, full slot scan, fastener family, source URL and STEP checksum.

| Profile | Family | Neck | Mass/m | Notes |
|---|---|---|---|---|
| `registry/motedis/20x20-b-typ-nut-6.json` | nut-6 | **6.20 mm** | 0.4375 kg/m | brief reference scan |
| `registry/motedis/20x20-i-typ-nut-5.json` | nut-5 | 5.20 mm | **0.4912 kg/m** (eff. 1228 kg/m³) | same 20×20 outer |

Re-running `measure --emit` on the same STEP reproduces the JSON **byte for byte**.
Contributing a new record is the obvious first pull request.

Mass and inertia always come from the **measured section**, never from “aluminium is
2700 kg/m³ and the bar is solid”. A T-slot is mostly air — using 2700 on the envelope
made one mast 2.2× too heavy.

## Honesty rules

- Every dimension carries provenance: `measured` / `vendor` / `assumed`.
- Assumed values never reach a cut list without a visible flag.
- Failed interference → **no cut list**. Mixed fastener families → **hard error**.
- This tool sizes parts. It does **not** certify a structure.

## Interference

Prefer CadQuery boolean intersection when available. Fallback: axis-aligned box overlap
that still catches buried rails and panel-corner/post hits. Limitation of the AABB path:
no rotated or curved collisions. Default shelf panels engage **front-and-back only**;
`--panel-four-sides` demonstrates corner overlaps and withholds the cut list — notch
corners or keep two-side engagement; the brief’s measured sag trade-off (0.80 → 0.65 mm)
is often not worth the notches.

## Out of scope

No GUI, no web configurator, no simulation, no motion, no vendor ordering integration,
no Docker, no framework, no telemetry, no account.

## Licence

MIT — see `LICENSE`. Warranty disclaimer included: free software, no certification.
