---
name: ad-swipe-engine
description: "End-to-end ad swipe pipeline. Reverse-engineer a competitor ad, recreate it for any brand, generate 3 concept images via Gemini/NanoBanana, and save them to an output folder. One-shot execution from competitor image to finished ad images. Use when the user wants to \"swipe\" or adapt a competitor ad, recreate an ad for their brand, generate ad concepts from a competitor creative, or build static image ads. Triggers include: swipe ad, steal ad, recreate ad, ad swipe, competitor ad, static ad, image ad, NanoBanana, ad concept, reverse engineer ad, adapt ad, ad creative. Requires: competitor ad image, brand name, and target product. Auto-discovers brand research docs from the user's Brands folder on Desktop."
---

# Ad Swipe Engine

Reverse-engineer a winning competitor ad and recreate it for any brand — end-to-end from competitor image to 3 finished AI-generated ad concepts saved to an output folder. No manual steps, no copy-pasting prompts. Claude handles everything: ad teardown, brand context, product anchoring, prompt engineering, browser-based image generation via Gemini/NanoBanana, downloading, file organization, and QC.

## How It Works

This skill runs a 5-phase autonomous pipeline:

1. **Teardown** — Analyze the competitor ad's structure, psychology, and visual recipe
2. **Brand + Product Anchoring** — Pull brand context from the research dossier and build a product spec sheet from the product page
3. **Concept Generation** — Create 3 ad concept variations with full NanoBanana image-gen prompts
4. **Image Generation** — Open Gemini in the browser, submit each prompt, wait for NanoBanana to generate, save each image
5. **QC + Delivery** — Review generated images, organize them in an output folder, present results

The key innovation is **Product Anchoring** — a detailed product spec sheet threads through every prompt so the product is never hallucinated or lost.

## Required Inputs

The user provides three things:

1. **Competitor ad image** — uploaded in the conversation
2. **Brand name** — e.g., "Table Clay" (used to locate the brand folder)
3. **Target product** — e.g., "Travel Cup" or a product URL (used for the product spec sheet)

Optional inputs the user may provide:
- A product URL (Claude will scrape it via browser for product details, images, price, reviews)
- Specific ad angle preferences (e.g., "I want a lifestyle angle")
- Target platform/aspect ratio (defaults to 4:5 portrait for Meta feed ads)

## Phase 1: Auto-Discovery + Data Gathering

### Step 1A: Find Brand Assets

Scan the user's mounted folder for brand research. Expected location:

```
{mounted-folder}/Desktop/Brands/{BrandName}/
```

Discovery logic:
1. Look for a folder matching the brand name (case-insensitive, fuzzy — "Table Clay" matches "TableClay" or "tableclay")
2. Inside, find the research document (files containing "research", "dossier", "strategy", "brand" in the filename, with .docx/.pdf/.md extensions)
3. Also check `{mounted-folder}/Brands/{BrandName}/` as a fallback path

If the folder or research doc isn't found, ask the user to point to the right path or upload the brand research directly. Don't block — work with whatever is available.

### Step 1B: Get Product Details

If the user provided a product URL:
1. Navigate to the product URL using the Chrome browser tools (WebFetch often gets 403'd by e-commerce sites)
2. Take a screenshot of the product page
3. Extract: product name, price, description, key features, review count/rating, available colors/variants
4. Take note of the primary product image visible on the page

If no URL is provided, ask the user for the product name and key details, or look for product info in the brand research dossier.

## Phase 2: Ad Teardown + Product Anchoring

### Step 2A: Competitor Ad Deep Audit

Analyze the uploaded competitor ad image across four dimensions:

**Visual Hierarchy** — Layout structure, primary focal point, secondary elements, visual flow path, aspect ratio

**Brand & Design Elements** — Color palette (estimate hex codes), font styles, image style (UGC/studio/lifestyle/etc.), contrast/whitespace/framing, texture treatments

**Copy & Hook Breakdown** — Extract ALL visible text, identify hook/promise/CTA/social proof, classify the primary psychological angle (pain relief, fear/urgency, status/identity, curiosity, ease/simplicity, authority/credibility, transformation, comparison)

**Structural Recipe** — Distill the ad to a reusable formula stripped of brand specifics. Example: "Value Triptych + Product Abundance — three icon badges across top, product hero on dark background, warm wood surface."

### Step 2B: Brand Context Extraction

Read the brand research document. Extract and summarize:
- Brand colors (hex codes if available)
- Brand voice & tone
- Target demographic
- Product positioning and key value props
- Emotional drivers
- Key proof points (reviews, awards, social proof, statistics)

### Step 2C: Product Spec Sheet (CRITICAL)

This is the most important output. Create a detailed visual description of the product that gets copy-pasted verbatim into every image generation prompt. This prevents the "wrong product" problem.

Using the product page screenshots and/or product images, write:

```
PRODUCT SPEC SHEET
==================
Product Name: [exact name]
Price: [price]
Shape (GEOMETRIC — use the Shape Protocol below): [geometric classification + silhouette trace + key ratios]
Physical Description: [dimensions relative to hands/table, materials, texture]
Color(s): [exact colors with descriptive names]
Key Visual Features: [what makes this product visually distinct]
Scale Reference: [size relative to common objects]
Accessories/Components: [what should appear — lids, sleeves, packaging, etc.]
What It Must NOT Look Like: [common misrenderings to avoid — MUST include wrong shape geometries]
```

#### Shape Protocol for Product Spec Sheets

Vague shape words like "rounder," "egg-shaped," or "more compact" cause NanoBanana to hallucinate the wrong product silhouette. Use this structured method:

1. **Silhouette trace (top to bottom):** Describe the outline as a path. Example: "Rim is the widest point (~3.5in), walls angle inward in a straight taper to a flat base (~2in wide)."
2. **Geometric classification** — use one of these terms:
   - **Cylindrical** — straight vertical walls, rim and base roughly equal width
   - **Tapered / conical** — wider at top, narrower at base, walls are straight but angled
   - **Tulip** — slight outward flare at the rim, then narrows toward base
   - **Barrel / convex** — walls bow outward, widest in the middle
   - **Bell** — narrow at top, flares wider toward the base
   - **Hourglass** — pinches in the middle, wider at top and bottom
3. **Key ratios:** Rim-to-base width ratio, height-to-width ratio, wall angle
4. **"What It Must NOT Look Like"** MUST include the wrong geometric shapes. Example: "NOT barrel-shaped, NOT egg-shaped, NOT cylindrical — the product is a truncated cone."

NEVER use "egg-shaped," "rounder," "more compact," or other subjective terms. Always lead with the geometric classification.

## Phase 3: Concept Generation + Prompt Writing

Generate **3 ad concept variations** using the structural recipe from Phase 2, adapted through different creative lenses.

### Concept Strategy

**Variation 1: Faithful Adaptation** — Closest to the original. Same composition and psychological angle, swapped to user's brand colors, copy voice, and product. The safe bet.

**Variation 2: Angle Shift** — Same layout structure, different psychological angle. If the original was identity/status, this version pivots to benefit-driven or transformation while keeping the visual bones.

**Variation 3: Scene Shift** — Same psychological angle, reimagined setting. If the original was a studio product shot, this puts the product in a lifestyle context (or vice versa). This is usually the most distinctive/scroll-stopping variant.

### For Each Concept, Produce:

**A. Ad Concept Brief** — 3-4 sentences describing the scene, copy, and intended emotion

**B. Adapted Ad Copy** — Headline/hook, subhead, CTA or badge text, rewritten in the user's brand voice

**C. NanoBanana Prompt** — Full image generation prompt following the template in `references/nanobanana-prompt-template.md`. The prompt MUST include:
1. Scene description
2. Full product spec sheet description (verbatim — never abbreviate)
3. Art style & medium
4. Lighting & atmosphere
5. Camera angle & depth of field
6. Composition & layout
7. Brand color instructions (hex codes)
8. Text overlay instructions (exact strings in quotes, font style, placement)
9. Aspect ratio (default 4:5)
10. Negative prompt / exclusions

### Prompt Rules
- NEVER use generic product descriptions — always the full spec sheet language
- ALWAYS include text strings in quotes with font/placement instructions
- ALWAYS include negative prompt elements
- Keep prompts under 500 words
- Use concrete, visual language — not "elegant" but "clean white background with soft drop shadow"
- Prefix each prompt with "Generate an image:" when submitting to Gemini so it triggers NanoBanana

### Output Documents

Save outputs to two separate top-level Desktop folders — one for analysis docs, one for generated images:

**Analysis doc** (the full teardown, brand context, product spec sheet, and all 3 concept briefs with prompts):
```
{mounted-folder}/Desktop/Ad Research/{BrandName}/Ad_Swipe_{ProductName}_{MonthYear}.md
```

**Generated images** (the 3 NanoBanana outputs, organized by brand and product):
```
{mounted-folder}/Desktop/Ad Outputs/{BrandName}/{ProductName}/
├── Concept1_Faithful_Adaptation_{ProductName}.png
├── Concept2_Angle_Shift_{ProductName}.png
└── Concept3_Scene_Shift_{ProductName}.png
```

Create both directory structures if they don't exist. The `Ad Outputs` folder sits at the top level of Desktop next to `Ad Research` so the user can easily find generated images.

## Phase 4: Image Generation via Gemini Browser Automation

This is the hands-free execution phase. Claude opens Gemini in the browser and generates all 3 images autonomously.

### Setup

1. Create the output folder: `{mounted-folder}/Desktop/Ad Outputs/{BrandName}/{ProductName}/`
2. Navigate to `https://gemini.google.com` in the browser (use existing Gemini tab if one is open, otherwise create a new tab)

### For Each Concept (repeat 3 times):

**Step 1: Enter the prompt**
- Find the contenteditable input field in Gemini
- Use JavaScript injection to insert the prompt text (Gemini's input is a contenteditable div, not a standard form input — use `document.execCommand('insertText', false, promptText)` after focusing the element)
- Prefix the prompt with "Generate an image:" to trigger NanoBanana

**Step 2: Submit**
- Find and click the "Send message" button
- If the button isn't found by accessibility query, click the send arrow icon at the bottom-right of the input area

**Step 3: Wait for generation**
- Take screenshots periodically to check progress
- Look for "Loading Nano Banana..." text which indicates generation is in progress
- Wait until the generated image appears in the chat (the loading indicator disappears and an image thumbnail appears)
- This typically takes 15-45 seconds

**Step 4: Save the image**
- Click on the generated image to open the lightbox/expanded view
- Find and click the "Save" or "Download full size image" button
- This downloads the image to the user's Downloads folder as a PNG with a name like `Gemini_Generated_Image_[hash].png`

**Step 5: Wait before next prompt**
- Ensure the previous generation is fully complete before entering the next prompt
- The input field should be empty and ready for new text

### Troubleshooting Browser Automation

**Input field not accepting text:** Gemini uses a contenteditable div, not a textarea. Standard form_input won't work. Use JavaScript: focus the element first, then `document.execCommand('insertText', false, text)`.

**Send button not found:** The send button appears only when there's text in the input field. After inserting text, search for a button with "Send message" in its accessible name, or click the arrow icon at the bottom-right of the input area.

**NanoBanana not loading:** Gemini needs to be in a mode that supports image generation ("Generate an..." mode or default mode). If NanoBanana doesn't trigger, make sure the prompt starts with "Generate an image:".

**Previous response still active:** If Gemini is still responding from a previous prompt, wait for it to finish before submitting the next one. Check for a stop button — if visible, generation is still in progress.

## Phase 5: QC + File Organization + Delivery

### Step 5A: Locate Downloaded Images

After all 3 images are generated and saved:
1. List the user's Downloads folder, sorted by modification time
2. Identify the 3 most recent `Gemini_Generated_Image_*.png` files
3. The oldest of the 3 is Concept 1, middle is Concept 2, newest is Concept 3

### Step 5B: Copy to Output Folder

Copy each image to the `Ad Outputs` folder on Desktop (organized by brand then product):
```
Desktop/Ad Outputs/{BrandName}/{ProductName}/
├── Concept1_Faithful_Adaptation_{ProductName}.png
├── Concept2_Angle_Shift_{ProductName}.png
└── Concept3_Scene_Shift_{ProductName}.png
```

### Step 5C: QC Review

Read each saved image and score it against 7 dimensions (see `references/qc-checklist.md`):

1. **Product Accuracy** — Does it match the spec sheet?
2. **Brand Palette** — Correct colors?
3. **Text Legibility** — All text readable?
4. **Text Accuracy** — Text says what was specified?
5. **Composition Fidelity** — Layout matches the structural recipe?
6. **Emotional Tone** — Conveys the intended angle?
7. **Professional Quality** — Looks like a real ad?

If any image scores below 5/7, flag it to the user with specific issues and offer to regenerate.

### Step 5D: Present Results

Show the user all 3 generated images with:
- A brief QC summary for each (passing/failing dimensions)
- Links to the files in their output folder
- The full analysis document link

## Error Handling

### No brand folder found
"I couldn't find a folder matching [brand name]. You can: (1) point me to the right path, (2) upload your brand research doc directly, or (3) tell me your brand colors, target customer, and key differentiator."

### Product page won't load
If the product URL returns a 403 or fails to load in the browser, ask the user: "The product page isn't loading. Can you tell me the product name, price, key features, and upload a product photo?"

### Gemini rate limited or unavailable
If Gemini shows an error or rate limit: "Gemini hit a rate limit. I've saved all 3 prompts in the analysis document — you can paste them into Gemini manually, or I can try again in a few minutes."

### Image generation fails
If NanoBanana fails to generate (timeout, error message), try once more. If it fails again, save the prompt and move to the next concept. Note which concepts need manual generation.

### Downloads folder not accessible
If the Downloads folder path doesn't exist or images aren't found: "I can't find the downloaded images. Can you check your Downloads folder for recent Gemini images and tell me the file names?"
