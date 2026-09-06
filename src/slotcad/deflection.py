"""Simple beam deflection estimates from measured second moments."""

from __future__ import annotations

from dataclasses import dataclass

# Aluminium Young's modulus (assumed; typical 6060/6063-T5/T6 band)
E_ALUMINIUM_MPA = 70_000.0  # N/mm²


@dataclass
class DeflectionResult:
    span_mm: float
    load_n: float
    i_mm4: float
    e_mpa: float
    delta_mm: float
    formula: str
    provenance_i: str
    provenance_e: str
    assumptions: list[str]


def simply_supported_center_load(
    span_mm: float,
    load_n: float,
    i_mm4: float,
    *,
    e_mpa: float = E_ALUMINIUM_MPA,
    provenance_i: str = "measured",
) -> DeflectionResult:
    """δ = F L³ / (48 E I) for a simply-supported beam, centre point load."""
    if i_mm4 <= 0 or e_mpa <= 0:
        delta = float("inf")
    else:
        delta = (load_n * span_mm**3) / (48.0 * e_mpa * i_mm4)
    return DeflectionResult(
        span_mm=span_mm,
        load_n=load_n,
        i_mm4=i_mm4,
        e_mpa=e_mpa,
        delta_mm=round(delta, 3),
        formula="F*L^3/(48*E*I) simply-supported centre load",
        provenance_i=provenance_i,
        provenance_e="assumed",
        assumptions=[
            f"E={e_mpa:g} N/mm² (assumed aluminium)",
            "simply supported, centre point load, linear elastic",
            "this sizes parts — it does not certify a structure",
        ],
    )


def uniformly_distributed(
    span_mm: float,
    total_load_n: float,
    i_mm4: float,
    *,
    e_mpa: float = E_ALUMINIUM_MPA,
    provenance_i: str = "measured",
) -> DeflectionResult:
    """δ = 5 w L⁴ / (384 E I) with w = total_load/L → 5 F L³ / (384 E I)."""
    if i_mm4 <= 0 or e_mpa <= 0:
        delta = float("inf")
    else:
        delta = (5.0 * total_load_n * span_mm**3) / (384.0 * e_mpa * i_mm4)
    return DeflectionResult(
        span_mm=span_mm,
        load_n=total_load_n,
        i_mm4=i_mm4,
        e_mpa=e_mpa,
        delta_mm=round(delta, 3),
        formula="5*F*L^3/(384*E*I) simply-supported UDL",
        provenance_i=provenance_i,
        provenance_e="assumed",
        assumptions=[
            f"E={e_mpa:g} N/mm² (assumed aluminium)",
            "simply supported, uniform load, linear elastic",
            "this sizes parts — it does not certify a structure",
        ],
    )
