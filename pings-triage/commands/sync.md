---
name: sync
description: Sync analyzed pings to Linear - create new issues, update existing, and auto-close responded
skill: pings-triage
---

# Sync to Linear

Create, update, and close Linear issues based on analyzed pings.

## What it does

For analyzed pings:
- **Create**: New Linear issues for untracked pings
- **Update**: Adds comments when new messages arrive in existing threads
- **Close**: Auto-closes issues when you've already responded (if enabled)

Each Linear issue includes:
- Title with author and action needed
- Summary of what they need from you
- Suggested action and priority
- Link back to original message
- Unique label for tracking

## When to use

- After analyzing: "Analysis looks good, sync to Linear"
- Periodic sync: "Sync any new pings to Linear"
- After replying manually: "Check which issues can be auto-closed"

## Threading strategy

Pings in the same conversation are handled intelligently:
- First ping creates a Linear issue
- Follow-up pings add comments to existing issue (not new issues!)
- Prevents duplicate issues for threaded conversations

## Auto-close behavior

If enabled in config (`auto_close_responded: true`):
- Detects when you've replied on the platform
- Detects when you've reacted with emoji/like
- Automatically moves Linear issue to "Done"
- Adds comment explaining why it was closed

## Output

Summary showing:
- Linear issues created (with links)
- Linear issues updated
- Linear issues auto-closed
- Link to your triage inbox

## Safety

**CRITICAL**: Only creates issues in your configured private team to protect information privacy.
