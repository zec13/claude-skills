# Nano Banana — Product Image Swap for Static Ads

## What Is Nano Banana?

"Nano Banana" is Google's nickname for **Gemini 2.5 Flash Image**, their image generation and editing model. "Nano Banana Pro" refers to **Gemini 3 Pro Image**. Both support multi-image input, which is exactly what you need — you can pass in a reference product image + an existing ad image, and prompt the model to swap the product.

---

## Core API Structure (What You Send)

Every request to the Gemini API for image editing follows this JSON structure. You POST to one of these endpoints:

- `gemini-2.5-flash-image` (standard — ~$0.039/image)
- `gemini-3-pro-image-preview` (pro — higher fidelity, ~$0.12/image)

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=YOUR_API_KEY
```

### Base JSON Body

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "YOUR PROMPT GOES HERE"
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "<BASE64_ENCODED_PRODUCT_IMAGE>"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "<BASE64_ENCODED_AD_IMAGE>"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

**Key points:**
- The `parts` array holds your text prompt + up to 14 reference images as `inline_data`
- Each image is base64-encoded with its MIME type
- Set `responseModalities` to `["IMAGE"]` for image-only output, or `["TEXT", "IMAGE"]` to also get a text description back
- Inline data works for files under ~20MB total request size

---

## Prompt Templates for Product Swapping

These are the prompt templates you can drop into the `"text"` field above. Each one is designed for a slightly different version of your use case.

### Template 1: Direct Product Replacement (Simplest)

```
Using image 2 as the base ad, replace the existing product with the product shown in image 1. Keep everything else in the image exactly the same — preserve the original style, lighting, composition, shadows, and background.
```

### Template 2: Product Placement with Lighting Match

```
Take the product from image 1 and place it into the scene shown in image 2, replacing the current product. Match the ambient lighting, color temperature, and shadow direction of image 2. The product should look like it was originally photographed in that scene. Preserve all text, graphics, and layout from image 2.
```

### Template 3: Product Swap with Scene Adaptation

```
Image 1 shows a product photographed on a white background. Image 2 is a finished static ad. Replace the product in image 2 with the product from image 1. Adapt the product's appearance to match the scene — adjust reflections, shadows, and scale so it looks natural. Do not change any other element of the ad (text, background, other objects, layout).
```

### Template 4: Product Swap Preserving Brand Elements

```
Swap the product in image 2 with the product from image 1. This is a brand ad — preserve all brand elements including logos, text overlays, color palette, and layout. The new product should be positioned and scaled identically to the original product. Match lighting and perspective exactly.
```

### Template 5: Table/Surface Product Shot → Ad Placement

```
Image 1 shows a product on a table/surface. Image 2 is a static product ad. Extract just the product from image 1 (ignore the table/background) and place it into image 2, replacing the existing product. Scale and orient the product to fit naturally. Match the lighting, shadows, and color grading of the ad.
```

---

## JSON Structured Prompts (For Consistency at Scale)

If you're generating multiple variations or want more precise control, use a JSON-structured prompt inside the text field. Nano Banana understands JSON formatting and it gives more repeatable results.

### JSON Prompt — Product Swap

```json
{
  "task": "product_replacement",
  "source_image": "image_1",
  "source_description": "Product photograph on white/neutral background",
  "target_image": "image_2",
  "target_description": "Finished static product ad",
  "instructions": {
    "action": "Replace the product in the target image with the product from the source image",
    "preserve": ["background", "text_overlays", "brand_elements", "layout", "color_grading"],
    "adapt": ["lighting_direction", "shadow_angle", "shadow_softness", "color_temperature", "scale", "perspective"],
    "constraints": "Do not alter any element except the product itself. The final image should look like the product was originally shot for this ad."
  },
  "style": {
    "photography_type": "commercial product photography",
    "lighting": "match target image exactly",
    "post_processing": "match target image color grade"
  }
}
```

### JSON Prompt — Product into Lifestyle Scene

```json
{
  "task": "product_placement",
  "label": "lifestyle-ad-product-swap",
  "source": {
    "image": "image_1",
    "description": "Product on white background or table",
    "extract": "product only, ignore background"
  },
  "target": {
    "image": "image_2",
    "description": "Lifestyle/scene-based static ad"
  },
  "composition": {
    "product_position": "replace existing product in scene",
    "scale": "match original product size in scene",
    "orientation": "match original product angle"
  },
  "lighting": {
    "method": "match target scene",
    "shadow_direction": "consistent with scene light source",
    "reflection": "add if surface is reflective"
  },
  "preserve": ["all text", "all logos", "background scene", "other objects", "overall layout"],
  "output": {
    "resolution": "match input",
    "format": "photorealistic, commercial quality"
  }
}
```

---

## Staged Workflow (For Complex Swaps)

If a single prompt doesn't nail it, break the work into a chain of smaller edits:

1. **Step 1 — Product extraction:** "Using image 1, isolate just the product on a transparent/white background. Remove the table and any other background elements."
2. **Step 2 — Product placement:** "Place the product from image 1 into image 2, replacing the existing product. Match position, scale, and orientation."
3. **Step 3 — Lighting/shadow refinement:** "Adjust the product's lighting and shadows to perfectly match the scene in image 2."
4. **Step 4 — Final polish:** "Do a final pass to ensure the product blends seamlessly — fix any edge artifacts, match color grading, and ensure shadows are consistent."

---

## Pre-Built n8n Automation Workflows

If you want to automate this at scale, these n8n workflow templates do exactly what you're describing:

| Workflow | What It Does |
|----------|-------------|
| [Generate Unlimited E-Commerce Ad Creative](https://n8n.io/workflows/8226) | Takes product images + influencer/model photos → generates ad creative with product naturally placed |
| [Generate Product Mockups](https://n8n.io/workflows/8194) | Takes product image → generates professional mockup scenes |
| [Generate Product Creative via Defapi](https://n8n.io/workflows/8484) | Form-based: submit product image URL + text prompt → AI-generated creative |
| [Create Viral Ads + Publish](https://n8n.io/workflows/8428) | Full pipeline: product image → ad creative → video → music → publish |
| [Create High Quality UGC Images](https://n8n.io/workflows/8644) | Multiple base images + prompts → UGC-style product content |
| [Facebook Ad Thief (n8n + GitHub)](https://github.com/lucaswalter/n8n-ai-automations) | Scrapes competitor ads → regenerates with your product using Nano Banana |

---

## API Access Options

| Provider | Model | Price | Notes |
|----------|-------|-------|-------|
| Google AI Studio | gemini-2.5-flash-image | ~$0.039/image | Official, web UI or API |
| Google AI Studio | gemini-3-pro-image-preview | Higher | Pro model, better fidelity |
| [NanoBananaAPI.ai](https://nanobananaapi.ai/) | Both models | ~$0.02/image | 50%+ cheaper than Google direct |
| [Together AI](https://www.together.ai/models/nano-banana-pro) | Nano Banana Pro | Varies | Up to 14 input images |
| [Puter.js](https://developer.puter.com/tutorials/free-unlimited-nano-banana-api/) | Both models | Free | Frontend-only, no API key needed |

---

## Key Tips

- **Start with plain text prompts** to find the right wording, then switch to JSON for production/consistency
- **Image order matters** — reference images in your prompt as "image 1", "image 2" etc. matching the order they appear in the `parts` array
- **For white-background product photos**, explicitly tell the model to "extract just the product, ignore the background"
- **Lighting match is the hardest part** — if results look off, try the staged workflow (swap first, then fix lighting separately)
- **JSON prompts are ~40% faster** and use ~25-30% less memory vs. natural language
- **Expect some imperfect outputs** — hand placement, edge artifacts, and lighting mismatches are common. Plan for ~70-80% usable rate with prompt tuning

---

## Source Links

- [Atlabs AI — Nano Banana Pro JSON Prompting Guide](https://www.atlabs.ai/blog/nano-banana-pro-json-prompting-guide-master-structured-ai-image-generation)
- [GitHub — awesome-nanobanana-pro (curated prompts)](https://github.com/ZeroLu/awesome-nanobanana-pro)
- [Max Woolf — Nano Banana JSON Prompt Engineering](https://minimaxir.com/2025/11/nano-banana-prompts/)
- [God of Prompt — How to Write JSON Prompts](https://www.godofprompt.ai/blog/write-json-prompts-for-gemini-nano-banana)
- [SuperMaker AI — Best AI Replace Prompts](https://supermaker.ai/blog/best-ai-replace-prompts-to-transform-your-photos-instantly/)
- [Google Official Docs — Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [GitHub — n8n AI Automations (Lucas Walter)](https://github.com/lucaswalter/n8n-ai-automations)
- [GitHub — Nano Banana JSON Schema Gist](https://gist.github.com/alexewerlof/1d13401a7647339469141dc2960e66a9)
- [freeCodeCamp — Nano Banana for Image Generation](https://www.freecodecamp.org/news/nano-banana-for-image-generation/)
- [ImagineArt — JSON Prompting for AI Image Generation](https://www.imagine.art/blogs/json-prompting-for-ai-image-generation)
