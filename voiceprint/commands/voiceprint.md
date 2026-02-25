---
name: voiceprint
description: Build a voice profile from your writing samples and generate a personalized writer skill
argument-hint: "generate | refine <path> | update <path>"
---

# /voiceprint

## Mode Requirement

This command requires execute mode. If plan mode is currently active, exit plan mode before proceeding. Use the ExitPlanMode tool, then continue with the command.

## Subcommand Routing

Route based on the first word of `$ARGUMENTS`:

### Route: `generate`

If the first word of `$ARGUMENTS` is `generate`, create a new voice profile.

Use skill: voiceprint

Follow the full workflow defined in the skill, starting with Phase 1: Introduction & Setup.

### Route: `refine`

If the first word of `$ARGUMENTS` is `refine`, refine an existing writer skill.

Use skill: voiceprint/refine

The remaining arguments after `refine` should be a directory path containing both `SKILL.md` and `voice-profile.md`. Pass this path as the target directory.

### Route: `update`

If the first word of `$ARGUMENTS` is `update`, update an existing writer skill with the latest voiceprint features.

Use skill: voiceprint/update

The remaining arguments after `update` should be a directory path containing both `SKILL.md` and `voice-profile.md`. Pass this path as the target directory.

### Route: No arguments or unrecognized

If `$ARGUMENTS` is empty or the first word doesn't match any subcommand above, display available subcommands:

> **Voiceprint** — create and manage personalized voice profiles.
>
> Available commands:
>
> - `/voiceprint generate` — Create a new voice profile from writing samples (~15 min)
> - `/voiceprint refine <path>` — Refine an existing writer skill at the given path
> - `/voiceprint update <path>` — Update an existing skill with the latest voiceprint features
>
> Example: `/voiceprint generate`
