---
name: slide-qc
description: "Quality-check consulting slides for spelling, grammar, data accuracy, formatting consistency, and slide structure. Run this checklist on any slides pasted as images or text. Use this skill whenever the user asks to QC slides, check a deck, proofread slides, review for errors, or pastes slide content for quality review. Also use when preparing slides for client share-out or when the user mentions proofreading a presentation. Triggers include: QC, quality check, proofread, check slides, review deck, slide errors, check my deck, proofread this, client share-out prep, deck review."
---

# Slide QC Checklist

Run this checklist whenever asked to "QC" slides (pasted as images or text).

## 1. Spelling & Grammar
- Spell-check every word on the slide (headlines, body, callouts, source line, axis labels)
- Check subject-verb agreement ("levers work" not "levers works")
- Check singular/plural consistency ("top 3 brands" not "top 3 brand")
- Flag missing words ("on the other hand" not "on the other")
- Brand name accuracy: verify official spelling, capitalization, and spacing (e.g., "Double Stuf" not "double stuff," "MadeGood" not "Made Good")

## 2. Punctuation & Formatting
- Consistent dash style: en dash with spaces for ranges and lists
- Consistent use of "%" vs. "percent" (slides = "%")
- Periods: if one bullet has a period, all should (or none)
- Colons after lead-in phrases should be consistent

## 3. Numbers & Data
- Do percentages in a chart/pie add to 100% (within rounding)?
- Do callout stats match the chart data they reference?
- Consistent decimal precision (don't mix 46.5% and 29%)
- Currency and unit formatting per style guide

## 4. Slide Structure
- Headline states a "so what," not just a topic
- Evidence in body supports the headline claim
- Source line present and specific (file name, date, or database)
- One core message per slide

## 5. Consistency Across Deck
- Brand names spelled the same way throughout
- Segment names consistent (e.g., "Focused Foodies" not sometimes "focused foodies")
- Color coding consistent (same color = same meaning)
- Slide numbering sequential

## Output Format

Return a table per slide:

| # | Issue | Type | Text on slide | Fix |
|---|-------|------|---------------|-----|

End with a count: **"X issues total across Y slides."**
