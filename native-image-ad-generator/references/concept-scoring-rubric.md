# Concept Scoring Rubric

Use this rubric to evaluate and rank ad concepts before selecting the top 5 for image generation. Each concept is scored 1-5 on five dimensions, for a maximum score of 25.

## Dimension 1: Emotional Resonance (1-5)

Does the concept tap into real emotional drivers identified in the brand research dossier?

| Score | Description |
|---|---|
| 5 | Directly addresses the #1 or #2 emotional driver from research. Uses language/imagery that mirrors real customer quotes. Would make the target persona feel genuinely understood. |
| 4 | Addresses a strong emotional driver (top 3-4). Connection to customer voice is clear but not verbatim. |
| 3 | Connects to a real emotional driver but in a generic way that could apply to many products. |
| 2 | Weak emotional connection. More feature-focused than feeling-focused. |
| 1 | No meaningful emotional resonance. Purely functional or decorative concept. |

**How to evaluate:** Go back to the research dossier's emotional drivers section and customer quotes. Does this concept make someone who said those quotes think "that's exactly how I feel"?

## Dimension 2: Scroll-Stop Power (1-5)

Would this image make someone stop scrolling in a social media feed? The average user scrolls past an ad in under 1 second — this concept needs to interrupt that.

| Score | Description |
|---|---|
| 5 | Visually arresting — high contrast, unexpected composition, or provocative imagery. Would stand out even among other ads in a busy feed. |
| 4 | Strong visual hook. Clear focal point that draws the eye. Noticeably better than average feed content. |
| 3 | Competent product photography but nothing unexpected. Would blend into a feed of similar brand content. |
| 2 | Generic-looking. Could be any brand's ad. Low visual distinctiveness. |
| 1 | Would be scrolled past without a second glance. No visual hook whatsoever. |

**How to evaluate:** Imagine this image appearing between a friend's vacation photo and a food reel. Does it earn a pause?

## Dimension 3: Brand Alignment (1-5)

Does the visual style, tone, and message feel authentically on-brand?

| Score | Description |
|---|---|
| 5 | Could be posted on the brand's website or Instagram tomorrow without any adjustment. Perfect match for brand colors, voice, aesthetic, and values. |
| 4 | Strong brand fit. Minor adjustments might be needed but the direction is clearly on-brand. |
| 3 | Generally in the brand territory but some elements feel off — wrong tone, slightly mismatched aesthetic. |
| 2 | Noticeable disconnect. The concept might work for the product category but doesn't feel like THIS brand. |
| 1 | Completely off-brand. Wrong tone, wrong aesthetic, wrong audience signal. |

**How to evaluate:** Reference the brand voice, visual identity, and target demographic sections of the research dossier. Would this feel at home alongside the brand's existing content?

## Dimension 4: Strategic Differentiation (1-5)

Does this concept say something competitors aren't saying? Does it exploit a gap identified in the research?

| Score | Description |
|---|---|
| 5 | Directly exploits a competitive gap identified in the research. No competitor is running this angle. First-mover advantage is clear. |
| 4 | Addresses a space where competitors are weak, even if not completely uncontested. The brand's unique positioning makes this concept work better for them than it would for competitors. |
| 3 | A good angle but one that competitors also use. The brand's version might be slightly better but isn't dramatically differentiated. |
| 2 | A common angle in the category that doesn't leverage the brand's unique positioning. Could be any competitor's ad. |
| 1 | Directly copies a competitor's approach without any meaningful differentiation. |

**How to evaluate:** Check the competitive landscape section of the research dossier. What are competitors saying? What are they NOT saying? Does this concept fill a gap?

## Dimension 5: Prompt Feasibility (1-5)

Can Gemini's image generation (via NanoBanana prompts) realistically produce this concept at a quality level that's usable for advertising?

| Score | Description |
|---|---|
| 5 | Simple, well-defined composition that AI excels at: product photography, lifestyle scenes, mood/atmosphere. Minimal or no text. High confidence in output quality. |
| 4 | Achievable with careful prompting. May include 1-2 short text elements or a moderately complex scene. Good odds of usable output. |
| 3 | Possible but may require 2-3 generation attempts. Includes elements that AI sometimes struggles with (hands, specific text, complex multi-element compositions). |
| 2 | Challenging for current AI image generation. Requires perfect text rendering, specific facial expressions, or highly detailed multi-product arrangements. May need significant post-editing. |
| 1 | Very unlikely to generate well. Requires elements AI consistently fails at: long text passages, specific logos, photorealistic hands in specific poses, or celebrity likenesses. |

**How to evaluate:** Consider known AI image generation strengths and weaknesses:
- **Strengths:** Product photography, atmospheric scenes, nature, food/beverage, abstract art, mood lighting
- **Weaknesses:** Perfect text rendering, specific hand poses, multiple distinct products in precise arrangements, brand logos, faces with specific expressions

## Selection Rules

After scoring all concepts:

1. Rank by total score (highest first)
2. **Diversity check:** The top 5 must include at least 3 different ad types. If duplicates cluster at the top, swap the lowest-scoring duplicate for the next highest-scoring concept from an unrepresented type.
3. **Funnel coverage check:** Ideally, the top 5 should include at least one concept for each stage: awareness (lifestyle/aspirational/brand identity), consideration (comparison/features/testimonial), and conversion (offer/benefit statement/social proof).
4. If two concepts score identically, prefer the one with higher Scroll-Stop Power — in a crowded feed, the ability to interrupt scrolling is the most valuable trait.

## Example Scoring

**High-scoring concept (Score: 23/25):**
- "Nightmare Scenario — Metallic Taste Horror" for a ceramic travel cup
- Emotional Resonance: 5 (metallic taste is the #1 customer pain point)
- Scroll-Stop Power: 5 (visceral, unexpected imagery)
- Brand Alignment: 4 (slightly edgier than brand's usual warm tone, but effective)
- Strategic Differentiation: 5 (no ceramic competitors run nightmare-style ads)
- Prompt Feasibility: 4 (split-screen concept with moody lighting — achievable)

**Low-scoring concept (Score: 12/25):**
- "Generic Product Shot with Features List" for the same cup
- Emotional Resonance: 2 (feature-focused, not feeling-focused)
- Scroll-Stop Power: 2 (looks like every other product listing)
- Brand Alignment: 3 (on-brand colors but bland)
- Strategic Differentiation: 1 (every competitor has feature-list ads)
- Prompt Feasibility: 4 (simple product photography — easy to generate)
