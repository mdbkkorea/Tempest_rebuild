# dllmain.dll: additive Diary → EGO patch

This documents the final additive Diary patch used by the current restoration setup. It is distinct from the earlier one-byte Adventure redirect. The binary DLL is not distributed here; use your own supported original with the hash-guarded patcher.

## Behavior before and after

Original menu: Adventure, Training, Management, System (or Quest in the alternate branch). The patch adds a separate Diary button linked to existing control ID102 and its dormant EGO handler. Adventure remains ID100 → World. Save/Load remain under System. Management retains its original visibility conditions.

The menu layout is reconstructed using surviving artwork. It is not a verified recreation of the historical unreleased EGO UI. The patch supplies an entry point, not the missing EGO resources: later ADV/LKC/ZMP restoration work is separate.

## Supported binaries

| Variant | Bytes | SHA-256 |
|---|---:|---|
| Original | 974848 | `c011b982ed37f720d418c1092ae989e8f1fdccea7144ba3f9e36002798241416` |
| Earlier Adventure redirect (accepted only for migration) | 974848 | `804ecba6e573f9444e02b12ff8feaead6a77b09e1c07ecac3a3c6872eaccab81` |
| Additive Diary output | 978944 | `9683b154dddd7cdabe87562db6c9f117ac3b74ee37cbd8e98c40db6f5841351a` |

Other DLL versions are unsupported. The tool checks the entire input hash, each edited byte range, and the final output hash; it refuses existing output files and never edits its input.

## Patch mechanism

Preferred image base: `0x10000000`. Original-code locations here have file offset equal to RVA; the newly added section does not.

1. At RVA `0x4A806` (preferred VA `0x1004A806`), replace the six-byte `mov [0x1048DD44],esi` with a relative CALL plus NOP. This hook is after the initializer resets exception-unwind state to−1. The helper replays the replaced selected-ID initialization.
2. Append a105-byte position-independent helper at file offset `0xEE000`, RVA `0x4B0000`, preferred VA `0x104B0000`, in a new read/execute `.diary` section. `helper.hex` contains its exact bytes and `helper_disassembly.txt` explains every instruction. The added raw section occupies4096 bytes, including zero padding.
3. The helper saves flags/registers, uses call/pop to compute the loaded module base, allocates the existing0x74-byte control, and calls original constructor `0x10046360` with ID102 (`0x66`). Null allocation skips the new control and still restores the overwritten initialization. Original constructor/destructor paths register and free the control.
4. Normal mode selects `m_font.spr` frames5/4/4 with highlight20; alternate mode uses13/12/12 with highlight19. No sprite file is edited. Anchor arguments are320,240. Four Management/System Y-anchor arguments move240→297, moving their graphics and hit rectangles together by57 pixels.
5. Neutralize the HIGHLOW relocation covering the overwritten absolute operand. Helper calls are relative and its data operand uses the computed module base. Update the PE section count, SizeOfCode and SizeOfImage. Imports and original callback/dispatch code are unchanged.

## Exact original-file edits

All offsets in this table are hexadecimal **file offsets**; byte strings are in on-disk order.

| Offset | Before | After | Purpose |
|---|---|---|---|
| `0x4a68f` | `f0000000` | `29010000` | Move Management/System anchor down 57 px; label, highlight and hit bounds move together |
| `0x4a6d7` | `f0000000` | `29010000` | Move Management/System anchor down 57 px; label, highlight and hit bounds move together |
| `0x4a7ab` | `f0000000` | `29010000` | Move Management/System anchor down 57 px; label, highlight and hit bounds move together |
| `0x4a7ef` | `f0000000` | `29010000` | Move Management/System anchor down 57 px; label, highlight and hit bounds move together |
| `0x4a806` | `893544dd4810` | `e8f557460090` | Call Diary helper after original SEH state reset; helper replays selected-ID initialization |
| `0xdfb0a` | `0838` | `0808` | Neutralize HIGHLOW relocation for replaced absolute operand |
| `0xe6` | `0400` | `0500` | Add .diary section |
| `0xfc` | `00f00a00` | `00000b00` | Increase SizeOfCode |
| `0x130` | `00004b00` | `00104b00` | Increase SizeOfImage |

At file offset `0x278`, the previously zero40-byte section-header slot becomes:

```text
2e646961727900006900000000004b000010000000e00e0000000000000000000000000020000060
```

Decoded: name`.diary`, VirtualSize105, RVA0x4B0000, SizeOfRawData0x1000, PointerToRawData0xEE000, characteristics0x60000020 (code/read/execute). See `diary/patch_manifest.json` for every edit and the append parameters.

## Historical Adventure redirect

The earlier diagnostic changed file offset `0x4A5C1` from`64` to`66` (ID100→ID102) so Adventure entered EGO. That is superseded. The additive patch keeps this byte`64` and adds Diary separately. If supplied the exact historical diagnostic DLL, the patcher first reverses that one byte and then builds the same final additive patch. **Do not apply the old redirect on top of the Diary patch.**

## Reproduce and undo

Python3 standard library is sufficient. Run on the modern host, with a separate output path:

```sh
python3 dll/diary/patch_tool.py apply /path/to/original/dllmain.dll /path/to/output/dllmain_diary.dll
python3 dll/diary/patch_tool.py undo /path/to/output/dllmain_diary.dll /path/to/output/restored_original.dll
```

Keep `patch_tool.py`, `patch_manifest.json` and `helper.hex` together. Undo reproduces the shipping original, not an earlier experimental DLL. For rollback to any other prior setup, restore your own backup instead.

## Test and install

Do not install over your only copy. Exit Tempest, back up its current DLL outside the game folder, and install a copy of the generated Diary DLL as`dllmain.dll` in a separate test installation. Retain the established EGO resource setup. Run normally in Win98/86Box without live debugging or OllyDbg.

Check Diary enters EGO; independently check Adventure opens World and System retains Save/Load. Check hover/click bounds and returning from EGO. Capture exact errors, menu screenshots and the deployed DLL hash. Roll back with the preserved DLL while the game is closed.

## Evidence and validation

- **Original offline evidence:**40 Unicorn CPU-emulated cases passed, covering two menu branches, Management present/absent, allocation failures, and load bases0x10000000/0x18000000. They exercise original constructors, click callback, ID102 dispatch and recursive destruction; allocation/free and state endpoints are stubbed. This is not full Windows emulation. Archived results are in`diary/emulation_validation.json`.
- **Reproduction now:**the published patch tool was rerun against original and historical diagnostic DLLs; both match the delivered Diary hash, undo matches the original, unsupported input is rejected, and existing outputs are refused. See`diary/publication_validation.json`.
- **User-reported runtime:**the current Diary ID102 setup reaches EGO; all ten character pages open/return; Clausewitz text displays/advances. These reports do not independently establish the deployed DLL hash, every menu branch, or every unrelated menu operation.

`diary/test_patch.py` is the original optional emulation harness. It requires Unicorn2.1.4, a locally generated `dllmain_diary.dll` beside it, and the included sprite geometry metadata. The previous successful run used x86_64 Python under Rosetta after an ARM-native Unicorn host fault. The emulation suite was not rerun during documentation publication. No full DLL, sprite pixels or game prose is included in these patch sources.
