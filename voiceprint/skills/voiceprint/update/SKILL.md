---
description: >
  Update an existing writer skill with the latest voiceprint features without
  re-profiling. Applies structural template updates while preserving all voice
  data, exemplars, and user customizations.
user-invocable: false
---

# Voiceprint Update - Upgrade Existing Writer Skills

Update an existing writer skill to the latest voiceprint template structure without re-running the full questionnaire. Preserves all voice data while applying structural improvements.

## Mode Check

If plan mode is active, exit it now using ExitPlanMode before starting this workflow. All voiceprint commands run in execute mode.

## Inputs

- **Target directory**: The path provided by the user (via `$ARGUMENTS` from the command). This directory must contain both `SKILL.md` and `voice-profile.md`.

## Workflow Overview

```
Phase 1: Read & Assess        (~30s)  → Read files, identify current template version
Phase 2: Extract Voice Data    (~30s)  → Pull all voice-specific content from existing files
Phase 3: Apply Updates         (~1 min) → Restructure to latest template, preserve voice data
Phase 4: Report                (~30s)  → Show what changed
```

---

## Phase 1: Read & Assess

### Step 1: Read the target files

Read both files from the provided directory path:
- `{TARGET_DIR}/SKILL.md` - The writer skill
- `{TARGET_DIR}/voice-profile.md` - The voice profile

If either file is missing, tell the user:

> I couldn't find a complete writer skill at that path. I need both `SKILL.md` and `voice-profile.md` in the directory. Check the path and try again.

Then stop.

### Step 2: Identify current template version

Check the SKILL.md structure to determine which voiceprint version generated it:

**v1.0.x / v1.1.x indicators** (pre-1.2.0):
- Has "Voice Quick Reference" table at top
- Has "Forbidden Patterns" section with subsections (Rejected Phrases, Setup Labels, Rejected Structures)
- Has "Active Patterns" section (before Forbidden Patterns or after)
- Has "Red Flags Checklist" with checkbox format (`- [ ]`)
- Has "Revision Strategy" section
- Does NOT have "Voice Exemplars" section
- Does NOT have "Core Instruction" section
- Does NOT have "Avoid List" (flat) section
- Does NOT have "Internal Checks" section

**v1.2.0 indicators** (current):
- Has "Core Instruction" section with execute mode guidance
- Has "Voice Exemplars" section with real writing samples
- Has "Voice Markers" with "Signature Moves" subsection
- Has flat "Avoid List" instead of multi-section "Forbidden Patterns"
- Has "Internal Checks" in prose format (no checkboxes)
- No "Voice Quick Reference" table (moved to profile only)
- No "Revision Strategy" section
- No "Red Flags Checklist"

If the skill is already on v1.2.0 format:

> Your writer skill is already using the latest voiceprint template structure. No structural updates needed.
>
> If you want to refine the content (add patterns, adjust tone, etc.), use `/voiceprint refine {path}` instead.

Then stop.

### Step 3: Also read reference files

Read these from the voiceprint skill directory for the latest templates and AI tells:
- `assets/writer-skill-template.md` - Current template structure
- `assets/voice-profile-template.md` - Current profile template
- `references/ai-tells.md` - Latest AI pattern catalog

Tell the user:

> Your writer skill was generated with an older voiceprint version. I'll update it to the v1.2.0 structure while keeping all your voice data intact.

---

## Phase 2: Extract Voice Data

Extract all voice-specific content from the existing files. This data will be preserved through the restructure.

### From SKILL.md, extract:

1. **Profile name** from frontmatter or heading
2. **Voice Quick Reference** table values (tone, formality, sentence length, etc.)
3. **Forbidden Patterns** — all rejected phrases, setup labels, rejected structures, additional rejections
4. **Active Patterns** — natural expressions and structural preferences
5. **Content Templates** — all format-specific guidance (blog, email, social, docs)
6. **Red Flags Checklist** — metric values (avg sentence length, burstiness ratio, contraction rate, first-person rate)
7. **Calibration Notes**

### From voice-profile.md, extract:

1. **All quantitative metrics** (sentence structure table, punctuation profile table)
2. **All descriptive sections** (tone, rhythm, specificity, vocabulary, voice markers)
3. **Forbidden Patterns** (full categorized version)
4. **Preferred Patterns** (natural expressions, structural preferences)
5. **Quick Reference Card** values
6. **Sample Transformation** examples
7. **Notes** (cross-reference, confidence, use case weighting)
8. **Writing Exemplars** (if present from a refine session)
9. **Changelog** (if present)

---

## Phase 3: Apply Updates

### Update SKILL.md

Restructure to the v1.2.0 template format:

1. **Add Core Instruction** section at the top (from template) with execute mode guidance and output rules
2. **Add Voice Exemplars** section — if the existing profile has Writing Exemplars from a refine session, use those. Otherwise, add the placeholder structure with a note:

> Note: This skill was updated from a pre-1.2.0 version that didn't collect writing exemplars. To add exemplars, use `/voiceprint refine {path}` and select "Provide a writing example."

3. **Restructure Active Patterns → Voice Markers** — move natural expressions and structural preferences under the new "Voice Markers" heading, add "Signature Moves" (derive 3-5 from the most distinctive active patterns) and "Rhythm" (derive from metrics)
4. **Restructure Content Templates → Platform Formats** — preserve all format-specific guidance, add synthesized exemplar placeholders with the same note about using refine to add them
5. **Compress Forbidden Patterns → Avoid List** — flatten all subsections into a single bullet list of the highest-impact items (~25-30). Move the full categorized version to voice-profile.md only (it should already be there)
6. **Replace Red Flags Checklist → Internal Checks** — convert checkbox items to prose "silently verify" format, preserving the metric values
7. **Remove** Voice Quick Reference table (now only in voice-profile.md)
8. **Remove** Revision Strategy section

### Update voice-profile.md

Apply lighter updates:

1. **Add Writing Exemplars** section between Quick Reference Card and Sample Transformations (if not already present) — use any exemplars found, or add placeholder structure with the refine note
2. **Expand Sample Transformations** — if only one before/after exists, add placeholder structure for up to 3 transformations
3. **Update Forbidden Patterns** — ensure it has the full categorized version (should already be there)
4. **Cross-check** against latest `ai-tells.md` — if new AI tell categories exist that weren't in the original profile, note them but do NOT automatically add them (the user should decide)

### Update ai-tells coverage

Compare the existing forbidden patterns against the latest `references/ai-tells.md`. If new categories exist:

> I noticed some new AI writing patterns in the latest catalog that aren't in your profile yet:
>
> {list of new categories with brief descriptions}
>
> Want me to add any of these to your avoid list?

Use `AskUserQuestion`:
- **Question**: "Add any of these new patterns?"
- **Options**:
  - "Add all of them" (description: "Block all new patterns")
  - "Let me pick" (description: "I'll choose which ones")
  - "Skip" (description: "Keep my current avoid list as-is")

---

## Phase 4: Report

Present a summary of all structural changes:

> **Updated {PROFILE_NAME}-writer to v1.2.0 structure:**
>
> **SKILL.md changes:**
> {numbered list of structural changes}
>
> **voice-profile.md changes:**
> {numbered list of structural changes}
>
> **Voice data preserved:**
> - All forbidden patterns ({count} items)
> - All active patterns/voice markers ({count} items)
> - All content template guidance
> - All metrics and calibration notes
>
> **To complete the update:**
> - Add writing exemplars: `/voiceprint refine {path}` → "Provide a writing example"
> - Add format exemplars (sample tweet, sample paragraph): same refine workflow

---

## Error Handling

- **Path doesn't exist**: Tell the user the path wasn't found and ask them to check it.
- **Missing files**: Explain which file is missing and suggest running `/voiceprint generate` first.
- **Already up to date**: If the skill is already v1.2.0 format, tell the user and suggest `/voiceprint refine` for content changes.
- **Unrecognized structure**: If the files don't match any known voiceprint template version, warn the user and offer to attempt a best-effort update, noting risks.
- **Partial data**: If some sections are missing from the old format, note what couldn't be migrated and suggest using refine to fill gaps.
