"""Fastener-family compatibility — mixing is a hard error."""

from __future__ import annotations

from slotcad.registry import ProfileRecord


class FastenerFamilyError(ValueError):
    """Raised when a topology mixes incompatible fastener families."""


# Families that must never share a build. Keyed by normalized family id.
INCOMPATIBLE_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset({"nut-5", "nut-6"}),
        frozenset({"i-typ-nut-5", "b-typ-nut-6"}),
        frozenset({"motedis-nut-5", "motedis-nut-6"}),
    }
)


def normalize_family(name: str) -> str:
    s = name.strip().lower().replace("_", "-").replace(" ", "-")
    aliases = {
        "nut5": "nut-5",
        "nut6": "nut-6",
        "slot-5": "nut-5",
        "slot-6": "nut-6",
        "i-typ-nut-5": "nut-5",
        "i-type-nut-5": "nut-5",
        "i-typ-slot-5": "nut-5",
        "b-typ-nut-6": "nut-6",
        "b-type-nut-6": "nut-6",
        "b-typ-slot-6": "nut-6",
        "motedis-nut-5": "nut-5",
        "motedis-nut-6": "nut-6",
    }
    return aliases.get(s, s)


def families_compatible(a: str, b: str) -> bool:
    na, nb = normalize_family(a), normalize_family(b)
    if na == nb:
        return True
    return frozenset({na, nb}) not in INCOMPATIBLE_PAIRS and na == nb


def assert_single_family(profiles: list[ProfileRecord]) -> str:
    """Return the sole family or raise FastenerFamilyError naming both."""
    families: list[str] = []
    labels: list[str] = []
    for p in profiles:
        fam = normalize_family(p.fastener_family)
        if fam not in families:
            families.append(fam)
            labels.append(f"{p.product_name or p.id} ({p.fastener_family})")
    if len(families) <= 1:
        return families[0] if families else "unknown"
    # Always hard-error on any mix of distinct families in one topology.
    raise FastenerFamilyError(
        "fastener family mix is a hard error: "
        + " vs ".join(labels)
        + " — they share no T-nut, bracket, or screw"
    )
