---
name: product-research
description: "Deep product research and market intelligence dossier builder. Takes any physical or digital product — with optional photos, URLs, competitor links, and existing sales pages — and produces a comprehensive research document (.docx) covering market landscape, competitive teardown, voice-of-customer analysis, objection kill sheets, persona-specific messaging, gift/parent positioning, ad angles, and pricing strategy. Use when the user mentions \"product research\", \"research dossier\", \"market research\", \"competitor analysis\", \"VoC analysis\", \"voice of customer\", \"objection kill sheet\", \"deep research\", or wants to research a product before writing copy. Also triggers on: \"research this product\", \"analyze this market\", \"find customer pain points\", \"build a research doc\". Do NOT use for writing final sales copy, building landing pages, or creating ads — this skill produces the research foundation those outputs are built on."
---

# Product Research Dossier Builder

## Purpose

This skill produces a comprehensive product research dossier — a single .docx document that synthesizes market intelligence, competitive analysis, voice-of-customer insights, objection handling, persona-based messaging, and pricing strategy into a ready-to-use reference for copywriters, marketers, and brand builders.

The dossier answers one core question: **"What does the market want to hear, in their own words, and how should we position this product to meet those desires while neutralizing every objection?"**

This is research-first, not copy-first. The output is a strategic foundation document, not final marketing copy.

## What Makes Great Product Research

Great product research doesn't guess — it listens. The market will tell you exactly what they want to hear. The skill's job is to:

1. **Mine real customer language** from reviews, Reddit, TikTok, YouTube, forums — actual words prospects use to describe their problems, desires, and objections
2. **Map the competitive landscape** to find positioning gaps — not just who competes but where they fall short
3. **Structure objections into rebuttable arguments** — every objection is a buying signal that needs a response, not a reason to hide
4. **Build persona-specific messaging** — different buyers need different arguments, not different products
5. **Ground everything in evidence** — every claim links back to a source (review, post, article, data point)

## Workflow

### Step 1: Gather Inputs from the User

Before starting research, collect everything available. Ask the user for:

- **Product description**: What is it? What does it include? What makes it different?
- **Target audience**: Who buys this? (Even rough guesses help — "mostly women 25-45 who like crafts")
- **Product URL / sales page**: Current landing page, Amazon listing, Shopify page, etc.
- **Competitor URLs**: Direct competitors the user already knows about
- **Photos**: Product photos, packaging, unboxing, lifestyle shots
- **Price point**: Current or planned pricing
- **Existing research**: Any prior customer surveys, reviews, feedback, avatar docs, etc.

If the user provides only a product name, that's fine — search for the rest. The skill should be able to work with as little as a product name and basic description, supplementing with web research.

**Important**: Don't skip this step. Even 30 seconds of clarifying questions saves hours of misdirected research. Ask what specific questions they want answered if they have them.

### Step 2: Conduct Deep Web Research

Use web search and web fetch tools aggressively. Research should cover:

#### 2a. Market Landscape
- What product categories does this fall into? (There are usually 3-7 relevant categories)
- What alternatives exist? (Direct competitors AND indirect substitutes)
- What macro trends favor or threaten this product?
- What "jobs to be done" does this product fulfill?

#### 2b. Competitive Analysis
Research 8-12 competitors. For each, capture:
- Product name, price, bundle contents
- Positioning and core promise
- Notable strengths (what they do well)
- Gaps and weaknesses (where they fall short)
- Sources: their website, Amazon listing, social media

Search for: `[product category] site:amazon.com`, `[product type] review`, `[competitor name] review`, `best [product category] [year]`

#### 2c. Voice of Customer Mining
This is the most critical research phase. Mine customer language from:
- **Amazon reviews** (both 5-star and 1-3 star — positive reviews reveal motivations, negative reveal objections)
- **Reddit** (search `[product category] site:reddit.com` — Reddit users are brutally honest)
- **TikTok/YouTube comments** (search for product demos, unboxings, reviews)
- **Forum discussions** (niche forums related to the product category)
- **Competitor reviews** (what people love/hate about alternatives)

For each source, extract:
- **Motivations**: Why did they buy? What problem were they solving?
- **Objections**: What almost stopped them? What disappointed them?
- **Language**: The exact words and phrases they use (these become copy gold)
- **Emotional drivers**: How do they *feel* about the problem and solution?

**Pull at least 25 verbatim quotes** with source attribution. These quotes are copy-ready ammunition.

#### 2d. Objection Identification
From VoC mining, compile every objection, concern, anxiety, or friction point. Typical categories:
- Quality/durability concerns
- Price/value questions
- Ease of use worries
- Results skepticism
- Comparison to alternatives
- Logistics (shipping, returns, refills)

#### 2e. Persona Research
Based on VoC patterns, identify 3-7 distinct buyer personas. For each, research:
- Demographics and psychographics
- Primary motivation for buying
- Primary objection/anxiety
- Where they hang out online
- What content they consume
- How they talk about the problem

### Step 3: Synthesize into Dossier Structure

Once research is complete, synthesize everything into the dossier. Read `references/dossier-template.md` for the exact output structure. For strategic positioning frameworks (belief chains, unique mechanisms, awareness levels), reference `references/belief-chains-and-positioning.md`. For search query templates and source-mining tactics, reference `references/search-strategies.md`.

The dossier has 10 sections. Each section should flow from research findings to actionable recommendations:

**Section 1: Executive Summary** — High-level overview of all findings. Write this LAST, after all other sections are complete.

**Section 2: Top 25 Copy-Ready Quotes** — Verbatim customer quotes with source citations, organized by theme. These are the most powerful quotes found during VoC mining.

**Section 3: Market Landscape Overview** — Categories, alternatives, needs mapping. Shows where the product sits in the broader market and what "jobs" it competes for.

**Section 4: Competitor & Offer Teardown** — Detailed table of 8-12 competitors with positioning, pricing, strengths, and gaps. Followed by narrative analysis of competitive advantages and differentiation opportunities.

**Section 5: Voice of Customer Analysis** — Organized by motivations (why people buy) and objections (what holds them back). Includes themed verbatim quotes.

**Section 6: Objection Kill Sheet** — Every major objection (aim for 12-15) with: the objection quote, root cause analysis, rebuttal strategy, sample microcopy, and recommended placement on the sales page.

**Section 7: Gift Positioning** (if applicable) — Gift-focused angles, hooks, and PDP section recommendations. Skip this section if the product isn't commonly gifted.

**Section 8: Persona-Specific Positioning** — For each identified persona: what they care about, what messaging resonates, what objections to pre-empt. Adapt this section's framing to whatever positioning angles are most relevant (parent/kid, professional/hobbyist, gift/self-purchase, etc.)

**Section 9: Messaging Hierarchy & Ad Angles** — Above-the-fold promises by persona, supporting bullets, and 10-15 ad angle concepts with hooks, opening lines, and visual concepts.

**Section 10: Pricing & Bundling Insights** — Competitive pricing analysis, bundle tier suggestions, pricing psychology tactics, and value justification strategies.

**References** — Numbered citation list with URLs for all sources used.

### Step 4: Generate the .docx Output

The output must be a professional .docx document. Follow these rules:

1. **Use the docx skill's approach** — Generate with `docx-js` (JavaScript). Read the docx skill instructions if needed for formatting specifics.
2. **US Letter size** (12240 x 15840 DXA) with 1" margins
3. **Professional formatting**:
   - Title page with product name and "Deep Research Dossier" subtitle
   - Table of contents (optional but recommended for longer docs)
   - Clear heading hierarchy (H1 for title, H2 for major sections, H3 for subsections)
   - Tables for competitor comparisons (with proper column widths summing to content width)
   - Blockquote-style formatting for customer quotes
   - Bold for emphasis on key findings
   - Numbered references at the end
4. **Length target**: 15-30 pages depending on product complexity. More complex products with more competitors and customer data should produce longer dossiers.
5. **Save to outputs folder** and provide a computer:// link to the user

### Step 5: Quality Check

Before delivering, verify:
- [ ] Every section has specific, researched content (no generic filler)
- [ ] At least 25 real customer quotes with source attribution
- [ ] Competitor table has 8+ entries with real data
- [ ] Objection kill sheet has 12+ objections with full treatment
- [ ] Messaging section has persona-specific angles, not one-size-fits-all
- [ ] All claims link back to research sources
- [ ] Document opens cleanly in Word

## Research Quality Standards

### What "good" looks like:
- **Specific over generic**: "42% of 1-star reviews mention cracking within 2 weeks" beats "some customers report quality issues"
- **Verbatim over paraphrased**: Use actual customer words in quotes. The phrases customers use ARE the copy.
- **Sourced over assumed**: Every insight should trace back to a review, post, article, or data point
- **Actionable over academic**: Each section should end with "so what" — what does this mean for positioning, messaging, or offer structure?
- **Balanced over cherry-picked**: Include negative findings. A dossier that only shows positive signals isn't research, it's confirmation bias.

### Common mistakes to avoid:
- **Generic market overviews** that could apply to any product — be hyper-specific to THIS product
- **Unsourced claims** — if you can't point to where you found it, don't include it
- **Copying competitor marketing language** as if it were research — that's their positioning, not customer truth
- **Thin objection handling** — "just show them it's good" is not a rebuttal strategy. Every objection needs a specific, evidence-backed response
- **Ignoring negative reviews** — 1-3 star reviews are research gold. They tell you exactly what to address.

## Handling Different Input Levels

### Minimal input (just a product name):
- Search extensively to fill gaps
- Note where research was limited and flag areas for the user to supplement
- Still produce all sections, but mark confidence levels where data is thin

### Rich input (product + page + competitors + photos):
- Analyze the existing sales page for messaging gaps
- Use provided competitor list as starting point but find 3-5 more
- Reference photos in visual/ad concept recommendations
- Cross-reference existing positioning against VoC findings

### User has existing research docs:
- Read them first before doing any new research
- Build on existing findings rather than duplicating
- Flag any contradictions between existing docs and new research
- Use their established personas/frameworks as a starting scaffold

## Output Naming Convention

`[Product Name] — Deep Research Dossier.docx`

Example: `Table Clay Mini Pottery Wheel Starter Bundle — Deep Research Dossier.docx`

## When Research Is Insufficient

If web research doesn't yield enough customer language (common for very new or niche products):
1. Say so explicitly — don't fabricate quotes or insights
2. Recommend specific research actions the user can take (e.g., "Run a survey on [platform]", "Interview 5 recent customers", "Monitor [subreddit] for 2 weeks")
3. Fill what you can and mark sections that need supplementation
4. Still deliver the full dossier structure so they have a framework to fill in
