# PHASE 2 — build `slotcad`

Read `research/RECOMMENDATION.md` and `research/vendors.json` first. **Do not commit any vendor STEP
file unless its licence plainly permits redistribution.** Default assumption: it does not.

## 1. The idea in one paragraph

Everyone building with aluminium extrusion fights the same three problems: the catalogue number is not
the real dimension, the bill of materials drifts from the design the moment anything changes, and
parts that look fine in a drawing collide in reality. `slotcad` fixes all three from one source of
truth — **the vendor's own solid** — and compiles a topology, not a drawing.

## 2. Truth comes from the vendor's solid, never from a datasheet

The core primitive: import the vendor's STEP, take the largest planar face at the bar's end as its
true cross-section, and re-extrude that wire to any length. Manufacturer-exact slot chamfers, core
bore and fillets come along for free — **no profile generator reproduces those**, and they are exactly
what determines whether a panel fits.

From that solid, measure and record: cross-sectional area, mass per metre, second moment of area about
both axes, and a **slot scan by depth from the outer face**. The slot scan is the thing nobody else
has. Measured on one real 20x20 "Nut 6" profile:

```
 0.0 – 0.5 mm     7.31 mm   chamfered entry
 0.5 – 1.5 mm     6.20 mm   the neck — the only part that grips a panel
 1.5 – 5.25 mm   ~12.0 mm   T-nut chamber; a panel just floats here
 5.5 mm                     bottom
```

So "Nut 6" is a **6.20 mm neck roughly 1 mm long**. A panel must be ≤ 5.9 mm, and a nominal 6 mm sheet
at the top of its tolerance band jams partway down a 760 mm slide. 5 mm acrylic goes in freely with
about 1.2 mm of play. No catalogue tells you any of that, and it is the difference between a shelf and
a pile of expensive parts. Reproduce this measurement on your reference profile and put it in the
README — it is the proof the whole project rests on.

**Two more measured values that are deliberately not the obvious ones**, both of which must be
returned by the library rather than left to the user:

- **Effective density, not aluminium's density.** A T-slot profile is mostly air: one measured profile
  came out at 0.4912 kg/m, an effective 1228 kg/m³ against solid aluminium's 2700. Using 2700 made a
  simulated mast 2.2× too heavy and destroyed the centre-of-gravity result. Any mass or inertia the
  library reports comes from the measured section, never from a nominal density.
- **The real second moment of area**, measured from the section, for deflection. Two profiles of the
  same nominal size differ here.

## 3. The profile registry — the part that becomes valuable

Because vendor STEP files probably cannot be redistributed, but **measurements derived from them can**,
the repo's durable asset is a registry: one JSON record per vendor profile, holding the measured area,
mass per metre, second moments, the full slot scan, the fastener family, and — so it is reproducible —
the source URL and a checksum of the STEP it was measured from.

```
registry/motedis/20x20-b-typ-nut-6.json
registry/motedis/20x20-i-typ-nut-5.json
```

A user with the vendor file regenerates a record and gets a byte-identical result; a user without it
still gets correct dimensions, deflection and panel sizing. `slotcad measure <step> --emit` produces a
record, and contributing one is the obvious first pull request. Design the schema and the contribution
path deliberately: this registry, not the geometry code, is what makes the project worth finding.

## 4. Topology in, everything out — together

The user declares a topology, never coordinates. Two reference topologies ship with the library, both
taken from real builds:

- **Frame** — two uprights plus rungs. A flat mast; the rungs sit *between* the uprights, so their
  length is the frame width minus both profile faces. Getting that subtraction wrong is the classic
  first error.
- **Box shelf** — four corner posts, and per level a closed rectangle of four rails, with a panel
  dropped into the inward-facing slots.

From one topology declaration, emit **in a single pass**: the solid (STEP and STL), the cut list, the
panel sizes with real clearance, bracket and fastener counts by type, the interference report, the
deflection estimate per loaded span, and the stock-nesting plan. They come from the same object, so
the bill of materials **cannot** drift from the geometry — that is the property to protect in tests,
not a convenience.

## 5. The checks that earn the tool its place

**Interference must be a real solid intersection**, not a bounding-box guess. In our two builds it
caught two things no amount of care would have:

- A rail buried inside a foot — invisible to the mass arithmetic, obvious to a boolean.
- Panel corners hitting the posts: a rectangle engaging all four slots overlaps each post by 5 × 5 mm.
  So either notch all four corners or hold the panel front-and-back only. The library must report the
  choice and its cost — measured, the notches bought only 0.80 → 0.65 mm of sag, which is not worth
  the work at that size. **Report the trade-off with its numbers; do not silently pick.**

**Fastener-family incompatibility is a hard error, not a warning.** 20x20 I-Typ Nut 5 and 20x20 B-Typ
Nut 6 are the same nominal size and share no T-nut, no bracket and no screw. A build mixing families
must fail to compile. This is the single most common expensive mistake in the hobby and it is
statically checkable, so check it.

**Assembly order is a result, not a note.** A closed rectangle cannot be retrofitted with a panel —
the panel goes in before the last rail. If the topology implies an order, emit it.

**Nesting against real stock.** Stock bars come in fixed lengths (one vendor's longest is 1980 mm) and
there is a minimum cut length (50 mm). Plain first-fit-decreasing pairs the long pieces and strands the
short ones into an extra bar; interleaving one of each length fits the same parts into four bars
instead of five. Report both the nested plan and the cut-to-length plan, and say plainly that if the
vendor cuts to length the nesting is irrelevant — **the honest answer is often "you do not need this
feature".**

## 6. Honesty rules

1. **Every dimension states its provenance**: `measured` (from the vendor solid), `vendor` (from a
   published table), or `assumed` (a default nobody checked). Print it in the BOM. Our own builds carry
   a shouting header saying every dimension is a placeholder until someone reaches for a caliper —
   keep that discipline, because a bill of materials that looks authoritative and is not will get
   ordered.
2. **Defaults are assumed, and say so.** Ship sensible defaults, mark them `assumed`, and never let an
   `assumed` value reach a cut list without a visible flag.
3. **A tolerance band is part of a dimension.** Panel fit is the worked example: a nominal 6 mm sheet
   is not 6 mm. Where a clearance matters, report the band, not the midpoint.
4. **No number without its units and its source** in any emitted artefact.
5. Refuse to emit an order-ready cut list when an interference check fails or a fastener family is
   mixed. A missing cut list is cheaper than a wrong delivery.

## 7. Scope

**In scope for v1:** the measure-and-re-extrude primitive; the profile registry with at least the two
reference profiles; the two reference topologies; cut list, panel sizes, fastener counts, interference,
deflection, nesting; a CLI; an HTML build sheet.

**Out of scope, in the README:** no GUI, no web configurator, no simulation, no motion, no
vendor-specific ordering integration, no attempt to model every bracket ever made. Support the
fastener families the reference builds use and let the registry grow by contribution.

**Anti-goals:** no Docker, no framework, no build step, no account, no telemetry. A stranger clones,
runs one command, and gets an orderable cut list for a shelf.

**Open core:** free is the library, the CLI and the registry.

The commercial seam — build toward it, do not build it — is **not affiliate revenue.** Checked
2026-09-06: Motedis runs no partner or affiliate programme; its site offers a CAD database, a
"Gebaut mit Motedis" showcase, and a business-and-volume account request, but no referral scheme, and
no public programme surfaced for Misumi, item or 80/20 either. Assume there is no commission to earn
and design accordingly.

What the market does show is the opposite flow: **vendors fund configurators themselves** to drive
part sales — Misumi gives away its FRAMES extrusion-design software free. So the three plausible
seams, in order of how well they fit a small software project:

1. **Sell the configurator to a vendor.** A vendor with a CAD database but no configurator is a
   customer, not a commission source. This is the strongest and it is why the vendor layer must be a
   clean interface: a white-label build for one vendor should be a configuration, never a fork.
2. **Priced cut lists across vendors, hosted.** Useful to buyers, neutral between sellers, and it
   works without anyone's permission.
3. **A trade account and resold kits.** Real, but it is a physical-goods business with inventory and
   shipping — a different company, not an extension of this one.

Verify all of that in phase 1 rather than trusting it; programmes appear and disappear. Keep geometry,
BOM emission and pricing behind clean interfaces so any of the three is an addition, not a fork.

## 8. House conventions

Python, `uv run python -m <module>`, Makefile as the source of truth. CadQuery is the one heavy
dependency and it is justified by the STEP work — justify anything else in a line. Self-contained HTML
build sheets: f-strings, `html.escape`, inline CSS, no Jinja. English throughout. Tests are real: a
committed profile *record* (not the vendor STEP) plus golden cut lists, so a geometry regression shows
up as a diff in a bill of materials rather than as a silent change in a solid.

## 9. Definition of done

1. `slotcad measure <vendor.step> --emit` writes a registry record with area, mass per metre, both
   second moments and the full slot scan, and re-running it reproduces the file byte for byte.
2. `slotcad build shelf --width 800 --depth 300 --height 900 --levels 2` emits solid, cut list, panel
   sizes, fastener counts, interference report, deflection and nesting in one pass.
3. Changing one parameter changes the cut list — with a test that asserts it, because "the BOM cannot
   drift" is the central claim and untested claims rot.
4. A topology that mixes Nut 5 and Nut 6 fasteners fails to compile, with a message naming both.
5. A deliberately overlapping topology produces a failed interference report and **no** cut list.
6. `make sheet` produces a self-contained HTML build sheet with every dimension carrying `measured` /
   `vendor` / `assumed`.
7. The README opens with the slot scan of a real profile and the sentence it proves: the catalogue
   number is not the dimension that holds your panel.
8. No vendor STEP file is committed unless phase 1 cleared it; `registry/` records carry source URL and
   checksum so anyone can reproduce them.

## 10. What to report back

The slot scan you measured and how it compared to the vendor's published figure. Which vendors' CAD
terms permit what. Whether any existing tool already derives geometry from the vendor solid. The two
reference builds' cut lists. Every departure from this brief and why. And the three things you would
build next, ranked, with the argument rather than a list.
