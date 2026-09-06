# Profile registry

Measurements derived from vendor STEP solids. **Do not commit `.step` / `.stp` files.**

Each record includes source URL + SHA-256 of the STEP it was measured from so anyone
with the vendor file can reproduce the JSON byte-for-byte via:

```bash
uv run python -m slotcad measure path/to/vendor.step --emit --out registry/.../id.json ...
```

Provenance on every dimension: `measured` | `vendor` | `assumed`.
