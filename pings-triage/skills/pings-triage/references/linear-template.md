# Linear Issue Template

This document defines how ping triage issues are formatted in Linear.

## Issue Structure

### Team
- Use the configured team ID from user config (default: "JCK" - James Kemp Personal)
- CRITICAL: Never create issues in other teams to prevent exposing private information

### Title
- Format: `{Author Name}: {Brief description of action needed}`
- Examples:
  - "Cvetan Cvetanov: Acknowledge their response"
  - "Elizabeth Bott: Review the Customers design"
  - "Laura Nelson & Poli Gilad: Clarify offline refund process"

### Description
The description is structured with specific sections:

```
{Summary from analysis}

---

**Action:** {Suggested Action}

{Specific Guidance from analysis (if not empty)}

---

{Metadata section with links}
```

### Status
- New issues: "Triage" (default status for incoming pings)
- Completed issues: "Done" (when ping has been responded to or marked complete)

### Assignee
- Always assign to the user (James Kemp)
- Use the configured user ID from Linear

### Priority
- Maps directly from analysis priority (0-4 scale)
- 0 = None
- 1 = Urgent
- 2 = High
- 3 = Normal (default)
- 4 = Low

### Labels
- Each ping gets a unique label with format: `ping-{hash}`
- The hash is derived from the message content and platform to ensure uniqueness
- Labels help track which Linear issue corresponds to which ping
- Example: `ping-0ac94172-e452-4...3d-16bf75fd6942`

## Metadata Section

The metadata section at the bottom of the description contains links back to the original message:

```
**Metadata:**
- [View in Slack](https://automattic.slack.com/archives/CHANNEL/pTIMESTAMP)
- [View in P2](https://example.p2.wordpress.com/posts/123)
- Platform: Slack | P2 | Figma
- Thread ID: {unique thread identifier}
- Ping ID: {unique ping identifier}
```

## Thread Handling

When multiple pings belong to the same conversation thread:

### Option 1: Single Issue with Updates
- Keep one Linear issue for the entire thread
- Update the description when new messages arrive in the thread
- Add a comment to the issue noting the new message
- Update priority if the new message is more urgent

### Option 2: Linked Issues
- Create separate issues but link them as "Related to"
- Use the thread ID to identify which issues belong together
- Parent-child relationship: First ping is parent, follow-ups are children

**Recommended**: Use Option 1 (single issue with updates) to minimize clutter and keep conversation context together.

## Example Issue

**Title**: Cvetan Cvetanov: Acknowledge their response

**Description**:
```
Cvetan thanked you, indicating everything is working as intended. No further action is needed from you at this time.

---

**Action:** Acknowledge

---

**Metadata:**
- [View message](https://automattic.slack.com/archives/C12345/p1234567890)
- Platform: Slack
- Thread ID: slack-C12345-1234567890
- Ping ID: ping-0ac94172-e452-4...3d-16bf75fd6942
```

**Status**: Triage
**Assignee**: James Kemp (jamesckemp)
**Priority**: 4
**Labels**: ping-0ac94172-e452-4...3d-16bf75fd6942

## Auto-closing Rules

Issues should be automatically closed (moved to "Done") when:
1. The user has replied to the message on the original platform
2. The user has reacted to the message with an emoji/like
3. The user manually marks the ping as handled
4. The suggested action was "Acknowledge" and sufficient time has passed (e.g., 24 hours)

When auto-closing, add a comment to the issue noting why it was closed:
- "Automatically closed: Reply detected on {platform}"
- "Automatically closed: Reaction added"
- "Automatically closed: Marked as handled"
