# slotcad — seed

Not built yet. Working directory for an external coding agent.

| | File | Output |
|---|---|---|
| Phase 1 | `PROMPT-1-research.md` | `research/` — VENDORS.md, vendors.json, FASTENERS.md, LANDSCAPE.md, PAINPOINTS.md, RECOMMENDATION.md |
| Phase 2 | `PROMPT-2-build.md` | the library, the registry, two reference topologies |

## What it is

Take the **vendor's own CAD solid** of an aluminium T-slot extrusion, measure what the profile really
is, then compile a declared *topology* — posts, rails, panels — into a solid, a cut list, panel sizes,
fastener counts, an interference check and a deflection estimate. All from one source of truth, so the
bill of materials cannot drift from the geometry.

The proof it rests on, measured off a real 20x20 "Nut 6" profile: the slot is a **6.20 mm neck about
1 mm long**. A nominal 6 mm sheet at the top of its tolerance band jams partway down a 760 mm slide.
No catalogue tells you that, and it is the difference between a shelf and a pile of expensive parts.

## Where it comes from

`personal/robot` (20x20 I-Typ Nut 5) and `personal/shelf` (20x20 B-Typ Nut 6). Their `profile.py`
files are near-identical — same trick, different vendor file — and each hand-rolls its own
topology-to-BOM. That duplication is the argument for this repo.

**No vendor STEP file gets committed.** What ships is the measurements derived from them, in
`registry/`, one JSON per profile with source URL and checksum. Derived facts are ours; the vendor's
artefact is not. Same line as the other two briefs — and here it is what makes the registry, rather
than the geometry code, the thing worth finding.

Background and the other briefs: `~/projects/personal/grok/README.md`.
