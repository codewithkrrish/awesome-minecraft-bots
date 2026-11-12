# Contributing

Thanks for helping keep this list useful. It's a small list on purpose — I'd rather have 40 links that work than 400 nobody checked.

## Suggesting a new entry

Open a pull request that adds one line to `README.md` in this format:

```markdown
- [project-name](https://link-to-the-project) — One sentence on what it does and why it's here.
```

Before you open it:

- **The link must work.** Run `python scripts/check_links.py` after adding it.
- **It has to be maintained, or historically important.** A plugin untouched since 2021 that only works on 1.16 doesn't belong here unless it's genuinely the only option.
- **Say why it's here.** If I can't tell from your one-liner what problem it solves, it probably doesn't belong on the list.
- **One entry per PR**, unless the entries are clearly related (like a plugin and its companion).

## Fixing a dead link

If a link 404s or a project moved, a PR that swaps in the new home (or removes the entry, if the project is gone) is very welcome. Same one-line format, same link check.

## What I don't list

- Paid-only tools with no free tier worth mentioning
- Client mods that are just cheat packs (Baritone and Meteor are here because bot devs build on them, not because of the cheating angle)
- My own projects, unless they're genuinely the best option for the job — and then I'll say so in the entry

## Running the checks

```bash
pip install pytest
python -m pytest tests/ -q
python scripts/check_links.py --dry-run   # list links without fetching
python scripts/check_links.py             # check them for real
```
