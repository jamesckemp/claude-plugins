---
name: setup-triage
description: Configure the Pings Triage plugin. Use when the user wants to set up triage, configure their Linear team, update analysis settings, customize the user context, or modify plugin settings. Triggers include "setup triage", "configure pings", "change my Linear team", "update triage settings".
---

# Setup Triage

## Overview

This skill helps you configure the Pings Triage plugin for first-time setup or updates to your settings.

## Configuration File Location

The configuration is stored at:
```
pings-triage-plugin/config/user-config.json
```

## Setup Workflow

### 1. Find User's Linear Team

First, help the user identify their Linear team ID. This is **CRITICAL** - the team must be their private team to avoid exposing private information.

Load the Linear provider:
```
mcp__context-a8c__context-a8c-load-provider with provider="linear"
```

List available teams:
```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "linear"
  tool: "list-teams"
  params: {}
```

Ask the user to identify their **private personal team** from the list. Explain:
- This MUST be their private team, not a shared team
- Creating issues in public teams risks exposing private information
- Look for a team with their name or "Personal" in the title

### 2. Gather User Context

Collect information about the user to personalize the analysis:

Ask:
1. **Name**: What's your full name?
2. **Email**: What's your email address?
3. **Role/Title**: What's your role? (e.g., "Core Product Manager for WooCommerce")
4. **Responsibilities**: What are you responsible for? What types of mentions do you typically receive?
5. **Decision Authority**: What decisions can you make? What should you delegate?
6. **Context Notes**: Any other context that would help analyze your pings?

Example user context:
```
- Core Product Manager responsible for WooCommerce product direction and roadmap
- Makes product decisions, not technical implementation decisions
- May be tagged for: product decisions, awareness/FYI, escalations
- Not responsible for: technical implementation, customer support, non-WooCommerce products
```

### 3. Configure Platforms

Ask which platforms they want to enable:

- **Slack**: Enable? Lookback hours? (default: 24)
- **P2**: Enable? Lookback hours? (default: 24)
- **Figma**: Enable? (requires Gmail MCP)

### 4. Update Configuration File

Read the current config:
```python
import json
from pathlib import Path

config_path = Path("pings-triage-plugin/config/user-config.json")
with open(config_path) as f:
    config = json.load(f)
```

Update with user's settings:
```python
config["linear"]["team_id"] = user_linear_team_id
config["user"]["name"] = user_name
config["user"]["email"] = user_email
config["user"]["role"] = user_role
config["user"]["context"] = user_context_description

config["platforms"]["slack"]["enabled"] = slack_enabled
config["platforms"]["slack"]["lookback_hours"] = slack_hours
config["platforms"]["p2"]["enabled"] = p2_enabled
config["platforms"]["p2"]["lookback_hours"] = p2_hours
config["platforms"]["figma"]["enabled"] = figma_enabled
```

Save the updated config:
```python
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
```

### 5. Verify MCP Connections

Verify that required MCPs are connected:

```
✓ context-a8c MCP - Required for Slack, P2, and Linear
✓ Gmail MCP - Optional, needed for Figma notifications
```

If context-a8c is not available, guide the user to connect it.

### 6. Initialize State

Initialize the state database if this is first-time setup:

```python
from pings-triage-plugin.skills.pings-triage.scripts.state_manager import StateManager

sm = StateManager()
print(f"State initialized at: {sm.state_file}")
print(f"Stats: {sm.get_stats()}")
```

### 7. Confirm Setup

Show the user a summary of their configuration:

```
✓ Setup Complete!

**Linear Configuration:**
- Team: {team_name} ({team_id})
- Status for new issues: Triage
- Status for completed: Done

**User Context:**
- Name: {name}
- Email: {email}
- Role: {role}

**Platforms Enabled:**
- Slack: ✓ (24 hours lookback)
- P2: ✓ (24 hours lookback)
- Figma: ✓ (via Gmail)

**Next Steps:**
1. Run "triage my pings" to collect and analyze your mentions
2. Your Linear triage inbox: [Link to team]
```

## Updating Configuration

To update an existing configuration, follow the same workflow but only update the fields the user wants to change:

**Common updates:**
- Change Linear team ID
- Update user context/role
- Enable/disable platforms
- Adjust lookback windows

## Configuration Schema

The complete configuration structure:

```json
{
  "linear": {
    "team_id": "ABC",
    "status_new": "Triage",
    "status_done": "Done",
    "label_prefix": "ping-"
  },
  "platforms": {
    "slack": {
      "enabled": true,
      "lookback_hours": 24
    },
    "p2": {
      "enabled": true,
      "lookback_hours": 24
    },
    "figma": {
      "enabled": true,
      "method": "gmail"
    }
  },
  "analysis": {
    "auto_close_responded": true,
    "thread_detection": true,
    "min_priority": 0
  },
  "user": {
    "name": "Full Name",
    "email": "email@example.com",
    "role": "Job Title",
    "context": "Description of responsibilities, decision authority, and typical mentions"
  }
}
```

## Validation

After configuration, validate:

1. **Linear team exists**: Verify team ID is valid
2. **User context complete**: Name, email, role all provided
3. **At least one platform enabled**: Can't triage with no platforms
4. **MCPs connected**: context-a8c is available

If validation fails, prompt user to fix issues before proceeding.

## Security Notes

- **NEVER create issues in public/shared Linear teams** - only use private personal teams
- User context may contain sensitive information - stored locally only
- State database is local to user's machine
- No data is sent to external services except Linear for issue creation
