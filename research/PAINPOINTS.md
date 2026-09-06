# Pain points — why slotcad exists

Fetch date: **2026-09-06**.

Builders keep losing money and weekends to the same four mistakes: ordering T-nuts by a marketing label (“2020”, “series 20”) instead of slot geometry; cutting or ordering panels without measuring the real neck of the slot; trusting cut-to-length without honest tolerances; and mixing same-nominal fastener families that do not share a slot. These are the failure modes the library is built to catch before an order goes out.

Every example below is a real, linked thread (forum / Stack Exchange / vendor-adjacent Q&A). Quotes are paraphrased tightly from the OP or accepted replies. Dead or bot-gated mirrors are noted; replacements or Wayback snapshots are given where needed.

---

## Cases (6)

### 1. Amazon “series 20” T-nuts jammed in 80/20 Series 20 (5.26 mm opening)

- **One-line failure:** Ordered generic 6 mm-slot T-nuts for 80/20 Series 20; opening was 5.26 mm — nuts would not go in without grinding.
- **Link + fetch date:** https://builds.openbuilds.com/threads/watch-out-for-this-detail-when-buying-extrusion-from-certain-suppliers.14970/ (fetched 2026-09-06). Live page is indexed; this research box could not resolve `builds.openbuilds.com` DNS — content verified via Wayback snapshot http://web.archive.org/web/20260208092354/https://builds.openbuilds.com/threads/watch-out-for-this-detail-when-buying-extrusion-from-certain-suppliers.14970/ (status 200).
- **What went wrong:** First-time buyer from an 80/20.net distributor measured a **5.26 mm** slot opening, then bought “a ton” of Amazon T-nuts labeled for series 20 / 2020. Those nuts are made for a **6 mm** opening. Fit was extremely tight; drop-ins and roll-ins would not seat; cast brackets needed a grinder. Listings rarely say “not for 5.25 mm opening.”
- **slotcad check:** **Fastener family hard error** (and interference / slot-scan neck check) — refuse to pair a 6 mm T-nut family with a profile whose measured opening/neck is ~5.26 mm.

### 2. “2020” is not one slot — standard M5 T-nuts may not fit the extrusion you can buy locally

- **One-line failure:** Wilson II build called for 2020 extrusion; local Bangkok stock had a markedly different slot profile, so catalog T-nuts were not a safe assumption.
- **Link + fetch date:** https://engineering.stackexchange.com/questions/13471/will-standard-m5-t-slot-nuts-fit-these-different-2020-aluminium-extrusions (fetched 2026-09-06; live).
- **What went wrong:** OP compared several “2020” cross-sections (recommended V-slot style vs local square-slot stock). Slot geometry differed enough that they asked whether full- and half-size M5 T-nuts would still fit. Update: on the Bangkok profile, only ordinary hexagonal M5 nuts would go in — not the assumed T-nuts.
- **slotcad check:** **Fastener family hard error** keyed to measured slot scan, not the word “2020”.

### 3. Metric 20-2020 shipped where fractional 1010 hardware was expected — sliders will not fit

- **One-line failure:** FIRST team ordered “20/20” from 80/20; channel came ~0.5 mm small vs prior stock; existing sliders would not fit and no matching sliders existed.
- **Link + fetch date:** https://www.chiefdelphi.com/t/problems-with-20-20/141101 (fetched 2026-09-06; live).
- **What went wrong:** Shipment labeled like prior years, but outer and inner channel measured ~0.5 mm undersize vs the team’s sliders. Replies pointed at **metric 20-2020 vs fractional 1010** (and similar same-nominal families): the company said “20 series should work,” but the slot families are not interchangeable. OP: “They don’t make any [sliders] for the channel we got.”
- **slotcad check:** **Mixing incompatible fastener families** → hard error (metric vs fractional / series mismatch on same-nominal “2020”).

### 4. Misumi “1515” treated as 80/20 “1515” — buttons drag or pull out

- **One-line failure:** Bought Misumi 1515 / 3030 expecting 80/20-compatible rail buttons; slots were too narrow or too wide — hardware from the other naming family failed.
- **Link + fetch date:** https://www.rocketryforum.com/threads/misumi-rail-xxxxx.64397/ (fetched 2026-09-06; live).
- **What went wrong:** OP: Misumi 1515 slot “too narrow and too thin” (button and screw head drag); Misumi 3030 “too wide” (button can be pulled out through the face). Reply clarifies the naming collision: Misumi 1515 = **15 mm** square; 80/20 1515 = **1.5 in** square. Misumi 1515 entrance ~3.4 mm / inner ~5.7 mm — not the fractional ecosystem’s hardware.
- **slotcad check:** **Fastener family hard error** / do-not-mix map (same catalog nickname, different slot family).

### 5. Cut-to-length V-slot arrived as two different lengths

- **One-line failure:** Ordered two pieces of 20×60×500 V-slot cut to length for a build; the two bars arrived different lengths — buyer had no accurate way to recut.
- **Link + fetch date:** https://builds.openbuilds.com/threads/innacurate-lengths-sent.11519/ (fetched 2026-09-06). Same DNS issue as case 1; content verified via Wayback http://web.archive.org/web/20251114094718/https://builds.openbuilds.com/threads/innacurate-lengths-sent.11519/ (status 200).
- **What went wrong:** “I ordered 2 pieces of 20x60x500 vslot. i recieved two different lengths… I dont have a way to cut this accurately which is why i ordered it in the proper length.” Classic cut-list / supplier-tolerance failure when the BOM pretends lengths are exact.
- **slotcad check:** **Cut list honesty** — emit length + tolerance provenance; never present assumed-exact cuts as guaranteed stock.

### 6. Shop-cut bars out of square and mismatched by 0.5–1 mm

- **One-line failure:** Extrusion taken to a local miter shop; ends not square and lengths differed by +0.5–1 mm — frame fit broken until remachined.
- **Link + fetch date:** https://www.mycncuk.com/threads/12439-The-dude-butchered-my-aluminum-extrusion-(-!!! (fetched 2026-09-06; live; title encoding retained).
- **What went wrong:** OP had lengths cut on a miter saw; “ends aren’t square and aren’t the same length +0.5-1mm from one another.” Willing to trim up to 5 mm if they can be matched and squared. Replies: chop-saw “accuracy” is operator- and trade-dependent; proper dead-stop / mill facing needed for frame work.
- **slotcad check:** **Cut list honesty** (+ interference on assembled topology) — call out squareness/tolerance assumptions; refuse a silent “exact” BOM.

### Bonus — panel play / wrong thickness for the slot (loose → rattle)

- **One-line failure:** 1/4″ panels in 80/20 slots rattled; gaskets / tape / floating methods were workarounds for clearance that was never designed from a slot scan.
- **Link + fetch date:** https://www.fordtransitusaforum.com/threads/what-the-best-way-to-stop-panels-from-rattling-in-80-20-slots.100904/ (fetched 2026-09-06; live index / search snippets; forum front may PoW-challenge automated clients).
- **What went wrong:** Galley builder with painted 1/4″ MDF in the slots: surface play against the slot edge caused rattle. Duct tape on the face helped but made sliding the panel in hard; commercial gasket worked on another bay. Thread is a catalog of clearance band-aids (gasket, rubber balls, z-rail, printed retainers) after the panel/slot match was wrong.
- **slotcad check:** **Panel clearance from slot scan** — size the panel from the measured neck (and engagement depth), with explicit clearance; jam or rattle both fail the check.

Vendor confirmation of the same rule (not a failure story, but the doctrine): Framing Tech — “Metric and inch profiles are not interchangeable — don’t mix them in the same build.” https://www.framingtech.com/t-slot-compatibility (fetched 2026-09-06).

---

## Where the community hangs out

| Place | URL | Notes |
| --- | --- | --- |
| OpenBuilds forums | https://builds.openbuilds.com/ | V-slot / C-Beam / DIY CNC; heavy T-nut & cut threads |
| OpenBuilds Discord | https://discord.gg/cbmteR7yRN (also listed as invite `cbmteR7yRN` on community indexes) | Active builder chat |
| CNCZone | https://www.cnczone.com/ | Classic CNC / extrusion builds (forum quieter than it was) |
| Unofficial CNC Discord | https://discord.gg/eMYefjxXNH | Hobby/semi-pro CNC (announced on MyCNCUK) |
| MyCNCUK | https://www.mycncuk.com/ | UK DIY CNC / gantry builds |
| Voron Design Discord | https://discord.gg/voron | Misumi / extrusion frames for CoreXY printers |
| Voron forum | https://forum.vorondesign.com/ | Self-sourced frames, Bosch vs Misumi hardware |
| Chief Delphi | https://www.chiefdelphi.com/ | FIRST robotics; 80/20 metric vs fractional pain |
| Practical Machinist | https://www.practicalmachinist.com/forum/ | T-nut / T-slot sizing (often mill tables; same geometry lesson) |
| Ford Transit USA Forum | https://www.fordtransitusaforum.com/ | Van builds on 10/15-series 80/20; panel & fastener threads |
| Reddit | https://www.reddit.com/r/CNC/ · https://www.reddit.com/r/hobbycnc/ · https://www.reddit.com/r/3Dprinting/ · https://www.reddit.com/r/VORONDesign/ | Cross-post extrusion / wrong-hardware questions |
| Engineering Stack Exchange | https://engineering.stackexchange.com/ | Occasional profile/T-nut geometry Q&A |
| Rocketry Forum | https://www.rocketryforum.com/ | Launch-rail extrusion naming collisions |
| Vendor Q&A / guides | https://www.framingtech.com/t-slot-compatibility · https://us.misumi-ec.com/maker/misumi/mech/product/al/faq/ · https://8020.net/ | Series color-codes, length tolerances, panel gasket thickness |

---

## Mapping to slotcad checks (summary)

| Failure mode | Cases | Library response |
| --- | --- | --- |
| Wrong T-nut / wrong slot opening | 1, 2 | Fastener family hard error; slot-scan neck vs nut body |
| Mixing same-nominal families | 3, 4 | Hard error on metric↔fractional / Misumi↔80/20 / Nut5↔Nut6 |
| Panel jam or too loose | Bonus | Panel clearance from slot scan |
| Bar too short / cut wrong | 5, 6 | Cut list honesty (tolerance + provenance); no silent exact lengths |

These six linked stories are the README “why it exists” set: measure the real slot, refuse mixed fastener families, size panels from the neck, and never emit a cut list the tool cannot stand behind.
