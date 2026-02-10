# NanoBanana Prompt Template

Use this exact structure when generating NanoBanana image prompts. Every prompt must follow this format to ensure consistent, high-quality output with accurate product representation.

## Prompt Structure

```
[SCENE DESCRIPTION]
A [image style] of [scene/setting description]. [Mood/atmosphere description].

[PRODUCT — COPY FULL SPEC SHEET]
In the [position in frame], [full product spec sheet description — do not abbreviate]. [Product interaction with scene — how is it placed, is someone using it, etc.].

[ART STYLE & MEDIUM]
[Photography style] — [specific style references]. [Texture/finish treatment].

[LIGHTING]
[Primary light source and direction]. [Secondary/fill lighting]. [Overall atmosphere — warm, cool, dramatic, soft, etc.].

[CAMERA]
[Angle — eye-level, overhead, 3/4, etc.]. [Lens feel — wide, portrait, macro, etc.]. [Depth of field — shallow bokeh, deep focus, etc.].

[COMPOSITION]
[Where each element sits — product center-right, text top-left, badge bottom-right, etc.]. [Rule of thirds, centered, asymmetric, etc.]. [Whitespace usage].

[BRAND COLORS]
Background: [color/hex]. Primary text: [color/hex]. Accent elements: [color/hex]. [Any gradients or color treatments].

[TEXT OVERLAYS]
"[EXACT HEADLINE TEXT]" — [font style], [size relative to image], [position], [color]
"[EXACT SUBHEAD TEXT]" — [font style], [size], [position], [color]
"[EXACT CTA TEXT]" — [font style], [size], [position], [color with background treatment]
[Any badge text: "[BADGE TEXT]" — [style], [position]]

[ASPECT RATIO]
--ar [ratio]

[NEGATIVE / EXCLUSIONS]
Do not include: [list of things to explicitly exclude — wrong product features, competing elements, common AI artifacts to avoid]
```

## Rules for Filling the Template

### Scene Description
- Lead with the image style (commercial product photography, lifestyle flat-lay, etc.)
- Be specific about the setting — not "a table" but "a warm-toned wooden kitchen table with soft morning light from a window to the left"
- Describe the mood in sensory terms — not "relaxing" but "calm, meditative atmosphere with soft earth tones and gentle natural lighting"

### Product Section
- ALWAYS copy the full product spec sheet from Phase 1. Never summarize.
- The shape description MUST use the geometric classification from the Shape Protocol (tapered/conical, cylindrical, barrel, tulip, bell, hourglass). Describe the silhouette top-to-bottom and include rim-to-base width ratio. NEVER use vague terms like "rounder," "egg-shaped," or "more compact" — these cause NanoBanana to hallucinate wrong silhouettes.
- Always include "NOT a [wrong shape]" to prevent drift. Example: "tapered/conical cup — rim is widest, straight walls angle inward to a base ~60% of rim width. NOT barrel-shaped, NOT egg-shaped."
- Add context for how the product appears in the scene (being held, sitting on a surface, in use, etc.)
- Include scale reference relative to other objects in the scene

### Art Style
- Match the competitor ad's style unless the concept calls for a shift
- Common effective styles for ads:
  - "Commercial product photography, clean and modern"
  - "Lifestyle photography with warm editorial feel"
  - "Studio product shot with dramatic lighting on seamless background"
  - "Flat-lay photography, overhead, styled with props"
  - "UGC-style photography, casual, authentic-feeling"

### Lighting
- Be specific about direction: "soft diffused light from upper-left", "rim lighting from behind", "even studio softbox lighting"
- Name the mood it creates: "creating warm, inviting shadows" or "producing clean, even illumination"
- If matching a competitor ad, describe the lighting you observed in Phase 1

### Camera
- Match the angle from the competitor ad analysis
- Include depth of field — this affects whether the product or the text is the hero
- "Slight overhead angle, approximately 30 degrees, with shallow depth of field keeping the product sharp and background softly blurred"

### Composition
- Map to a grid: "Product occupies the right 40% of the frame, headline text in the upper-left quadrant"
- Reference the competitor ad's layout recipe from Phase 1
- Be explicit about whitespace: "20% breathing room around the product"

### Brand Colors
- Use hex codes when available
- Specify where each color appears — don't just list them
- "Background: soft sage green (#B8C5A3), headline text: charcoal (#333333), CTA button: warm terracotta (#C67B5C)"

### Text Overlays
- ALWAYS put exact text in quotes — this is critical for AI text rendering
- Specify font style descriptively: "bold condensed sans-serif", "elegant thin serif", "casual handwritten script"
- Be explicit about size: "large, taking up approximately 30% of the image width"
- Include color AND any background treatment: "white text on semi-transparent dark overlay"

### Negative Prompt
- Always include product-specific exclusions from the spec sheet's "What It Must NOT Look Like"
- Add: "no distorted text, no misspelled words, no extra fingers, no brand logos other than [user's brand]"
- If lifestyle: "no uncanny valley faces, no anatomical errors"

## Example: Complete Prompt

```
Commercial product photography of a cozy, well-lit crafting table scene. Warm, inviting atmosphere with earth tones and natural textures. A sense of creative calm and weekend relaxation.

In the center-right of the frame, a compact portable mini pottery wheel approximately 8 inches in diameter with a sage green matte-finish base and cream-colored turntable head. A small USB charging port is visible on the right side of the base. Next to the wheel, a set of 5 wooden pottery tools and 2 blocks of white air-dry clay, all sitting on a natural linen placemat. The wheel is turned slightly to show its profile.

Commercial lifestyle product photography with warm editorial styling. Clean, modern, approachable — like a premium DTC brand product page hero image.

Soft, warm natural light coming from a window to the upper-left, creating gentle shadows. Fill light from the right keeps details visible. Overall warm color temperature, golden-hour feeling.

Eye-level camera angle, slightly elevated (about 15 degrees). Portrait lens feel with medium depth of field — product and immediate props sharp, background elements softly blurred.

Product and accessories occupy the right 60% of the frame. Left 40% is breathing room for text overlay. Rule of thirds — product sits at the right-third intersection. Small potted succulent and coffee mug in soft focus in the upper-left background for lifestyle context.

Background: warm off-white/cream (#F5F0E8). Text: charcoal (#2D2D2D). Accent elements: sage green (#8FA87A) matching the product. CTA: warm terracotta (#C4724E).

"YOUR NEW WEEKEND RITUAL" — bold condensed sans-serif, large, positioned in the upper-left quadrant, charcoal color
"Everything you need to start creating" — light sans-serif, medium, directly below headline, sage green color
"SHOP THE BUNDLE →" — bold sans-serif, small, bottom-left, terracotta on white rounded pill button
"★★★★★ 2,000+ Happy Creators" — small, thin sans-serif, bottom-left below CTA, charcoal color

--ar 1:1

Do not include: full-size pottery wheels, foot pedals, splashguards, electric outlets, kilns, wet clay or water mess, any brand logos, distorted or misspelled text, extra fingers if hands are shown
```

## Gemini/NanoBanana Submission Format

When submitting prompts to Gemini via browser automation, follow these rules:

1. **Prefix**: Always start with "Generate an image:" before the prompt body — this triggers NanoBanana image generation mode
2. **Single block**: Write the prompt as one continuous flowing paragraph or a few paragraphs — do NOT use the section headers (SCENE, PRODUCT, etc.) in the submitted prompt. Those are for your planning structure only. The final prompt Gemini receives should read as natural, descriptive text.
3. **Aspect ratio**: Include as "4:5 portrait" or "1:1 square" in natural language, not the Midjourney-style `--ar` flag
4. **Negative prompt**: Write as "Do not include:" followed by a comma-separated list at the end
5. **Keep it under 500 words** — NanoBanana works best with dense, specific prompts that don't dilute attention

### Example: Submitted Prompt (what Gemini actually receives)

```
Generate an image: Commercial product photography of a cozy, well-lit crafting table scene. Warm, inviting atmosphere with earth tones. In the center-right, a compact portable mini pottery wheel approximately 8 inches in diameter with a sage green matte-finish base and cream-colored turntable head. A small USB charging port on the right side. Next to it, 5 wooden pottery tools and 2 blocks of white air-dry clay on a natural linen placemat. Commercial lifestyle photography, clean and modern, premium DTC brand feel. Soft warm natural light from upper-left window, fill light from right. Eye-level, slightly elevated. Portrait lens, medium depth of field. Product occupies right 60% of frame. Text overlay area in left 40%. Background warm off-white cream. Bold text at top-left: "YOUR NEW WEEKEND RITUAL" in charcoal condensed sans-serif. Below: "Everything you need to start creating" in sage green. Bottom-left badge: "★★★★★ 2,000+ Happy Creators." 4:5 portrait. Do not include: full-size pottery wheels, foot pedals, splashguards, kilns, brand logos, distorted text, extra fingers.
```

## Quick Checklist Before Finalizing Any Prompt

- [ ] Product shape uses geometric classification (tapered/conical, cylindrical, barrel, tulip, bell, hourglass) with silhouette trace and rim-to-base ratio — NO vague terms
- [ ] "NOT a [wrong shape]" included to prevent NanoBanana drift
- [ ] Full product spec sheet description included (not abbreviated)
- [ ] All text strings are in quotes with font/placement instructions
- [ ] Brand colors specified with hex codes and placement
- [ ] Composition explicitly mapped (which elements go where)
- [ ] Negative prompt includes product-specific exclusions
- [ ] Aspect ratio specified in natural language
- [ ] Prompt is under 500 words total
- [ ] Prompt starts with "Generate an image:"
- [ ] Prompt is written as flowing text (no section headers)
