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

The target writer skill directory is:

**`$ARGUMENTS`**

Do NOT search, glob, or attempt to locate the writer skill automatically — the path above has already been validated. Pass it directly as the target directory containing `SKILL.md` (and optionally `voice-profile.md` from older versions that will be merged).
