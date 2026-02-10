---
name: product-placer
description: |
  Generate a JSON swap prompt for NanoBanana/Gemini that replaces an AI-generated product in an ad with the real product photo. Claude analyzes both images and outputs a structured JSON prompt the user pastes into NanoBanana alongside the uploaded ad (image 1) and product reference (image 2). Works with any brand or product — no brand-specific knowledge required.

  TRIGGERS: place product, swap product, product placement, replace product in ad, fix product in ad, product doesn't match, wrong product, put our product in, composite product, product swap, real product, actual product image, product isn't right, swap the product, place real product, product compositing
---

# Product Placer

Generate a JSON prompt for NanoBanana/Gemini to swap an AI product in an ad with the real product photo.

## Inputs

1. **Image 1 (ad):** The ad containing the AI-generated product
2. **Image 2 (reference):** The real product photo to swap in

The user provides both images. If only one is provided, ask for the other.

## Workflow

### 1. Get both images

Save working copies to the ad's output folder:
```
{ad_folder}/product_swap_ad.png
{ad_folder}/product_swap_reference.png
```

If the user provides a URL for the product reference instead of a file, download it first.

### 2. Analyze both images

Read both images with the Read tool. Document:

**Ad (image 1):**
- AI product appearance: shape (see shape protocol below), color, texture, material, distinguishing features
- Exact text overlays — every word, verbatim
- Product context: how it's held/placed, angle, scale relative to scene
- Scene: lighting direction, background elements, mood

**Real product (image 2):**
- Actual appearance: shape (see shape protocol below), color, texture, material, distinguishing features
- Key visual differences from the AI version (these become the `key_differences` array)

#### Shape Analysis Protocol (CRITICAL)

Vague shape words like "rounder," "egg-shaped," or "more compact" cause NanoBanana to hallucinate the wrong product. You MUST describe shape using this structured method:

**Step A — Silhouette trace (top to bottom):**
Describe the product's outline as a path from top to bottom. Example: "Rim is the widest point (~3.5in), walls angle inward in a straight taper to a flat base (~2in wide)" vs "Rim is ~3in, walls bow outward to a belly (~3.5in at widest), then curve back inward to a ~2.5in base."

**Step B — Classify the base geometry using these terms:**
- **Cylindrical** — straight vertical walls, rim and base roughly equal width
- **Tapered / conical** — wider at top, narrower at base, walls are straight but angled
- **Tulip** — slight outward flare at the rim, then narrows toward base
- **Barrel / convex** — walls bow outward, widest in the middle
- **Bell** — narrow at top, flares wider toward the base
- **Hourglass** — pinches in the middle, wider at top and bottom

NEVER use "egg-shaped," "rounder," "more compact," or other subjective terms as the primary shape description. Always lead with the geometric classification, then add nuance.

**Step C — Key ratios:**
- Rim-to-base width ratio (e.g., "rim is ~1.5x wider than the base")
- Height-to-width ratio (e.g., "about as tall as it is wide at the rim" or "1.5x taller than its rim width")
- Wall angle (e.g., "walls angle inward at roughly 10 degrees" or "walls are nearly vertical")

**Step D — Write the key_differences using the geometric terms:**
BAD: "Shape: replace the straight-walled body with the rounder, egg-shaped profile"
GOOD: "Shape: replace the cylindrical straight-walled body with a tapered/conical profile — the rim is the widest point, walls angle inward in a straight line to a base that is roughly 60% of the rim width. The silhouette is a truncated cone, NOT a barrel or egg."

Always state what the shape IS and what it is NOT, because NanoBanana tends to over-interpret vague descriptors.

### 3. Generate the JSON prompt

Build the JSON object. Fill every field from your analysis — no placeholders:

```json
{
  "action": "edit",
  "source": "image_1",
  "instruction": "Replace the [product type] in this image with the exact [product type] from image 2. Do not regenerate — edit the original image only.",
  "preserve": {
    "scene": "[describe: hands/surface, background, lighting direction and quality]",
    "text": ["[exact headline]", "[exact subtitle]", "[any other text or logos]"],
    "composition": "[describe: product position, angle, framing, scale]"
  },
  "replace": {
    "target_object": "[product type] in image 1",
    "replacement_source": "[product type] from image 2",
    "key_differences": [
      "[difference 1: most important visual change needed]",
      "[difference 2: second most important]",
      "[difference 3: if applicable]"
    ]
  }
}
```

**Rules:**
- `"action"` — always `"edit"`, never `"generate"`. This tells the model to modify image 1, not create from scratch.
- `"source"` — always `"image_1"`.
- `"instruction"` — must include "exact [product] from image 2" and "Do not regenerate."
- `"preserve" > "text"` — list every visible text element word-for-word. Missed text gets dropped by NanoBanana.
- `"replace" > "key_differences"` — only what's DIFFERENT between the AI product and the real one. Don't describe things that already match. Be specific about color, texture, shape, and any features that need adding or removing.
- **Shape differences MUST use the geometric classification from the Shape Analysis Protocol.** Lead with the geometry name (tapered, cylindrical, barrel, etc.), then describe the silhouette top-to-bottom, then state the rim-to-base ratio. Always include "NOT a [wrong shape]" to prevent NanoBanana from drifting. Example: "Tapered/conical — rim is widest, straight walls angle inward to a base ~60% of rim width. NOT barrel-shaped, NOT egg-shaped."

### 4. Generate iteration prompts

Build 2 follow-up JSON prompts for common failures:

**If product doesn't match reference:**
```json
{
  "action": "edit",
  "source": "previous_output",
  "instruction": "The [product] doesn't match image 2. Look at image 2 again — use that exact [product]. Do not generate a new one.",
  "fix": "[describe specific detail that's wrong]"
}
```

**If scene changed:**
```json
{
  "action": "edit",
  "source": "image_1",
  "instruction": "Start over from image 1. Only replace the [product] with the one from image 2. Do not change anything else.",
  "preserve": {
    "scene": "[re-list scene elements]",
    "text": ["[re-list all text]"]
  }
}
```

### 5. Deliver

Present to the user:

```
**Image 1 (ad) — upload first:**
[computer:// link to product_swap_ad.png]

**Image 2 (product reference) — upload second:**
[computer:// link to product_swap_reference.png]

**Open NanoBanana / Gemini, upload both images, paste this JSON prompt:**

[primary JSON prompt]

**If the product doesn't match, paste this:**

[iteration JSON 1]

**If the scene changed, paste this:**

[iteration JSON 2]
```

### 6. QC (when user shares result)

Compare result to both source images:
1. Does the product match image 2? (shape, color, texture, key features)
2. Does the scene match image 1? (background, lighting, hands/surface)
3. Is all text preserved word-for-word?
4. Pass → save with `_PLACED` suffix in the ad's output folder
5. Fail → write a targeted iteration prompt addressing the specific issue
