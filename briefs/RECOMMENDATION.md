# RECOMMENDATION — slotcad Phase 1

**Date:** 2026-09-06  
**Inputs:** `VENDORS.md` + `vendors.json`, `FASTENERS.md`, `LANDSCAPE.md`, `PAINPOINTS.md`.

## Reference vendor: **Motedis**

Build the v1 reference profiles against **Motedis 20×20 I-Type slot 5** and **20×20 B-type slot 6**.

Why:

1. **Public CAD without an account** — [CAD & Info Database](https://www.motedis.com/en/cad-database). Measure locally; never commit the STEP.
2. Naming matches the brief and the two real builds (`personal/robot`, `personal/shelf`).
3. Cut-to-length is normal (stock packs include 1980 mm; custom ~50–6000 mm). Nesting against 1980 mm is a real feature, not cosplay.
4. Licence **forbids** handing drawings to third parties → the measurements-only registry model is the correct product shape, not a workaround.

**OpenBuilds** is the only surveyed vendor with an **explicitly permissive** STEP story (CC BY-SA on branded works). Use it later if we want a redistributable solid in-tree; it is a different geometry (V-Slot) and trademark-constrained. Do not switch the reference to OpenBuilds just for licence comfort.

**item / Misumi / 80/20** are fine as *measurement sources* once you can download a solid, but they are worse first references: account walls and clear anti-redistribution terms. Their configurators (Engineeringtool, FRAMES, IdeaBuilder) are the feature bar to beat, not the licence path.

## May any vendor STEP be redistributed?

| Answer | Vendors |
|--------|---------|
| **No (quoted ban)** | Motedis, item, Misumi, 80/20 |
| **Default no / unverified** | Bosch Rexroth, MayTec, Alutec KK, MiniTec, TSLOTS, MakerBeam |
| **Yes (CC BY-SA)** | OpenBuilds only |

**Ship:** `registry/` JSON (area, mass/m, Ixx/Iyy, full slot scan, fastener family, source URL, STEP checksum).  
**Do not ship:** vendor STEP files, catalogue mirrors, or prices.

Derived measurements are `unclear` in almost every licence. Keep provenance loud (`measured` / `vendor` / `assumed`) and the README disclaimer that there is no vendor relationship.

## Landscape: the gap is real

Nothing surveyed **measures real T-slot geometry from a vendor STEP** and drives topology → BOM from that. Closest products regenerate catalogue geometry inside a vendor silo. Closest open tools sketch or approximate profiles. General STEP feature recognition exists; extrusion metrology for frames does not. Phase 2 is not reinventing a configurator — it is filling the measurement gap.

## Fasteners: the hard error is load-bearing

Nut 5 vs Nut 6 on the same 20×20 outer size share **no** T-nut, bracket, or screw — verified. Mixing families must fail compile.

Biggest naming trap for the README: **Misumi “5 Series” has a 6 mm groove** (M5 bolts). Opposite of item/Motedis “Nut 5” = 5 mm opening. Also: Misumi 1515 ≠ 80/20 1515; “2020” is not one geometry.

## Pain points (README fuel)

Six linked real failures are in `PAINPOINTS.md`. Lead with wrong T-nuts for “series 20 / 2020”, Misumi↔80/20 naming collisions, and panels sized without a real slot neck.

## Monetisation (do not assume commission)

- Motedis: **no** traditional affiliate (confirmed); kit “idea fee” + Efficiency Club only.
- Affiliates found: **80/20**, **OpenBuilds**.
- Vendors funding their own free design tools (Misumi FRAMES, item Engineeringtool, MayCad) are **potential buyers of a white-label configurator**, not commission sources.
- No public price API found among the eleven vendors → cross-vendor priced cut lists need agreements or published machine-readable prices (LEGAL.md already says this).

## Single biggest risk

**A cut list that looks authoritative and is wrong.** Legal exposure on a free tool is mostly capped, but a fused BOM that people order against is the failure mode that scales with usefulness. Mitigations already in the brief — provenance flags, hard fastener errors, refuse cut list on failed interference, no `assumed` values unflagged — are the product, not polish. Second risk: silently treating “derived measurements OK” as settled law when licences mostly say `unclear`; stay conservative and cite.

## Phase 2 go / no-go

**Go.** Reference = Motedis; registry = measurements only; OpenBuilds STEP redistribution is optional later; nothing in the landscape removes the need for the measure-and-re-extrude primitive.

## Three things to build next (ranked, with argument)

1. **`slotcad measure` + registry schema** — without a reproducible slot scan and checksummed record, the rest is a drawing tool. This is the asset strangers will PR into.
2. **Fastener-family hard error + two reference topologies** (frame, box shelf) — catches the expensive mistakes in `PAINPOINTS.md` before anyone cares about nesting.
3. **Interference → no cut list** — the honesty rule that makes the tool trustworthy; nesting and deflection are valuable but secondary to “refuse to emit what you cannot stand behind”.
