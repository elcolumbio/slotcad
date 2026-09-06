# Legal ground rules

Orientation, not legal advice — nobody here is a lawyer. But these are the four places this project
can actually go wrong, and three of them are cheap to stay clear of.

Context: the project is **free and non-commercial**, published under an open-source licence, and it
links to a vendor shop without any commercial relationship with that vendor.

## 1. Linking to Motedis — fine

Plain hyperlinks to a shop's own, freely accessible product pages need nobody's permission. Under EU
case law a link to lawfully published, freely accessible content is not itself a copyright act
(*Svensson*, C-466/12). The one qualifier in *GS Media* (C-160/15) — that a for-profit linker is
presumed to know whether the target was published unlawfully — does not bite here: Motedis publishes
its own pages, and we earn nothing.

Naming the vendor is likewise fine. Using someone's trade mark to say what a product actually is, or
what your tool is compatible with, is permitted referential use (§ 23 MarkenG; Art. 14 EUTMR).

**Do:** link to product pages, name Motedis in prose, say which profile a record was measured from.
**Don't:** use their logo or wordmark as a badge, put "Motedis" in the repo or domain name, style
pages to look like theirs, or write anything that reads as partnership, endorsement or authorisation.
Add one line to the README saying there is no relationship with any vendor. That sentence is free and
removes the only ambiguity worth removing.

Since there is no affiliate programme and no money changes hands, the German advertising-labelling
rule for paid links (§ 5a Abs. 4 UWG) does not apply. If that ever changes, the label goes on first.

## 2. Their CAD files — the real risk, and it is already handled

Do not redistribute vendor STEP files. Their download terms may or may not permit it, and "may not" is
the safe default until phase 1 says otherwise in writing.

What we publish is **measurements derived from those solids** — cross-section, mass per metre, second
moments, the slot scan — each with the source URL and a checksum of the file it came from. Measured
facts about a physical object are not the vendor's artefact. A user with the vendor file reproduces
the record exactly; a user without it still gets correct numbers.

This is the same line the other two briefs in this family draw, and it has now shaped three repos.

## 3. Their catalogue and prices — the limit on how far this may go

Single links: fine. Systematically copying the catalogue or scraping prices into our own dataset:
not fine. The EU sui generis database right (§§ 87a ff. UrhG) protects a substantially invested
collection even where no individual item is protected, and a competing extraction of it is exactly
what that right exists to stop.

So: link out for price, never mirror it. If a cross-vendor priced cut list is ever built, it needs
either published machine-readable prices with terms that permit the use, or the vendor's agreement.
Phase 1 asks that question.

## 4. Someone orders €800 of aluminium on our cut list and it is wrong

This is the risk people forget, and it is the one that scales with the project's usefulness.

Giving it away is itself protective here. German law holds a giver to intent and gross negligence
only (§ 521 BGB), a limit routinely read across to free software; the standard open-source warranty
disclaimer (MIT, Apache-2.0) says the same in contract terms. What that limit does **not** cover is
personal injury or gross negligence (§ 309 Nr. 7 BGB) — so a disclaimer is not a substitute for the
tool being careful, and a shelf that collapses is a different conversation from a wrong cut list.

The engineering answers are already in the brief, and they matter more than the licence text:

- Every dimension carries `measured` / `vendor` / `assumed`, and an `assumed` value never reaches a
  cut list unflagged.
- A failed interference check emits **no** cut list.
- Mixing fastener families is a hard error.
- Load and deflection figures state their assumptions, and the README says plainly that this tool
  sizes parts, it does not certify a structure.

## 5. If it ever gets a website

A GitHub repository needs nothing. A hosted page operated from Germany needs an Impressum under
§ 5 DDG — which replaced § 5 TMG on 14 May 2024, so do not cite the old section — plus a privacy
notice if it processes anything at all. Purely private, non-commercial pages are treated more
leniently, but the cheap move is simply to have one.

## The short version

Link freely, name the vendor, claim no relationship. Ship measurements, never their files. Never
mirror the catalogue or prices. Refuse to emit a cut list the tool cannot stand behind.
