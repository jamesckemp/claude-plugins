---
name: analyze
description: Analyze unprocessed pings to determine action needed and priority
skill: pings-triage
---

# Analyze Pings

Categorize and prioritize all unprocessed pings using your personalized user context.

## What it does

For each unprocessed ping:
1. Loads thread context if part of a conversation
2. Applies analysis prompt with your role and responsibilities
3. Determines suggested action: Acknowledge, Review, Reply, Decide, or Delegate
4. Assigns priority 0-4 based on urgency signals
5. Generates summary and specific guidance
6. Stores analysis in state database

## When to use

- After fetching: "I've collected pings, now analyze them"
- Re-analyze after config change: "I updated my context, re-analyze"
- Review before syncing: "Show me the analysis before creating issues"

## Analysis uses your context

The analysis is personalized using your configured:
- Name and role
- Responsibilities and decision authority
- Types of mentions you typically receive

## Output

Breakdown showing:
- Total pings analyzed
- Distribution by action type (Reply, Review, Acknowledge, etc.)
- Distribution by priority (Urgent, High, Normal, Low)
- Examples of high-priority items

## Next steps

After analyzing:
- Run `/sync` to create Linear issues from analysis
- Or run `/triage` next time to do everything at once
