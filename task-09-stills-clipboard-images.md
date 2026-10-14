# Task 09 — Source real clipboard-style / Google images for the film (the "alive" layer)

**Issue title:** T09 — Image layer: real archival/clipboard-style images in every scene

**Source:** task-main.md — "want to apeal more with real clipboard style images or Google images embed inside each screen where needed to improve better"
**Reference:** The pasted transcript from the documentary-engine session — they built a stills pipeline (Wikimedia Commons search → download → PIL "archival plate" prep → ledger) for the Isdal case.

## What needs to happen

The v1 of our film (The Keeper of Cape Vespers) uses 74 AI-generated images. The user wants real, "clipboard-style" images embedded inside scenes — actual archival photographs presented as evidence-board plates, taped polaroid frames, or document-style cutouts.

This is a huge visual upgrade: instead of every image being AI-generated, key scenes get a real archival image (lighthouse lens, Fresnel lens close-up, Salish Sea chart, 1897-era lighthouse service manual, fog-signal whistle diagram, antique crank handle, ship-in-storm archival footage frame, etc.) presented in a clipboard / evidence-board style.

## Steps

1. Build a stills search tool (`scripts/search_commons.py`) using the Wikimedia Commons API:
   - Search by keyword
   - Filter by license (PD, CC BY, CC BY-SA — only)
   - Return image URL, license, creator, description
2. Build a stills prep tool (`scripts/prep_plate.py`) using PIL:
   - Crop to 16:9 or appropriate aspect
   - Apply cold-archival duotone treatment (cold steel-blue + warm amber)
   - Add film grain + vignette
   - Add a taped/polaroid frame around the image
   - Add a credit label at the bottom
3. Run searches for each scene's "real image" candidates:
   - Fresnel lens close-up (for the lighthouse interior shots)
   - Cape Vespers / Salish Sea / Pacific Northwest lighthouse exteriors
   - Old keeper's logs / journals / handwritten pages
   - Antique brass crank handles
   - Fog-signal whistles / compressed-air horns
   - 1890s-1900s lighthouse keeper portraits (for Marisol's flashback)
   - Wooden docks / boathouses / corrugated-iron sheds
   - Storm at sea / waves on rocks
   - Lighthouse blueprints / schematics
4. Download the candidates, prep them as plates, save to `assets/stills/`.
5. Maintain a license ledger at `assets/stills/LICENSES.md` with creator, license, source URL per image.
6. The new shot list (Task 05) integrates these stills into the scene timeline. Some shots are AI-generated (the actors), some are real archival stills (the objects, the environment, the atmosphere).

## License rules

- Only use images that are explicitly public domain (PD), CC BY, or CC BY-SA.
- Skip anything marked "fair use" or "non-commercial only."
- Document every image's license in the ledger.
- Credit the creator on screen (bottom corner, small text).

## Acceptance

- `scripts/search_commons.py` exists and queries Commons.
- `scripts/prep_plate.py` exists and produces taped archival plates.
- 15-25 real archival stills sourced, prepped, and integrated into the timeline.
- `assets/stills/LICENSES.md` documents every still's license + creator.
- The final film has a visible mix of AI-generated character shots and real archival object/environment plates — a richer, more "alive" visual texture.

## Status

- [ ] Not started
