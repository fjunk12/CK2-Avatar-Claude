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
