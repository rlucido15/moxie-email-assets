#!/bin/bash
# Build the Spanish dictionaries, publish them to the assets repo, pin that commit for the embeds, then rebuild the embeds.
set -e
cd /home/claude/build
python3 es/build.py
R=/home/claude/moxie-email-assets
mkdir -p $R/website/es && cp es/mx-*.json es/app-*.json $R/website/es/
cd $R && git add website/es && (git commit -qm "Spanish dictionaries for page embeds

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_011pe2gqfE6yJzGMJuDAKJUi" || true) && git push -q
git rev-parse --short HEAD > /home/claude/build/es/_cdn.txt
cd /home/claude/build && for f in home buy refi products faqs about cs calc ad lo header footer; do python3 $f.py 2>&1 | tail -1; done
