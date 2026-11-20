# ATLA Fixes - changes

All edits are marked `# ATLA Fixes` in the files.

| # | Problem | File | Fix |
|---|---|---|---|
| 1 | "Send a family member to Team Avatar" showed an empty list: the candidate had to be of the **Avatar's** dynasty and in the Avatar's court (`ROOT`) | `decisions/ATLA_avatar_decisions.txt` | Candidate must be of the sender's dynasty and court (`FROM`) |
| 2 | Combustion benders lost combustion bending when they gained lightning, blue flames, smoke or inner flame (opposite traits are removed automatically) | `events/ATLA_bending.txt`, `ATLA_bloodline_events.txt`, `ATLA_society_agni_kai.txt`, `ATLA_random_events.txt`, `ATLA_special.txt` | All 10 unguarded grants skip combustion benders |
| 3 | Spiritual journeys disappeared for the rest of the game once the Hundred Year War flag `HYW_0` was set (never cleared; set at start in the 830, 850, 918 and 928 bookmarks). Northern Water Tribe faith not allowed | `decisions/ATLA_religious_decisions.txt` | `HYW_0` block removed; `tui_and_la` added |
| 4 | Reincarnation is a 16-year delayed event on a random player character; it is lost if that character dies (or in observe mode), so no Avatar returns | `events/atlafix_avatar_events.txt`, `common/on_actions/zz_atlafix_on_actions.txt` | Yearly safety net: if no Avatar is alive 18+ years after the last one died, the next one spawns |
| 5 | Noble-born Avatar check (`NAE.002`) could create a second Avatar next to a living canon Avatar (canon spawns never clear `avatar_interregnum`) | `events/ATLA_avatar_system.txt` | `NAE.002` and `NAE.004` only run while no Avatar is alive |
| 6 | Peasant Avatar could spawn in an empty, ownerless province | `events/ATLA_avatar_system.txt` | Spawn province must have an owner |
| 7 | `NAE.004` used `new_character` for a character created in another event; air nomad gender rule lived there | `events/ATLA_avatar_system.txt` | Stale block removed, gender rule moved to `NAE.0041` |
| 8 | Sozin's Comet (`ATLAE.23`): a Fire Lord holding `e_fire_nation` before `HYW_15` (or the reverse) had no option; the Fire Lord's buff ignored firebending | `events/ATLA_hundred_year_war.txt` | Options cover every case; buff only for firebenders |
| 9 | Water tribes could build castles but never convert a tribal holding (decision required `is_feudal`) | `decisions/settlement_decisions.txt` | `water_tribe_government` allowed |
| 10 | Water tribe vassals ignored calls to arms (GitHub #125) | `common/governments/tribal_governments.txt` | `water_tribe_government` added to `vassal_call_to_arms` (probable cause) |
| 11 | Warrior lodge duel called a non-existent event `HF.10095` | `decisions/hf_warrior_lodge_decisions.txt` | `HFP.10095` |
| 12 | Air nomad war CBs checked laws with `realm = { has_law }`, which does not work from a character | `common/cb_types/03_cb_types_ATLA.txt` | `primary_title = { has_law }`, as the mod's own events do (probable cause of air temples being unable to use their CBs) |
| 13 | Crash to desktop when hovering Avatar help options (e.g. Provide Military Support): `new_character` in the tooltip before the character exists | `events/ATLA_avatar_interfere_events.txt` | Those 4 blocks hidden from the tooltip (probable cause) |
