# QC Checklist — Image Verification Protocol

Use this checklist when the user uploads generated images back from NanoBanana. Run every check for every image. Be specific and actionable in your feedback — vague notes like "product looks off" don't help. Say exactly what's wrong and how to fix it.

## The 7 QC Dimensions

### 1. Product Accuracy (HIGHEST PRIORITY)

Compare the generated product against the Product Spec Sheet from Phase 1.

Check:
- [ ] Correct geometric shape — compare silhouette against the spec sheet's geometric classification (tapered/conical, cylindrical, barrel, tulip, bell, hourglass). Trace the outline top-to-bottom: does the rim-to-base width ratio match? Are the walls straight/angled/curved as specified?
- [ ] Shape is NOT one of the excluded geometries from "What It Must NOT Look Like" (e.g., if spec says "NOT barrel-shaped," verify the product isn't barrel-shaped)
- [ ] Correct proportions — height-to-width ratio and wall angle match the spec sheet
- [ ] Correct colors (body color, lid color, accent colors)
- [ ] Correct size relative to scene objects (is it the right scale?)
- [ ] Key distinguishing features present (ports, buttons, logos, textures)
- [ ] No hallucinated features (extra parts, wrong accessories, merged objects)
- [ ] Accessories/components match (if they should be in frame)

Common AI failures to watch for:
- **Wrong silhouette (MOST COMMON)** — tapered cup rendered as barrel/egg, cylindrical mug rendered as tapered, etc. Vague shape prompts are the #1 cause. Always compare against the geometric classification, not vibes.
- Product morphs into a different category (mini wheel becomes full-size wheel)
- Colors shift (sage green becomes teal or gray)
- Extra features appear (pedals, splashguards, controls that don't exist)
- Product merges with background or props
- Scale is wildly off (product looks dollhouse-sized or industrial-sized)

Scoring:
- **Pass**: Product is immediately recognizable and matches spec sheet
- **Needs Fix**: Product is close but has 1-2 fixable issues (slight color shift, minor proportion issue)
- **Fail**: Product is wrong category, severely distorted, or unrecognizable

### 2. Brand Palette

Compare colors in the image against the brand colors extracted in Phase 1.

Check:
- [ ] Background color matches specification
- [ ] Text colors are correct
- [ ] Accent colors appear where specified
- [ ] Overall color temperature matches brand feel
- [ ] No clashing or off-brand colors introduced

Scoring:
- **Pass**: Colors are on-brand, recognizable as the brand's visual identity
- **Needs Fix**: Generally right palette but 1-2 colors are shifted (fixable with color correction)
- **Fail**: Completely wrong palette, looks like a different brand

### 3. Text Legibility

Check whether all text in the image can be read clearly.

Check:
- [ ] Text is sharp, not blurry or pixelated
- [ ] Sufficient contrast between text and background
- [ ] Text is not obscured by other elements
- [ ] Font style approximately matches what was specified
- [ ] Text is not distorted, warped, or fragmented

Scoring:
- **Pass**: All text is immediately readable at ad-display size
- **Needs Fix**: Most text is readable but some characters are slightly off
- **Fail**: Text is garbled, unreadable, or severely distorted

### 4. Text Accuracy

Check whether the text says exactly what was specified in the prompt.

Check:
- [ ] Headline matches exactly (no missing or extra words)
- [ ] Subhead matches exactly
- [ ] CTA matches exactly
- [ ] Badge text matches exactly
- [ ] No hallucinated text (random words or characters that weren't in the prompt)
- [ ] Correct spelling on every word

Scoring:
- **Pass**: All text matches prompt exactly
- **Needs Fix**: Minor issues (one word slightly different, missing punctuation)
- **Fail**: Major text errors (wrong words, missing text, hallucinated text)

Note: If text accuracy is the only issue, often the best fix is to add text in Canva/Figma rather than regenerating. Flag this recommendation.

### 5. Composition Fidelity

Compare the image's layout against the original competitor ad's structure.

Check:
- [ ] Visual hierarchy matches (what draws the eye first, second, third)
- [ ] Element placement matches layout specification (product position, text position)
- [ ] Whitespace usage is appropriate (not too crowded, not too sparse)
- [ ] Focal point is correct (product vs. text vs. lifestyle element)
- [ ] Aspect ratio is correct

Scoring:
- **Pass**: Layout clearly echoes the competitor ad's winning structure
- **Needs Fix**: Generally right structure but some elements are shifted
- **Fail**: Completely different layout from what was specified

### 6. Emotional Tone

Assess whether the image conveys the intended psychological angle.

Check:
- [ ] Does the mood match the concept brief? (calm, urgent, aspirational, fun, etc.)
- [ ] Does the color temperature support the intended emotion?
- [ ] Do the lifestyle elements (if any) resonate with the target demographic?
- [ ] Would the target customer feel "this is for me" when seeing this ad?

Scoring:
- **Pass**: Image clearly conveys the intended emotion and would resonate with the target audience
- **Needs Fix**: Close but something feels slightly off (too clinical, too dark, wrong energy)
- **Fail**: Completely wrong emotional tone (supposed to be calming but feels chaotic)

### 7. Professional Quality

Assess whether the image looks like a real advertisement.

Check:
- [ ] No obvious AI artifacts (extra fingers, melted objects, impossible physics)
- [ ] Consistent lighting across the scene (no conflicting light sources)
- [ ] Realistic shadows and reflections
- [ ] Professional-level composition (not amateurish or stock-photo generic)
- [ ] Would this pass as a real brand's ad in a social feed?

Scoring:
- **Pass**: Looks like a professionally produced advertisement
- **Needs Fix**: Generally professional but has 1-2 minor AI artifacts
- **Fail**: Obviously AI-generated in a distracting way

## QC Report Format

```
IMAGE [X] — "[Concept Name]"
==============================
Overall: [X/7 passing] — [READY / NEEDS REFINEMENT / REGENERATE]

✅ Pass: [list passing dimensions]
⚠️ Needs Fix: [list with specific issues]
   → [Dimension]: [Exact problem]. Fix: [Specific action to take]
❌ Fail: [list with critical problems]
   → [Dimension]: [Exact problem]. Fix: [Regenerate with revised prompt / Use Gemini correction]

Recommendation: [Ship it / Fix text in Canva / Gemini product correction / Regenerate with revised prompt]
```

## Decision Tree After QC

```
All 7 pass? → Ship it (or let human choose from passing variations)
     |
Product fails? → Is the scene/composition good?
     |              Yes → Gemini product correction (Phase 4)
     |              No  → Regenerate with revised NanoBanana prompt
     |
Only text fails? → Fix in Canva/Figma (faster than regeneration)
     |
Composition fails? → Regenerate with revised NanoBanana prompt (adjust layout instructions)
     |
Minor fixes only? → Try one regeneration with tweaked prompt. If still off, fix in editor.
```
