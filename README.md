# CK2-Avatar-Claude

Fixes and (later) expansions for **Avatar - Four Nations Restored**, the Avatar: The Last Airbender mod for Crusader Kings II.

## ATLA Fixes (submod)

Install: copy `ATLA Fixes.mod` and the `ATLA Fixes` folder into
`Documents/Paradox Interactive/Crusader Kings II/mod/` and enable **ATLA Fixes** together with **Avatar - Four Nations Restored**.
The `.mod` declares the main mod as a dependency, so it loads after it.

Built against the GitHub master of [Rystic/ATLA-restored](https://github.com/Rystic/ATLA-restored) at commit `cf387c7` (24 Feb 2025).
The submod overrides whole files, so if the main mod changes one of these files later the submod must be rebuilt from the new version.
Not yet tested in game.

Works with existing saves: no new traits or titles. Changes to events that are already queued in a save apply the next time they fire.

The Python builder in `tools/` regenerates the submod from a clean copy of the main mod:
`python3 -I tools/build.py <main mod folder> <output folder>` (round 1 and 2 file edits) and
`python3 -I tools/mkloc.py <main mod folder> <output>/localisation/0000_atlafix.csv`.
The two hand-written files (`events/atlafix_avatar_events.txt`, `common/on_actions/zz_atlafix_on_actions.txt`) live only in this repo.

See [CHANGES.md](CHANGES.md) for every fix and where it is.

## ATLA Expanded (submod, separate from the fixes)

New content for the Fire Nation and Earth Kingdom regions (including the Si Wong Desert and the Sun Warriors).
Install like ATLA Fixes: copy `ATLA Expanded.mod` and the `ATLA Expanded` folder into the mod folder and enable it
with the main mod. It does not need ATLA Fixes and does not override any file of the main mod. Not yet tested in game.

### v0.1: Ba Sing Se's tribute
- Independent Earth realms owe Ba Sing Se according to the Earth King's Royal Authority and their distance from the
  Royal Palace (province 109): under 450 map pixels is near, 450-850 middle, over 850 far.

| Royal Authority | Near | Middle | Far |
|---|---|---|---|
| Recognised (dukes 2, kings 4, emperors 8 gold a year) | 1+ | 21+ | 51+ |
| Tribute (dukes 4, kings 8, emperors 16) | 21+ | 51+ | 81+ |
| Obedience (tribute, counts 2, called to defend against foreign attackers) | 61+ | 81+ | never |

- No obedience while Kyoshi's constitution is in force (the main mod's `kyoshi_parliamental_monarch` flag).
- Exempt: Way of Chin realms, Si Wong tribes (sandbender culture or Si Wong faith, or a capital in the desert),
  barbarians, tributaries and anyone at war with the Earth King. The collector must be an Earth Kingdom ruler of an
  Earth faith holding the Earth Kingdom (a foreign or Chin conqueror of Ba Sing Se collects nothing).
- All tribute goes into the **treasury of Ba Sing Se** (a global variable), never to the Earth King personally.
- Regional kings: if a payer's capital lies in the de jure kingdom of another independent Earth ruler of king tier or
  higher, that ruler collects it for the crown and gains prestige.
- Decisions for payers: "Ba Sing Se and Us" (shows the current obligation), "Withhold Tribute" (each year where tribute
  is expected: Royal Authority -1, the Earth King's opinion -20, some prestige for the defier), "Resume Tribute".
- Refusing a call to arms: prestige -50, Royal Authority -3, the Earth King's opinion -40.

### v0.2: the treasury of Ba Sing Se
The ruler of Ba Sing Se spends the treasury through decisions. Projects last ten years and carry over to the next ruler.

| Decision | Cost | Effect |
|---|---|---|
| Strengthen the Borders | 100 | Every border province of the realm: garrison +30%, fort level +1, levy reinforcement +20%, for 10 years |
| Reform the Bureaucracy | 100 | Tax +10%, building cost -10%, and graft on the treasury drops from 10% to 3% a year |
| Fund the Council of Five | 120 | Retinue +300, levies +10%, morale +5% |
| Fund the Dai Li | 80 | Plot power +15%, plot defence +30%, plot discovery +20% |
| Send Relief to the Provinces | 60 | Every tribute-owing ruler +15 opinion of the crown for 5 years, Royal Authority +3 (every 5 years) |
| Proclaim the Mandate | 150 | Royal Authority +10 (every 10 years) |
| Draw on the Treasury | 100 | 50 gold to your own purse, Royal Authority -5 (every 2 years) |
| The Treasury of Ba Sing Se | - | Shows the balance |

- Graft: the treasury loses 10% a year (3% with a reformed bureaucracy).
- If a foreign power or a Way of Chin ruler holds Ba Sing Se, they loot the whole treasury into their own purse.
