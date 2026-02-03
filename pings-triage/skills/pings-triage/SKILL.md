---
name: pings-triage
description: Intelligent notification triage system for managing mentions across Slack, P2, and Figma. Use when the user wants to collect their pings, organize notifications, triage mentions, check their inbox, or manage their Linear triage issues. Automatically deduplicates threads, detects existing responses, and creates organized Linear issues with proper categorization and priority.
---

# Pings Triage

## Overview

This skill helps you collect, analyze, and organize pings (mentions and notifications) from multiple platforms: Slack, P2, and Figma. It solves the common problem of duplicate Linear issues for threaded conversations and automatically detects when you've already responded to messages.

**Core capabilities:**
- Collects mentions from Slack and P2 (via context-a8c MCP) and Figma (via Gmail)
- Deduplicates threaded conversations - no more duplicate issues for follow-up comments
- Analyzes each ping to determine action needed (Reply, Review, Acknowledge, Decide, Delegate) and priority (0-4)
- Detects when you've already responded and auto-closes corresponding Linear issues
- Creates organized Linear issues in your private team with full context and links back to source
- Tracks state between runs to avoid re-processing

## Quick Commands

The plugin supports running individual workflow steps or the complete triage process:

### Complete Triage (Recommended)
**Trigger**: "triage my pings", "run triage", "organize my notifications"

Runs the full workflow:
1. **FETCH**: Collect pings from all enabled platforms
2. **DEDUPE**: Group threads and check for existing responses
3. **ANALYZE**: Categorize and prioritize each ping
4. **SYNC**: Create/update/close Linear issues

### Individual Commands

**FETCH**: "fetch my pings", "collect notifications"
- Only collects new pings from platforms
- Updates state with new mentions
- Useful for just gathering data without analysis

**ANALYZE**: "analyze my pings", "categorize pings"
- Only analyzes unprocessed pings
- Determines action and priority
- Doesn't create Linear issues yet

**SYNC**: "sync to linear", "update linear"
- Only syncs analyzed pings to Linear
- Creates new issues, updates existing, closes responded
- Useful after reviewing analysis results

**SETUP**: "setup triage", "configure pings"
- Initial configuration wizard
- Set Linear team, user context, platform settings
- See `setup-triage` skill for details

### Using Workflow Commands

The workflow commands helper provides Python functions for each command:

```python
from scripts.workflow_commands import TriageWorkflow

workflow = TriageWorkflow()

# Run individual commands
fetch_results = execute_fetch(workflow)
dedupe_results = execute_dedupe(workflow)
analyze_results = execute_analyze(workflow)
sync_results = execute_sync(workflow)

# Or run complete triage
triage_results = execute_triage(workflow)
```

## Workflow

### 1. Initialize and Load Configuration

First, load the user configuration to get Linear team ID and platform settings:

```python
import json
from pathlib import Path

# Load user config
config_path = Path(__file__).parent.parent / "config" / "user-config.json"
with open(config_path) as f:
    config = json.load(f)

linear_team_id = config["linear"]["team_id"]
platforms = config["platforms"]
user_info = config["user"]
```

### 2. Load Required MCPs

The skill requires two MCPs:

```
1. context-a8c MCP for Slack and P2 access
2. Linear MCP for issue management
```

Check if they're available and load them:
```
mcp__context-a8c__context-a8c-load-provider with provider="slack"
mcp__context-a8c__context-a8c-load-provider with provider="wpcom"
```

### 3. Collect Pings from Platforms

Use the state manager to track what's been collected:

```python
from scripts.state_manager import StateManager

sm = StateManager()

# Get last sync times
last_slack_sync = sm.get_last_sync("slack")
last_p2_sync = sm.get_last_sync("p2")
```

#### Slack Collection

Use context-a8c MCP tools to search for mentions:

```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "slack"
  tool: "search-messages"
  params: {
    query: "mentions:@jamesckemp",
    after: <last_sync_timestamp>
  }
```

For each message found:
1. Extract message metadata (channel, timestamp, author, content, thread_ts)
2. Generate thread_id using format: `slack-{channel_id}-{thread_ts}`
3. Check if message has existing replies from user
4. Add to state manager:

```python
ping_id = sm.add_ping(
    platform="slack",
    message_id=msg["ts"],
    timestamp=msg["timestamp"],
    author=msg["user"],
    content=msg["text"],
    thread_id=thread_id,
    metadata={
        "channel_id": msg["channel"],
        "channel_name": msg["channel_name"],
        "permalink": msg["permalink"],
        "reactions": msg.get("reactions", [])
    }
)
```

#### P2 Collection

Similarly collect from P2:

```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "wpcom"
  tool: "search-posts"
  params: {
    mentions: "jamesckemp",
    after: <last_sync_timestamp>
  }
```

Generate thread_id using format: `p2-{site_id}-{post_id}`

#### Figma Collection (Optional)

If Gmail MCP available, search for Figma notification emails:

```
Tool: search_gmail_messages
Parameters:
  query: "from:figma.com (mentioned OR comment)",
  time_min: <last_sync_timestamp>
```

Parse email body to extract file link and comment details.

### 4. Detect Responses and Deduplicate

For each ping, check if user has already responded:

**Slack:**
- Fetch thread messages
- Look for messages from user posted after the mention timestamp
- Check if user reacted to the message

**P2:**
- Fetch post/comment replies
- Look for comments from user after the mention
- Check for user likes

**Figma:**
- Check if user replied to comment (requires Figma API or manual detection)

Mark pings as handled if response detected:
```python
if user_responded:
    sm.mark_ping_responded(ping_id)
```

For threaded conversations:
- Group pings by thread_id
- Only create ONE Linear issue per thread
- Update issue when new messages arrive in thread

### 5. Analyze Pings

For each unprocessed ping, analyze using the analysis prompt logic.

Load the analysis prompt from references:

```python
# Read analysis-prompt.md for detailed instructions
```

For each ping:

```python
from scripts.ping_analyzer import PingAnalyzer

analyzer = PingAnalyzer()

# Get thread context if applicable
thread_pings = sm.get_thread_pings(ping["thread_id"]) if ping["thread_id"] else []

# Format for analysis
formatted = analyzer.format_for_analysis(ping, thread_context=thread_pings[:-1])

# Present to Claude for analysis (Claude should follow analysis-prompt.md)
# Expected output format:
analysis = {
    "title": "Author Name: Action needed",
    "summary": "Brief summary of what the author said/needs",
    "suggested_action": "Acknowledge|Review|Reply|Decide|Delegate",
    "priority": 0-4,
    "specific_guidance": "Additional context or notes"
}

# Validate and normalize
if analyzer.validate_analysis(analysis):
    normalized = analyzer.normalize_analysis(analysis)
    sm.update_ping_analysis(ping_id, normalized)
```

**Analysis Guidelines:**

See `references/analysis-prompt.md` for complete analysis instructions. Key points:

- Default priority is 3 (Normal) unless urgency signals present
- Suggested actions: Acknowledge, Review, Reply, Decide, Delegate
- Priority 1 = Urgent (blocking, deadline today)
- Priority 2 = High (deadline this week, time-sensitive)
- Priority 4 = Low (FYI only, no response needed)

### 6. Sync with Linear

For each analyzed ping, create or update Linear issue.

See `references/linear-template.md` for issue format details.

**Creating New Issue:**

```
Tool: mcp__9de9bba7-6263-489c-b945-4616c5232220__create_issue
Parameters:
  team: <linear_team_id from config>
  title: <analysis.title>
  description: <formatted description with summary, action, guidance, metadata>
  state: "Triage"
  assignee: <user_id>
  priority: <analysis.priority>
  labels: [<ping_id as label>]
```

**Issue Description Format:**

```
{analysis.summary}

---

**Action:** {analysis.suggested_action}

{analysis.specific_guidance (if not empty)}

---

**Metadata:**
- [View in {platform}]({link})
- Platform: {platform}
- Thread ID: {thread_id}
- Ping ID: {ping_id}
```

**Threading Strategy:**

For pings in same thread:
1. Check if thread already has Linear issue (from state)
2. If yes: Update existing issue with comment about new message
3. If no: Create new issue and link to thread

```python
thread = sm.state["threads"].get(thread_id)
if thread and thread.get("linear_issue_id"):
    # Update existing issue
    existing_issue_id = thread["linear_issue_id"]
    # Add comment about new message in thread
else:
    # Create new issue
    # Link to state manager
    sm.link_linear_issue(ping_id, linear_issue_id)
```

**Auto-Closing Issues:**

For pings where response was detected:

```
Tool: mcp__9de9bba7-6263-489c-b945-4616c5232220__update_issue
Parameters:
  id: <linear_issue_id>
  state: "Done"
```

Add comment explaining auto-close:
```
Tool: mcp__9de9bba7-6263-489c-b945-4616c5232220__create_comment
Parameters:
  issueId: <linear_issue_id>
  body: "Automatically closed: Reply detected on {platform}"
```

### 7. Present Results

Show user a summary of what was processed:

```
## Pings Triage Results

**Collected:**
- Slack: X new mentions
- P2: Y new mentions
- Figma: Z new notifications

**Analysis:**
- Priority 1 (Urgent): N pings
- Priority 2 (High): N pings
- Priority 3 (Normal): N pings
- Priority 4 (Low): N pings

**Actions:**
- Created X new Linear issues
- Updated Y existing issues
- Auto-closed Z issues (responses detected)

**Your Linear triage inbox:**
[Link to Linear team inbox]
```

## Configuration

### User Configuration

Edit `config/user-config.json` to customize:

- **linear.team_id**: Your Linear team ID (CRITICAL - must be your private team)
- **platforms**: Enable/disable each platform and set lookback period
- **analysis.auto_close_responded**: Auto-close issues when responses detected
- **user**: Your name, email, and role for analysis context

### State Management

State is persisted in `~/.pings-triage/state.json` and tracks:
- All collected pings with analysis
- Thread groupings
- Linear issue mappings
- Last sync timestamps
- Response detection status

State is automatically managed by `state_manager.py`.

## Scripts

### state_manager.py
Manages persistent state database. Tracks pings, threads, Linear issues, and sync timestamps.

Key methods:
- `add_ping()`: Add new ping to state
- `update_ping_analysis()`: Store analysis results
- `mark_ping_responded()`: Mark ping as handled
- `link_linear_issue()`: Connect ping to Linear issue
- `get_thread_pings()`: Get all pings in a thread

### ping_analyzer.py
Formats pings for analysis and validates results.

Key methods:
- `format_for_analysis()`: Prepare ping for LLM analysis
- `validate_analysis()`: Ensure analysis has required fields
- `extract_urgency_signals()`: Detect urgency keywords
- `normalize_analysis()`: Standardize analysis format

## References

### analysis-prompt.md
Complete instructions for analyzing pings. Defines voice/tone, action types, priority rules, and output format. **Read this file when performing analysis.**

### linear-template.md
Defines Linear issue structure, including title format, description layout, status, priority mapping, threading strategy, and auto-close rules. **Reference when creating/updating Linear issues.**

### platform-guide.md
Technical guide for interacting with each platform (Slack, P2, Figma). Covers MCP tool usage, response detection, thread identification, and metadata extraction. **Reference when collecting pings or checking responses.**

## Troubleshooting

**No pings collected:**
- Verify MCPs are connected (context-a8c, Linear)
- Check last_sync timestamps in state
- Verify platform configurations are enabled

**Duplicate Linear issues:**
- Check that thread_id is being generated correctly
- Verify state manager is tracking threads properly
- Ensure existing issue lookup is working

**Wrong Linear team:**
- CRITICAL: Verify linear.team_id in config matches your private team
- Never create issues in public teams - privacy risk

**Analysis errors:**
- Ensure analysis-prompt.md is being followed
- Validate analysis output has all required fields
- Check priority is 0-4 integer

**Response detection not working:**
- Verify platform API access for reading threads
- Check timestamp comparison logic
- Ensure user ID matching is correct
