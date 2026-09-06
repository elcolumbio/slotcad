"""slotcad — measure real T-slot geometry and compile topologies into cut lists."""

__version__ = "0.1.0"

from slotcad.registry import ProfileRecord, load_profile, save_profile
from slotcad.topology import BoxShelf, Frame

__all__ = [
    "__version__",
    "ProfileRecord",
    "load_profile",
    "save_profile",
    "BoxShelf",
    "Frame",
]
