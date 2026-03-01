# Voiceprint Version Changelog

Single source of truth for version detection and migration requirements.

## Current Version

**1.6.0**

## Version Detection

Follow this decision tree to identify the version of a writer skill:

1. **Check frontmatter** — Read `SKILL.md` and look for `voiceprint-version` in the YAML frontmatter.
   - If present and matches the **Current Version** above → **Current**
   - If present but lower → **Outdated** (use the version number to determine migration path)
   - If missing → continue to step 2

2. **Check for `voice-profile.md`** — Does the directory contain `voice-profile.md`?
   - If yes → **Old format** (two-file layout, see structural fingerprinting below)
   - If no → continue to step 3

3. **Structural fingerprinting** — Examine the SKILL.md content:
   - Has "Core Instruction" + "Voice Exemplars" sections → **Outdated** (v1.2.0–1.5.x, single file but missing version field)
   - Has "Voice Quick Reference" or "Red Flags Checklist" → **Old format** (pre-1.2.0)
   - None of the above → **Unknown**

## Quick Decision Table

| Detection Result | Action |
|-----------------|--------|
| **Current** | Proceed — no migration needed |
| **Outdated** | Run `/voiceprint update` to migrate to the current version |
| **Old format** | Run `/voiceprint update` to migrate to the current version |
| **Unknown** | Warn user — structure not recognized; ask before proceeding |

## Version History

### v1.6.0 (Current)

**Detection fingerprint:** `voiceprint-version: "1.6.0"` (or later) in SKILL.md frontmatter.

**Structure:**
- Single `SKILL.md` file containing all voice data
- Sections: Core Instruction, Quick Reference, Voice Exemplars, Voice Profile, Voice Markers, Platform Formats, Sample Transformations, Forbidden Patterns, Internal Checks, Calibration Notes
- No `voice-profile.md` file

**Migration from earlier versions:** Run `/voiceprint update` — merges two files into one, adds Quick Reference table, categorizes forbidden patterns, sets `voiceprint-version` frontmatter.

### v1.2.0–1.5.x (Outdated)

**Detection fingerprint:** No `voiceprint-version` field. Both `SKILL.md` and `voice-profile.md` exist. SKILL.md has "Core Instruction" + "Voice Exemplars" sections and a flat "Avoid List".

**Structure:**
- Two files: `SKILL.md` + `voice-profile.md`
- SKILL.md: Core Instruction, Voice Exemplars, Voice Markers, Platform Formats, Avoid List, Internal Checks, Calibration Notes
- voice-profile.md: Quantitative metrics, Quick Reference Card, Sample Transformations, categorized Forbidden Patterns

**Migration requirements:** Merge voice-profile.md into SKILL.md, restructure Avoid List into categorized Forbidden Patterns, add Quick Reference table, set `voiceprint-version` frontmatter.

### Pre-1.2.0 (Old format)

**Detection fingerprint:** No `voiceprint-version` field. Both files exist. SKILL.md has "Voice Quick Reference" or "Red Flags Checklist" but no "Core Instruction" or "Voice Exemplars" sections.

**Structure:**
- Two files: `SKILL.md` + `voice-profile.md`
- SKILL.md: Voice Quick Reference, Forbidden Patterns, Active Patterns, Content Templates, Red Flags Checklist, Calibration Notes
- voice-profile.md: Quantitative metrics, Quick Reference Card, Sample Transformations, Preferred Patterns

**Migration requirements:** Full restructure into v1.6.0 single-file format. Some sections may need manual filling (e.g., Voice Exemplars if not collected in original profiling).

---

## Adding a New Version

When a release changes the writer skill output format (new sections, restructured layout, changed frontmatter), add a new entry:

1. Update `## Current Version` to the new version number
2. In the **Quick Decision Table**, update the "Current" row to reference the new version
3. In **Version History**, relabel the previous "(Current)" entry to "(Outdated)"
4. Add the new version at the top of Version History using this template:

```markdown
### vX.Y.0 (Current)

**Detection fingerprint:** [How to identify this version — frontmatter field, structural markers]

**Structure:**
- [File layout — single file, multiple files, etc.]
- [Key sections and their order]

**Migration from earlier versions:** [What `/voiceprint update` does to get here]
```

5. If the detection tree in **Version Detection** needs new branches, update it

**Not every plugin release needs a changelog entry.** Only add one when the writer skill format that users receive actually changes (new sections, restructured output, changed frontmatter schema). Bug fixes and internal refactors don't need entries here.
