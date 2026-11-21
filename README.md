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

### Ba Sing Se (v0.5)

**Tribute.** Independent Earth realms owe Ba Sing Se according to the crown's *effective authority* and their distance
from the Royal Palace (province 109): under 450 map pixels is near, 450-850 middle, over 850 far.

| Effective authority | Near | Middle | Far |
|---|---|---|---|
| Recognised (dukes 2, kings 4, emperors 8 gold a year) | 1+ | 21+ | 51+ |
| Tribute (dukes 4, kings 8, emperors 16) | 21+ | 51+ | 81+ |
| Obedience (tribute, counts 2, called to defend against foreign attackers) | 61+ | 81+ | never |

- Effective authority = Royal Authority shifted by the main mod's Earth Kingdom unity law (Earth imperialism):
  Disunion (the 560 start, until 602 or the Earth King's story chain) = -30, no obedience; Territories = no change, no obedience; States = +15, obedience possible;
  Monarchism = +30, but resentment fades more slowly. (The main mod requires 100 Royal Authority to change that law,
  so it shifts the tiers instead of capping them.) No obedience under Kyoshi's constitution either.
- All tribute goes into the **treasury of Ba Sing Se**, never to the Earth King personally. Regional kings collect it for
  the crown and gain prestige. Exempt: Way of Chin realms, the Si Wong tribes, barbarians, tributaries (the main mod's own
  "pledge to the Earth King" tributaries), and anyone at war with the Earth King.
- Payers can review, withhold or resume tribute. Withholding costs the crown authority where tribute is expected.

**The treasury.** Ba Sing Se itself pays in 10 gold a year (+10 at Royal Authority 30, +10 at 60), on top of tribute.
For players, all treasury decisions sit behind **Check Possible Works** in the Intrigue tab (press **Return to
Decisions** to hide them again); the AI always sees them. Each yearly run writes a line starting `ATLA Expanded:` to
game.log (crown revenue, tribute, paying and owing realms, treasury, authority). Graft takes 10% a year (3% while the bureaucracy is paid, 5% more while the Dai Li are strong).
A foreign or Way of Chin holder of Ba Sing Se loots it.

| Budget programme (on/off) | Yearly cost | While funded |
|---|---|---|
| Pay the Bureaucracy | 12 | Tax +10%, building cost -10%, graft 3% |
| Fund the Council of Five | 15 | Retinue +300, levies +10%, morale +5% |
| Fund the Dai Li | 10 | Plot power/defence/discovery up, saboteurs caught more often, but Dai Li influence +4 a year |
| Garrison the Borders | 15 | Border provinces: garrison +30%, fort level +1, levy reinforcement +20% |

Unpaid programmes lapse.

| Work (built in yearly stages) | Start | Stages | Once finished | Drawback |
|---|---|---|---|---|
| Royal Messenger Network (Royal Authority 30+, not Disunion) | 200 | 4 x 200 | Distance bands widen (near 650, far 1100) | Upkeep 20/yr, resentment +20 |
| Royal Roads | 100 | 4 x 125 | Earth provinces outside the desert: supply +2, tax +5% | Helps invaders too, upkeep 15/yr, resentment +10 |
| A Single Law for the Kingdom (States or Monarchism law, paid bureaucracy) | 200 | 3 x 200 | Tribute +50%, Royal Authority +5 | Payers -10 opinion, resentment +25 |
| Raise the Outer Wall | 100 | 4 x 100 | Ba Sing Se region: fort level +2, garrison +50%, prestige +100 | Royal Authority -5, resentment +15 |
| Royal Granaries | 100 | 2 x 100 | Ba Sing Se region tax +10%, famine relief at half cost | - |
| Investigate the Dai Li (Dai Li influence 20+, repeatable) | 50 | 2 x 75 | Dai Li influence -30 | - |

- Each year one stage is paid. If the treasury cannot pay, the work stalls; three stalls in a row abandon it.
- Several works can run at once if the treasury allows.
- **Sabotage:** tribute payers and Way of Chin realms of the Earth Kingdom can pay 25 gold to sabotage a running work
  (once every 5 years). It may set a random work back a year, do nothing, or be caught (more likely while the Dai Li are
  funded or strong), in which case the Earth King learns who did it, gains 2 authority and hates the saboteur.
- **Help requests:** far realms (middle or far band) that recognise the crown sometimes ask for help (famine, daofei,
  raiders; at most two requests a year). Helping costs 30-70 gold (Royal Authority +1, resentment -3, their gratitude);
  refusing costs 2 Royal Authority and adds 3 resentment, and the realm may stop paying. When Dai Li influence is 75+,
  requests never reach the king.
- **Resentment** (0-100) rises with great works and refusals, fades 5 a year (3 under Monarchism). Above 25 some states
  stop paying each year. Relief (60) lowers it by 10.
- **Dai Li influence** (0-100) grows while they are funded (+4) or the crown is weak (+2), fades otherwise (-2).
  At 50+ they skim the treasury; at 75+ they intercept requests and may take over the court (Royal Authority -5).
  Purge the Dai Li (100, needs 50+) resets it, at a cost of 5 authority.
- One-off actions: Send Relief (60, every 5 years), Proclaim the Mandate (150, Royal Authority +10, every 10 years),
  Draw on the Treasury (100 -> 50 to your purse, Royal Authority -5, every 2 years).
