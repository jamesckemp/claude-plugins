---
description: >
  Update an existing writer skill with the latest voiceprint features. Interactively
  walks users through what's changing and lets them decide what to update. Handles
  migration from old two-file format to the new single-file format.
user-invocable: false
---

# Voiceprint Update - Upgrade Existing Writer Skills

Update an existing writer skill to the latest voiceprint template structure. Walks you through each change interactively — nothing is applied silently.

## Mode Check

If plan mode is active, exit it now using ExitPlanMode before starting this workflow. All voiceprint commands run in execute mode.

## Inputs

- **Target directory**: The exact path shown after "The target writer skill directory is:" in the command output above. This directory must contain `SKILL.md` (and may also contain `voice-profile.md` from older versions).

## Reference Files

These paths are resolved automatically — read them directly, do not search or glob:

- **Version changelog**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/references/version-changelog.md`
- **AI tells catalog**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/references/ai-tells.md`
- **Writer skill template**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/assets/writer-skill-template.md`
- **Voice profile template (legacy)**: `!`echo ${CLAUDE_PLUGIN_ROOT}`/skills/voiceprint/assets/voice-profile-template.md`

## Workflow Overview

```
Phase 1: Read & Detect         (~30s)  → Read files, identify version
Phase 2: Explain & Plan        (~1 min) → Tell user what's different, confirm proceed
Phase 3: Extract Voice Data    (~30s)  → Pull all voice content from existing file(s)
Phase 4: Interactive Selection  (~2 min) → Walk through each change area with questions
Phase 5: Apply                 (~1 min) → Construct merged SKILL.md, backup old files
Phase 6: Validate              (~1 min) → Generate test content, confirm it sounds right
Phase 7: Report                (~30s)  → Summary of what changed
```

---

## Phase 1: Read & Detect

### Step 1: Read the target files

Do NOT search, glob, or look up the writer skill by name — use the provided path directly.

Read from the provided directory path:
- `{TARGET_DIR}/SKILL.md` - The writer skill (required)
- `{TARGET_DIR}/voice-profile.md` - The voice profile (may or may not exist)

If `SKILL.md` is missing, tell the user:

> I couldn't find a writer skill at that path. I need at least `SKILL.md` in the directory. Check the path and try again.

Then stop.

### Step 2: Identify current version

Read the version changelog listed in Reference Files above and follow the **Version Detection** decision tree to determine the format status.

Store the detection result as `CURRENT_VERSION`.

### Step 3: Check if already current

Compare `CURRENT_VERSION` against the **Current Version** listed in the changelog. If the skill is already current:

> Your writer skill is already using the latest voiceprint format (v1.6.0). No structural updates needed.
>
> Want me to check for content updates instead?

Use `AskUserQuestion`:
- **Question**: "What would you like to do?"
- **Options**:
  - "Check for new AI patterns" (description: "Scan against latest AI tells catalog")
  - "Nothing, I'm good" (description: "Exit")

If they want to check patterns, jump to Phase 4 Step 2 (Forbidden patterns check). Otherwise, stop.

### Step 4: Read reference files

Read these files from the paths listed in Reference Files above:
- Writer skill template - Current merged template
- Voice profile template (legacy) - For understanding old structure
- AI tells catalog - Latest AI pattern catalog

---

## Phase 2: Explain & Plan

Tell the user what version they're on and what will change.

**For v1.2.0–1.5.x profiles:**

> Your writer skill was generated with voiceprint v1.2.0–1.5.x, which used two files (`SKILL.md` + `voice-profile.md`). The current format (v1.6.0) merges everything into a single `SKILL.md` that works everywhere — including Claude Desktop and other tools that only read one file.
>
> Here's what the update involves:
> 1. **Merge into one file** — All voice profile data (metrics, vocabulary, punctuation, etc.) gets folded into SKILL.md
> 2. **Categorized forbidden patterns** — Your flat Avoid List becomes organized by type (phrases, structures, additional)
> 3. **Quick Reference table** — Added to the top of SKILL.md for fast scanning
> 4. **Sample Transformations** — Before/after examples moved into SKILL.md
> 5. **Backup** — Your `voice-profile.md` gets renamed to `voice-profile.backup.md`
>
> All your voice data is preserved — nothing is lost.

**For pre-1.2.0 profiles:**

> Your writer skill was generated with an early voiceprint version (pre-1.2.0). The update will restructure it to the current v1.6.0 format. This is a larger migration:
> 1. **New structure** — Core Instruction, Voice Exemplars, Voice Profile, Voice Markers, Platform Formats, Forbidden Patterns, Internal Checks
> 2. **Single file** — Everything merges into one self-contained SKILL.md
> 3. **Backup** — Your `voice-profile.md` gets renamed to `voice-profile.backup.md`
>
> Some sections may need manual filling (like Voice Exemplars if they weren't collected in the original profiling).

Then confirm:

Use `AskUserQuestion`:
- **Question**: "Ready to proceed with the update?"
- **Options**:
  - "Yes, let's go" (description: "Walk me through the changes")
  - "Tell me more first" (description: "I have questions about the update")
  - "Not now" (description: "I'll come back later")

If "Tell me more first", answer their questions then re-ask. If "Not now", stop.

---

## Phase 3: Extract Voice Data

Extract all voice-specific content from the existing file(s). This data will be preserved through the restructure.

### For v1.2.0–1.5.x (two-file format)

**From SKILL.md, extract:**

1. **Profile name** from frontmatter or heading
2. **Voice Exemplars** — all 6 categorized samples
3. **Voice Markers** — Signature Moves, Natural Expressions, Structural Preferences, Rhythm
4. **Platform Formats** — all format-specific guidance and synthesized exemplars
5. **Avoid List** — all forbidden items (flat bullets)
6. **Internal Checks** — metric values (avg sentence length, burstiness ratio)
7. **Calibration Notes**

**From voice-profile.md, extract:**

1. **All quantitative metrics** (sentence structure table, punctuation profile table)
2. **All descriptive sections** (tone, rhythm, specificity, vocabulary, voice markers)
3. **Forbidden Patterns** (full categorized version with Rejected Phrases, Rejected Structures, Additional Rejections)
4. **Quick Reference Card** values
5. **Sample Transformations** (before/after pairs)
6. **Notes** (cross-reference, confidence, use case weighting)

### For pre-1.2.0 (old two-file format)

**From SKILL.md, extract:**

1. **Profile name** from heading
2. **Voice Quick Reference** table values
3. **Forbidden Patterns** — all rejected phrases, setup labels, rejected structures, additional rejections
4. **Active Patterns** — natural expressions and structural preferences
5. **Content Templates** — all format-specific guidance
6. **Red Flags Checklist** — metric values
7. **Calibration Notes**

**From voice-profile.md, extract:**

1. **All quantitative metrics**
2. **All descriptive sections**
3. **Forbidden Patterns** (full categorized version)
4. **Preferred Patterns**
5. **Quick Reference Card** values
6. **Sample Transformations**
7. **Notes**
8. **Writing Exemplars** (if present from a refine session)

---

## Phase 4: Interactive Selection

Walk through each change area individually. Let the user decide what to include.

### Step 1: File merge

Use `AskUserQuestion`:
- **Question**: "Ready to merge your two files into one self-contained SKILL.md?"
- **Options**:
  - "Yes, merge them" (description: "Combine everything into one file")
  - "Tell me more" (description: "What exactly gets merged?")
  - "Skip" (description: "Keep the two-file format for now")

If "Tell me more", explain what sections from voice-profile.md get added to SKILL.md (Quick Reference, Voice Profile with metrics/vocabulary/punctuation/voice detail, Sample Transformations, categorized Forbidden Patterns). Then re-ask.

If "Skip", warn that the two-file format won't work in Claude Desktop or single-file tools, and stop the update.

### Step 2: Forbidden patterns check

Read the AI tells catalog listed in Reference Files above and compare against the existing forbidden patterns.

If new patterns are found that aren't already in the profile:

> I found some AI writing patterns in the latest catalog that aren't in your profile yet:

List the new categories with brief descriptions.

Use `AskUserQuestion`:
- **Question**: "Want to add any of these new patterns to your forbidden list?"
- **multiSelect**: true
- **Options** (dynamically generated from new categories found, up to 4):
  - "{Category 1 name}" (description: "{brief description}, {count} phrases")
  - "{Category 2 name}" (description: "{brief description}, {count} phrases")
  - "None of these" (description: "Keep my current forbidden patterns as-is")

If no new patterns are found:

> Your forbidden patterns are up to date with the latest AI tells catalog.

### Step 3: Exemplar completeness

Count the voice exemplars in the existing profile.

If fewer than 6:

Use `AskUserQuestion`:
- **Question**: "Your profile has {N} exemplar(s). The current format supports 6. Want to add placeholder notes for the missing slots?"
- **Options**:
  - "Add placeholders" (description: "I can fill them in later with /voiceprint refine")
  - "Keep as-is" (description: "Only use the exemplars I have")

### Step 4: Sample transformations

If sample transformations exist in the extracted data:

Use `AskUserQuestion`:
- **Question**: "Include your {N} sample transformation(s) (before/after examples) in the merged file?"
- **Options**:
  - "Include them" (description: "Copy them into the merged SKILL.md")
  - "Show me first" (description: "Let me review before deciding")
  - "Skip" (description: "Leave them out")

If "Show me first", display the transformations and re-ask with just "Include" and "Skip".

If no transformations exist, note that placeholder structure will be added.

### Step 5: Calibration notes

If calibration notes exist:

Use `AskUserQuestion`:
- **Question**: "Keep your existing calibration notes?"
- **Options**:
  - "Keep them" (description: "Preserve current notes")
  - "Add something" (description: "I want to add or change a note")
  - "Skip" (description: "Clear calibration notes")

If "Add something", ask for the new note in free text.

---

## Phase 5: Apply

### Construct the merged SKILL.md

Using the extracted data from Phase 3 and the user's choices from Phase 4, build the new SKILL.md following the writer skill template structure (see Reference Files above):

1. **Frontmatter**: Set `voiceprint-version: "1.6.0"`, preserve name and description
2. **Core Instruction**: Preserve existing or use template default (remove any `voice-profile.md` references)
3. **Quick Reference**: Populate from extracted Quick Reference Card values
4. **Voice Exemplars**: Populate from extracted exemplars (add placeholder notes for missing slots if user chose that)
5. **Voice Profile**: Populate Core Characteristics, Sentence Metrics, Punctuation Profile, Vocabulary, and Voice Detail from extracted profile data
6. **Voice Markers**: Preserve existing Signature Moves, Natural Expressions, Structural Preferences, Rhythm
7. **Platform Formats**: Preserve existing format guidance and synthesized exemplars
8. **Sample Transformations**: Include if user chose to; add placeholder structure otherwise
9. **Forbidden Patterns**: Organize into Rejected Phrases, Rejected Structures, Additional Rejections. Add any new patterns the user selected in Phase 4 Step 2
10. **Internal Checks**: Preserve metric values, remove any `voice-profile.md` references
11. **Calibration Notes**: Preserve or update based on user choice

### Write the file

Write the constructed SKILL.md to `{TARGET_DIR}/SKILL.md`, replacing the old version.

### Backup old files

If `voice-profile.md` exists, rename it:
- `{TARGET_DIR}/voice-profile.md` → `{TARGET_DIR}/voice-profile.backup.md`

---

## Phase 6: Validate

### Step 1: Generate test content

Read the newly written SKILL.md and generate a short paragraph (3-5 sentences) following the skill's instructions. Pick a topic relevant to the user's stated use cases (from the profile's calibration notes or use case weighting).

### Step 2: Present and verify

> Here's a test paragraph written with your updated skill:
>
> {test paragraph}
>
> Does this still sound like you? The update shouldn't change your voice — just the file structure.

Use `AskUserQuestion`:
- **Question**: "How does this sound?"
- **Options**:
  - "Sounds right" (description: "My voice is intact")
  - "Something's off" (description: "I'll tell you what changed")

If "Something's off", collect feedback and apply fixes to the new SKILL.md. Re-validate.

---

## Phase 7: Report

Present a summary of all changes:

> **Updated {PROFILE_NAME}-writer to v1.6.0:**
>
> **Structural changes:**
> {numbered list of what changed}
>
> **Voice data preserved:**
> - All voice exemplars ({count})
> - All forbidden patterns ({count} items)
> - All voice markers and platform formats
> - All metrics and calibration notes
>
> **Files:**
> - `SKILL.md` — Updated to single-file v1.6.0 format
> - `voice-profile.backup.md` — Backup of your old voice profile (safe to delete once you're satisfied)
>
> Your writer skill now works everywhere — Claude Code, Claude Desktop, and any tool that supports SKILL.md files.

---

## Error Handling

- **Path doesn't exist**: Tell the user the path wasn't found and ask them to check it.
- **Missing SKILL.md**: Explain the file is missing and suggest running `/voiceprint generate` first.
- **Already up to date**: If v1.6.0+, offer content-only updates (new AI patterns) or exit.
- **Unrecognized structure**: If files don't match any known voiceprint template version, warn the user and offer to attempt a best-effort update, noting risks.
- **Partial data**: If some sections are missing from the old format, note what couldn't be migrated and suggest using `/voiceprint refine` to fill gaps.

## References

All reference files are listed with resolved paths in the Reference Files section above.
