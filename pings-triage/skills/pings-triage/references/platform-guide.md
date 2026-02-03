# Platform Integration Guide

This document explains how to interact with each platform to collect pings, check responses, and perform actions.

## Slack (via context-a8c MCP)

### Loading the Provider
```
context-a8c-load-provider with provider: "slack"
```

### Collecting Mentions
Use the Slack search tool to find messages where the user was mentioned:
```
Tool: search-slack-messages
Parameters:
  query: "@james.kemp" or "mentions:me"
  time_range: Last 24 hours (configurable)
```

### Checking for Responses
To determine if the user has already responded to a message:
1. Fetch the thread using thread ID
2. Check if any messages in thread are from the user
3. Check if user has reacted to the message

### Getting Thread Context
```
Tool: get-slack-thread
Parameters:
  channel_id: {channel}
  thread_ts: {timestamp}
```

### Sending Reactions
```
Tool: add-slack-reaction
Parameters:
  channel: {channel_id}
  timestamp: {message_ts}
  emoji: "thumbsup" | "eyes" | "white_check_mark"
```

### Replying to Messages
```
Tool: send-slack-message
Parameters:
  channel: {channel_id}
  thread_ts: {original_timestamp}
  text: {reply_content}
```

### Metadata to Extract
- Channel ID and name
- Message timestamp (for threading)
- Thread timestamp (if part of thread)
- Author name and ID
- Message text and attachments
- Existing reactions
- Thread participants

## P2 (via context-a8c MCP)

### Loading the Provider
```
context-a8c-load-provider with provider: "wpcom"
```

### Collecting Mentions
Use P2 search to find posts/comments where user was mentioned:
```
Tool: search-p2-mentions
Parameters:
  user: "jamesckemp"
  time_range: Last 24 hours (configurable)
```

### Checking for Responses
To determine if the user has already responded:
1. Fetch the post/comment thread
2. Check if any replies are from the user
3. Check for user's likes/reactions

### Getting Thread Context
```
Tool: get-p2-post
Parameters:
  post_id: {post_id}
  include_comments: true
```

### Sending Reactions/Likes
```
Tool: like-p2-post
Parameters:
  post_id: {post_id}
  comment_id: {comment_id (optional)}
```

### Replying to Posts/Comments
```
Tool: create-p2-comment
Parameters:
  post_id: {post_id}
  parent_comment_id: {comment_id (if replying to comment)}
  content: {reply_content}
```

### Metadata to Extract
- P2 site URL
- Post ID and URL
- Comment ID (if applicable)
- Author name and username
- Post/comment content
- Thread structure (parent/child relationships)
- Existing likes/reactions

## Figma (via Gmail MCP)

Figma doesn't have a direct MCP integration, but notifications are sent via email.

### Loading the Provider
```
Load Gmail MCP (if available)
```

### Collecting Mentions
Search Gmail for Figma notification emails:
```
Tool: search-gmail-messages
Parameters:
  query: "from:figma.com mentions OR comments"
  time_range: Last 24 hours (configurable)
```

### Email Patterns
Figma sends notification emails with specific patterns:
- Subject: "You have new comments in {File Name}"
- Subject: "{Person} mentioned you in {File Name}"
- Body contains links to specific comments in format:
  `https://www.figma.com/file/{file_id}/{file_name}?node-id={node_id}`

### Extracting Information
Parse the email body to extract:
- File name
- Author name
- Comment text
- Link to comment in Figma

### Limitations
- Cannot directly reply or react via Figma API
- Users need to click through to Figma to respond
- Detection of user responses is difficult without Figma API access

### Alternative: Figma API (Future Enhancement)
If Figma API access is available:
```
GET /v1/files/{file_key}/comments
POST /v1/files/{file_key}/comments/{comment_id}/reactions
POST /v1/files/{file_key}/comments
```

## Thread Detection Logic

### Slack Threading
- Messages with same `thread_ts` belong to same conversation
- Thread ID format: `slack-{channel_id}-{thread_ts}`

### P2 Threading
- Comments with same `post_id` belong to same conversation
- Nested comments share parent-child relationships
- Thread ID format: `p2-{site_id}-{post_id}`

### Figma Threading
- Comments on same file/node belong to same conversation
- Thread ID format: `figma-{file_id}-{node_id}`

### Cross-Platform Threading
- Generally not possible to detect
- Each platform conversation is treated as separate thread

## Response Detection

To check if user has already responded to a ping:

1. **Slack**: Check if user has:
   - Posted a message in the thread after the mention
   - Reacted to the message with any emoji

2. **P2**: Check if user has:
   - Commented on the post/comment after the mention
   - Liked the post/comment

3. **Figma**: Check if:
   - User has replied to the comment in Figma (requires Figma API)
   - Email thread shows user response (limited reliability)

## Linear (via context-a8c MCP)

### Loading the Provider
```
context-a8c-load-provider with provider: "linear"
```

### Creating Issues
```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "linear"
  tool: "create-issue"
  params: {
    team: {team_id},
    title: {title},
    description: {description},
    state: "Triage",
    priority: {priority},
    labels: [{label}]
  }
```

### Updating Issues
```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "linear"
  tool: "update-issue"
  params: {
    id: {issue_id},
    state: "Done"
  }
```

### Adding Comments
```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "linear"
  tool: "create-comment"
  params: {
    issueId: {issue_id},
    body: {comment_text}
  }
```

### Listing Teams
```
Tool: mcp__context-a8c__context-a8c-execute-tool
Parameters:
  provider: "linear"
  tool: "list-teams"
  params: {}
```

## Deduplication Strategy

1. **Generate unique ping ID**: Hash of (platform + message_id + timestamp)
2. **Generate thread ID**: Platform-specific thread identifier
3. **Group by thread ID**: All pings with same thread ID belong together
4. **Check for updates**: If thread ID exists, this is a follow-up
5. **Check for responses**: If user responded, mark as handled

## Priority Boosting Based on Platform

Some platforms/contexts may warrant priority adjustments:

- **Direct DMs**: Consider bumping priority +1
- **Executive mentions**: Consider context and urgency
- **Multiple mentions in short time**: May indicate urgency
- **Cross-platform duplicates**: Consolidate and use highest priority
