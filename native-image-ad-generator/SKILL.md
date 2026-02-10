---
name: native-image-ad-generator
description: |
  End-to-end native image ad creator. Takes a brand name and product, finds the research dossier in Desktop/Brands/, generates 10-20 emotionally resonant static image ad concepts with NanoBanana text-to-image prompts, auto-selects the top 5 based on brand strategy fit, then uses Claude in Chrome to generate 5 final images in Google Gemini (one per concept, 4:5 ratio) and saves all outputs to Desktop/Ad Outputs/[Brand]/[Product]/. Runs fully autonomously — no user approval needed mid-workflow.

  TRIGGERS: native image ads, static image ads, ad concepts, NanoBanana, image ad generator, generate ads, create ad images, ad variations, text to image ads, run ad generator, image ads for [brand], generate image ads

  Do NOT use for: Meta Ad Library research (use meta-ads-research), ad copy/scripts without images (use tableclay-prompts 1A), competitor ad analysis (use meta-ads-research), video ad production, email marketing.
---

# Native Image Ad Generator

Fully autonomous workflow: brand + product in, finished ad images out. Reads the research dossier, generates concepts, scores and selects the top 5, generates one image per concept via Gemini (4:5 ratio), and saves everything to the desktop. No mid-workflow approval gates — runs silently from input to output.

## Quick Reference

| Step | What Happens | User Interaction |
|---|---|---|
| 1. Input | Receive brand name + product name | User provides these |
| 2. Find research | Locate dossier in `Desktop/Brands/[BrandName]/` | None (auto) |
| 3. Analyze | Deep-read dossier for strategy inputs | None (auto) |
| 4. Generate concepts | Create 10-20 concepts with NanoBanana prompts | None (auto) |
| 5. Auto-select top 5 | Score, rank, and select — no approval gate | None (auto) |
| 6. Generate images | Gemini via browser — 1 image per concept (4:5), save all options | None (auto) |
| 7. Save & deliver | Save to `Desktop/Ad Outputs/[Brand]/[Product]/` with summary | Link to folder |

## Autonomy Rules

This skill runs **fully autonomously** once the user provides a brand and product. Do not stop for approval, confirmation, or review at any step. Do not show scoring tables, concept lists, or progress updates to the user. Work silently through all steps and deliver the final output folder with a brief completion message.

The only exceptions where you should stop and ask:
- The research dossier cannot be found (ask which file to use)
- The brand has multiple products and the user didn't specify which one
- Gemini is not logged in (ask user to log in manually)

## Detailed Workflow

### Step 1: Receive Input

The user provides:
- **Brand name** (e.g., "Table Clay", "Aniwove", "Vertifarm")
- **Product name** (e.g., "Ceramic Travel Cup", "Custom Pet Mug")

If the user only provides a brand name, check `Desktop/Brands/[BrandName]/` for available dossiers. If there's exactly one, use it. If multiple exist, ask which product.

### Step 2: Find the Research Dossier

Research dossiers live in `Desktop/Brands/` on the user's computer:

```
Desktop/Brands/
├── [BrandName]/
│   ├── [Product Name] — Deep Research Dossier.docx
│   └── ...
```

**Locating the file:**
1. List `Desktop/Brands/[BrandName]/` (try casing variations: exact, title case, lowercase)
2. Match `.docx` files containing "Deep Research Dossier" to the user's product name (fuzzy match — "Travel Cup" matches "Ceramic Travel Cup — Deep Research Dossier.docx")
3. If no match or ambiguous, show available files and ask

### Step 3: Analyze the Research Dossier

Read the full dossier using python-docx extraction. Internalize these elements silently (do not output them):

1. **Product spec sheet** — physical description, dimensions, colors, materials, textures, what it must NOT look like
2. **Emotional drivers** — ranked purchase motivations from the research
3. **Customer voice** — verbatim quotes revealing how customers talk about the product
4. **Objections** — barriers to purchase and rebuttal strategies
5. **Competitive landscape** — gaps and differentiation opportunities
6. **Target personas** — psychographics, jobs-to-be-done
7. **Brand voice & visual identity** — colors (hex codes), tone, photography style
8. **Messaging frameworks** — positioning angles, belief chains, proof points
9. **Pricing context** — competitive positioning, anchoring strategy

Compile a product spec sheet internally using the template in `assets/product-spec-template.md`. This spec sheet is used word-for-word in every NanoBanana prompt to ensure product accuracy.

### Step 4: Generate 10-20 Ad Concepts with NanoBanana Prompts

Generate between 10 and 20 unique static image ad concepts. Each concept gets a **complete NanoBanana prompt** including the `--ar 4:5` aspect ratio suffix (the standard Meta/Instagram feed format).

**Concept Categories** (pick the strongest for this product — aim for variety):

Before & After, Nightmare Scenario, Comparison / Us vs. Them, Big Benefit Statement, Offer Heavy, Media / Press / Authority, Reasons Why, Features & Benefits, Testimonial / Review, Humor / Fun, Lifestyle / Aspirational, UGC-Style, Pain Agitation, Seasonal / Contextual, Value Triptych, Unboxing / First Impression, Gift Angle

**For Each Concept:**

1. **Concept Name** — short, descriptive
2. **Ad Type** — category from above
3. **Strategic Rationale** — 1-2 sentences grounded in research insights
4. **Ad Copy Elements** — text overlays (headlines, subheads, badges)
5. **NanoBanana Prompt** — complete prompt WITH `--ar 4:5` appended at the end

**NanoBanana Prompt Rules:**

Read `references/nanobanana-prompt-guide.md` for the full guide. Key principles:
- Natural English paragraphs (not bullet points)
- Start with scene/setting, then product description using exact spec sheet language
- Include lighting, camera angle, depth of field, color palette with hex codes
- Include text overlays with exact copy, font style, size, placement, and color
- End with negative prompts (what to exclude), then `--ar 4:5`
- Be extremely specific about product appearance to prevent AI hallucinations

### Step 5: Auto-Select Top 5

Score all concepts and select the top 5 automatically. Do not show scores or ask for approval.

**Scoring Criteria (1-5 each, max 25):**

1. **Emotional Resonance** — taps into core emotional drivers from research
2. **Scroll-Stop Power** — visually arresting enough to interrupt scrolling
3. **Brand Alignment** — matches brand identity, voice, and visual style
4. **Strategic Differentiation** — exploits competitive gaps
5. **Prompt Feasibility** — Gemini can realistically generate this well

See `references/concept-scoring-rubric.md` for the detailed rubric.

**Auto-Selection Rules:**
1. Score all concepts
2. Rank by total score
3. Select top 5
4. **Diversity enforcement:** top 5 must include at least 3 different ad types. If duplicates cluster, swap the lowest-scoring duplicate for the next-highest concept from an unrepresented type
5. **Funnel coverage:** ensure at least one concept each for awareness, consideration, and conversion
6. Proceed immediately to image generation — no user checkpoint

### Step 6: Generate Images in Gemini (1 Per Concept)

Use Claude in Chrome browser automation to generate images in Google Gemini. Generate **1 image per concept** in 4:5 ratio (the standard Meta/Instagram feed format). That's 5 total Gemini generations — **no more**.

> **CRITICAL — Zero-Waste Rule:** Every Gemini image generation costs the user quota. You get exactly 5 generations for 5 concepts. Do NOT generate test images, do NOT retry prompts unless Gemini explicitly refuses, do NOT send a prompt until you have verified the input method works on an empty chat. Wasted generations are unacceptable.

#### 6A. Pre-Flight Check (Run Once Before Any Concept)

Before generating any concepts, verify the browser automation pipeline works. This uses ZERO Gemini generations.

1. **Open Gemini:** Navigate to `https://gemini.google.com/app`
2. **Verify login:** Take a screenshot. If you see a login page, STOP and ask the user to log in.
3. **Verify the input field exists:** Run this JavaScript — it must return `true`:
   ```javascript
   const editor = document.querySelector('.ql-editor.textarea');
   editor !== null && editor.getAttribute('contenteditable') === 'true';
   ```
4. **Verify you can insert text:** Run this JavaScript (inserts then clears test text — does NOT submit):
   ```javascript
   const editor = document.querySelector('.ql-editor.textarea');
   editor.focus();
   document.execCommand('selectAll');
   document.execCommand('delete');
   document.execCommand('insertText', false, 'PRE-FLIGHT TEST');
   const worked = editor.innerText.includes('PRE-FLIGHT TEST');
   document.execCommand('selectAll');
   document.execCommand('delete');
   worked; // must return true
   ```
5. **Verify the send button exists:**
   ```javascript
   document.querySelector('button[aria-label="Send message"]') !== null;
   ```

If any check fails, try refreshing the page and re-running. If it still fails, output all 5 prompts in `REMAINING_PROMPTS.md` for the user to paste manually. Do NOT burn generations troubleshooting.

#### 6B. Gemini Browser Automation Playbook

These are the exact, tested methods for interacting with Gemini. **Use these verbatim — do NOT experiment with alternatives.**

**Tool Usage:**
- All JavaScript must be executed via the `javascript_tool` with `action: "javascript_exec"` (not "execute" or any other value)
- All click actions must use `left_click` (not "click")

**The Input Field:**
- Gemini uses a Quill.js rich text editor, NOT a standard `<input>` or `<textarea>`
- The element is a `<div>` with classes `ql-editor textarea` and attribute `contenteditable="true"`
- Standard `form_input` tool WILL NOT WORK on this element — always use JavaScript
- The `innerHTML` property is blocked by TrustedHTML CSP — never try to set it directly

**How to Insert a Prompt (JavaScript):**
```javascript
const editor = document.querySelector('.ql-editor.textarea');
editor.focus();
document.execCommand('selectAll');
document.execCommand('delete');
document.execCommand('insertText', false, '<YOUR PROMPT TEXT HERE>');
```
- Always clear first (`selectAll` + `delete`) then insert
- The prompt text should be a single string — escape any special characters
- Always prefix the prompt with "Generate an image: " before the NanoBanana prompt body

**How to Submit (JavaScript):**
```javascript
document.querySelector('button[aria-label="Send message"]').click();
```

**How to Wait for Generation:**
- After clicking send, wait **50 seconds** (`sleep 50`) before checking
- Then take a screenshot and scroll down to see if the image appeared
- If still loading (blue sparkle icon visible), wait another 20 seconds
- Maximum total wait: 90 seconds. If no image after 90s, treat as failed.

**How to Download the Generated Image:**
- **DO NOT** click the "Save" button in the lightbox — it saves to Google Photos, NOT to local Downloads
- **DO NOT** try JavaScript `fetch()` or `blob` downloads — they are blocked by CORS
- **DO** use the hover overlay method:
  1. Scroll down until the generated image is visible in the chat
  2. Hover over the image (use the `hover` action at the center of the image)
  3. Three overlay icons appear in the top-right of the image: Share, Copy, Download (left to right)
  4. Click the rightmost icon (Download) — it's approximately at the image's top-right corner area
  5. The file saves to `~/Downloads/` as `Gemini_Generated_Image_[hash].png`
  6. Wait 5 seconds, then verify the download by checking for the newest file in Downloads

**How to Start a New Chat:**
- Click the pencil/edit icon in the top-right area of the Gemini header (near the profile icon)
- OR navigate directly to `https://gemini.google.com/app`
- Wait 3 seconds for the new chat to load
- Verify you see "Ask Gemini" placeholder text in the input field before proceeding

#### 6C. Per-Concept Generation Loop

For each of the 5 selected concepts, execute this exact sequence:

```
1. START NEW CHAT
   → Click new chat icon OR navigate to gemini.google.com/app
   → Wait 3 seconds
   → Verify fresh chat (no conversation history visible)

2. INSERT PROMPT
   → Use JavaScript insertText method (see 6B above)
   → Verify prompt appears in editor (take screenshot if uncertain)

3. SUBMIT
   → Click send button via JavaScript
   → Start 50-second wait timer

4. CHECK RESULT
   → After 50s: scroll down + screenshot
   → If loading: wait 20 more seconds, check again
   → If image visible: proceed to download
   → If error/refusal: note in summary, promote next concept, start new chat

5. DOWNLOAD IMAGE
   → Hover over image in chat to reveal overlay icons
   → Click the download icon (rightmost)
   → Wait 5 seconds
   → Verify file exists in ~/Downloads/ (check newest Gemini_Generated_Image_*.png)

6. COPY TO OUTPUT FOLDER
   → Copy from ~/Downloads/ to Desktop/Ad Outputs/[Brand]/[Product]/4x5/Concept[N]_[ShortName].png

7. REPEAT from step 1 for next concept
```

**Strict Rules:**
- **ONE generation per concept** — no retries unless Gemini explicitly refuses (shows an error message, not just a slow response)
- **Always new chat** between concepts — never reuse a conversation
- **Never submit a prompt as a "test"** — every submission generates an image and costs quota
- If the download fails, try the hover-download method once more. If it fails again, note the Gemini conversation URL so the user can download manually later.

#### 6D. Failure Handling

| Situation | Action |
|---|---|
| Gemini shows safety refusal | Note in summary, promote 6th concept, move on |
| Image not generated after 90s | Note as timeout, promote next concept |
| Download button not appearing | Try scrolling to image and hovering again. If fails, note Gemini URL for manual download |
| Browser connection drops | Save all completed images + remaining prompts in `REMAINING_PROMPTS.md` |
| More than 3 concepts fail | Save successful outputs + create `FAILED_PROMPTS.md` with all failed prompts |
| Input field not found after refresh | Output all prompts in `REMAINING_PROMPTS.md` — do not keep retrying |

**What NEVER to do:**
- Never generate an image just to "test" if the pipeline works
- Never retry a prompt that already produced an image (even if you had trouble downloading it)
- Never send the same prompt to multiple Gemini conversations
- Never use `form_input` tool on Gemini — it will fail on the contenteditable div
- Never set `innerHTML` on the editor — blocked by TrustedHTML CSP
- Never use JavaScript fetch/blob to download — blocked by CORS

### Step 7: Save Outputs & Deliver

Save everything to the user's desktop in this structure:

```
Desktop/Ad Outputs/
└── [Brand Name]/
    └── [Product Name]/
        ├── Concept1_[ShortName].png
        ├── Concept2_[ShortName].png
        ├── Concept3_[ShortName].png
        ├── Concept4_[ShortName].png
        ├── Concept5_[ShortName].png
        └── Ad_Concepts_Summary.md
```

**Folder structure rules:**
- Create `Desktop/Ad Outputs/` if it doesn't exist
- Brand folder uses the brand's display name (spaces OK)
- Product folder uses the product's display name (spaces OK)
- Image files: `Concept[N]_[ShortName].png` — sanitize concept name (underscores, no special chars)
- All images are 4:5 ratio (Meta/Instagram feed format)

**Summary file (`Ad_Concepts_Summary.md`):**

Create this file documenting everything about the generation run:

```markdown
# [Brand] — [Product] Ad Concepts
Generated: [Date]

## Generation Summary
- Concepts generated: [N]
- Top 5 selected by score
- Format: 4:5 (Meta/Instagram feed)
- Total images: 5

## Selected Concepts

### Concept 1: [Name]
- **Type:** [Ad Type]
- **Score:** [N]/25 (Emotional: X, Scroll-Stop: X, Brand: X, Differentiation: X, Feasibility: X)
- **Strategic Rationale:** [Why this concept works]
- **Ad Copy:** [Text that appears on image]
- **File:** [filename]
- **NanoBanana Prompt:**
[full prompt]

### Concept 2: [Name]
... [repeat for all 5]

## Failed Generations (if any)
[Note any prompts Gemini refused and why]

## Research Dossier Used
[Filename and path of the dossier]
```

**Final delivery message:**

After saving everything, provide a single completion message with a link to the output folder. Keep it brief:

"Done — 5 ad concepts generated in 4:5 format. [View your ad images](computer:///path/to/Ad Outputs/Brand/Product/)"

## Error Handling

### Research dossier not found
List contents of `Desktop/Brands/` and subfolders. Ask user to confirm brand/product name.

### Gemini not logged in
Stop and ask user to log into Google in Chrome. Resume once confirmed.

### Gemini refuses a concept
Note it, move to next. If a concept fails, promote 6th-ranked. If 3+ concepts fail, output `FAILED_PROMPTS.md`.

### Browser automation failure
If Chrome connection drops, save all completed images and output remaining prompts as `REMAINING_PROMPTS.md` so the user can paste them manually.

### python-docx extraction failure
If the .docx can't be read, try markitdown as a fallback: `python -m markitdown [file.docx]`

## Scope

**Handles:** Static image ad concepts from brand research, NanoBanana prompt engineering, automated Gemini generation, strategic scoring and selection.

**Does NOT handle:** Creating research dossiers (use product-research skill), video ads, ad copy without images, Meta Ad Library research (use meta-ads-research), campaign management, email marketing.

## Reference Files

- [nanobanana-prompt-guide.md](references/nanobanana-prompt-guide.md) — Prompt engineering guide for high-quality Gemini image generation
- [concept-scoring-rubric.md](references/concept-scoring-rubric.md) — Scoring criteria with examples for concept selection
- [product-spec-template.md](assets/product-spec-template.md) — Template for extracting accurate product specifications from dossiers
