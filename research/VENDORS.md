# Aluminium T-slot extrusion vendors — research for slotcad

**Fetch date for all citations: 2026-09-06.**  
Companion machine-readable file: [`vendors.json`](./vendors.json).

## Project policy (legal context)

slotcad ships **measurements derived from vendor solids** (cross-section area, mass/m, Ixx/Iyy, slot scan geometry) together with **source URL + checksum**. It does **not** redistribute STEP/solid CAD unless a licence **plainly** permits. Linking to product pages and naming the vendor is fine. No vendor logos as badges. Claim no commercial relationship.

Default posture when terms are silent or vague: **`may_redistribute_step: false`** / treat as **unverified** — never invent licence quotes.

---

## Cross-vendor naming map (starter)

| Approximate family | Motedis | item | Bosch Rexroth | 80/20 | Alutec KK | MayTec | OpenBuilds | MakerBeam | MiniTec |
|---|---|---|---|---|---|---|---|---|---|
| ~20 mm / small slot | 20x20 **I-Type slot 5**; 20x20 **B-type slot 6** | **Profile / Line 5** 20x20 | **6 mm slot**, 20 mm modular | **10 Series** / metric small | **Module 20 / groove 5** | PG **20** (slot gauges ~5.2 mm class) | **V-Slot 20x20** | MakerBeam **10x10**; XL/OpenBeam **15x15** | (smaller / series 30 start) |
| ~30 mm | 30x30 **B-Type slot 8** | **Line 6** | **8 mm slot**, 30 mm modular | — | **Module 30 / groove 6 or 8** | PG **30** | V-Slot 20x40 / 20x60 | — | **Series 30** |
| ~40 mm | 40x40**L I-Type slot 8**; 40x40 **B-type slot 10** | **Line 8** 40x40 | **8 mm / 40 mm modular**; **10 mm / 45** | **15 Series (1515)**; **40 Series** | **Module 40 / groove 8 or 10** | PG **40** | **V-Slot 40x40**; **C-Beam 40x80** | — | **Series 45** (45 mm grid) |
| ~45 mm | 45x45 **B-Type slot 10** | Line 8/10 mixes | **10 mm slot**, 45 mm modular | — | **Module 45 / groove 8 or 10** | PG **45** | — | — | Series 45 |
| Heavy / large | 80x80, 90x90, etc. | **Line 12** | 50/60 mm modular, 10 mm slot | 25/40 Series | Module **50 / groove 10** | PG **50/60** | C-Beam actuators | — | large 45-grid |

**Slot naming dialects:** EU shops often say **Nut 5 / Nut 6 / slot 6 / groove 5 / Rowek 5 / Line 5**. US fractional shops say **1515 / 15 Series**. OpenBuilds uses trademarked **V-Slot® / C-Beam®**. These are **not** interchangeable without verifying nut geometry and accessory catalogues.

---

## 1. Motedis

**Region:** EU (DE headquarters; country shops e.g. `.com`, `.co.uk`, `.es`).  
**Why it matters for slotcad:** Clear public CAD database, maker-friendly cut-to-length, and naming that matches the brief’s **20x20 Nut 5 / Nut 6** builds.

### CAD
- **Free downloadable CAD** (ZIP packages; product pages also link 3D ZIPs) for aluminium profiles and many accessories: [CAD & Info Database](https://www.motedis.com/en/cad-database).
- Formats advertised on the CAD database include ZIP (models) and PDF drawings; product pages label **3D** downloads as ZIP (industry practice: STEP inside — confirm per ZIP; treat format list as STEP-capable solids).
- **Account required:** No for the public CAD database listings checked 2026-09-06.

### Terms / redistribution
- Conditions of Use: [motedis.com conditions-of-use](https://www.motedis.com/en/conditions-of-use:_:3.html) (fetched 2026-09-06).
- **Quote (§2):** *“On drawings, constructions and other documents from us we reserve property rights and copyright exploitation rights unrestricted before; The customer must not have access to these third parties do.”*
- **Verdict:** `may_redistribute_step: **false**`. Derived measurements: **unclear** (not addressed); project default remains measurements-only with citation.

### Families / naming
- **B-Type** vs **I-Type** (connector/fitment families).
- Slots: **slot 5, 6, 8, 10** (e.g. Profile 20x20 B-type slot 6; Profile 20x20 I-Type slot 5; 30x30 B-Type slot 8; 40x40L I-Type slot 8; 45x45 B-Type slot 10). Overview: [Slot profiles](https://www.motedis.co.uk/en/Slot-profiles).

### Stock / cutting
- Precut / pack lengths commonly **500 / 1000 / 1500 / 1980 / 6000 mm**; custom cut ranges such as **50–6000 mm** and **50–1980 mm** appear on product pages (example: [20x20 B-Type Slot 6](https://www.motedis.es/en/Profile-20x20-B-type-slot-6)).
- **Cut-to-length:** Yes (FAQ / shop: profiles cut to needed length).
- **Min cut / cut tolerance:** Min ~**50 mm** shown on custom range; **tolerance unverified**.

### Monetisation
- **Affiliate programme:** **No** traditional affiliate confirmed 2026-09-06 (prior check stands).
- **Kit idea fee:** Users can publish kits with a self-chosen “idea fee” ([create kit](https://www.motedis.com/shop/create_offers_kit.php?oID=)) — not a classic affiliate network.
- **Efficiency Club:** Loyalty / self-service discount club ([Efficiency Club](https://www.motedis.com/en/efficiency-club)); not a trade price API.
- **Trade / volume:** Same public prices for private and business in marketing copy; some “big customers” login options for certain cut modes; Efficiency Club for experienced buyers.
- **Price API / cart-prefill:** No public price API found. Shop cart is the ordering path.
- **Design software giveaway:** No (CAD files only).

---

## 2. item (item Industrietechnik)

**Region:** EU (Solingen); global sales partners.  
**Site:** [item aluminium profiles](https://www.item24.com/en-de/theme-world/building-kit-system/aluminium-profiles).

### CAD
- Per-product **CAD Data and Downloads**; also **TraceParts**; browser **Engineeringtool** exports CAD as project documentation.
- **Account:** Registration required for full Online Platform save/download/order flows ([Platform usage agreement](https://www.item24.com/en-gb/legal/platform-usage-agreement), dated May 2026).

### Terms / redistribution
- GTC §2(1) ([terms and conditions](https://www.item24.com/en-de/legal/terms-and-conditions), Issued July 2023):  
  **Quote:** *“… catalogues, technical documentation … other product descriptions or documents – also in electronic form – to which we reserve ownership rights and copyrights; they may not be reproduced and made accessible to third parties without our express consent in writing.”*
- Platform T&Cs: CAD may be downloaded and used for **application-related purposes**; Clause 21 limits use to testing, viewing, documenting in-house, selling item products, enquiries/orders — further use prohibited.
- **Verdict:** `may_redistribute_step: **false**`. Derived measurements: **unclear**.

### Families / naming
- **Line / Profile 5, 6, 8, 10, 12** (e.g. Profile 5 20x20). Variants: standard, light, economy (E).

### Stock / cutting
- TraceParts selectors show cut lengths roughly **>20 … 6000 mm**; packaging max **6000 mm** (example Profile 6 60x60 on TraceParts). Confirm live shop stock.
- **Cut-to-length:** Yes. **Tolerance:** unverified.

### Monetisation
- Free **Engineeringtool** / Online Tools; B2B Marketplace.
- **Affiliate:** none found. **Trade accounts:** yes (partners / marketplace). **Price API:** none found.

---

## 3. Bosch Rexroth (aluminium profiles / EcoShape / strut)

**Region:** EU/US global.  
**Tools:** [FRAMEpro](https://www.boschrexroth.com/en/us/products/industrial-solutions/assembly-technology/aluminum-profile-kit/framepro-cad-plug-in/), MTpro, Rexroth Store, TraceParts.

### CAD
- **FRAMEpro** (Inventor / SolidWorks), **MTpro** (exports common CAD formats including STEP per brochure copy), TraceParts for EcoShape / components.
- **Account:** Typically required for software / store.

### Terms / redistribution
- **No clean primary CAD-redistribution quote** extracted 2026-09-06 from public Rexroth pages (FRAMEpro / store ToS not fully retrieved).  
- **Verdict:** `may_redistribute_step: **false**` by project default; quote field **`unverified`**. Do not ship Rexroth STEP.

### Families / naming
- Strut profiles by **slot width + modular dimension**: 6 mm / 20 mm; 8 mm / 30 or 40 mm; **10 mm** / 45, 50, 60 mm.
- **EcoShape** tubular (e.g. D28L) with integrated ~10 mm slot, compatible with modular aluminium framing.

### Stock / cutting
- Packaging units often **6070 mm** usable length (actual ~+100 mm for anodising contacts) — see catalog extracts such as [aluminum structural framing PDF](https://esd.equipment/dokumente/bosch-rexroth/sonstiges/aluminum-structural-framing-system-en.pdf).
- Variable cut e.g. **50…6070 mm** on datasheets. **Tolerance:** unverified.

### Monetisation
- Free MTpro / FRAMEpro. Trade via Rexroth & partners. **Affiliate:** none found. **Price API:** none found.

---

## 4. Misumi

**Region:** JP / US / EU / global e-catalogs.  
**FRAMES:** [US FRAMES](https://us.misumi-ec.com/service/promotion/frames/), [UK FRAMES](https://uk.misumi-ec.com/en/services/frames/).

### CAD
- Product-page CAD (STEP and others) — **login required** (regional user guides).
- **FRAMES** free desktop app: design frames, export **STEP / Parasolid / DXF**, BOM, quote/order into MISUMI account.

### Terms / redistribution
- US CAD Terms ([service/info/terms](https://us.misumi-ec.com/service/info/terms/)): purpose limited to informing customers of product characteristics for designs;  
  **Quote:** *“Without prior approval from MISUMI, no part of the Data may be utilized (reproduced, modified, reverse-engineered, uploaded, presented, sent, distributed, licensed, sold, or published) for any purpose other than that mentioned above.”*
- FRAMES EULA ([FRAMES EULA](https://us.misumi-ec.com/service/promotion/frames/frames-end-user-license-agreement.html)): Documentation is MISUMI property; **no copy/share/distribute to third parties** without permission; ordering from third parties based on Documentation prohibited.
- **Verdict:** `may_redistribute_step: **false**` (clearest ban among industrial vendors surveyed). Derived measurements: **unclear**.

### Families / naming
- Configurable MISUMI aluminium extrusions via e-catalog / FRAMES part numbers. Exact Nut-N map **unverified** without live catalogue scrape — do not invent aliases.

### Stock / cutting
- Configurable cut-to-length via e-catalog/FRAMES. Specific stock bar lengths / tolerances: **unverified** 2026-09-06.

### Monetisation
- **FRAMES free** (registration). Trade/account customers. **Affiliate:** none found. Instant quote in-account; **no public price API** found.

---

## 5. 80/20 Inc

**Region:** US (Columbia City, IN) + distributors.  
**Design tools:** [8020.net/design-software](https://8020.net/design-software), IdeaBuilder, AutoQuoterSW/X.

### CAD
- Free CAD library / PartSource; IdeaBuilder exports STEP; product-page models; streamlined DXF/SolidWorks/Inventor/SketchUp packs historically catalogued.
- **Account:** Not required for many downloads; some tools benefit from accounts.

### Terms / redistribution
- [Terms and Conditions of Sale](https://8020.net/terms-conditions):  
  **Quote:** *“80/20 PROPERTY. All photographs, samples, descriptions, drawings or intellectual property provided by 80/20 to Buyer shall remain the property of 80/20 and shall only be used by Buyer to market 80/20 products to third parties. … All such property shall be returned to 80/20 upon demand …”*
- **Verdict:** `may_redistribute_step: **false**`. Derived measurements: **unclear**.

### Families / naming
- Fractional **10 / 15 / 25 / 40 Series** (e.g. **1515**); metric series also sold. Naming does not match EU “Nut 6”.

### Stock / cutting
- Cut-to-length and machining widely offered. Exact stock lengths in mm: **unverified** without product scrape (US customary bars).

### Monetisation
- **Affiliate programme:** Yes — Affiliate Program Terms URL [8020.net/amasty-affiliate-conditions](https://8020.net/amasty-affiliate-conditions) (Cloudflare challenge on fetch; existence confirmed via search index 2026-09-06).
- Free IdeaBuilder / plugins. Distributor/trade network. IdeaBuilder XML for ordering. **No public price API** found.

---

## 6. MayTec

**Region:** EU (DE) / partners US / AU.  
**MayCad:** [maytec.de/en/maycad](https://www.maytec.de/en/maycad/).

### CAD
- **MayCad®** free for authorised users / partners; exports assemblies as **3D STEP**, DXF, PDF. Not a public anonymous STEP dump like Motedis.

### Terms / redistribution
- MayCad marketed as **proprietary**, *“only available directly from MayTec or one of our authorized partners.”*  
- Dedicated CAD redistribution licence text: **`unverified`**.  
- **Verdict:** `may_redistribute_step: **false**` by default.

### Families / naming
- Profile groups **PG 16–60** by basic measure; slot types H/F/E3 etc. MayTec USA documents T-slot gauges for 20/30/40 mm series ([profile specifications](https://www.maytec-usa.com/engineering-resources/aluminum-profile-specifications)).

### Stock / cutting
- Standard **3 m / 6 m** stock referenced; production deviations per **DIN EN 12020 part 2**; cut-to-length via distributors. Exact cut tolerance: **unverified**.

### Monetisation
- Free MayCad (authorised). Partner/trade sales. **Affiliate:** none found. **Price API:** none found.

---

## 7. Alutec / Alutec KK (ALUTEC KK s.r.o.)

**Region:** EU (Czech manufacturer; multi-country sites).  
**System overview:** [aluminium structural system](https://www.aluteckk.co.uk/aluminium-structural-system).

### CAD
- **Autodesk Inventor** Content Center libraries ([3D libraries](https://www.aluteckk.co.uk/3d-libraries-in-autodesk-inventor)) — downloadable ZIP/.idcl.
- **TraceParts** STEP and many formats: [ALUTEC KK on TraceParts](https://www.traceparts.com/en/search/alutec-kk-sro?CatalogPath=ALUTEC_500759239%3AF_ALUTEC).
- Online 3D catalogue / configurators (desks, conveyors, tubular).

### Terms / redistribution
- GTC pages exist (e.g. [LT GTC](https://www.aluteckk.lt/general-terms-conditions)) but **no explicit CAD redistribution clause extracted** 2026-09-06 → **`unverified`**.  
- **Verdict:** `may_redistribute_step: **false**` by default (TraceParts ToS also apply to that channel).

### Families / naming
- **Module / groove:** 20/5, 30/6, 30/8, 40/8, 40/10, 45/8, 45/10, 50/10 (+ specials). Polish shop: Moduł / Rowek.

### Stock / cutting
- Standard profiles often **6 m**; custom cutting. Structural system cut-to-length via order/inquiry.

### Monetisation
- Free Inventor libs / configurators. Inquiry e-shop / trade. **Affiliate:** none found. **Price API:** none found.

---

## 8. MakerBeam

**Region:** EU (NL webshop).  
**Drawings:** [technical-drawings](https://www.makerbeam.com/technical-drawings/), [FAQ](https://www.makerbeam.com/service/), Drive library linked from FAQ.

### CAD
- **.stp, .dxf, .pdf, .svg** technical drawings on Google Drive — **no account** for browsing Drive link.
- Specs published for MakerBeam / XL / OpenBeam including area and Ixx/Iyy ([specifications post](https://www.makerbeam.com/blogs/makerbeam/specifications-makerbeam-and-openbeam/)).

### Terms / redistribution
- Files offered for planning; **no CC licence text** found on current technical-drawings / FAQ pages (2026-09-06).  
- **Do not invent** historical “open source” claims as current terms.  
- **Verdict:** `may_redistribute_step: **unclear**` → do not redistribute STEP until clarified in writing. Derived measurements from published numeric specs may be citeable; still mark licence **unclear**.

### Families / naming
- **MakerBeamXS 5×5**, **MakerBeam 10×10**, **MakerBeamXL 15×15**, **OpenBeam 15×15** (M3 ecosystem).

### Stock / cutting
- Precut lengths commonly **40–1500 mm** (e.g. 300, 600, 900, 1500); FAQ mentions **cutting service**. Min cut / tolerance: **unverified**.

### Monetisation
- Direct shop. **Affiliate:** none found. No free design suite. No price API.

---

## 9. OpenBuilds

**Region:** US Part Store + community.  
**Licence page:** [us.openbuilds.com/open-source-license](https://us.openbuilds.com/open-source-license) (HTTP 500 on WebFetch 2026-09-06; content corroborated via search index + GrabCAD attribution strings).  
**CAD:** [GrabCAD OpenBuilds](https://grabcad.com/openbuilds-1/models), [project resources](https://builds.openbuilds.com/projectresources/).

### CAD
- Official **STEP** models on GrabCAD (GrabCAD account may be needed to download). Community resources also host STEP/SolidWorks.

### Terms / redistribution
- OpenBuilds Branded Works shared under **CC BY-SA 4.0** with required attribution string:  
  *“This design incorporates OpenBuilds, LLC design work(s) shared Open Source under the CC BY-SA 4.0 License.”*
- Trademarks (**OpenBuilds, V-Slot, C-Beam**) remain restricted ([OSHW support article](https://support.openbuilds.com/support/solutions/articles/65000167819-embracing-open-source-philosophy)).
- **Verdict:** `may_redistribute_step: **true**` (with BY-SA attribution + share-alike on derivatives). Derived measurements: **true** under same licence, with attribution. Still avoid using trademarks as badges.

### Families / naming
- **V-Slot** 20x20, 20x40, 20x60, 20x80, 40x40; **C-Beam**; OpenRail.

### Stock / cutting
- Custom cuts: min **100 mm**, tolerance **±1 mm**, whole-mm increments; note exact length at checkout; allow **5 mm** kerf per cut ([custom cuts support](https://support.openbuilds.com/support/solutions/articles/65000167794-custom-cuts-and-tapping) — 500 on direct fetch; content from search index).
- Standard retail lengths on Part Store (exact list unverified).

### Monetisation
- **Affiliate:** Yes — [affiliates.openbuildspartstore.com](https://affiliates.openbuildspartstore.com/).  
- No free industrial design suite comparable to FRAMES/MayCad (community CAD). No public price API found.

---

## 10. Other Europe / US vendors that clearly matter

### MiniTec
- EU origin; US framing partners. Free **iCAD Assembler**; STEP/SolidWorks ZIPs ([MiniTec Solutions downloads](https://www.minitecsolutions.com/downloads/)); Inventor libraries on [minitec.de](https://www.minitec.de/en/service/software/cad-library).
- Families: **profile series 30 and 45** (uniform grooves within series).
- CAD redistribution: **unverified** dedicated clause → default **false**.
- Trade channel; free design software; no affiliate found.

### TSLOTS (Bonnell Aluminum)
- US extruder. CAD on TraceParts; DesignPro SolidWorks add-in historically free ([tslots.com](https://tslots.com/)).
- Metric / fractional / B-Series naming. Cut-to-length / make-to-order. CAD ToS **unverified** → default no STEP redistribution.

*(Many regional distributors resell item / Rexroth / MayTec / MiniTec — prefer primary manufacturer CAD + terms.)*

---

## Monetisation quick matrix (2026-09-06)

| Vendor | Affiliate | Trade / volume | Free design software | Public price API |
|---|---|---|---|---|
| Motedis | **No** (kit idea fee only) | Efficiency Club / big-customer options | No (CAD files) | No |
| item | No | Yes / Marketplace | Engineeringtool | No |
| Bosch Rexroth | No | Yes | MTpro, FRAMEpro | No |
| Misumi | No | Yes | **FRAMES** | No (account quotes) |
| 80/20 | **Yes** | Distributors | IdeaBuilder, plugins | No |
| MayTec | No | Partners | **MayCad** | No |
| Alutec KK | No | Yes | Inventor libs / configurators | No |
| MakerBeam | No | unverified | No | No |
| OpenBuilds | **Yes** | unverified | Community CAD | No |
| MiniTec | No | Yes | iCAD Assembler | No |
| TSLOTS | No | Distributors | DesignPro (verify) | No |

---

## STEP redistribution verdicts

| Verdict | Vendors |
|---|---|
| **Clear ban / reserved rights (do not redistribute STEP)** | Motedis, item, Misumi, 80/20; default-ban: Bosch Rexroth, MayTec, Alutec KK, MiniTec, TSLOTS |
| **Explicitly permissive (CC BY-SA)** | **OpenBuilds** (branded works; trademarks still restricted) |
| **Unclear — obtain written OK** | **MakerBeam** (files public, licence silent) |

Derived **measurements**: nowhere clearly blessed except OpenBuilds (CC BY-SA). Elsewhere mark **`unclear`** and keep the project’s conservative “measurements + URL + checksum, no STEP” policy.

---

## Strongest reference-implementation candidate

**Motedis** remains the strongest default for slotcad’s first reference profiles:

1. **Public, free CAD database** without account friction.  
2. Naming matches the brief (**20x20 B-type slot 6 / I-Type slot 5**, Nut 5/6 language).  
3. Maker-grade **cut-to-length** and transparent EU webshop.  
4. Licence clearly **forbids** handing drawings to third parties → fits the **measurements-only** shipping model (derive locally, cite URL + checksum, do not vendor-STEP).

**OpenBuilds** is the strongest candidate if the goal is **redistributable STEP** under CC BY-SA (CNC / V-Slot ecosystem) — different geometry and trademark constraints than classic EU Nut-6 machine profiles.

**item** / **Misumi** / **80/20** are excellent industrial coverage but have **harder CAD access** (accounts) and **clear anti-redistribution** terms — fine as measurement sources, poor as shipped solids.

---

## Blockers / gaps

| Issue | Detail |
|---|---|
| OpenBuilds licence page | `https://us.openbuilds.com/open-source-license` returned **HTTP 500** on WebFetch; corroborated via search + GrabCAD attributions. Re-fetch later. |
| OpenBuilds custom-cut article | Support URL returned **500**; content from search index. |
| 80/20 affiliate terms page | Cloudflare challenge on fetch; programme existence confirmed. |
| Misumi US CAD Terms full page | One fetch timed out; quotes taken from successful search-indexed excerpts + FRAMES EULA full fetch. Re-fetch `us.misumi-ec.com/service/info/terms/` for archival. |
| Bosch Rexroth / MayTec / Alutec / MiniTec / TSLOTS / MakerBeam | Missing or incomplete **dedicated CAD redistribution** clauses → marked **unverified** / default false. |
| Cut tolerances | Rarely published as a single number; often “unverified” or standard DIN EN 12020 / ISO 2768 references only. |
| Misumi / 80/20 exact stock length lists | Not scraped product-by-product; left empty / notes. |
| Paywalls | No hard paywall for the CAD surveyed; **login walls** (Misumi, item platform, MayCad authorisation) are the main friction. |

---

## Method note

Primary sources preferred (vendor legal pages, CAD portals, product pages). Forums and third-party blogs used only as pointers. All factual URLs above were checked or search-corroborated on **2026-09-06**. Where text could not be extracted cleanly, the files say **`unverified`** rather than guessing.
