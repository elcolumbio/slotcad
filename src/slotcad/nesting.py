"""Stock nesting against fixed bar lengths."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NestBar:
    stock_mm: float
    cuts_mm: list[float] = field(default_factory=list)

    @property
    def used_mm(self) -> float:
        return sum(self.cuts_mm)

    @property
    def remnant_mm(self) -> float:
        return self.stock_mm - self.used_mm


@dataclass
class NestPlan:
    name: str
    stock_mm: float
    min_cut_mm: float
    bars: list[NestBar]
    notes: list[str] = field(default_factory=list)

    @property
    def bar_count(self) -> int:
        return len(self.bars)


def first_fit_decreasing(
    lengths_mm: list[float],
    *,
    stock_mm: float = 1980.0,
    min_cut_mm: float = 50.0,
) -> NestPlan:
    """Plain FFD: long pieces pack first; shorts often strand into an extra bar."""
    parts = sorted((L for L in lengths_mm if L >= min_cut_mm), reverse=True)
    skipped = [L for L in lengths_mm if L < min_cut_mm]
    bars: list[NestBar] = []
    for L in parts:
        placed = False
        for bar in bars:
            if bar.remnant_mm >= L:
                bar.cuts_mm.append(L)
                placed = True
                break
        if not placed:
            if L > stock_mm:
                raise ValueError(f"cut {L} mm exceeds stock {stock_mm} mm")
            bars.append(NestBar(stock_mm=stock_mm, cuts_mm=[L]))
    notes = [
        f"first-fit-decreasing against {stock_mm:g} mm stock (min cut {min_cut_mm:g} mm).",
    ]
    if skipped:
        notes.append(f"skipped {len(skipped)} pieces below min cut: {skipped}")
    return NestPlan("first-fit-decreasing", stock_mm, min_cut_mm, bars, notes)


def interleaved(
    lengths_mm: list[float],
    *,
    stock_mm: float = 1980.0,
    min_cut_mm: float = 50.0,
) -> NestPlan:
    """Pair long+short when possible — often fewer bars than plain FFD."""
    parts = sorted((L for L in lengths_mm if L >= min_cut_mm), reverse=True)
    skipped = [L for L in lengths_mm if L < min_cut_mm]
    bars: list[NestBar] = []
    used = [False] * len(parts)
    for i, long in enumerate(parts):
        if used[i]:
            continue
        bar = NestBar(stock_mm=stock_mm, cuts_mm=[long])
        used[i] = True
        # try to add the shortest remaining piece that fits, then next, etc.
        for j in range(len(parts) - 1, -1, -1):
            if used[j]:
                continue
            if bar.remnant_mm >= parts[j]:
                bar.cuts_mm.append(parts[j])
                used[j] = True
        bars.append(bar)
    notes = [
        f"interleaved long+short against {stock_mm:g} mm stock.",
        "If the vendor cuts to length, nesting is irrelevant — you do not need this feature.",
    ]
    if skipped:
        notes.append(f"skipped {len(skipped)} pieces below min cut: {skipped}")
    return NestPlan("interleaved", stock_mm, min_cut_mm, bars, notes)


def compare_nesting(
    lengths_mm: list[float],
    *,
    stock_mm: float = 1980.0,
    min_cut_mm: float = 50.0,
) -> dict:
    ffd = first_fit_decreasing(lengths_mm, stock_mm=stock_mm, min_cut_mm=min_cut_mm)
    inter = interleaved(lengths_mm, stock_mm=stock_mm, min_cut_mm=min_cut_mm)
    return {
        "stock_mm": stock_mm,
        "min_cut_mm": min_cut_mm,
        "cut_to_length_note": (
            "If the vendor cuts to length, nesting is irrelevant — "
            "the honest answer is often that you do not need this feature."
        ),
        "first_fit_decreasing_bars": ffd.bar_count,
        "interleaved_bars": inter.bar_count,
        "first_fit_decreasing": [
            {"cuts_mm": b.cuts_mm, "remnant_mm": round(b.remnant_mm, 1)} for b in ffd.bars
        ],
        "interleaved": [
            {"cuts_mm": b.cuts_mm, "remnant_mm": round(b.remnant_mm, 1)} for b in inter.bars
        ],
        "notes": ffd.notes + inter.notes,
    }
