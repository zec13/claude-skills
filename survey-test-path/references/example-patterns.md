# Example Patterns for Test Path Entries

This document provides concrete examples of how to write test path entries for common question types and scenarios. These patterns are derived from actual test plan documents and represent the standard of quality expected.

## Pattern 1: Screener Demographics (Simple Selection, Avoid Termination)

### Age Question (Dropdown, Immediate Termination Risk)
```
**S2 – Age**
- Select [age value, e.g., "32"] from dropdown
- Ensure dropdown displays ages from [range per survey doc, e.g., "1-100" or "Under 13 to Over 80"]
- Ensure respondents selecting outside qualifying range [e.g., below 18 or above 70] are terminated immediately
- After selection, respondent should be assigned <age group> = [e.g., "Millennial"] based on age ranges defined in survey
```

### Income Question (Held Termination Risk, Conditional Termination)
```
**S6 – Household Income**
- Select R[x] "[income range]" (must avoid termination options)
- Ensure single-select
- Ensure response options are not randomized
- Ensure "Prefer not to answer" is anchored at bottom and mutually exclusive
- Note: Respondents selecting R1 "[lowest range]" will be terminated at end of screener
```

### Sensitive Industries (Multi-select, Immediate Termination on Specific Options)
```
**S3 – Sensitive Industries**
- Select any EXCEPT R[terminate options] (selecting [R7 Advertising, R8 Grocery Retail, R9 Marketing, R10 Beverage Manufacturer] triggers immediate termination)
- Ensure multi-select
- Ensure rows are randomized
- Ensure "None of the above" is anchored at bottom and mutually exclusive
```

## Pattern 2: Category/Brand Purchase Grids (Multi-column, Variable Assignment)

### Beverage/Category Engagement Grid
```
**S10 – Beverage Engagement**
- Select R1 "Shelf Stable Juice" in C1, C2, AND C3
- Select [additional categories as needed for path, e.g., R6 "Diet Soft Drinks" in C1 and C2]
- Ensure three-column grid: C1 "Purchased in the past year", C2 "Purchased in the past 6 months", C3 "Purchased in the past 3 months"
- Ensure must select in C1 before C2, and C2 before C3
- Ensure multi-select in all columns
- Ensure rows are randomized
- Ensure images and descriptions display for each beverage category
- Ensure "None of the above" is anchored at bottom, mutually exclusive, and triggers immediate termination
- Note: NOT selecting R1 "Shelf Stable Juice" in C3 will terminate respondent
- After selection, respondent should be assigned <Adjacent LRB> = [assigned category, if applicable]
```

### Brand Purchase Grid
```
**S14 – Brands**
- Select R1 "Ocean Spray" in C1 "Purchased in the past 3 months"
- Select R1 "Ocean Spray" in C2 "Purchased most recently"
- Ensure question reads: "Which of these brands have you purchased for [yourself / your child(ren)] in the past 3 months?"
  - Text should say "yourself" because respondent is assigned <Myself>
  - OR text should say "your child(ren)" because respondent is assigned <Purchasing for child(ren)>
- Ensure two-column grid: C1 "Purchased in the past 3 months", C2 "Purchased most recently"
- Ensure multi-select for C1, single-select for C2
- Ensure must select in C1 before selecting in C2
- Ensure rows are randomized
- Ensure "Mainstream private label" and "Premium private label" are anchored together
- Ensure "Other, please specify" is anchored at bottom with open-end field
- Ensure "I didn't notice/don't remember" is anchored at bottom and mutually exclusive
- After selection, respondent should be assigned:
  - <brand> = "Ocean Spray"
  - <brand type> = "<Ocean Spray>"
```

## Pattern 3: Conditional Question Text (If/Then Piping)

When question text changes based on variable assignments:

```
**Q301 – High-level Needs**

If path is <Myself>:
- Select any in C1 "Past 3 months", then select any of C1 selections in C2 "Most recently"
- Ensure question reads: "In the past 3 months, why have **you** consumed shelf-stable juice products?"
- Ensure you DO NOT see child-oriented wording

If path is <Purchasing for child(ren)>:
- Select any in C1 "Past 3 months", then select any of C1 selections in C2 "Most recently"
- Ensure question reads: "In the past 3 months, why have **your child(ren)** consumed shelf-stable juice products?"
- Ensure you DO NOT see self-oriented wording

Both paths:
- Ensure multi-select C1, single-select C2
- Ensure must select in C1 before C2
- Ensure rows are randomized
```

## Pattern 4: Channel/Retailer Conditional Display

When response options change based on a variable:

```
**S21 – Retailer**
- Ensure you DO see this question (respondent's <channel> is <Grocery>, <Mass>, or <Club>)
  OR
- Ensure you DO NOT see this question (respondent's <channel> is not <Grocery>, <Mass>, or <Club>)

If <channel> = <Grocery>:
- Ensure only grocery retailer options are visible (Publix, Meijer, Kroger, HEB, etc.)
- Ensure mass and club options are NOT visible
- Select R[x] "[retailer name]"

If <channel> = <Mass>:
- Ensure only mass retailer options are visible (Target, Walmart, Other mass)
- Select R[x] "[retailer name]"

If <channel> = <Club>:
- Ensure only club retailer options are visible (Costco, Sam's Club, BJ's, Other clubs)
- Select R[x] "[retailer name]"

All visible paths:
- Ensure single-select
- Ensure rows are randomized
- Ensure "Other, please specify" is anchored at bottom with open-end field
- After selection, respondent should be assigned <retailer> = "[selected retailer]"
```

## Pattern 5: Looped/Carousel Questions

When a question repeats for multiple assigned categories:

```
**S9 – Consumption Frequency**
Loops for each assigned <priority category>. This path has [N] priority categories assigned.

Loop 1: [Category Name, e.g., "gummy candy"]
- Ensure carousel shows "[category name]" bolded at top
- Select any frequency option
- Ensure single-select for this category
- Ensure frequency options are not randomized

Loop 2: [Category Name, e.g., "packaged cookies"]
- Ensure carousel shows "[category name]" bolded at top
- Select any frequency option
- Ensure single-select for this category

[Continue for each assigned priority category]

General ensures for this question:
- Ensure all assigned <priority category> values appear in the carousel
- Ensure categories are randomized in display order
- Ensure frequency options are NOT randomized
```

## Pattern 6: Brand Assignment with Priority Logic

When brands are assigned using a priority hierarchy:

```
**S10 – Brands Purchased** (for <category quota> = gummy candy)
- Ensure brand list shows ONLY gummy candy brands (not cookie brands, not cereal brands, etc.)
- Select R1 "Nerds Gummy Clusters" in C1, C2, AND C3 (this is highest priority brand for assignment)
- Also select R4 "Sour Patch" in C1 and C2 (secondary brand for potential second <brand> assignment)
- Ensure three-column grid with correct headers
- Ensure multi-select C1, C2; select up to two in C3
- Ensure must select in C1 → C2 → C3 progression
- Ensure rows are randomized
- Ensure "Mainstream Private Label" and "Premium Private Label" are kept together
- Ensure "Other; please specify" is anchored at bottom with open-end field
- After selection: <brand> should be assigned as "Nerds Gummy Clusters" (first priority) and "Sour Patch" (second priority)
```

## Pattern 7: Non-Buyer Category Questions (Special Routing)

When terminated respondents get routed to a specific question before exiting:

```
**S14 – Barriers to Purchase** (Non-buyer routing)
- Ensure you see this question if assigned <non-buyer category 1> and/or <non-buyer category 2>
- Ensure you DO NOT see this question if no non-buyer categories are assigned
- If both non-buyer categories assigned: Ensure question loops twice (once per category)
- Ensure question text pipes the correct non-buyer category name
- Loop 1: Ensure question reads "You mentioned that you have not bought [non-buyer category 1] in the past year. Why not?"
- Select any applicable barriers
- Ensure multi-select
- Ensure rows are randomized
- Ensure conditional response options appear/hide correctly:
  - "Makes my stomach hurt" should only show if non-buyer category is "gummies" or "non-chocolate non-gummy candy"
  - "Makes me jittery" should only show if non-buyer category is "gummies" or "non-chocolate non-gummy candy"
```

## Pattern 8: Scale/Attitude Questions (5-point or 10-point)

```
**Q401 – SSJ Attitudes and Behaviors**
- For each statement, select any scale value
- Ensure 5-point scale: "Strongly disagree" to "Strongly agree"
- Ensure statements are randomized
- Ensure scale values are NOT randomized
- Ensure single-select per statement
- Ensure carousel format (one statement at a time)
- Ensure all [N] statements appear in the carousel
- If any statements are conditional:
  - Ensure "[conditional statement text]" DOES / DOES NOT appear (because respondent is / is not assigned <variable>)
```

## Pattern 9: Fulfillment Method (Conditional Question Display)

```
**S22 – Fulfillment Method**
- Ensure you DO see this question (respondent is NOT assigned <online-only> for <channel>)
  OR
- Ensure you DO NOT see this question (respondent IS assigned <online-only> for <channel>)

If visible:
- Select R1 "At <retailer> store physically" in C1 and C2
- Ensure question text pipes <retailer> correctly: "At [Kroger] store physically"
- Ensure multi-select C1, single-select C2
- Ensure must select in C1 before C2
- After selection: <fulfillment method> = <in-store>
```

## Pattern 10: Backward-Tracing Piped Variables to Force Specific Selections

When a variable is NOT in the test matrix but gets piped into many downstream questions, you must trace backward to identify the required selection.

### Example: Product Variable Not in Matrix but Piped Everywhere
The test matrix specifies `<brand>=Ocean Spray` but does NOT specify `<product>`. However, downstream questions Q301-Q411 all reference "Ocean Spray cranberry" — meaning `<product>` must equal "cranberry".

**Step 1**: Identify that "cranberry" appears in downstream piping
**Step 2**: Trace `<product>` back to the question that assigns it (e.g., S17 Products)
**Step 3**: Look at S17's response table: R1=Cranberry, R2=Cranberry blends, R3=Apple...
**Step 4**: Select R1 at S17 to assign `<product>=cranberry`

```
**S17 – Products**
- Ensure "Other, please specify" is anchored at bottom
- Ensure "Ocean Spray" is piped through
- Ensure multi select for C1 and single select for C2
- Ensure R1 & R2 are together
- Ensure R3 & R4 are together
- Ensure R8 & R9 are together
- Select R1 and any others in C1
- Select R1 in C2
- Ensure assigned <product> = cranberry
```

**DON'T** write "Select any" at S17 just because `<product>` isn't in the test matrix. That makes all downstream piping unverifiable.

## Pattern 11: Conditional Response Options — Count R# from FULL Table

When a question shows different response options based on a variable, R# numbers come from the FULL table.

### Example: Retailer Question with Channel-Conditional Display
The survey document lists retailers in one table:
```
R1: Target (<Mass>)
R2: Walmart (<Mass>)
R3: Other mass (<Mass>)
R4: Publix (<Grocery>)
R5: Meijer (<Grocery>)
R6: Kroger (<Grocery>)
...
```

For a path where `<Channel>=Grocery`, only grocery options are visible. But Meijer is still R5, NOT R2.

```
**S21 – Retailer**
- Ensure "Other, please specify" is anchored at bottom
- Ensure "Ocean Spray cranberry" is piped through
- Ensure you only see response options for <Grocery>
- Select R5
- Ensure assigned <retailer>=Meijer
```

**DON'T** renumber visible options starting from R1. The R# is the position in the FULL response table.

## Anti-Patterns to Avoid

**DON'T write vague ensure checks:**
- BAD: "Ensure piping works correctly"
- GOOD: "Ensure 'Ocean Spray cranberry' is piped through"

**DON'T forget termination implications:**
- BAD: "Select any" (when R3 triggers termination)
- GOOD: "Select any EXCEPT R3 (selecting 'Less than half' triggers termination)"

**DON'T use variable names instead of actual values in pipe checks:**
- BAD: "Ensure question pipes <brand>"
- GOOD: "Ensure 'Ocean Spray cranberry' is piped through"

**DON'T skip loop iterations:**
- BAD: "Repeat for all priority categories"
- GOOD: Write out each loop iteration explicitly with the specific category

**DON'T assume R# numbering without checking:**
- BAD: Guessing R3 is the third option
- GOOD: Count from the survey document's response table to confirm R3 is actually the third listed option

**DON'T renumber R# for conditional display questions:**
- BAD: Meijer is "R2" because it's the second visible grocery option
- GOOD: Meijer is "R5" because it's the fifth option in the FULL response table

**DON'T default to "Select any" without checking downstream piping:**
- BAD: "Select any" at S17 Products (when Q301-Q411 pipe "cranberry")
- GOOD: "Select R1 in C2, Ensure assigned <product> = cranberry" (because downstream piping requires it)

**DON'T be verbose — match the terse reference style:**
- BAD: "Select R5 'Meijer' (visible since <Channel>='Grocery')"
- GOOD: "Select R5"
- BAD: "Ensure R1 'Cranberry' and R2 'Cranberry blends (e.g., Cranberry-Apple, Cranberry-Grape)' are kept together"
- GOOD: "Ensure R1 & R2 are together"

**DON'T invent question IDs:**
- BAD: Q204, Q205, Q206 (sequential across batteries)
- GOOD: Q301, Q302, Q303 (matching survey document's battery numbering)
