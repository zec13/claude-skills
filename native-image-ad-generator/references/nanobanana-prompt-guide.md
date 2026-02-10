# NanoBanana Prompt Engineering Guide

This guide covers how to write text-to-image prompts that generate high-quality, brand-accurate static ad images when pasted into Google Gemini's image generation.

## Prompt Structure

Every NanoBanana prompt should follow this sequence. Order matters — Gemini weighs earlier descriptions more heavily.

### 1. Scene & Setting (Opening)

Start with the overall scene type and mood. This anchors everything that follows.

```
Commercial product photography of [product] on [surface/setting].
[Background description]. [Atmosphere/mood in 5-10 words].
```

**Examples:**
- "Commercial product photography of a ceramic travel cup on a warm-toned wooden tabletop surface. Dark charcoal background creating dramatic contrast. Warm, artisan atmosphere with earth tones."
- "Lifestyle product photography of a hand holding a ceramic travel cup in warm morning light. Cozy desk near a window. Golden, intimate atmosphere."
- "Split-screen comparison image showing two coffee cups side by side on a marble counter. Clean, clinical left side vs. warm inviting right side."

### 2. Product Description (Critical Section)

This is the most important section. AI image generators will hallucinate product details if you're not extremely specific. Pull physical descriptions directly from the research dossier's product spec sheet.

**Must include:**
- Exact dimensions/scale reference
- Material and finish (matte vs. glossy, texture description)
- Color with specificity (not just "green" — "soft sage green with a fine speckled texture like natural stone")
- Form factor (shape, proportions, distinguishing features)
- Accessories shown (lids, sleeves, cases, etc.)

**Must also include "NOT" descriptions:**
- What the product must NOT look like (critical for preventing AI hallucinations)
- Common wrong interpretations to explicitly exclude

```
A handmade ceramic travel cup approximately 5-6 inches tall with a soft sage
green speckled matte glaze finish. The ceramic body has a slightly tapered
cylindrical form — wider at the rim, narrowing toward the base — with a fine
speckled texture like natural stone. On top sits a warm cream/beige silicone
slip-on lid with a smooth dome top and slight rim overhang. The cup has no
handle. The glaze is matte, not glossy, with subtle natural variations.
```

### 3. Scene Elements (Supporting Props)

If the concept includes props or environmental elements, describe them after the product. Keep them secondary — they should support, not compete with, the hero product.

```
In the soft-focus background, a small pour-over coffee dripper on a glass
carafe and a bag of specialty coffee beans, slightly blurred but recognizable.
```

### 4. Text Overlays (If Applicable)

Gemini has improving but still imperfect text rendering. Keep text overlays simple and short.

**Rules for text in prompts:**
- Maximum 3-5 words per text element — shorter text generates more accurately
- Specify exact copy, font style, size relative to image, placement, and color
- Use descriptive font terms: "bold condensed sans-serif", "thin elegant serif", "handwritten script"
- Specify placement precisely: "top 20% of image, centered", "bottom-left corner"
- Keep the total number of text elements to 3 or fewer per image

```
At the top of the image, bold text: "PURE CERAMIC. PURE TASTE." in large
condensed sans-serif, cream white. Below in smaller text: "Handmade for
your morning." At the bottom-left, small: "4.9 stars 236 Reviews"
```

**Common text failure modes to avoid:**
- Long sentences (Gemini will misspell or truncate)
- Multiple paragraphs of text
- Text in unusual fonts or very small sizes
- Overlapping text elements

### 5. Photography Style

Specify the overall photographic approach:

```
Commercial lifestyle photography with warm, editorial styling. Premium
DTC brand aesthetic. [Specific mood reference].
```

### 6. Lighting

Lighting dramatically affects mood and product perception. Be specific:

```
Soft warm directional light from the upper-left creating gentle highlights
on the cup rim and lid, with soft shadows falling to the right. Warm color
temperature overall.
```

**Lighting vocabulary:**
- Directional vs. diffused
- Warm vs. cool color temperature
- Key light direction (upper-left, window-right, backlit)
- Fill light presence
- Rim/edge lighting for product separation
- Natural vs. studio

### 7. Camera & Composition

```
Slightly elevated camera angle, approximately 20 degrees above eye level.
Medium depth of field — product is tack-sharp, background falls to smooth blur.
```

**Camera terms that work well:**
- Eye-level, slightly elevated (15-30 degrees), overhead/flat-lay, worm's-eye
- Shallow/medium/deep depth of field
- Close-up, medium shot, wide establishing shot
- Portrait lens feel (85mm equivalent)

### 8. Composition & Layout

Specify where elements sit in the frame:

```
Cup occupies the center-right 40% of the frame. Icon badges span the top 25%.
Warm wooden surface fills the bottom 30%. Rule of thirds positioning.
```

### 9. Color Specifications

Include hex codes when available from brand guidelines. This helps maintain brand consistency:

```
Background: deep charcoal (#2D3436). Product: sage green (#B5C4A1) body
with cream (#F0E6D8) lid. Text: cream white (#FFF8F0).
```

### 10. Text Specifications (Detailed)

If the image includes text overlays, repeat them with precise formatting specs:

```
"PURE CERAMIC. PURE TASTE." — bold condensed sans-serif, large (spanning 80%
of image width), top of image, cream white with subtle drop shadow
"Handmade for your morning." — light sans-serif, medium-small, below headline
```

### 11. Aspect Ratio

End every prompt with `--ar 4:5` — the standard Meta/Instagram feed ad format. This is the default and only ratio generated per concept.

Compose images for 4:5 portrait framing — product centered in frame, text overlays in the top or bottom third with comfortable margins.

### 12. Negative Prompts

End with explicit exclusions to prevent common AI mistakes:

```
Do not include: multiple cups, handles on the cup, metallic sheen, glossy
finish, dramatic drip-glaze patterns, screw-on lids, straws, distorted or
misspelled text, product that looks mass-produced
```

## Concept-Specific Prompt Patterns

### Before & After
Use a split-screen composition. Left side shows the "before" (problem state) with cooler, harsher lighting. Right side shows the "after" (with product) with warm, inviting lighting. A clear visual divider or gradient separates the two halves. The product appears on the "after" side.

### Comparison / Us vs. Them
Similar to before/after but framed as product comparison. Two products side by side — the competitor product on the left (generic, cold, industrial) and your product on the right (warm, handmade, beautiful). Use labeling text.

### Big Benefit Statement
Dominant bold text headline occupying the top 30-40% of the image. Hero product below or alongside. Minimal other elements. The text IS the focal point, product provides proof.

### Value Triptych
Three circular icon badges with short value-prop labels, evenly spaced across the top third. Product below on a warm surface. Dark moody background for premium feel. Proven high-performer from competitor research.

### Testimonial / Review
Customer quote as the dominant text element, in quotation marks, with a subtle attribution. Product shown alongside or below. Warm, personal lighting. Design should feel like a social media testimonial post.

### UGC-Style
Slightly imperfect framing, natural lighting, casual setting (kitchen counter, desk, car cupholder). Should feel like a real customer took the photo, not a professional photographer. Less polished, more authentic.

### Lifestyle / Aspirational
Person using the product in a beautiful, aspirational setting. The product is present but the lifestyle is the hero — the viewer wants to BE in this scene. Warm, golden, editorial photography style.

## Quality Checklist

Before submitting a prompt, verify:

- [ ] Product description matches the research dossier spec sheet exactly
- [ ] "Must NOT look like" exclusions are included
- [ ] Text overlays are 5 words or fewer per element
- [ ] No more than 3 text elements total
- [ ] Lighting and mood match the concept's emotional intent
- [ ] Color hex codes are included where available
- [ ] Prompt ends with `--ar 4:5`
- [ ] Negative prompts cover common AI hallucination risks for this product category
- [ ] The prompt reads as natural English paragraphs, not a bullet list
