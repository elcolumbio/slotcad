"""Reference topologies: Frame and BoxShelf. User declares topology, never coordinates."""

from __future__ import annotations

from dataclasses import dataclass, field

from slotcad.registry import ProfileRecord


@dataclass
class Member:
    name: str
    role: str  # post | rail | rung | panel
    length_mm: float
    profile_id: str
    # AABB placement in assembly coords (mm)
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float
    provenance: str = "assumed"


@dataclass
class Topology:
    name: str
    profiles: list[ProfileRecord]
    members: list[Member] = field(default_factory=list)
    params: dict = field(default_factory=dict)
    assembly_order: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def primary_profile(self) -> ProfileRecord:
        return self.profiles[0]


def _outer(profile: ProfileRecord) -> float:
    return float(profile.outer_mm[0])


@dataclass
class Frame:
    """Two uprights plus rungs between them.

    Rung length = width - 2 * profile_face. Getting that subtraction wrong is
    the classic first error.
    """

    width_mm: float
    height_mm: float
    rungs: int = 3
    profile: ProfileRecord | None = None
    # optional second profile to demonstrate mix errors
    profile_b: ProfileRecord | None = None
    force_overlap: bool = False

    def build(self) -> Topology:
        if self.profile is None:
            raise ValueError("Frame requires a profile")
        profiles = [self.profile]
        if self.profile_b is not None:
            profiles.append(self.profile_b)
        o = _outer(self.profile)
        # uprights along Z, spaced in X
        upright_len = self.height_mm
        rung_len = self.width_mm - 2 * o
        if rung_len <= 0:
            raise ValueError(
                f"rung length {rung_len} mm — width must exceed 2× profile face ({o} mm)"
            )

        members: list[Member] = [
            Member(
                "upright-left",
                "post",
                upright_len,
                self.profile.id,
                0,
                o,
                0,
                o,
                0,
                upright_len,
                provenance="assumed",
            ),
            Member(
                "upright-right",
                "post",
                upright_len,
                (self.profile_b or self.profile).id,
                self.width_mm - o,
                self.width_mm,
                0,
                o,
                0,
                upright_len,
                provenance="assumed",
            ),
        ]
        # rungs between uprights (sit between the faces)
        if self.rungs < 2:
            raise ValueError("need at least 2 rungs (top and bottom)")
        for i in range(self.rungs):
            z = 0.0 if i == 0 else (
                self.height_mm - o if i == self.rungs - 1 else i * (self.height_mm - o) / (self.rungs - 1)
            )
            x0 = o
            x1 = o + rung_len
            if self.force_overlap and i == 1:
                # bury a rung inside the left upright
                x0 = 0.0
                x1 = o + 5.0
            members.append(
                Member(
                    f"rung-{i+1}",
                    "rung",
                    (x1 - x0) if self.force_overlap and i == 1 else rung_len,
                    self.profile.id,
                    x0,
                    x1,
                    0,
                    o,
                    z,
                    z + o,
                    provenance="assumed",
                )
            )

        order = [m.name for m in members if m.role == "post"] + [
            m.name for m in members if m.role == "rung"
        ]
        return Topology(
            name="frame",
            profiles=profiles,
            members=members,
            params={
                "width_mm": self.width_mm,
                "height_mm": self.height_mm,
                "rungs": self.rungs,
                "rung_length_mm": rung_len,
                "profile_face_mm": o,
            },
            assembly_order=order,
            notes=[
                f"rung length = width − 2×face = {self.width_mm:g} − 2×{o:g} = {rung_len:g} mm",
            ],
        )


@dataclass
class BoxShelf:
    """Four corner posts; per level a closed rectangle of four rails + a panel
    dropped into the inward-facing slots.
    """

    width_mm: float
    depth_mm: float
    height_mm: float
    levels: int = 2
    profile: ProfileRecord | None = None
    profile_b: ProfileRecord | None = None
    panel_thickness_mm: float | None = None
    panel_clearance_mm: float = 0.3
    force_overlap: bool = False
    # If True, panel engages all four slots (corners hit posts).
    # If False, panel held front-and-back only (no corner notches needed).
    panel_four_sides: bool = False

    def build(self) -> Topology:
        if self.profile is None:
            raise ValueError("BoxShelf requires a profile")
        profiles = [self.profile]
        if self.profile_b is not None:
            profiles.append(self.profile_b)
        o = _outer(self.profile)
        neck = self.profile.neck_width_mm
        if self.panel_thickness_mm is None:
            # default: 1 mm under neck, flagged assumed/measured mix
            self.panel_thickness_mm = round(max(1.0, neck - 1.2), 2)

        post_len = self.height_mm
        # Rails form a closed rectangle BETWEEN the posts.
        rail_x = self.width_mm - 2 * o  # front/back rail length (along X)
        rail_y = self.depth_mm - 2 * o  # left/right rail length (along Y)
        if rail_x <= 0 or rail_y <= 0:
            raise ValueError("shelf width/depth must exceed 2× profile face")

        members: list[Member] = []
        # four posts at corners
        post_xy = [
            ("post-fl", 0, 0),
            ("post-fr", self.width_mm - o, 0),
            ("post-bl", 0, self.depth_mm - o),
            ("post-br", self.width_mm - o, self.depth_mm - o),
        ]
        for name, x, y in post_xy:
            members.append(
                Member(
                    name,
                    "post",
                    post_len,
                    self.profile.id,
                    x,
                    x + o,
                    y,
                    y + o,
                    0,
                    post_len,
                    provenance="assumed",
                )
            )

        # levels distributed from bottom
        level_zs = []
        for i in range(self.levels):
            if self.levels == 1:
                z = 0.0
            else:
                z = i * (self.height_mm - o) / (self.levels - 1)
            level_zs.append(z)

        engage = min(self.profile.slot_bottom_mm * 0.5, 3.0)

        for li, z in enumerate(level_zs):
            # front rail (y=0 side, between posts)
            fx0, fx1 = o, o + rail_x
            if self.force_overlap and li == 0:
                fx0 = 0.0  # bury into left post
            members.append(
                Member(
                    f"L{li+1}-rail-front",
                    "rail",
                    fx1 - fx0,
                    self.profile.id,
                    fx0,
                    fx1,
                    0,
                    o,
                    z,
                    z + o,
                    provenance="assumed",
                )
            )
            members.append(
                Member(
                    f"L{li+1}-rail-back",
                    "rail",
                    rail_x,
                    self.profile.id,
                    o,
                    o + rail_x,
                    self.depth_mm - o,
                    self.depth_mm,
                    z,
                    z + o,
                    provenance="assumed",
                )
            )
            members.append(
                Member(
                    f"L{li+1}-rail-left",
                    "rail",
                    rail_y,
                    self.profile.id,
                    0,
                    o,
                    o,
                    o + rail_y,
                    z,
                    z + o,
                    provenance="assumed",
                )
            )
            members.append(
                Member(
                    f"L{li+1}-rail-right",
                    "rail",
                    rail_y,
                    (self.profile_b or self.profile).id,
                    self.width_mm - o,
                    self.width_mm,
                    o,
                    o + rail_y,
                    z,
                    z + o,
                    provenance="assumed",
                )
            )

            # Panel dropped into inward-facing slots.
            if self.panel_four_sides:
                # rectangle engaging all four slots — overlaps each post by ~engage²
                px0 = o - engage
                px1 = self.width_mm - o + engage
                py0 = o - engage
                py1 = self.depth_mm - o + engage
                panel_note = "four-side engagement (corners hit posts — notch or accept overlap)"
            else:
                # front-and-back only
                px0 = o
                px1 = self.width_mm - o
                py0 = o - engage
                py1 = self.depth_mm - o + engage
                panel_note = "front-and-back engagement only (no corner notches)"

            t = float(self.panel_thickness_mm)
            # panel sits on top of rail inner ledge — approximate z at rail top - small
            pz = z + o - 1.0
            members.append(
                Member(
                    f"L{li+1}-panel",
                    "panel",
                    0.0,  # not a bar cut
                    self.profile.id,
                    px0,
                    px1,
                    py0,
                    py1,
                    pz,
                    pz + t,
                    provenance="assumed",
                )
            )
            members[-1].length_mm = 0.0  # panels sized separately

        order = [m.name for m in members if m.role == "post"]
        for li in range(self.levels):
            # panel before last rail of the closed rectangle
            order += [
                f"L{li+1}-rail-front",
                f"L{li+1}-rail-left",
                f"L{li+1}-rail-right",
                f"L{li+1}-panel",
                f"L{li+1}-rail-back",
            ]

        panel_w = self.width_mm - 2 * o + (2 * engage if self.panel_four_sides else 0)
        panel_d = self.depth_mm - 2 * o + 2 * engage

        return Topology(
            name="box-shelf",
            profiles=profiles,
            members=members,
            params={
                "width_mm": self.width_mm,
                "depth_mm": self.depth_mm,
                "height_mm": self.height_mm,
                "levels": self.levels,
                "profile_face_mm": o,
                "rail_x_mm": rail_x,
                "rail_y_mm": rail_y,
                "panel_thickness_mm": self.panel_thickness_mm,
                "panel_clearance_mm": self.panel_clearance_mm,
                "panel_size_mm": [round(panel_w, 2), round(panel_d, 2)],
                "panel_four_sides": self.panel_four_sides,
                "neck_width_mm": neck,
                "engage_mm": engage,
            },
            assembly_order=order,
            notes=[
                "closed rectangle cannot be retrofitted with a panel — "
                "panel goes in before the last rail",
                panel_note,
                f"panel sized from neck {neck:g} mm with clearance "
                f"{self.panel_clearance_mm:g} mm → thickness {self.panel_thickness_mm:g} mm",
            ],
        )
