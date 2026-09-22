# Tempest Rebuild — project direction and staged roadmap

Status: planning proposal based on the user's stated goals. No battle redesign or engine migration has been implemented or authorized for installation by this document. Existing Stage 6 remains the working baseline.

## Goals

1. Reuse as much surviving Tempest material and working behavior as practical.
2. Restore EGO as far as the evidence allows.
3. Explore replacing Macbeth combat with an SRPG system influenced by the other Genesis games, while preserving a stage-like presentation and compact, isolated battlefields.
4. Treat flying enemies as a meaningful tactical category, including clear rules for ground characters' ability to engage them.
5. If the original engine cannot reasonably support the design, consider Godot or another modern engine while reusing Tempest's original characters, graphics and available content.

“Original sources” currently means the available game binaries, scripts, graphics, data and recovered behavior. Availability of original engine source code has not been established. Patching a compiled DLL and rebuilding an engine from source are different levels of work.

## Evidence versus proposed design

User-confirmed: Diary → ID102 → EGO; all ten character routes open and return; Clausewitz's recovered Korean text displays and advances. Nine other character pages remain diagnostic notices. These results do not establish a fully restored EGO system or tactical-combat feasibility.

Reference images supplied by the user: one shows a contained airship hub; the other shows an isolated elevated battlefield with a movement/attack grid, turn information and action previews. The proposal borrows spatial containment and tactical readability. It does not assume those screenshots establish the mechanics of a specific Genesis game or require their block-style artwork.

User-reported current restriction: land-based characters cannot attack flying enemies. The engine condition responsible has not yet been traced. The exact meaning of Macbeth's intended stage feeling has not been historically established here. Working design assumption: preserve both theatrical presentation and compact arenas; this remains open to the user's preference.

## Recommended structure

Maintain two clearly identified products sharing extraction and research tools:

- **Original-engine restoration:** original campaign and graphics, additive Diary access, evidence-based EGO restoration, reversible patches.
- **Battle redesign experiment:** small tactical prototypes with explicit new rules. It must prove its value and integration before replacing any campaign combat.

A modern-engine experiment is a fallback for the redesign, not a reason to abandon the original-engine preservation build. A modern-engine implementation would be a reimplementation, not a claim that the original executable has been recovered.

## Phase 0 — make the existing work reproducible

Deliver one host-side builder accepting a user's original game installation/disc folders. It checks supported hashes, extracts or locates required inputs, builds the Diary patch, derives E_TOP from its validated donor, creates the EGO ADV/LKC resources, and writes a separate installation package with manifest and rollback instructions. It must not depend on unpublished intermediate files from a developer's workstation.

Input inventory includes original dllmain.dll, _ego.adv, _ego.lkc, surviving 123.adv, the validated V_BG02.zmp donor and the required SPR/registry resources. Exact locations and supported variants must be checked before implementation. No generic compatibility with every edition is implied.

Acceptance: reproduce the accepted hashes from original inputs on a clean folder; refuse unsupported inputs and overwrites; preserve originals; install instructions use Diary ID102; a user can follow the guide without understanding binary offsets. Keep proprietary inputs and generated full game binaries outside the public repository. Portable export formats retain source file hashes, record offsets and unknown fields.

## Phase 1 — continue EGO recovery

Create a content matrix for all character, political, family and event routes: original menu label, dependencies, recovered text/images, evidence source, reconstructed UI, unknowns and runtime status. Navigation notices must never count as recovered content.

Search surviving scripts, registries and asset banks, then prioritize archive interiors or alternate/deleted content where there is a concrete lead. Distinguish original facts, text from story dialogue, and genuinely missing descriptions; do not manufacture biographies to fill the matrix. Preserve story-unlock conditions in the normal restoration; keep the all-visible menu explicitly a diagnostic variant.

Acceptance: each new restoration has source provenance and a separate runtime check. Improve the Clausewitz reader's usability only after the provenance/rebuild baseline is complete. EGO completeness is not a prerequisite for the bounded combat feasibility study.

## Phase 2 — bounded original-engine combat audit

First document one existing battle by static analysis and normal Win98 execution. Record turn/timing behavior, actor storage, movement, target eligibility, animation dispatch, damage/status handling, enemy AI, victory/defeat and story return. Use a ground enemy and flying enemy as comparison cases. Do not infer capabilities from menu hooks alone.

For each capability below, deliver addresses/offsets where established, source evidence, a minimal reversible experiment and its result:

| Requirement | Evidence/proof needed |
|---|---|
| Exclusive turns | Pause/resume non-active units without breaking animation, UI or script timing |
| Tactical positioning | Identify coordinates, occupancy/collision, route finding and safe movement completion |
| Explicit actions | Select a unit and valid target, perform one action, then reliably finish its turn |
| Ground/air targeting | Locate and independently control movement mode and target eligibility |
| Enemy turn | One enemy chooses a legal reachable action and terminates its turn |
| Battle lifecycle | Enter a bounded encounter, win/lose, and return to a controlled story context |
| Campaign integrity | Relevant party state, resources and rewards are preserved; save/load effects understood |

Bound the study to one encounter and these questions. Review results after the first documented audit and one minimal turn-control probe; do not escalate indefinitely into reconstructing the whole engine. An unresolved result is “not demonstrated,” not “impossible.”

**Continue original-engine redesign only if** the required hooks can be understood, changed reversibly and tested repeatedly without compromising story progression or saves. UI readability and maintainability matter as much as whether a single patch runs.

**Move the battle prototype to a modern engine if** essential turn/position/target/lifecycle control remains unreliable, or the proposed patch effectively replaces most combat logic while remaining harder to test than a separate implementation. Record the failed or costly requirements before deciding. Reconsider an audit extension with the user if evidence is promising but incomplete.

## Phase 3 — one complete small tactical battle

Suggested starting parameters, not final balance: a roughly12×10 board, three player characters (melee, ranged, support), two ground enemies and one flying enemy. Use one simple arena, four-direction movement and one blocking terrain feature. Start with flat terrain. Height variation and complex combos are later additions.

Initial rules: player phase then enemy phase; each unit moves and takes one action, or waits; show movement range, target validity and an honest attack preview before confirmation. Keep battle calculations separate from animations so dramatic presentation does not control the rules. Do not silently import every mechanic from another Genesis title; choose the specific reference game and desired turn model before expanding.

The complete playable loop is deployment → player actions → enemy actions → victory/defeat → result. Test a return-to-story context. In Godot, a mock result screen is only an internal prototype milestone; it is not proof of integration with the original game.

Acceptance: the user can understand whose turn it is, why an attack is legal/illegal and how to defeat the flyer; no overlapping occupancy, stuck turns or unwinnable last-enemy state; retries behave consistently; supported asset frames play without inventing missing directional artwork. Capture both ordinary play and edge cases.

## Preserving the stage-like feel

Proposed interpretation: battles feel like directed scenes within Tempest, rather than anonymous large tactical maps.

- Bounded arenas with a readable stage edge, distinct entrance points and deliberate opening formations.
- Original Tempest sprites, portraits, backgrounds and attack effects where decoded and usable.
- A fixed or tightly controlled viewing angle suited to available sprite directions.
- Short entrances, reaction moments, dialogue and dramatic attacks; allow skipping or speeding up repeated animation.
- Meaningful objectives such as holding a position, reaching an exit or interrupting an enemy action, after the basic battle works.
- Grid/range overlays appear for decisions; visual staging remains readable when overlays are hidden.

No full 3D art conversion or rotating camera is required for the initial prototype. Existing flat backgrounds are not automatically navigable 3D environments; a 3D arena would require geometry, collision and occlusion work.

## Flying enemies — proposed first rules

Separate **movement mode**, **targetable state**, and **terrain height**. A character standing on high ground is not the same as a flying character. For the first battle use only grounded/airborne states, without arbitrary altitude levels or stacking ground and air units on the same board cell.

| Action | Grounded target | Airborne target |
|---|---|---|
| Ordinary melee | Allowed when in range | Not allowed; explain why before selection |
| Bow/gun or explicitly anti-air skill | Allowed if skill permits | Allowed within its declared range and line-of-sight rules |
| Ordinary magic | Defined per skill | Defined per skill; not automatically universal |
| Grounding/support action | Normal specified effect | Can create a temporary grounded vulnerability if the skill permits |
| Waiting/defending | Available | Available; can prepare for a telegraphed landing opportunity |

A flyer can bypass designated ground obstacles, but still obey arena bounds and legal end positions. Display its occupied cell and airborne status clearly. Use a telegraphed dive/landing or a grounding mechanism to give melee units a role without granting every sword unlimited air reach. These are proposed new mechanics, not recovered Tempest rules.

Avoid an anti-air softlock: before accepting deployment, ensure at least one viable counter or a universal encounter mechanic. Test losing the last ranged unit, exhausting magic, blocked landing cells, flyers at the boundary, and an airborne final enemy. Any forced landing must choose a legal cell deterministically or defer safely; never place units outside the arena or on an occupied cell. Enemy AI must evaluate the same rules as the player.

## Phase 4 — engine decision and integration

If the original engine passes the gate, integrate only the tested battle type first. Validate story transitions, rewards and save compatibility before converting additional encounters. Keep the original combat build available for comparison and rollback.

If it fails the gate, Godot is the first modern-engine candidate, not an irrevocable choice. Prefer 2D/isometric sprites initially; optionally test sprites on a simple3D stage if that substantially improves the desired presentation. Godot provides grid pathfinding and Sprite3D support, but it does not supply Tempest rules, script compatibility or an automatic battle-system replacement.

A Godot route targets modern desktop systems. Do not assume Windows98 support; the original restoration remains the Win98 preservation route. Decide modern platform targets and minimum hardware before choosing renderer/export settings.

A standalone tactical demo can consume exported original assets, character data and a documented encounter description. Exporters should preserve original identifiers, provenance and unknown fields independently of the rendering engine. Original ADV commands need documented interpretation or explicit conversion; an engine switch does not make unknown script semantics disappear.

Only after the battle is convincing should we choose between a modern standalone reconstruction and a proven integration boundary. Do not promise launching Godot from the Win98 game or transparently sharing its saves. Replacing only combat across two engines requires a separately proven state-transfer, launch and return interface.

## Phase 5 — a representative campaign segment

Rebuild or adapt one short segment containing dialogue, exploration/management, an EGO update, a tactical battle, rewards and save/reload. Verify original character identity, story continuity, audio/font behavior and asset provenance. Then expand encounter by encounter. A full Tempest reimplementation includes much more than combat: scripts, inventory, progression, triggers, menus, saves, audio and localization.

## Immediate work order

1. Complete the reproducible original-input builder and capture the current baseline with exact deployed hashes.
2. Build the EGO content/dependency matrix and select the strongest recovery lead.
3. Audit one existing Macbeth battle, especially turn control and the air-target restriction.
4. Review the gate; build one tactical battle in the justified engine.
5. Have the user evaluate readability, pace, stage feeling and flyer counterplay before adding features.

This plan deliberately uses demonstrated milestones instead of promising dates for unknown reverse engineering. Planning approval does not itself select an engine or authorize installation into a live game copy.

## Official engine references

- Godot AStarGrid2D: https://docs.godotengine.org/en/stable/classes/class_astargrid2d.html
- Godot Sprite3D: https://docs.godotengine.org/en/stable/classes/class_sprite3d.html
- Godot system requirements: https://docs.godotengine.org/en/stable/about/system_requirements.html

These establish available engine building blocks and platform requirements, not feasibility of converting Tempest. The engine recommendation is an engineering proposal based on the stated reuse and tactical-design goals.
