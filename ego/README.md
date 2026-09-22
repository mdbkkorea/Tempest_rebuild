# EGO tools

The builders use Python 3's standard library. Each locates its `evidence` directory relative to its script. Inputs and generated resources are ignored by Git. On the original workstation these inputs have been copied into the project; a fresh clone needs the locally retained evidence listed below.

## Build

```sh
mkdir -p ego/tools/stage5/Adv ego/tools/stage6/Adv ego/tools/stage6/Link
python3 ego/tools/stage5/build_reader.py
python3 ego/tools/stage6/build_all_characters.py
```

Stage 5 expects `evidence/stage4_working.adv`: the recovered `123.adv` with only its 12-byte map field changed to `E_TOP.zmp` plus NUL padding. Expected SHA-256: `7fbfaef22ee314c2dacee8541ecf6e9d4cca077487377a65de35e6651f509aa3`.

Stage 6 expects:

- `evidence/stage3_blank.adv`: original `_ego.adv`, SHA-256 `5740821c4f1323858ec8c9d6d51b2f77a70c2d098ebf1d3ddf11057476adc927`.
- `evidence/original_ego.lkc`: original global `_ego.lkc`.
- `evidence/stage5_clausewitz.adv`: stage-5 output, SHA-256 `a7c3266f9942d25ddd8713c7f5f4f46abf8734bedb397cf2d86b656d955a7c2c`.

The full historic packages, reports, and evidence are retained locally under `ego/local-archive/session-outputs/`, excluded from Git. Historical generated reports may say runtime pending; STATUS.md and TEST_LOG.md record the later user confirmation.

## Installation and rollback

Use a separate test copy. Exit Tempest, back up existing ADV files and `Link/_ego.lkc`, and note which character ADV files were absent. Install only generated ADV resources and the stage-6 diagnostic LKC. Retain the working Diary ID102 DLL, diagnostic E_TOP.zmp, `_e_s1.adv`, sprites and registry. No debugger or DLL change is required for these resource tests.

Run Diary → 개인 정보. Test each character, text continuation and return. Native return point approximately (80,42) lies inside all ten original return rectangles. After testing, restore backed-up files and remove only newly added files to roll back. Revert the DLL only to undo the separate Diary entry configuration.

## Next research

Search additional formats and alternate/deleted/archive content for other biographies. The four-disc primary ADV scan found only the Clausewitz prototype by the EGO key/map criteria; that is not proof other biographies never existed. Keep raw facts, static interpretations, reconstructed behavior and user runtime observations separate.
