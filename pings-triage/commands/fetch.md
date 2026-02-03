---
name: fetch
description: Collect new pings from all enabled platforms without analyzing or syncing
skill: pings-triage
---

# Fetch Pings

Collect new mentions and notifications from enabled platforms without analyzing or creating Linear issues.

## What it does

Queries each enabled platform for new mentions:
- **Slack**: Searches for messages where you're mentioned
- **P2**: Searches for posts/comments with your @mention
- **Figma**: Checks Gmail for Figma notification emails

Updates the state database with new pings but doesn't analyze them yet.

## When to use

- Pre-analysis review: "Let me see what's out there before analyzing"
- Collecting data for later: "Fetch my pings while I'm in this meeting"
- Testing platform connections: "Make sure fetch is working"

## Output

Summary showing:
- Number of pings collected per platform
- Time range queried (based on lookback hours setting)
- Total unprocessed pings in state

## Next steps

After fetching:
- Run `/analyze` to categorize the pings
- Run `/sync` to create Linear issues
- Or run `/triage` to do everything at once
