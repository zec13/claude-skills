---
name: nano-banana-product-swap
description: Generate JSON prompts for swapping products in static ad images using NanoBanana (Gemini 2.5 Flash Image / Gemini 3 Pro Image). Use when user uploads an ad image and a product reference image and wants a ready-to-paste prompt for NanoBanana. Triggers include "product swap", "swap the product", "NanoBanana prompt", "nano banana", "replace product in ad", "product image swap", "ad creative swap". Outputs both a JSON structured prompt and a full API request body. Does NOT call the NanoBanana API directly — only generates the prompt text.
---

# NanoBanana Product Swap Prompt Generator

Generate optimized JSON prompts for swapping a product into an existing static ad image using Google's NanoBanana (Gemini image models). The user provides two images, and you output a prompt they can paste directly into NanoBanana's UI plus the full API request body for automation workflows.

## How This Skill Works

The user gives you two images. You analyze both, then generate a tailored prompt. You do NOT call the NanoBanana API — you produce the prompt as text output that the user copies and uses themselves. This saves model credits and gives the user full control over generation.

## Workflow

### Step 1: Receive and Analyze the Images

The user will upload two images:

- **Image A — The Ad:** An existing static product ad. This is the "scene" that should be preserved. It may contain background elements, text overlays, brand logos, lifestyle context, models/people, or other design elements.
- **Image B — The New Product:** A photo of the product that should replace whatever product is currently in the ad. This is typically shot on a white background, a table, or another simple surface.

When you receive the images, study them carefully and note:

1. **What product is currently in the ad** (Image A) — its size, position, angle, how it interacts with the scene (is someone holding it? is it on a surface? is it floating?).
2. **What the new product looks like** (Image B) — its shape, color, size relative to the original, any distinctive features. Also note the background — is it white/clean, or does it include a surface/context that should be ignored?
3. **The ad's visual characteristics** — lighting direction, color grading/temperature, style (minimalist, lifestyle, bold, etc.), any text or brand elements present.
4. **The difficulty level** of the swap — a simple swap (similar product, same category) vs. a complex one (different shape/size, product is being held, etc.).

Tell the user what you observed in a brief summary before generating the prompt. This builds trust and lets them correct any misreading.

### Step 2: Generate the JSON Structured Prompt

Build a JSON prompt tailored to what you observed in the images. The JSON goes inside the `"text"` field of the NanoBanana API request.

The prompt should strike a balance between preserving the ad and producing natural results. Key principles:

- **Be specific about what to preserve** — call out text, logos, layout, background, and other non-product elements by name when you see them.
- **Be flexible about adaptation** — let the model adjust lighting, shadows, reflections, and scale naturally rather than demanding pixel-perfect matching. Overconstrained prompts produce stiff, unnatural composites.
- **Reference the images by order** — Image 1 is the ad (the scene to preserve), Image 2 is the new product. This matches the order they appear in the API `parts` array.
- **Describe the product context** — if the product in the ad is being held, sitting on a surface, or interacting with the scene in some way, describe that interaction so the model knows how to place the new product.

Use this JSON schema as your foundation, then customize the values based on what you actually see in the images:

```json
{
  "task": "product_replacement",
  "scene_image": "image_1",
  "product_image": "image_2",
  "scene_analysis": {
    "current_product": "[describe the product currently in the ad]",
    "product_context": "[how the product sits in the scene — held, on surface, floating, etc.]",
    "scene_elements": "[key non-product elements — background, text, logos, people, props]"
  },
  "product_analysis": {
    "new_product": "[describe the new product from the reference image]",
    "background_handling": "[ignore white background / extract from table / etc.]"
  },
  "instructions": {
    "action": "Replace the product in image 1 with the product from image 2",
    "placement": "[specific guidance based on how the current product sits in the scene]",
    "preserve": ["[list specific elements you see that should NOT change]"],
    "adapt_naturally": ["lighting", "shadows", "reflections", "scale", "perspective"],
    "tone": "[describe the overall feel — the result should look like the product was originally photographed for this ad]"
  },
  "style": {
    "photography_type": "[match what you see — commercial, lifestyle, studio, editorial, etc.]",
    "lighting_notes": "[describe the dominant light direction and quality you observe]",
    "color_grade": "[warm, cool, neutral, vibrant, muted — match the ad]"
  }
}
```

Customize every field based on your actual observation of the images. Do NOT use generic placeholder values — the whole point is that you've looked at the images and written a prompt that's specific to this particular swap.

### Step 3: Generate the Full API Request Body

After the JSON prompt, also output the complete API request body the user can use for automation (n8n, scripts, etc.). Use this structure:

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "[THE JSON PROMPT FROM STEP 2 GOES HERE, STRINGIFIED]"
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "[BASE64_AD_IMAGE — paste your ad image base64 here]"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "[BASE64_PRODUCT_IMAGE — paste your product reference base64 here]"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["IMAGE"]
  }
}
```

**Important notes to include with the API body:**

- The endpoint is: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=YOUR_API_KEY`
- For higher fidelity, swap the model to `gemini-3-pro-image-preview`
- The image order in `parts` MUST match the order referenced in the prompt (image_1 = ad, image_2 = product)
- Set `responseModalities` to `["TEXT", "IMAGE"]` if the user also wants a text description back alongside the generated image
- For third-party providers (NanoBananaAPI.ai, Together AI), the body structure is the same but the endpoint URL differs

### Step 4: Present the Output

Structure your response clearly with three sections:

1. **Image Analysis** — Brief description of what you see in both images and how you've tailored the prompt.
2. **JSON Prompt** — The prompt to paste into NanoBanana's text field. Present it in a clean code block.
3. **Full API Request Body** — The complete request body with placeholder slots for base64 images. Present in a separate code block.

Optionally, if the swap looks particularly complex (product is held by a person, dramatically different shape, etc.), suggest a **staged approach** — break the swap into multiple sequential prompts:
- First prompt: Extract the product, adapt lighting
- Second prompt: Place into scene, blend naturally
- Third prompt: Final polish pass

Only suggest staging when a single prompt is unlikely to nail it. For straightforward swaps (similar-shaped products, simple backgrounds), one prompt is fine.

## Edge Cases

### The new product is a very different shape/size than the original
Add explicit guidance about scaling and repositioning. Something like: `"placement": "The new product is significantly [larger/smaller/wider/taller] than the original. Scale it to fit naturally in the same space — it does not need to be the exact same size, but should look proportional to the scene."`

### The product is being held by a person
This is the hardest case. Call it out: `"placement": "The current product is being held by a person. Place the new product in their hand in the same position. Pay careful attention to finger placement and grip — the hand should look like it's naturally holding this specific product."`

### There's significant text/branding in the ad
List every text element you can see: `"preserve": ["headline text reading '[exact text]'", "logo in [position]", "CTA button reading '[text]'", "tagline at bottom"]`

### The product reference has a busy background (not white)
Tell the model to extract: `"background_handling": "The reference image shows the product on [describe surface]. Extract only the product itself — ignore the [table/background/surface]. Use the product's shape, color, and features but not its surroundings."`

### User wants multiple variations
Generate 2-3 prompt variants with slight differences in tone or instruction specificity. Label them (e.g., "Version A: Tight match", "Version B: Natural adaptation", "Version C: Creative freedom") so the user can test which produces the best results.

## What This Skill Does NOT Do

- It does NOT call the NanoBanana API or generate images directly
- It does NOT modify the uploaded images in any way
- It does NOT require an API key — it only produces prompt text
- It does NOT handle video or animated ad formats — static images only
