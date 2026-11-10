# Moxie website embed generators

Python scripts that generate the Lofty Custom Code embeds in `website/embeds/`.

## Setup (fresh workspace)
```bash
git clone https://github.com/rlucido15/moxie-email-assets /home/claude/moxie-email-assets
mkdir -p /home/claude/build/out /home/claude/work
cp /home/claude/moxie-email-assets/build/*.py /home/claude/build/
cp /home/claude/moxie-email-assets/build/work/* /home/claude/work/
npm i --prefix /tmp/jsmin terser        # optimize.py minifies JS with terser
```
Scripts use absolute paths (`/home/claude/build/out`, `/home/claude/work`), so keep this layout.

## Build
`cd /home/claude/build && python3 <page>.py`, output goes to `out/`. Pages: buy, refi, products, faqs, footer,
home, about, calc (hub + 3 calculator pages), cs (client success), ad (Area Director; reads the canvas design `AreaDirector.dc.html`, snapshot in `work/`).

## Client success stories
Data: `work/stories.py` (`STORIES` list + `FEATURED`). Add a tuple per new story:
`(slug, title, who, where, one-line summary, [tags], outcome chip)`. Tags: first, refi, va, special, invest, move, hawaii, credit.
Rebuild with `python3 cs.py`, then copy `out/moxie-client-success-embed.html` to `website/embeds/` and commit.
After building, copy changed `work/*` files back into `build/work/` here and commit so the next run starts current.
