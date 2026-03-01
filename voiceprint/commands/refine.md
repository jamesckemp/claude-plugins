---
description: Refine an existing writer skill
argument-hint: "<path to writer skill directory>"
---

# /refine

Refine an existing writer skill by analyzing additional writing samples and updating the voice profile.

## Mode Requirement

This command requires execute mode. If plan mode is currently active, exit plan mode before proceeding. Use the ExitPlanMode tool, then continue with the command.

## Workflow

Load skill `voiceprint:refine` using the Skill tool.

The user wants to refine the writer skill at the following path:

**Directory:** `$ARGUMENTS`

Pass this path as the target directory containing `SKILL.md`.
