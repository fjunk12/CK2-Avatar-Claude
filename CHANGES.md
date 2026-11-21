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

## Round 2

| # | Problem | File | Fix |
|---|---|---|---|
| 14 | Slave colony CB never created the tributary (GitHub #632): the new ruler was made tributary, then made the attacker's vassal, which breaks the bond (`breaks_on_realm_change = yes`) | `common/cb_types/outlaw_religions_cbs.txt` | New ruler made independent first, then tributary |
| 15 | Roku did not die in the eruption (GitHub #615): the Fire Lord's half of the event needed `HYW_1`, which is usually not set by 818 | `events/ATLA_hundred_year_war.txt` (`ATLAE.10`) | `HYW_1` requirement removed |
| 16 | Killing the Avatar in the Avatar State never ended the cycle, although the manual says it does: nothing set `avatar_cycle_broken` | `events/ATLA_Duel_events.txt`, `events/ATLA_avatar_system.txt`, `events/atlafix_avatar_events.txt` | Using the Avatar State in a duel marks the Avatar for 10 days; dying in that window breaks the cycle (no reincarnation, news event `atlafix.10` to all players) |
| 17 | "Air Nomads survived" (`ATLAE.69`) fired between 840 and 845 even after a successful purge: the temple-destroyed flags `HYW_5`-`HYW_8` are never set | `events/ATLA_hundred_year_war.txt` | Fires only if air faiths still hold an air temple |
| 18 | "Airbender purge started" (`HYW_4`) was never set, so the modifiers that use it never applied | `events/ATLA_hundred_year_war.txt` (`ATLAE.23`) | Set when the Fire Lord launches the purge with the comet |
| 19 | "Recruit the Barbarians" (`imperial_ambitions_22`) was never available: it needed `HYW_8` | `decisions/ATLA_imperialism_decisions.txt` | Needs `HYW_4` and the Northern Air Temple out of Air Nomad hands |
| 20 | Prince's Ambition (`ATLAE.118`, `ATLAE.132`): the fallback "random adult child" always ran and replaced Ozai as the scheming son | `events/ATLA_hundred_year_war.txt` | Fallback only when there is no adult Ozai |
| 21 | Pacifist Air Nomads could take the aggressive "Expand your Realm" ambition (GitHub #608) | `common/objectives/00_ambitions.txt` | Not for the three pacifist air faiths |
| 22 | Earth King's final reform (`earthking.66`) had no option for a ruler of foreign culture holding the Earth Kingdom | `events/ATLA_earthking.txt` | Option B no longer needs Earth Kingdom culture |
| 23 | Rare pet search kept running after "Give up" and could open the success event with no options | `events/ATLA_pets_events.txt` (`PETS.5`) | Search stops once the search flags are cleared |
| 24 | About 120 missing or mistyped text keys: the whole pet shop (`PET.` vs `PETS.`), Avatar notifications and options, Barbarian honour guard, duel tooltips (the base file quotes them), decisions such as Found the Air Nation, Proclaim the Earth Empire, Give to the Sages, Loyalty Campaign, Mandate of the Spirits modifiers, Earth Kingdom Upkeep description (GitHub #597), Earth Monarchy description that still described China (GitHub #609), and the past-lives event whose option texts were shifted by one (abdicating read "There is only one option left") | `localisation/0000_atlafix.csv` | Mistyped keys copy the existing text; the rest is new text. Named `0000_` so it loads before the base mod's files |

### Looked at, not changed

- GitHub #567 ("A New Era" repeating): the current `ATLA_imperial.1` sets a one-time title flag, so this looks fixed by the later rewrite.
- GitHub #36 (crash when warning a suspected plotter): the event chain (63011 and the events it calls) is identical to vanilla. Needs an error.log if it still happens.
- GitHub #620 (crash, division by zero, Earth King start, war path, 582-583): every variable division in the mod divides by a constant. Needs a log or save.
- GitHub #49 (Ozai having children while his wife is imprisoned): no script forces it; pregnancy is handled by the engine.
- GitHub #493 (Royal Earth Palace usurped): the missing titles named in the issue are no longer referenced.
- GitHub #501 (childhood events giving the wrong sub-bending): every sub-bending grant found is checked against the right element.

## Round 3

| # | Problem | File | Fix |
|---|---|---|---|
| 25 | Winning the Avatar's Crisis War never destroyed the defeated realm's kingdom and empire titles: the effect used `any_realm_title`, which does not exist in CK2 (error.log: "Unknown effect-type" at line 1120) | `common/cb_types/03_cb_types_ATLA.txt` (`cb_shatter_realm`) | The ruler's own titles, then every vassal's, the way the same CB's reverse-demand branch already does it |
