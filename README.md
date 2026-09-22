# Tempest Rebuild

Rebuilding The War of Genesis: Tempest.

Evidence-based preservation and restoration tools for Tempest, with the current focus on its dormant EGO information mode.

## Working baseline

User-reported Windows 98 / 86Box tests confirm Diary → ID102 → EGO, access and return for all ten character pages, and readable Korean text with working progression for Clausewitz. Adventure remains ID100. Save and Load remain under System.

Only Clausewitz currently has recovered biography content: eleven passages found in the shipped `123.adv` prototype. The remaining nine pages are explicitly labeled navigation diagnostics, not recovered biographies. The dialogue presentation is reconstructed, not established original EGO design.

## Files

- `dll/README.md`: exact Diary DLL changes, reproducible patching, and rollback.
- `STATUS.md`: evidence status and next steps.
- `TEST_LOG.md`: offline and user-reported runtime results.
- `ego/tools/stage5/build_reader.py`: reproducible Clausewitz reader builder.
- `ego/tools/stage6/build_all_characters.py`: all-character diagnostic builder.
- `ego/README.md`: required local inputs and rebuilding.

Original game assets, recovered game prose, disk images and generated binary packages are not distributed here. Supply your own local evidence. Preserve originals and test separate copies. Do not use live breakpoints or OllyDbg with this Win98/86Box setup.
