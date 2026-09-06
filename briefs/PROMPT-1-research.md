# PHASE 1 — the landscape, and what may be redistributed

Research pass, no code. One report plus `vendors.json`. Everything carries a URL and a fetch date;
write `unverified` rather than guessing.

## What is being built

A library that takes a **vendor's own CAD solid** of an aluminium T-slot extrusion, measures what the
profile actually is, and compiles a declared *topology* — posts, rails, panels — into a solid, a cut
list, panel sizes, fastener counts, an interference check and a deflection estimate, all from the same
source of truth so the bill of materials cannot drift from the geometry.

## The survey

**Vendors and their CAD.** For each of Motedis, item, Bosch Rexroth, Misumi, 80/20, Maytec,
Alutec/Alutec KK, MakerBeam, OpenBuilds, and anyone else you find that matters in Europe or the US:

1. Does it publish downloadable STEP or other solid CAD for its profiles? At what URL, and does it
   require an account?
2. **What do the terms of use say about redistribution and about derived works?** Quote and link
   them. This is the question the whole phase exists for.
3. Which profile families and slot sizes does it sell, and what naming does it use — "Nut 6",
   "slot 8", "1515 series", "20x20 B-Typ" and so on? Build the cross-vendor naming map, because the
   naming is genuinely confusing and a map of it is useful on its own.
4. Stock bar lengths, minimum cut length, cut tolerance, and whether cut-to-length is offered.

**Fastener systems.** Which T-nut, bracket and screw families go with which slot, and — the question
that matters — **which are interchangeable and which absolutely are not**. Our two builds are 20x20
I-Typ Nut 5 and 20x20 B-Typ Nut 6: same nominal size, no shared fastener at all. Map that properly.

**What already exists.** Vendor configurators (80/20's, Misumi's, item's), open-source extrusion
libraries and CAD generators, FreeCAD and Fusion add-ins, parametric-furniture projects. For each:
what it does, whether it derives geometry from the vendor's own solid or regenerates an approximation,
whether it emits a bill of materials, whether it checks interference, and its licence. **Look hard for
anything that measures the real slot rather than trusting a catalogue number** — we believe nothing
does, and being wrong about that is worth knowing on day one rather than after the build.

**Monetisation, since we may not assume it.** For each vendor: is there an affiliate or referral
programme, a reseller or trade account, a public price API, or a cart-prefill / quote endpoint a tool
could hand a cut list to? Our own check on 2026-09-06 found **no** affiliate programme at Motedis —
only a business-and-volume account request — and none surfaced for the others. Confirm or correct
that, and note who publishes prices in a machine-readable form at all, because that decides whether a
cross-vendor priced cut list is even possible. Also note which vendors already give away design
software (Misumi's FRAMES, for one) — a vendor funding its own configurator is a potential buyer, not
a commission source.

**Community.** Where do people building with extrusion actually ask questions — forums, subreddits,
Discords? What do they get wrong repeatedly? Collect five real, linked examples of someone ordering
the wrong T-nut, mis-sizing a panel, or having a bar arrive too short. Those are the failure modes
the library exists to prevent, and they belong in the README as the reason it exists.

## Deliverables

Into `research/`, or in full if you have no working tree:

1. `VENDORS.md` + `vendors.json` — per vendor: CAD availability, URL, account required, **licence
   verdict** (`may_redistribute_step: true|false|unclear`) with quoted terms, profile families, slot
   naming, stock lengths, minimum cut.
2. `FASTENERS.md` — the compatibility map, stated as what may *not* be mixed.
3. `LANDSCAPE.md` — existing tools, ranked by how close they come to this.
4. `PAINPOINTS.md` — the five linked real-world failures.
5. `RECOMMENDATION.md` — one page: which vendor to build the reference implementation against, whether
   any STEP may be redistributed, and the single biggest risk.
