---
description: Update an existing writer skill to the latest voiceprint template
argument-hint: "<path to writer skill directory>"
---

# /update

Update an existing writer skill with the latest voiceprint features and template improvements.

## Mode Requirement

This command requires execute mode. If plan mode is currently active, exit plan mode before proceeding. Use the ExitPlanMode tool, then continue with the command.

## Workflow

Load skill `voiceprint:update` using the Skill tool.

The user wants to update the writer skill at the following path:

**Directory:** `$ARGUMENTS`

Pass this path as the target directory containing `SKILL.md` (and optionally `voice-profile.md` from older versions that will be merged).
