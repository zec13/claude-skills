# NanoBanana Prompt Patterns Reference

Quick-reference patterns for common product swap scenarios. Use these as building blocks when constructing prompts in the main workflow.

## Natural Language Prompt Templates

These can be used instead of (or alongside) JSON prompts. Some users prefer to start with natural language to experiment, then graduate to JSON for production consistency.

### Simple Direct Replacement
```
Using image 1 as the base ad, replace the existing product with the product shown in image 2. Keep everything else in the image exactly the same — preserve the original style, lighting, composition, shadows, and background.
```

### Lighting-Aware Replacement
```
Take the product from image 2 and place it into the scene shown in image 1, replacing the current product. Match the ambient lighting, color temperature, and shadow direction of image 1. The product should look like it was originally photographed in that scene. Preserve all text, graphics, and layout from image 1.
```

### White-Background Product into Ad
```
Image 2 shows a product photographed on a white background. Image 1 is a finished static ad. Replace the product in image 1 with the product from image 2. Adapt the product's appearance to match the scene — adjust reflections, shadows, and scale so it looks natural. Do not change any other element of the ad.
```

### Brand-Safe Replacement
```
Swap the product in image 1 with the product from image 2. This is a brand ad — preserve all brand elements including logos, text overlays, color palette, and layout. The new product should be positioned and scaled to fit naturally in the same space. Match lighting and perspective.
```

### Table/Surface Product Extraction + Placement
```
Image 2 shows a product on a table/surface. Image 1 is a static product ad. Extract just the product from image 2 (ignore the table/background) and place it into image 1, replacing the existing product. Scale and orient the product to fit naturally. Match the lighting, shadows, and color grading of the ad.
```

## JSON Prompt Skeleton

Minimal JSON structure — fill in only the fields that matter for the specific swap:

```json
{
  "task": "product_replacement",
  "scene_image": "image_1",
  "product_image": "image_2",
  "instructions": {
    "action": "Replace the product in image 1 with the product from image 2",
    "preserve": [],
    "adapt_naturally": ["lighting", "shadows", "scale"]
  }
}
```

## Difficulty-Based Prompt Adjustments

### Easy Swap (same category, similar size)
Keep the prompt minimal. Overconstrained prompts for simple swaps tend to produce worse results.
- Use 3-5 preserve items max
- Let `adapt_naturally` handle lighting/shadows without specific instructions
- Skip the `scene_analysis` block

### Medium Swap (different shape, or product on a surface)
Add context about how the current product sits in the scene.
- Include `product_context` field
- Add specific `placement` guidance
- Mention `background_handling` for the reference image

### Hard Swap (person holding product, dramatic size difference, heavy branding)
Use full JSON schema with all fields populated. Consider suggesting staged approach.
- Full `scene_analysis` with detailed `current_product` and `product_context`
- Detailed `preserve` list naming every text/logo element
- Explicit `placement` instructions for hand/grip if applicable
- May need staged prompts (extract → place → polish)

## Staged Prompt Sequence (For Complex Swaps)

### Stage 1: Product Extraction
```
Using image 2, isolate just the product on a clean transparent background. Remove the table/surface and any background elements. Preserve the product's exact shape, color, texture, and details.
```

### Stage 2: Product Placement
```
Place the extracted product into image 1, replacing the existing product. Match the position, scale, and orientation of the original product. The new product should sit naturally in the same space.
```

### Stage 3: Lighting and Shadow Refinement
```
Adjust the product's lighting and shadows to perfectly match the scene in image 1. The light direction, shadow softness, and color temperature should be consistent with the rest of the image.
```

### Stage 4: Final Polish
```
Do a final pass to ensure the product blends seamlessly into the ad — fix any edge artifacts, match color grading exactly, and ensure shadows are consistent with the scene's light source. The result should look like the product was originally photographed for this ad.
```

## API Endpoint Reference

| Provider | Endpoint | Model |
|----------|----------|-------|
| Google (standard) | `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent` | gemini-2.5-flash-image |
| Google (pro) | `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent` | gemini-3-pro-image-preview |
| NanoBananaAPI.ai | See their docs — same body format, different URL | Both models |
| Together AI | See their docs | nano-banana-pro |

## Key Tips

- Image order in the `parts` array MUST match the image references in the prompt (image_1 first, image_2 second)
- JSON prompts are ~40% faster and use ~25-30% less memory vs. natural language
- For `responseModalities`, use `["IMAGE"]` for image-only output, `["TEXT", "IMAGE"]` to also get a text description
- Total request size limit is ~20MB for inline base64 images
- Expect ~70-80% usable output rate — prompt tuning and iteration are normal
