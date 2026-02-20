# Voiceprint Question Bank

Complete question text, options, and analysis notes for each question in the voiceprint questionnaire.

---

## Phase 2: Writing Samples

### Prompt 1: Casual/Natural Voice

**Prompt**: "First up - just write naturally. Tell me about something you did recently, work or personal. Don't overthink it, just write a few sentences like you would to a friend or colleague."

**Analysis targets**:
- Baseline sentence length and variance
- Default connector words (and, but, so, then, also)
- Contraction rate (don't vs do not)
- First-person frequency
- Comma usage patterns
- How they start sentences (subject-first, prepositional, temporal)
- Casual vocabulary markers (just, kinda, pretty much, honestly)

**Red flags for self-consciousness**: If the response reads like a polished paragraph rather than casual speech, the user may be performing. Compare against later samples to detect this.

---

### Prompt 2: Explanatory/Teaching Voice

**Prompt**: "Now explain something you know well. Pick a concept from your work or a hobby and explain it to a peer (not a beginner). Write it the way you'd actually write it in a message or document."

**Analysis targets**:
- Technical vocabulary density
- Explanation structure: top-down (conclusion first, then details) vs bottom-up (build to the point)
- Use of analogies or examples
- Assumed knowledge markers ("you know how...", "basically...")
- Parenthetical asides for caveats
- Whether they use lists/bullets or prose for structured info

---

### Prompt 3: Excited/Enthusiastic Voice

**Prompt**: "Tell me about something that genuinely excited you recently. A discovery, a tool, an idea, a project - anything that made you think 'this is great.' Write a few sentences about it."

**Analysis targets**:
- Enthusiasm markers: exclamation points, intensifiers (so, really, incredibly, genuinely)
- Specificity of excitement (vague "it's amazing" vs concrete "it reduced our build time by 40%")
- Whether excitement shows as speed (shorter sentences, fragments) or expansion (longer, more detailed)
- Hyperbole patterns or lack thereof
- Sharing instinct (do they explain why others should care?)

---

### Prompt 4: Frustrated/Concerned Voice

**Prompt**: "Now something that frustrated you or a problem you noticed. Describe something that bugs you - at work, in your industry, in daily life. Be honest about it."

**Analysis targets**:
- Directness of complaint (hedged vs blunt)
- Whether they propose solutions alongside problems
- Emotional vocabulary range
- Sarcasm or irony markers
- Sentence length shift under frustration (usually shorter)
- "Should" statements and expectation-setting language
- Blame direction (systemic vs individual, specific vs general)

---

### Prompt 5: Persuasive/Opinionated Voice

**Prompt**: "Last writing sample - give me a take. What's something most people seem to accept but you think is wrong or overrated? Make your case in a few sentences."

**Analysis targets**:
- Conviction level ("I think" vs "clearly" vs stating as fact)
- Counterargument acknowledgment (do they preemptively address objections?)
- Rhetorical questions usage
- Evidence style (anecdotal, data, logical argument, authority)
- How they position themselves relative to the majority ("most people" framing)
- Hedging vs committing to the take

---

## Phase 3: Style Preferences

### Question 6: Sentence Structure

**Question**: "Which of these feels closest to how you naturally write?"

**Options**:

1. **"Short and direct"**
   - Description: "I keep it simple. One idea per sentence."
   - Preview:
     ```
     The project launched last week. It went well.
     We hit our targets. The team was relieved.
     Now we're planning the next phase.
     ```

2. **"Flowing and connected"**
   - Description: "I link ideas together and let sentences breathe."
   - Preview:
     ```
     The project launched last week and it went better than
     expected, which was a relief for the whole team since
     we'd been worried about the timeline. Now that it's
     behind us, we're starting to plan what comes next.
     ```

3. **"Mixed - varies by feel"**
   - Description: "Short when punchy, long when it needs room."
   - Preview:
     ```
     The project launched last week. It went better than
     expected, which was a relief for the whole team. Now
     we're planning the next phase. Big question: can we
     keep this momentum going?
     ```

**Analysis note**: Cross-reference against actual sentence length patterns from writing samples. If they pick "short and direct" but their samples average 18+ words per sentence, note the discrepancy and trust the samples.

---

### Question 7: Punctuation Habits

**Question**: "Which punctuation do you reach for most when writing? Select all that feel natural to you."

**multiSelect**: true

**Options**:

1. **"Em dashes"**
   - Description: "For asides, interruptions, or emphasis - like this"

2. **"Parentheses"**
   - Description: "For side notes and qualifiers (like this)"

3. **"Semicolons"**
   - Description: "To connect related thoughts; keeps things flowing"

4. **"Ellipses"**
   - Description: "For trailing off or implying more... you know"

**Analysis note**: Punctuation preferences are highly discriminating in stylometry. People are remarkably consistent in their punctuation patterns. Verify against samples - if they claim semicolons but never use one in 5 samples, deprioritize.

---

### Question 8: Rhythm Preference

**Question**: "When you reread your own writing, which rhythm feels most like you?"

**Options**:

1. **"Punchy and staccato"**
   - Description: "Short bursts. Gets to the point. Doesn't waste words."

2. **"Steady and flowing"**
   - Description: "Even-paced sentences that carry the reader along smoothly"

3. **"Deliberately varied"**
   - Description: "I mix short and long on purpose. Contrast creates energy."

**Analysis note**: Burstiness (variation in sentence length) is the #2 discriminator of individual style after function words. Option 3 indicates high burstiness, which is actually the hallmark of skilled writers. Calculate from samples: stdev(sentence_length) / mean(sentence_length). Values > 0.5 indicate high burstiness.

---

### Question 9: Transition Style

**Question**: "How do you typically move from one idea to the next?"

**Options**:

1. **"Casual connectors"**
   - Description: "So, anyway, thing is, the point being, turns out..."

2. **"Formal connectors"**
   - Description: "However, additionally, that said, on the other hand..."

3. **"Questions"**
   - Description: "I ask a question to pivot: 'So what does this mean?'"

4. **"Direct jumps"**
   - Description: "I just start the next point. No bridge needed."

**Analysis note**: Transition style is topic-independent and highly author-stable, making it one of the most reliable voice markers. People who use questions as transitions tend to have a more conversational, exploratory style. Direct jumpers tend to be more assertive.

---

### Question 10: Formality & Word Choice

**Question**: "Would any of these words naturally show up in your writing? Select the ones you'd actually use."

**multiSelect**: true

**Options**:

1. **"Leverage, utilize, facilitate"**
   - Description: "Corporate/formal register"

2. **"Basically, honestly, literally"**
   - Description: "Conversational intensifiers"

3. **"Robust, scalable, groundbreaking"**
   - Description: "Tech/marketing register"

4. **"Look, here's the thing, the reality is"**
   - Description: "Direct/assertive openers"

**Analysis note**: This calibrates the user's vocabulary register. Overlap between categories is informative - someone who picks both "corporate" and "conversational" likely code-switches by context. Check against samples for verification.

---

### Question 11: Specificity Level

**Question**: "When you're making a point, which approach feels more natural?"

**Options**:

1. **"Concrete and specific"**
   - Description: "I reach for numbers, names, examples. 'We cut load time by 2 seconds.'"

2. **"Conceptual and general"**
   - Description: "I talk about patterns and ideas. 'Performance improved significantly.'"

3. **"Story-driven"**
   - Description: "I illustrate with a specific scenario or anecdote to make the point"

**Analysis note**: Detail density in generated content should match this. Concrete writers need actual numbers and specifics (or placeholders to fill). Conceptual writers sound wrong when forced into specifics. Story-driven writers need narrative framing.

---

### Question 12: Personal Voice

**Question**: "How much of 'you' shows up in your writing?"

**Options**:

1. **"Heavily personal"**
   - Description: "Lots of 'I think', 'I've found', personal anecdotes. My perspective is the frame."

2. **"Lightly personal"**
   - Description: "Some first-person, but I focus on the topic more than myself"

3. **"Minimal self-reference"**
   - Description: "I keep myself out of it. The subject speaks for itself."

**Analysis note**: First-person frequency is a key voice marker. Count "I/my/me/we/our" in samples. High (>5%) = heavily personal. Medium (2-5%) = lightly personal. Low (<2%) = minimal. Cross-reference with stated preference.

---

### Question 13: Opening/Hook Style

**Question**: "When you start a piece of writing (email, blog post, message), how do you usually open?"

**Options**:

1. **"Direct statement"**
   - Description: "Jump right in. 'Here's the problem with X.'"

2. **"Question"**
   - Description: "Open with a question. 'Have you ever noticed...?'"

3. **"Story or scenario"**
   - Description: "Start with a specific moment. 'Last Tuesday, I was debugging and...'"

4. **"Observation"**
   - Description: "Name something interesting. 'Most teams handle deploys the same way.'"

**Analysis note**: Opening style is a structural fingerprint. Check the first sentence of each writing sample to verify. Most people are remarkably consistent in how they begin.

---

## Phase 4: Pattern Rejection

### Question 14: AI Phrase Rejection

**Question**: "Which of these phrases would feel wrong or unnatural if they appeared in your writing? Select all that apply."

**multiSelect**: true

**Options**:

1. **"It's worth noting that..."**
   - Description: "Hedging/qualifying phrase"

2. **"In today's fast-paced world..."**
   - Description: "Generic contextual opener"

3. **"This serves as a testament to..."**
   - Description: "Overblown attribution"

4. **"Let's dive in / Let's unpack this"**
   - Description: "Forced engagement phrase"

**Analysis note**: Expand rejections to full categories using `references/ai-tells.md`. If they reject "It's worth noting that", also flag: "It bears mentioning", "It should be noted", "What's interesting is", and similar hedging constructions. Category-level rejection is more useful than phrase-level.

**Follow-up**: After the selection, ask as plain text: "Are there any other specific phrases or expressions that feel 'off' to you in AI-generated text? Things that make you think 'a human wouldn't write that'?" Capture any freeform additions.

---

### Question 15: Structural Pattern Rejection

**Question**: "Which of these writing patterns feel artificial or forced to you? Select all that apply."

**multiSelect**: true

**Options**:

1. **"Rule of three lists"**
   - Description: "Always grouping things in exactly three: 'faster, better, stronger'"

2. **"Moreover/Furthermore/Additionally"**
   - Description: "Formal stacking connectors between paragraphs"

3. **"Not only X, but also Y"**
   - Description: "Negative parallelism construction"

4. **"The question isn't X, it's Y"**
   - Description: "Reframe-then-pivot structure"

**Analysis note**: These structural patterns are often invisible to casual readers but immediately recognizable to people who read a lot of AI output. High rejection rates here indicate the user is pattern-aware and the writer skill should actively avoid these constructions.

---

### Question 16: Emoji & Formatting

**Question**: "How do you feel about emoji and formatting in your writing?"

**Options**:

1. **"I use emoji naturally"**
   - Description: "Emoji are part of my voice, I use them without thinking"

2. **"Rarely, if ever"**
   - Description: "I keep my writing clean of emoji"

3. **"Depends on context"**
   - Description: "Casual messages yes, professional writing no"

**Analysis note**: This is especially important for social media and messaging use cases. Some people's voice genuinely includes emoji as punctuation. Others find any emoji in generated text jarring.

---

### Prompt 17: Closing Writing Sample

**Prompt**: "One last thing - write a few sentences about why you're creating this voice profile. What do you hope to use it for? What would 'good' look like to you?"

**Analysis targets**:
- Final authentic sample for cross-referencing with Prompt 1
- Captures meta-awareness (how they think about their own voice)
- Motivation context for the profile (helps weight which content types matter)
- Natural closing style
- Compare sentence patterns with opening sample to confirm consistency

---

## Cross-Reference Matrix

After collecting all responses, build this comparison:

| Dimension | Observed in Samples | Stated Preference | Conflict? | Trust |
|-----------|-------------------|-------------------|-----------|-------|
| Sentence length | avg: X, stdev: Y | Q6 selection | Yes/No | Samples |
| Punctuation | em-dashes: N, parens: M | Q7 selection | Yes/No | Samples |
| Burstiness | ratio: Z | Q8 selection | Yes/No | Samples |
| Transitions | most-used: [...] | Q9 selection | Yes/No | Balanced |
| Vocabulary | register: [...] | Q10 selection | Yes/No | Balanced |
| Specificity | detail density: X | Q11 selection | Yes/No | Samples |
| Personal voice | I-frequency: X% | Q12 selection | Yes/No | Samples |
| Opening style | first sentences: [...] | Q13 selection | Yes/No | Samples |

**Conflict resolution**: When samples and preferences disagree, always trust samples for measurable features (sentence length, punctuation). For subjective features (transitions, vocabulary), weight both equally - the user may be describing aspirational voice vs habitual voice, and both have value.
