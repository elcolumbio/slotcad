# slotcad — Makefile is the source of truth for every README command.

PYTHON ?= uv run python
PROFILE_NUT6 ?= registry/motedis/20x20-b-typ-nut-6.json
STEP_NUT6 ?= /tmp/slotcad-dl/Motedis Profile 20x20 B-Type slot 6.stp

.PHONY: help test measure build-shelf build-frame sheet clean

help:
	@echo "targets: test measure build-shelf build-frame sheet clean"

test:
	$(PYTHON) -m pytest -q

# Re-measure a local vendor STEP (not committed). Requires CadQuery + the file.
measure:
	$(PYTHON) -m slotcad measure "$(STEP_NUT6)" --emit --out $(PROFILE_NUT6) \
		--id 20x20-b-typ-nut-6 --vendor motedis \
		--product-name "20x20 B-Typ Nut 6" \
		--product-url "https://www.motedis.com/en/Profile-20x20-B-type-slot-6" \
		--source-url "https://www.motedis.com/shop/products_files/motedis-profile-20x20-b-type-slot-6.zip" \
		--family nut-6 --groove-nominal 6 --groove-depth 5.5 --core-thread M6

build-shelf:
	$(PYTHON) -m slotcad build shelf --width 800 --depth 300 --height 900 --levels 2 \
		--profile 20x20-b-typ-nut-6 --out-dir out --sheet out/shelf.html

build-frame:
	$(PYTHON) -m slotcad build frame --width 600 --height 1200 --rungs 3 \
		--profile 20x20-b-typ-nut-6 --out-dir out --sheet out/frame.html

sheet: build-shelf
	@echo "HTML build sheet: out/shelf.html"

clean:
	rm -rf out .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
