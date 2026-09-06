# T-slot fastener compatibility map

Fetch date for all live pages below: **2026-09-06**, unless a PDF’s own publication date is noted.

Every dimensional claim is tied to a URL. Where a figure could not be confirmed from a primary catalogue page, the cell says **unverified**.

Scope: which T-nut / bracket / screw families belong with which slot system, and — more importantly — **which must not be mixed**. The reference pair from the project brief is verified in §3.1.

---

## 1. Slot / nut naming glossary

European vendors often name a system by **groove opening (mm)** (“Nut 5”, “slot 8”, “Line 8”). US fractional vendors name by **outer modular size in tenths of an inch** (“10-series”, “15-series”). Misumi names by **series ≈ preferred bolt size**, which is *not* the same as groove opening in mm. That clash is the single most expensive naming trap in this space.

| Name you will see | What it usually means | Typical outer modular size | Typical groove opening | Typical primary thread | Vendors that use this name |
| --- | --- | --- | --- | --- | --- |
| **Nut 5 / slot 5 / I-Typ Nut 5 / Line 5 / Profiles 5** | European **I-type** family with **5 mm** groove | 20 mm grid (e.g. 20×20) | **5 mm** | M3–M5 in the groove; core often M5 | Motedis (`I-Typ … slot 5` / product no. `… Nut 5`); item **Line 5**; item-compatible “i-Typ Profiles 5” |
| **Nut 6 / slot 6 / B-Typ Nut 6** | European **B-type** family with **6 mm** groove (Bosch-compatible lineage) | 20 mm grid (e.g. 20×20) | **6 mm** | M3–M6 in the groove; core often M6 | Motedis (`B-Typ … slot 6` / product no. `… Nut 6`); Bosch Rexroth **6 mm slot**; many “2020 European / B-type” resellers |
| **I-Typ slot 6 / 30 I-type slot 6** | I-type geometry, **6 mm** groove (not B-type) | 30 mm grid | **6 mm** | typically M3–M6 | Motedis filter “30 I-type slot 6”; item **Line 6** |
| **B-Typ slot 8 / 30 B-type slot 8** | B-type geometry, **8 mm** groove | 30 mm grid | **8 mm** | typically M4–M8 | Motedis filter “30 B-type slot 8”; Bosch Rexroth **8 mm slot** |
| **I-Typ slot 8 / Line 8 / Profiles 8** | I-type / item Line 8, **8 mm** groove | 40 mm grid | **8 mm** | typically M4–M8 | Motedis “40 I-type slot 8”; item **Line 8**; item-compatibles |
| **B-Typ slot 10 / 45 B-type slot 10** | B-type, **10 mm** groove | 45 mm grid (also Bosch 40/45/50/60 with 10 mm) | **10 mm** | typically M5–M8+ | Motedis; Bosch Rexroth **10 mm slot** |
| **O-Typ slot 8** | Motedis “O-type” with square/spring nuts for slot 8 | often 45 mm class | **8 mm** (O geometry) | M5–M8 | Motedis filter “45 O-type slot 8” |
| **item Line 5 / 6 / 8 / 10 / 12** | Line number ≈ **groove width in mm**; modular outer = 20 / 30 / 40 / 50 / 60 mm | as above | 5 / 6 / 8 / 10 / 12 mm | line-matched T-Slot Nuts F etc. | item Industrietechnik |
| **Bosch Rexroth 6 / 8 / 10 mm slot** | Slot opening N; modular R = 20 / 30 / 40 / 45 / 50 / 60 mm | matches R | **6 / 8 / 10 mm** | T-nuts sold per slot width (M4–M8 and UNC) | Bosch Rexroth |
| **Misumi 5 Series (HFS5-…)** | Series ≈ **M5 hardware family**; groove opening is **6 mm**, *not* 5 mm | base 20 (also 25, double-20 40×40) | **6 ± 0.30 mm** | **M5** | Misumi |
| **Misumi 6 Series (HFS6-…)** | Series ≈ M6 family | base 30 | wider than 5-series (exact mm: see Misumi datasheet per SKU) | **M6** | Misumi |
| **Misumi 8 Series / 8-45 Series** | Series ≈ M8 family; 8 and 8-45 **share T-nut slot geometry**, brackets still series-specific | base 40 / 45 | 8-series slot (exact mm: see Misumi datasheet) | **M8** | Misumi |
| **80/20 10-series** | Fractional; outer ~1″ | 1″ grid (1010, 1020, …) | **~0.255–0.26″** (~6.5 mm) | **1/4-20** primary | 80/20 Inc and clones (Parco, Framing Tech, …) |
| **80/20 15-series** | Fractional; outer ~1.5″ | 1.5″ grid (1515, …) | **~0.322–0.32″** (~8.2 mm) | **5/16-18** primary | 80/20 Inc and clones |
| **80/20 metric 20 / 25 / 30 / 40 / 45** | Metric catalogue lines | as named | series-specific (unverified per SKU here) | metric T-nuts | 80/20 Inc |
| **Maytec H-slot / F-slot / E3-slot / E4-slot** | MayTec’s own slot-shape families, keyed by **profile group (PG)** | PG16 / 20 / 30 / 40 / 45 / 50 / 60 | H: width **6.2**, depth **6.2**; F: width **8.2**, depth **6.5**; E3: width **8.2**, depth **11.5**; E4: width **8.2**, depth **12.5** (catalogue table) | fasteners marked H / F / E | MayTec |
| **OpenBuilds V-Slot / C-Beam** | Maker linear-rail extrusion; ~20-series metric with V-guide faces | 20×20, 20×40, 20×60, 20×80, C-Beam 40×80, … | commonly treated as **~6 mm** European-style opening; OpenBuilds M5 tee nuts | **M5** | OpenBuilds |
| **MakerBeam / MakerBeamXL / OpenBeam / MakerBeamXS** | Miniature beams | 10×10 / 15×15 / 15×15 / 5×5 | MakerBeamXL slots **3 mm** wide (FAQ); others: see MakerBeam drawings | **M3** (XS: **M1.2**) | MakerBeam |

### Naming collision to memorise

| Spoken as “five” | Actual groove | Actual bolt bias |
| --- | --- | --- |
| item / Motedis **Nut 5 / Line 5 / I-Typ slot 5** | **5 mm** | M3–M5 |
| Misumi **5 Series** | **6 mm** | **M5** |

Do not order “5-series T-nuts” for an item Line 5 / Motedis I-Typ Nut 5 profile without checking which vendor’s “5” you mean.

---

## 2. Compatibility matrix

Legend:

- **C** = compatible when both the **system geometry** (I / B / O / Maytec H|F|E / fractional / Misumi series) *and* the **slot opening** match the fastener’s stated family
- **N** = not compatible (will not seat, will bind, or will not hold load safely)
- **~** = sometimes physically inserts but **not recommended** (loose, wrong thread, wrong locator tabs, or vendor warns against mixing)
- **U** = unverified from primary sources fetched on 2026-09-06

Rows = slot systems. Columns = fastener families.

| Slot system (profile) ↓ \ Fastener family → | I-Typ / item Line **5** T-nuts & brackets (5 mm) | B-Typ / Bosch **6 mm** T-nuts & brackets | I-Typ / item Line **6** (6 mm I-geometry) | B-Typ / Bosch **8 mm** | I-Typ / item Line **8** (8 mm I-geometry) | B-Typ / Bosch **10 mm** | Misumi **5 Series** (M5, 6 mm groove) | Misumi **8 Series** T-nuts | 80/20 **10-series** (1/4-20) | 80/20 **15-series** (5/16-18) | OpenBuilds **M5** tee nuts | MakerBeam **M3** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Motedis 20×20 I-Typ Nut 5** (5 mm / 6.35 mm deep / M5 core) | **C** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** |
| **Motedis 20×20 B-Typ Nut 6** (6 mm / 5.5 mm deep / M6 core) | **N** | **C** | **~** / **N**† | **N** | **N** | **N** | **~**‡ | **N** | **~** | **N** | **~**‡ | **N** |
| **item Line 5** (20 mm modular, 5 mm groove) | **C** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** |
| **item Line 6** (30 mm modular, 6 mm groove) | **N** | **~** / **N**† | **C** | **N** | **N** | **N** | **U** | **N** | **N** | **N** | **U** | **N** |
| **item Line 8** (40 mm modular, 8 mm groove) | **N** | **N** | **N** | **~** / **N**† | **C** | **N** | **N** | **~**§ | **N** | **~** | **N** | **N** |
| **Bosch Rexroth 6 mm slot (20 mm modular)** | **N** | **C** | **~** / **N**† | **N** | **N** | **N** | **~**‡ | **N** | **~** | **N** | **~**‡ | **N** |
| **Bosch Rexroth 8 mm slot** | **N** | **N** | **N** | **C** | **~** / **N**† | **N** | **N** | **~**§ | **N** | **~** | **N** | **N** |
| **Bosch Rexroth 10 mm slot** | **N** | **N** | **N** | **N** | **N** | **C** | **N** | **N** | **N** | **N** | **N** | **N** |
| **Misumi HFS5-2020 (5 Series, 6 mm groove, M5)** | **N** | **~**‡ | **U** | **N** | **N** | **N** | **C** | **N** | **~** | **N** | **~**‡ | **N** |
| **Misumi HFS8-4040 (8 Series)** | **N** | **N** | **N** | **~**§ | **~**§ | **N** | **N** | **C** | **N** | **~** | **N** | **N** |
| **80/20 10-series (~0.26″ slot)** | **N** | **~** | **N** | **N** | **N** | **N** | **~** | **N** | **C** | **N** | **N** | **N** |
| **80/20 15-series (~0.32″ slot)** | **N** | **N** | **N** | **~** | **~** | **N** | **N** | **~** | **N** | **C** | **N** | **N** |
| **OpenBuilds V-Slot / C-Beam (M5 ecosystem)** | **N** | **~**‡ | **U** | **N** | **N** | **N** | **~**‡ | **N** | **N** | **N** | **C** | **N** |
| **MakerBeam / XL / OpenBeam** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **N** | **C** |
| **Maytec H-slot (PG20)** | **N** | **U** | **U** | **N** | **N** | **N** | **U** | **N** | **N** | **N** | **U** | **N** |
| **Maytec F-slot (PG20/30)** | **N** | **N** | **N** | **U** | **U** | **N** | **N** | **U** | **N** | **U** | **N** | **N** |
| **Maytec E3/E4-slot (PG40+)** | **N** | **N** | **N** | **U** | **U** | **U** | **N** | **U** | **N** | **U** | **N** | **N** |

Notes on the matrix:

- **†** Same *nominal* opening (e.g. both “slot 6” or both “slot 8”) but **I-type vs B-type groove geometry / chamfers differ**. Motedis: accessories must match *both* system type and slot width; mixing “is possible, but you have to know what you are doing” and is not recommended for beginners. Treat as **do not mix** unless you have measured both solids.
- **‡** OpenBuilds / many “2020” M5 drop-ins and Misumi 5-series share a ~6 mm opening with B-type 20×20, so a hammer nut *may* drop in. Slot depth, lip shape, and V-chamfers differ; brackets with 6 mm locator tabs or V-wheel clearances are not universal. Treat structural joints as **unverified** until measured.
- **§** Third-party sellers market “15 / 40 series” or “8 mm” drop-ins that claim to span 80/20 15-series and metric 40/8. Thread (5/16-18 vs M8) and outer modular size (1.5″ vs 40 mm) still disagree. Do not assume bracket hole patterns transfer.

Motedis’s own T-nut shop filter is the ground truth for their catalogue — families are listed as separate slot sizes, not as one interchangeable bin:

`20 I-type slot 5` · `30 I-type slot 6` · `40 I-type slot 8` · `20 B-type slot 6` · `30 B-type slot 8` · `45 B-type slot 10` · `45 O-type slot 8`

---

## 3. Hard incompatibilities (“do not mix X with Y”)

### 3.1 Critical pair — verified

**Do not mix Motedis `20x20 I-Typ Nut 5` with Motedis `20x20 B-Typ Nut 6`.**

| | **20×20 I-Typ Nut 5** | **20×20 B-Typ Nut 6** |
| --- | --- | --- |
| Product no. | `20x20 I-Typ Nut 5` | `20x20 B-Typ Nut 6` |
| System type | I-type | B-type |
| Groove width | **5 mm** | **6 mm** |
| Groove depth | **6.35 mm** | **5.5 mm** |
| Core / end thread | **M5** | **M6** |
| Matching T-nuts (examples) | “T-nut … I-Type slot 5 [M3/M4/M5]” | “T-nut B-type slot 6 [M3/M4/M5/M6]”, spring-steel Nut 6, threaded plates B-Type slot 6 |
| Matching end machining | M5 counterbore options | M6 counterbore / D9 SSV options |

**Why nothing is shared:**

1. **Neck width** — a 6 mm hammer / T-nut body will not pass a 5 mm opening; a 5 mm nut is loose or wrong-shaped in a 6 mm B-type cavity.
2. **T-nut / slot geometry** — I-type vs B-type differ in cross-section, lips, and chamfers even when the nominal opening number coincides on larger sizes; on 20×20 the opening numbers also differ (5 vs 6).
3. **Thread** — end taps and many connectors assume **M5** (I-Typ 20) vs **M6** (B-Typ 20). Screws are not interchangeable at the core.

Sources: Motedis product pages and accessories guide (URLs in §5).

### 3.2 Same opening number, different system type

**Do not mix I-type slot 8 accessories with B-type slot 8 accessories** (and likewise I-type slot 6 with B-type slot 6), even though both say “8” or “6”.

- Why: slot *shape* (lips, chamfers, depth) differs by system type; T-nuts and connectors are tooled for one geometry.
- Vendor rule (Motedis): match **system type and slot width**.
- MaunSystem (item-compatible reseller): I-type ↔ item; B-type ↔ Bosch-compatible — different catalogue trees.

### 3.3 Misumi “5 Series” ≠ European Nut 5

**Do not mix Misumi 5 Series hardware with item Line 5 / Motedis I-Typ Nut 5.**

- Misumi HFS5-2020: groove **6 ± 0.30 mm**, for **M5** bolts.
- item / Motedis Nut 5: groove **5 mm**.
- Why: neck width and T-nut planform disagree; the shared word “5” refers to different quantities (bolt series vs millimetres of opening).

### 3.4 Same outer 40×40, different Misumi series

**Do not mix Misumi HFS5-4040 hardware with HFS8-4040 hardware.**

- Both are 40×40 mm outside.
- HFS5-4040 = double base-20, **two** slots per face, **M5** / 5-series.
- HFS8-4040 = single base-40, **one** slot per face, **M8** / 8-series.
- Why: slot count, slot geometry, and thread all differ. Misumi: “Grabbing the wrong series hardware is one of the more common assembly mistakes.”

Exception inside Misumi: **8 Series and 8-45 Series share T-nut slot geometry**; brackets remain series-specific — do not swap brackets between 8 and 8-45.

### 3.5 Fractional 10-series vs 15-series

**Do not mix 80/20 10-series T-nuts/screws with 15-series slots (or the reverse).**

- 10-series slot ~**0.255–0.26″**, primary fasteners **1/4-20**.
- 15-series slot ~**0.322–0.32″**, primary fasteners **5/16-18**.
- Why: neck width and thread disagree; anchor/end fasteners are machined to one series.

### 3.6 Fractional 15-series vs metric 40-series

**Do not treat 80/20 15-series (1.5″ ≈ 38.1 mm) as interchangeable with metric 40×40 slot-8.**

- Outer size is close enough to fool a ruler glance; slot (~0.322″ vs 8 mm) and threads (5/16-18 vs M8) are not the same.
- Some aftermarket drop-in T-nuts are marketed for “15 / 40”; that does **not** make brackets, end fasteners, or hole patterns compatible.

### 3.7 MakerBeam vs everything 20 mm

**Do not mix MakerBeam / MakerBeamXL / OpenBeam (M3, 10×10 or 15×15) with 20×20 European or OpenBuilds M5 ecosystems.**

- Why: outer size, slot width (~3 mm on XL), and thread (M3 / M1.2) are a different scale. MakerBeam FAQ: they do not sell larger than 15×15.

### 3.8 MayTec slot letters vs B/I numbers

**Do not assume MayTec H / F / E fasteners match a Motedis/item/Bosch “slot 6/8/10” of the same millimetre width.**

- MayTec publishes its own widths (H 6.2, F/E 8.2) and depths, and marks accessories with PG + slot-type symbols.
- Cross-vendor fit: **unverified** without measuring both solids.

### 3.9 Bosch slot widths among themselves

**Do not mix Bosch 6 mm, 8 mm, and 10 mm T-nuts across slot sizes.**

- Bosch catalogues T-nuts explicitly by slot (e.g. 6 mm M4 part 3 842 523 135; 8 mm M6 3 842 501 753; 10 mm M8 3 842 530 287).
- Profiles within one Bosch “profile range” share slot dimensions; accessories are sold per slot width.

---

## 4. Lookalikes that cause expensive mistakes

| Lookalike pair | Same at a glance | Actually different | Typical failure |
| --- | --- | --- | --- |
| **20×20 I-Typ Nut 5** vs **20×20 B-Typ Nut 6** | Outer 20×20 bar | 5 vs 6 mm opening; 6.35 vs 5.5 mm depth; M5 vs M6 core; I vs B geometry | Entire bag of T-nuts / brackets / end screws wrong; corner brackets with 6 mm tabs will not enter Nut 5 |
| **item/Motedis “5”** vs **Misumi “5 Series”** | The digit 5 | 5 mm groove vs 6 mm groove; different T-nut planform | Ordered “5-series nuts” for the wrong continent’s standard |
| **Misumi HFS5-4040** vs **HFS8-4040** | Both 40×40 mm | Dual 20-grid M5 slots vs single 40-grid M8 slot | Brackets and T-nuts from the other series will not seat; BOM looks “correct” by outer size |
| **80/20 1515** vs **metric 4040** | ~1.5″ vs 40 mm (~1.57″) | Slot 0.32″ vs 8 mm; 5/16-18 vs M8; centreline 0.75″ vs 20 mm | Plates almost line up, joints crush or leave a gap |
| **80/20 1010** vs **metric 2020 B-type** | ~1″ vs 20 mm | Slot ~0.26″ vs 6 mm; 1/4-20 vs M5/M6 | Nuts rattle or will not enter |
| **OpenBuilds V-Slot 2020** vs **B-Typ 20×20** | Both ~20 mm, ~6 mm opening, M5 common | V-chamfers for wheels; different face for MGN rails; depth/lip details | T-nuts often work; V-wheels need V-Slot; flat MGN shoes prefer non-V B-type |
| **I-type slot 8** vs **B-type slot 8** | Both “slot 8” on a 40-ish bar | Groove geometry / accessory tooling | Nut wedges, anti-rotation flats miss, ESD ridges scrape wrong faces |
| **MakerBeamXL 15×15** vs **Misumi / European 15 mm** | 15 mm outer | MakerBeam is M3 / ~3 mm slot ecosystem | Standard 15 mm European T-nuts will not fit |
| **MayTec PG40 E-slot** vs **item Line 8 / Bosch 8 mm** | ~40 mm, ~8 mm class opening | MayTec E3 depth 11.5 / wall 3.0 vs other vendors’ slot packs | MayTec H/F/E nuts and connectors are a separate kit |

Community-facing symptom (secondary source, useful as failure mode illustration): on I-type 5 mm 20×20, “standard hammer head T-nuts won’t fit due to 6 mm width” and cast brackets with 6 mm locator tabs need grinding — i.e. people bought B-type hardware for I-type bar.

---

## 5. Sources (URL + fetch date)

Primary vendor / catalogue pages preferred. Secondary pages marked as such.

| # | Source | URL | Fetched / dated | Used for |
| --- | --- | --- | --- | --- |
| 1 | Motedis — B-Type vs I-Type guide | https://www.motedis.com/en/blog/aluminium-profiles-guide | 2026-09-06 | Naming grammar; must match system type **and** slot width; mixing not recommended |
| 2 | Motedis — Profile 20×20 I-Typ slot 5 | https://www.motedis.com/en/Aluminium-Profile-20x20-I-Typ-slot-5 | 2026-09-06 | 5 mm width, 6.35 mm depth, M5 core; art. no. `20x20 I-Typ Nut 5` |
| 3 | Motedis — Profile 20×20 B-Type slot 6 | https://www.motedis.nl/en/Profile-20x20-B-type-slot-6 | 2026-09-06 | 6 mm width, 5.5 mm depth, M6 core; art. no. `20x20 B-Typ Nut 6` |
| 4 | Motedis — In-the-slot T-nuts catalogue filters | https://www.motedis.com/en/In-the-slot-T-nut-guidedslotted-block-flange-nut-and-more | 2026-09-06 | Separate filters: 20 I-5, 30 I-6, 40 I-8, 20 B-6, 30 B-8, 45 B-10, 45 O-8 |
| 5 | Motedis — T-nut I-Type slot 5 M5 | https://www.motedis.com/en/T-nut-with-spring-ball-with-guidance-I-Type-slot-5-M5 | 2026-09-06 | Explicit I-Type slot 5 / M5 nut SKU |
| 6 | item — Aluminium profiles / Lines 5–12 | https://www.item24.com/en-de/theme-world/building-kit-system/aluminium-profiles | 2026-09-06 | Lines 5/6/8/10/12; modular 20/30/40/50/60; groove grows with line |
| 7 | item — T-Slot Nut F (Line 6 / 8) | https://www.item24.com/en-us/t-slot-nut-f-6-st-m6-bright-zinc-plated-61321 | 2026-09-06 | Line-specific nut widths (e.g. Line 6 width 10.6 mm; Line 8 width 13.3 mm) |
| 8 | MaunSystem — item-compatible i-Typ size guide | https://www.maunsystem.de/en/item-compatible-profiles/ | 2026-09-06 | Groove 5/6/8/10/12 mm ↔ series; I-type = item; B-type = Bosch-compatible category |
| 9 | Bosch Rexroth — Basic Mechanic Elements catalogue (mirror) | https://esd.equipment/dokumente/bosch-rexroth/katalog/catalog-basic-mechanic-elements-en.pdf | 2026-09-06 (PDF undated in fetch) | Slot N = 6/8/10 mm; modular R; 20×20 listed under 6 mm slot |
| 10 | Bosch Rexroth — Fasteners / T-nuts datasheet (distributor PDF) | https://files.valinonline.com/userfiles/documents/bosch-rexroth-fasteners-10mm-m8-t-nut.pdf | 2026-09-06 (PDF labelled 12/09) | T-nuts sold per 6/8/10 mm slot with part numbers and torques |
| 11 | Misumi USA blog — series & hardware | https://blog.misumiusa.com/aluminum-extrusion-profiles-shapes-types-series-best-practices/ | 2026-09-06 (page dated May 19, 2026) | Series = slot/hardware family; HFS5-4040 vs HFS8-4040; 8 vs 8-45 T-nut exception |
| 12 | Misumi Thailand — HFS5-2020 | https://th.misumi-ec.com/en/vona2/detail/110302683830/?HissuCode=HFS5-2020-%5B50-4000%2F0.5%5D%2F | 2026-09-06 | **5 Series groove width 6 ± 0.30 mm**, for M5 bolts |
| 13 | Misumi Japan — 5 Series overview | https://jp.misumi-ec.com/special/alumiframe/selection/lineup/size/5series/ | 2026-09-06 | 溝幅6mm; depth 6 mm; T-groove 12 mm; M5 |
| 14 | 80/20 intro ebook (Knotts / HubSpot) | https://cdn2.hubspot.net/hub/13219/file-1339828543-pdf/eBooks/8020_e_book_final.pdf | 2026-09-06 | 10-series vs 15-series outer sizes; 15-series example uses 5/16-18 fasteners |
| 15 | Parco fractional catalogue (distributor) | https://www.parco-inc.com/wp-content/uploads/Parco-Fractional-March-2015.pdf | 2026-09-06 (PDF March 2015) | 10-series slot **0.255″**; 15-series slot **0.322″** |
| 16 | Framing Tech — T-slot compatibility colour key | https://www.framingtech.com/t-slot-compatibility | 2026-09-06 (WebFetch timed out; title/snippet from search — treat detailed colour map as **partially verified** via search snippet: 10-series 0.26″, 15-series 0.32″, 20-05 = 5 mm, 20-series = 6 mm, etc.) | Fractional vs metric series map |
| 17 | MayTec — The Profile System 1/2018 GB | https://www.maytec.de/wp-content/uploads/2024/03/The_Profile_System_1_2018_GB_V02.pdf | 2026-09-06 (catalogue 1/2018) | PG + H/F/E3/E4 slot dimensions table (§1.02) |
| 18 | MakerBeam FAQ | https://www.makerbeam.com/service/ | 2026-09-06 | 10×10 / 15×15 / 5×5; M3 / M1.2; XL slot 3 mm |
| 19 | OpenBuilds — Tee Nuts M5 (search/cache) | https://us.openbuilds.com/tee-nuts-m5-pack/ | 2026-09-06 (live fetch 500; content from search index) | M5 tee nuts for V-Slot / C-Beam |
| 20 | Secondary — 20×20 profile comparison | https://designfor3d.co.uk/index.php/design-for-3d-printing/7-battle-of-the-profiles-comparison-20x20-profiles | 2026-09-06 | Failure modes: 6 mm hammer nuts on I-type 5; Misumi 5-series has 6 mm groove; V-Slot ≈ B-type for many accessories |
| 21 | Secondary — TNUTZ DB-015 “15 / 40 Series” drop-in | https://www.tnutz.com/product/db-015/ | 2026-09-06 | Aftermarket claim of 15-series **and** 40-series / 8 mm fit (illustrates lookalike marketing; not a licence to mix brackets) |

---

## 6. Working rules for `slotcad`

1. Key every profile and every fastener by the tuple  
   `(vendor_family, system_geometry, slot_opening_mm_or_in, preferred_thread)`  
   — never by outer size alone, and never by a lone digit “5/6/8”.
2. Refuse BOM lines that pair I-Typ Nut 5 bar with any B-Typ / Bosch-6 / Misumi-5 / OpenBuilds-M5 fastener (and the reverse).
3. Treat “compatible if opening matches” as **false** when system geometry differs (I vs B vs O vs Maytec H/F/E vs fractional).
4. When only a catalogue number is known, resolve it through the glossary in §1 before emitting a cut list or fastener count.
5. Anything not backed by a URL above stays **unverified** — measure the vendor STEP before asserting fit.

---

*End of FASTENERS.md — research pass 2026-09-06.*
