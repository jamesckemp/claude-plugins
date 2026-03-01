---
description: Create a new voice profile from your writing samples (~15 min)
---

# /generate

## Mode Requirement

This command requires execute mode. If plan mode is currently active, exit plan mode before proceeding. Use the ExitPlanMode tool, then continue with the command.

## Reference Files

These paths are resolved — read them directly, do not search or glob:

- **Question bank**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/references/question-bank.md`
- **AI tells catalog**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/references/ai-tells.md`
- **Writer skill template**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/assets/writer-skill-template.md`

## Workflow

Load skill `voiceprint:voiceprint` using the Skill tool.

Follow the full workflow defined in the skill, starting with Phase 1: Introduction & Setup.
