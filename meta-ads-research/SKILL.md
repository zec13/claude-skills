---
name: meta-ads-research
description: |
  Deep competitor research using Meta Ad Library. Use when analyzing competitor Facebook/Instagram ads, extracting ad angles and hooks, identifying winning ad patterns, or building creative strategy from competitor intelligence.

  TRIGGERS: Meta Ad Library, Facebook ads research, Instagram ads competitor analysis, ad library analysis, competitor ad research, creative strategy research, ad angle extraction, winning ad patterns

  This skill uses browser automation to navigate Meta Ad Library URLs, screenshot ads, extract copy/creative details, and generate structured analysis reports with actionable insights mapped to the user's brand context.
---

# Meta Ads Library Research

Deep competitor ad research using Meta Ad Library with browser automation.

## Quick Start

1. Get a Meta Ad Library URL for the competitor (e.g., `facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=BrandName`)
2. Run this skill — navigate, screenshot ads, extract data
3. Receive two deliverables saved to `ad-research/[BrandName]/`:
   - **Research Report** — full analysis with angle extraction and strategic recommendations
   - **Creative Brief** — actionable ad concepts ready for production

## Core Workflow

### Phase 1: Setup & Navigation

1. Navigate to provided Meta Ad Library URL
2. Set filters: Country=US, Category=All Ads, Status=Active
3. Take initial screenshot to capture ad count and overview

### Phase 2: Ad Capture (aim for 5-10 key ads)

For each relevant ad:
1. Screenshot the creative (video thumbnail or static image)
2. Extract: headline, primary text, CTA, start date, placement info
3. Note format (video/static/carousel) and any "low count" labels
4. Skip ads with "low count" label unless noting new angles

**Prioritize**: Long-running ads, ads with multiple variants, ads appearing across formats

### Phase 3: Analysis

Apply methodology from [references/methodology.md](references/methodology.md):

**Winning Ad Signals:**
- Longevity (weeks/months = likely winner)
- Creative families (multiple variants = A/B testing)
- Offer persistence (same discount repeated = works)
- Cross-format presence (Feed + Stories + Reels = scaling)

**For each captured ad, extract:**
- **Angle**: Core persuasion hypothesis
- **Hook**: First 1-3 seconds / opening line
- **Promise**: What the customer gets
- **Pain**: Problem being addressed
- **Proof**: Evidence shown (demo, testimonial, stat)
- **Offer**: Discount/bundle/CTA
- **Objection addressed**: What concern it handles

See [references/analysis-framework.md](references/analysis-framework.md) for detailed extraction framework.

### Phase 4: Brand Mapping

Map findings to user's brand context. For Table Clay, use taxonomy from [references/table-clay-context.md](references/table-clay-context.md):

- Match competitor angles to brand's angle enums
- Identify gaps in current angle coverage
- Flag objections competitors address that brand doesn't
- Note proof types to consider testing

### Phase 5: Output Files & Folder Organization

All outputs go into a structured folder inside the user's workspace. This keeps research organized by competitor and easy to find later — especially when running multiple competitor analyses over time.

**Folder structure:**
```
ad-research/
└── [BrandName]/
    ├── [BrandName]_Ad_Research_Report.md    ← Full analysis report
    └── [BrandName]_Creative_Brief.md        ← Actionable creative brief
```

- Use the workspace/outputs folder as the root (e.g., `/sessions/.../mnt/outputs/ad-research/`)
- Create the `ad-research/` directory if it doesn't exist yet
- Create a subfolder named after the competitor brand (sanitized for filesystem — spaces become underscores, e.g., `Nova_Ceramics/`)
- Save both deliverables inside that subfolder
- When sharing links at the end, link to both files individually using `computer://` paths

**Deliverable 1: Research Report** — Generate using [assets/report-template.md](assets/report-template.md):

1. **Competitor Overview**: Brand, ad count, date range analyzed
2. **Winning Ad Signals Summary**: What patterns indicate success
3. **Top Ads Deep-Dive**: 3-5 ads with full angle extraction
4. **Strategic Recommendations**: Mapped to brand's taxonomy
5. **Content Production Ideas**: Specific angles/hooks to test

**Deliverable 2: Creative Brief** — Generate using [assets/creative-brief-template.md](assets/creative-brief-template.md):

A separate, action-ready document that distills the research into concrete ad concepts Table Clay can produce immediately. This is the "so what do we actually make?" companion to the research report. Include:

1. **3-5 Ad Concepts** — each with a specific hook/opening line, body copy direction, format recommendation (video/static/carousel), and what proof elements are needed to produce it
2. **Angle-to-concept mapping** — which competitor insight or gap inspired each concept, so the reasoning is traceable
3. **Production checklist** — for each concept, what assets/footage/props are needed and estimated complexity (quick win vs. full shoot)
4. **Priority ranking** — rank concepts by opportunity size, with biggest uncontested gaps first

## Browser Automation Notes

- Always screenshot ads immediately (URLs expire when ads stop)
- Use `scroll` to load more ads in the Library feed
- Filter by Platform (Instagram) or Media (Video) if researching specific formats
- Check for "Paid partnership" labels indicating influencer/UGC content

## Brand Context

Default brand context: **Table Clay** (ceramics/pottery ecommerce)

To analyze for a different brand:
1. Provide brand context document with: product lines, target personas, current angles, known objections
2. I'll map competitor findings to your specific taxonomy

## Reference Files

- [methodology.md](references/methodology.md) - Full playbook: winning signals, workflow SOP, common pitfalls
- [analysis-framework.md](references/analysis-framework.md) - Promise/Pain/Proof/Hook/Offer/Objection extraction
- [table-clay-context.md](references/table-clay-context.md) - Table Clay brand taxonomy (default context)
- [report-template.md](assets/report-template.md) - Research report output template
- [creative-brief-template.md](assets/creative-brief-template.md) - Creative brief output template
