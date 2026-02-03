---
name: triage
description: Run the complete ping triage workflow - collect, deduplicate, analyze, and sync to Linear
skill: pings-triage
---

# Triage Pings

Run the complete notification triage workflow across all enabled platforms.

## What it does

1. **FETCH**: Collects new mentions from Slack, P2, and Figma
2. **DEDUPE**: Groups threaded conversations and checks for existing responses
3. **ANALYZE**: Categorizes each ping by action (Reply, Review, Acknowledge, Decide, Delegate) and priority (0-4)
4. **SYNC**: Creates/updates/closes Linear issues in your triage inbox

## When to use

- Daily triage routine: "Run /triage to organize my pings"
- After being away: "I haven't triaged in a few days, run /triage"
- Quick check-in: "What new pings do I have? Run /triage"

## Prerequisites

- Plugin configured with `/setup` command
- context-a8c MCP connected (Slack, P2, Linear)
- Linear team ID set to your private team

## Output

You'll receive:
- Summary of pings collected per platform
- Breakdown by priority (Urgent, High, Normal, Low)
- Count of Linear issues created/updated/closed
- Link to your Linear triage inbox

## Options

Run individual steps instead:
- `/fetch` - Just collect pings
- `/analyze` - Just analyze unprocessed pings
- `/sync` - Just sync to Linear
