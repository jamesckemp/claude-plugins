---
description: Update an existing writer skill to the latest voiceprint template
argument-hint: "<path to writer skill directory>"
---

# /update

Update an existing writer skill with the latest voiceprint features and template improvements.

## Mode Requirement

This command requires execute mode. If plan mode is currently active, exit plan mode before proceeding. Use the ExitPlanMode tool, then continue with the command.

## Reference Files

These paths are resolved — read them directly, do not search or glob:

- **Version changelog**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/references/version-changelog.md`
- **AI tells catalog**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/references/ai-tells.md`
- **Writer skill template**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/assets/writer-skill-template.md`
- **Voice profile template (legacy)**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/assets/voice-profile-template.md`

## Workflow

Load skill `voiceprint:update` using the Skill tool.

The target writer skill directory is:

**`$ARGUMENTS`**

Do NOT search, glob, or attempt to locate the writer skill automatically — the path above has already been validated. Pass it directly as the target directory containing `SKILL.md` (and optionally `voice-profile.md` from older versions that will be merged).
