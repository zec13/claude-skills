---
name: qc-cookbook
description: "Paste-ready reference for quality checks, math formulas, and sanity checks used in CPG consulting. Covers index calculations, Top-2-Box/Bottom-2-Box, combined bases, household penetration, share calculations, growth/CAGR, RYG threshold system, z-score normalization, PowerPoint data labels, survey fielding math, rounding rules, base size rules, and a full QC checklist. Use this skill whenever the user needs consulting quant QC, Excel formula help for indices or shares, data table validation, RYG color coding, base size rules, or is running a final QC pass before a client deliverable. Triggers include: QC cookbook, index formula, T2B, B2B, top 2 box, base size, RYG, sanity check, quant QC, Excel formula, data check, share calculation, CAGR, rounding rules, combined bases."
---

# Consulting QC Cookbook

A paste-ready reference for the quality checks, math, formulas, and sanity checks used daily at Seurat Group. Every formula is Excel-native.

## 1. Index Calculations

Index = (Segment Value / Benchmark Value) x 100

Excel: `=ROUND((B2/C2)*100, 0)`

Always state the benchmark. ">100 = over-indexes, =100 = parity, <100 = under-indexes"

## 2. Top-2-Box / Bottom-2-Box

- T2B: Sum of top two response options
- B2B: Sum of bottom two response options
- T2B Index = (Segment T2B % / Total T2B %) x 100

**Critical Rule**: Weight by Counts, Not Averages. Never average index numbers directly — go back to counts.

## 3. Combined Bases

1. Combined count = n(seg1) + n(seg2)
2. Combined % = Combined count / Combined total base
3. Index vs. Total = (Combined % / Total %) x 100

## 4. Household Penetration

HH Penetration % = (HH in custom group / Total HH universe) x 100

Same universe, same filters, weighted vs. unweighted clarity.

## 5. Share Calculations

- Share % = Part / Whole x 100
- Share Change: Always use "pp" (percentage points), not "%"
- QC: Shares must sum to 98-102%

## 6. Growth & CAGR

- YoY % = (Current - Prior) / Prior x 100
- CAGR = (End / Start)^(1/n) - 1
- Always state the time period

## 7. RYG Threshold System

**Option A — Balanced (default)**: Red < 105, Yellow 105-114, Green >= 115

**Option B — Stricter**: Red < 110, Yellow 110-119, Green >= 120

Green should capture ~20-30% of cells.

Excel: `=IF(B2>=115,"G",IF(B2>=105,"Y","R"))`

## 8. Z-Score Normalization (0-100)

Use when comparing metrics on different scales.

Excel: `=ROUND(NORM.S.DIST((B2-AVERAGE($B$2:$B$15))/STDEV.S($B$2:$B$15),TRUE)*100,0)`

~50 = average, ~84 = top 15%, ~16 = bottom 15%

## 9. Data Labels for PowerPoint Charts

Format: `(Incidence%, Index#)` — e.g., `(32%, 115)`

Excel: `=CONCATENATE("(", TEXT(B2,"0%"), ", ", TEXT(C2,"0"), ")")`

## 10. Survey Quota & Fielding Math

Invites Needed = Target Completes / (Incidence Rate x Completion Rate)

Over-recruit by 10-15%. Check at soft launch for quota proportions, completion time, bot detection.

## 11. Rounding Rules

| What | Precision | Example |
|------|-----------|---------|
| Percentages | 1 decimal | 23.4% |
| Indices | Whole number | 115 |
| Share changes | 1 decimal + "pp" | +2.3pp |
| CAGR | 1 decimal | 4.2% |
| Dollar values | Match source | $1.2B |
| Base sizes | Whole number | n=312 |

## 12. Base Size Rules

| Base Size | Rule |
|-----------|------|
| n >= 100 | Report normally |
| n = 30-99 | Caution footnote: "small base, interpret directionally" |
| n < 30 | Do NOT report percentages. Use counts only or suppress |

## 13. QC Checklist (Run Every Time)

**Numbers**: Shares sum? Indices vs correct benchmark? Growth rates consistent? Base sizes >= 30? Units consistent?

**Labels**: Base definition stated? Data labels in right format? Footnotes for small bases?

**Formulas**: Spot-check 2-3 cells. Combined bases using counts? Denominator correct?

**Deliverable**: RYG matches convention? External data cited? Would a partner understand?

**Copy**: Spelling pass? Double spaces removed? Brand names correct? Bullets parallel? Source lines correct?

## 14. Common Pitfalls

1. **Averaging Indices** — Go back to counts, never average
2. **Wrong Denominator** — Always verify what "total" means
3. **% Change vs. pp Change** — 3pp != 3% growth
4. **Tiny Bases** — n=15 doesn't support reliable percentages
5. **False Precision** — Don't add decimals that aren't in the data
6. **Over-Indexing != Large** — Index 150 on base of 2% = still tiny (3%)
7. **RYG on Wrong Scale** — Don't apply index thresholds to percentage columns
