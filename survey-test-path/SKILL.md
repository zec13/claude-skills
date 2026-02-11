---
name: survey-test-path
description: "Generate survey test path documents from survey documents and test matrices. A test path is a detailed QA walkthrough that specifies—for each question in a survey—exactly what a tester should select, verify, and expect to see or not see. Use this skill whenever the user mentions 'test path', 'test plan', 'test matrix', 'survey QA', 'survey testing', 'test path document', 'test grid', or wants to create testing documentation for a programmed survey. Also trigger when the user uploads a survey document alongside a test matrix/grid and asks for test paths, QA documentation, or testing instructions. This skill handles complex survey logic including variable assignments, conditional branching, piping, looping, termination logic, randomization, and anchoring verification."
---

# Survey Test Path Generator

## What This Skill Does

This skill transforms a survey document and test matrix into a complete test path document—a .docx file that QA testers use to systematically verify every branch, variable, pipe, and display rule in a programmed survey. Each test path walks through the entire survey question by question, specifying exactly what to select, what to verify, and what should or shouldn't appear based on the path's variable assignments.

This is high-stakes work. Surveys are expensive to field, and errors in programming logic (wrong piping, broken skip patterns, incorrect termination) can invalidate data. The test paths must be exhaustive and precise—every response option number must be correct, every conditional display rule must be checked, and every piped variable must be verified.

## Inputs Required

1. **Survey Document** (.docx): The full survey specification containing all questions, response options, programming instructions, variable assignments, conditional logic, quotas, and piping rules.

2. **Test Matrix** (.xlsx or similar): A grid where rows are key survey variables and columns are individual test paths. Each cell specifies the value that variable should take for that path.

Before starting, read both input files completely. Read the survey document at least twice—once for overall flow, once for variable/conditional logic detail. Understanding the full survey structure before writing any test paths prevents cascading errors.

## Core Workflow

### Phase 1: Deep Survey Analysis

Before writing a single test path, build a complete mental model of the survey. Read `references/survey-analysis-guide.md` for the detailed procedure on how to extract and catalog:

1. **All variables created** — Every hidden variable, assignment, and computed value
2. **All conditional display rules** — Which questions/options appear based on which variables
3. **All termination points** — Immediate vs. held terminations, and what triggers each
4. **All piping rules** — Where variable values get inserted into question text or response options
5. **All looping/carousel logic** — Questions that repeat for multiple category or brand assignments
6. **All randomization and anchoring rules** — What gets randomized, what stays anchored, what stays grouped together
7. **Response option numbering** — Map every response option to its R# for each question

This analysis phase is the foundation. Rushing it causes errors that cascade through every test path. Take the time to build a thorough variable map before proceeding.

### Phase 2: Parse the Test Matrix

The test matrix defines which variable combinations each path should exercise. For each column (test path):

1. Identify every variable assignment specified in that column
2. Trace the implications of those assignments forward through the survey — what becomes visible, what gets piped, what gets skipped
3. Determine the specific response options (R# in C#) needed at each question to produce those variable assignments. This requires cross-referencing the survey document's response tables.
4. Identify questions where the path has no specific matrix requirement — these will typically be "Select any" unless certain options would cause termination, unwanted variable assignments, or unintended skip patterns

### Phase 3: Determine Response Selections for Non-Matrix Questions

For questions not directly driven by a matrix variable, the skill must reason about what to select:

- **Default**: "Select any" — when no selection affects the path
- **Avoid termination**: "Select any EXCEPT R[x]" — when certain options would terminate the respondent before the path is complete. Identify these by checking the survey doc's termination instructions for each question.
- **Avoid unwanted assignments**: "Select any EXCEPT R[x]" — when certain options would assign a variable that conflicts with the path's intended route
- **Avoid skipping content**: Sometimes selecting certain options causes the respondent to skip questions the tester should verify. Select options that keep the tester in the fullest version of the path.
- **Ensure downstream visibility**: If a later question requires a particular earlier response (e.g., "Only show if respondent selected R1 in S10"), make sure the earlier selection supports this

**CRITICAL — Backward-trace piping to determine required selections**: Before defaulting to "Select any" at a non-matrix question, scan ALL downstream questions for piped values that depend on this question's selection. If later questions pipe a specific value from this question (e.g., `<product>` = "cranberry" appears in Q301-Q411 as "Ocean Spray cranberry"), you MUST work backward to determine which specific R# produces that piped value, and select that R# explicitly. This is NOT optional — the test path is broken if piped values can't be verified. Common examples:
  - `<product>` is not in the matrix but is selected at a product question and piped throughout the survey
  - Demographic variables like `<low income>` require specific selections (e.g., "Select R2") even when the matrix doesn't list them, if they affect downstream logic or if the reference test plan assigns them
  - Any variable that gets piped into question text, response options, or messages must be traced back to its assignment question and a specific selection must be made there

**CRITICAL — Check the test matrix for implicit variable requirements**: Some matrix rows imply selections even at non-matrix questions. For example, if the matrix shows a specific brand consumption frequency, that implies a specific R# selection at the frequency question. Trace every matrix variable back to the question where it originates and select the exact R# needed.

### Phase 4: Write the Test Path Document

Generate a .docx file using the docx skill. Read `references/document-structure.md` for the exact formatting specification.

The document has these sections, in order:

#### Section 1: General Checks
A standardized list of formatting and behavior checks that apply across all survey testing. These are mostly consistent across projects. Read `references/general-checks-template.md` for the standard template. Customize only if the survey has unusual formatting requirements.

#### Section 2: Screener Termination Checks
This is a GENERAL section (not per-path). It provides instructions for any tester checking termination points. Format it as a paragraph of instructions followed by a list of all termination points.

**Opening paragraph**: Include general instructions like:
- "For all termination checks – ensure all respondents see the disqualification message and are terminated at the end of the screener unless otherwise specified"
- "Make sure that when testing these termination points, you only answer the specified question 'wrong' and all other responses in a qualifying way, in order to isolate termination to the specified question"

**Termination list**: List each termination point as a single line:
- Question identifier and brief trigger description
- Mark immediate terminations with "*terminate immediately"
- For special routing (e.g., "send non-user to S25 before terminating"), include that routing detail
- Held terminations are the default (no special marker needed)

Example format:
```
S1: age (outside of age 18-70, inclusive) *terminate immediately
S3: sensitive industries (advertising, grocery retail, marketing, beverage manufacturer) *terminate immediately
S4: household income (below 25k)
S10: beverage engagement (has not purchased shelf stable juice in the past three months) *send non-user directly to S25 before terminating, send lapsed user directly to S24 before terminating
```

Generate this by scanning the survey document's screener section for every termination instruction.

#### Section 3: Test Paths (one per matrix column)

Each test path is a numbered column (Test 1, Test 2, etc.) that walks through every survey question in order. For each question, include:

**a) Selection instruction**: What the tester should select
- Use exact R# and C# notation from the survey document (e.g., "Select R3 in C1 and C2")
- For "select any" scenarios, still be specific about exclusions
- For open-ended responses, specify what to type if it matters for piping

**b) Ensure checks**: What the tester should verify at this question
- Question text contains correct piped values (e.g., "Ensure question text reads 'How often do you drink Ocean Spray shelf-stable juice?'")
- Correct response options are visible/hidden based on conditional display
- Randomization is working (options appear in different order)
- Anchored items remain at bottom/top
- Grouped items stay together ("Keep R1 and R2 together")
- Correct question type (single-select vs multi-select)
- Conditional messages appear/don't appear
- Scale labels and carousel behavior are correct

**c) Variable assignment verification**: What variables should be assigned after this question
- "After selection, respondent should be assigned variable_name = value"

**d) Skip/routing verification**: If this question should be skipped for this path
- "Ensure you DO NOT see this question" with explanation of why

### Phase 5: Cross-Reference and Verify

After generating all paths, verify:

1. **Every matrix variable is exercised** — Each variable value in the matrix has at least one path that tests it
2. **No termination conflicts** — Selections in each path don't accidentally terminate the respondent
3. **Piping consistency** — Variables assigned early in the path are correctly referenced in later "Ensure" checks
4. **Response option accuracy** — Every R# reference matches the actual position in the survey document's response tables (R1 is the first option, R2 is the second, etc.)
5. **Skip logic completeness** — Every conditional display rule in the survey is verified in at least one path (either "should see" or "should NOT see")
6. **Loop/carousel handling** — Questions that loop for multiple categories are properly expanded with the right categories for each path

## Critical Rules

These rules exist because errors here have caused real problems in past test plans:

**Response option numbering**: R1 is always the first response option listed in the survey document's table for that question, R2 is the second, etc. Do not skip numbers, do not renumber. If the survey document's table shows 10 options, they are R1-R10 in order. Column numbering follows the same pattern (C1, C2, C3...).

**CRITICAL — R# numbering on conditional display questions**: When a question selectively shows response options based on a variable (e.g., "Only show if <channel>=Grocery"), the R# numbers are assigned from the FULL response table, NOT just the visible subset. For example, if a retailer question lists Target (R1), Walmart (R2), Other mass (R3), Publix (R4), Meijer (R5)... and only grocery options are visible for a given path, Meijer is still R5 — not R2. Count from the top of the complete response table in the survey document, regardless of which options are visible for the current path. This is the single most common R# error.

**Pipe verification must use actual values**: When checking piped text, don't write "Ensure question pipes correctly." Write the actual expected text: "Ensure question reads 'Which of these brands have you purchased for yourself in the past 3 months?'" — using the exact words that should appear given the path's variable assignments.

**Termination awareness at every selection**: Before writing "Select any" for a question, check if ANY response option at that question triggers termination. If so, write "Select any EXCEPT R[x]" and explain why.

**Held vs. immediate terminations**: These are different and the test plan must distinguish them. Immediate terminations end the survey right away. Held terminations let the respondent continue through the screener (seeing all remaining screener questions) before terminating at the end.

**Question numbering**: Use the question identifiers from the survey document (S1, S2, Q301, etc.). If the survey document uses custom numbering (like "S10" for screener question 10, or "Q503" for main survey question), mirror that exactly. Do NOT invent your own numbering. Do NOT renumber questions sequentially (e.g., Q204, Q205, Q206...) if the survey document numbers them differently (e.g., Q301, Q302, Q303...). The survey document's question identifiers are what appear in the programmed survey, and testers navigate by these exact IDs.

**CRITICAL — Deriving question IDs from the survey document**: Main survey questions are typically numbered with a hundreds-group pattern: Q101, Q102, Q103 for one battery, Q201, Q202, Q203 for the next, Q301-Q308 for another, etc. These IDs appear in section headers, question labels, or programming notes in the survey document. You MUST find and use these exact IDs. If the survey document doesn't explicitly label questions with IDs, derive them from the section structure using the hundreds-group convention. Never generate sequential IDs (Q204, Q205...) across battery boundaries.

## Output Quality Standards

The finished document should be indistinguishable from one a senior researcher wrote by hand. This means:

- No placeholder text or TODO markers in the final output
- Every R#/C# reference has been verified against the survey document
- Piped text uses the actual variable values, not variable names
- The document is complete — no "continue pattern for remaining questions" shortcuts
- Formatting is clean and consistent with the reference examples

## Writing Style — Terse and Action-Focused

Test paths should be **concise and action-oriented**. Testers scan these documents quickly; verbosity slows them down. Follow these style rules:

**Selection instructions**: Use bare R#/C# notation. Do NOT include full response option text unless needed for clarity.
- GOOD: "Select R5"
- GOOD: "Select R1 and any others in C1, Select R1 in C2"
- BAD: "Select R5 'Meijer' (visible since <Channel>='Grocery')"
- BAD: "Select R1 'Cranberry' in C1 'Past 3 Months' and C2 'Most Recently'"

**Piping checks**: Use the shorthand patterns, not full question text quotes.
- GOOD: "Ensure 'Ocean Spray cranberry' is piped through"
- GOOD: "Ensure question text for <myself> is piped through"
- BAD: "Ensure question reads 'Which of these brands have you purchased for yourself in the past 3 months? Please select all that apply.'"

**Conditional display**: Use R# notation for visibility checks.
- GOOD: "Ensure you do not see R20"
- GOOD: "Ensure you see R12-R15"
- BAD: "Ensure 'Make me feel better when giving to my child(ren)' is NOT visible (respondent is assigned <Myself>, not <Purchasing for child(ren)>)"

**Grouping checks**: Use bare R# ranges.
- GOOD: "Ensure R1 & R2 are together"
- BAD: "Ensure R1 'Cranberry' and R2 'Cranberry blends (e.g., Cranberry-Apple, Cranberry-Grape)' are kept together"

**Question identifiers**: Use the bare ID. Do NOT add descriptive names or alternate numbering.
- GOOD: "S17"
- GOOD: "Q301"
- BAD: "S17 – Products (Q305)"
- BAD: "Q301 – High-level Needs"

**Variable assignments**: Keep it brief.
- GOOD: "Ensure assigned <product> = cranberry"
- GOOD: "Ensure assigned <low income>"
- BAD: "After this selection, respondent should be assigned <product> based on C2 selection according to the mapping table in the survey document"

**Explanations**: Only add explanatory notes in parentheses when the reason for a selection or exclusion is not obvious.
- GOOD: "Select any EXCEPT R3 (termination)"
- GOOD: "Select R1 or R2" (no explanation needed — it's obvious R3 triggers termination)

Each question entry should typically be 2-6 bullet points. If you find yourself writing 10+ bullets for a single question, you're probably over-explaining.

## Reference Documents

Read these before generating output:

| Reference | When to Read | What It Contains |
|-----------|-------------|-----------------|
| `references/survey-analysis-guide.md` | Always, first | How to systematically extract variables, conditions, and logic from a survey document |
| `references/document-structure.md` | Before writing output | Exact formatting spec for the .docx output, including heading styles, bullet formats, and table structure |
| `references/general-checks-template.md` | Before writing General Checks section | Standard boilerplate for the General Checks section |
| `references/example-patterns.md` | When writing test path entries | Common patterns showing how to write selection instructions and ensure checks for different question types |

## Messages vs. Questions

Survey documents contain two distinct element types. Treat them differently:

**Messages (M1, M2, M3, etc.)** are standalone display elements that appear between question batteries. They serve as transition markers and sometimes carry piped data. In test paths:
- Messages never have "Select" instructions — they are verification-only
- Write: "M2: Ensure you see message" or "M2: Ensure you do not see message"
- If the message contains piped text: "M7: Ensure you see message with [variable] piped through"
- Messages signal section transitions (e.g., M2 often marks screener-to-main-survey transition, M3 marks entry to category-level questions)

**Questions (S1, Q301, D1, etc.)** always have both selection instructions and ensure checks.

## Survey Numbering Convention

Surveys follow a hierarchical numbering system. Mirror the survey document's exact numbering:

- **M-series (M1, M2, M3...)**: Messages — transition markers between sections, no selections. The introduction/welcome message at the start of the survey is always M1, NOT S1. Any text display without response options is an M-series message.
- **S-series (S1, S2, S10, S10A...)**: Screener questions — qualification, demographics, category engagement. S1 is the first actual QUESTION (with response options) in the screener. S-series continues through ALL questions in the screener section, which typically includes demographics, category engagement, brand/product selection, channel/retailer selection, and any attitudes questions that appear BEFORE the main survey entry message (M3).
- **Q-series with hundreds grouping**: Main survey questions grouped by battery. These appear AFTER the screener transition message (typically M3). Each battery gets its own hundreds group:
  - Q1xx: First main survey battery (e.g., broader category/brand perception)
  - Q2xx: Second battery (e.g., brand-specific exploration, triggers)
  - Q3xx: Third battery (e.g., shopping decision factors)
  - Q4xx: Fourth battery (e.g., purchase consideration, feature importance)
  - Q5xx: Fifth battery (e.g., future intent, consumer segments)
- **D-series (D1, D2, D3...)**: Demographics — always at the end of the survey
- **Sub-questions (S10A, Q211A)**: Follow-ups or carousel continuations within a question block

**CRITICAL — Screener boundary**: ALL questions from S1 through the last screener question (before the main survey transition message, usually M3) are S-series, even if they cover topics like brands, products, channels, retailers, fulfillment methods, or attitudes. These are screener questions because they qualify and route respondents. Do NOT relabel screener questions as Q-series.

**CRITICAL — Finding Q-series IDs**: The main survey questions after M3 are numbered in hundreds groups. Look for section headers, battery labels, or explicit Q### references in the survey document to determine the exact IDs. If the survey document groups questions into named sections (e.g., "Broader Beverage Attitudes", "Triggers & Planning", "Shop", "Buy", "Consume"), each section typically corresponds to a hundreds group (Q1xx, Q2xx, Q3xx, Q4xx, Q5xx). Count how many questions are in each section to derive the individual IDs (Q101, Q102, Q103, etc.).

**CRITICAL — Don't skip batteries**: Every Q-series battery in the survey document must appear in the test path. If you see sections for Q1xx, Q2xx, Q3xx, Q4xx, and Q5xx, all five must appear. A common error is skipping Q1xx and jumping from M3 directly to Q2xx.

## Test Matrix Section in the Document

Between the Screener Termination Checks and the Test Paths, include the **Test Matrix** as a reference table. This reproduces the matrix grid the user provided, formatted as a table in the .docx with:
- Rows = key survey variables being tested
- Columns = test path numbers (Test 1, Test 2, etc.)
- Cells = the assigned values for each variable in each path

This gives testers a quick reference for understanding what each path is designed to exercise, without needing to read through the full path detail.

## Exact Language for "Ensure" Checks

Use these exact phrasings — they match the established standard and testers are trained to look for them:

**Visibility**: "Ensure you see [element]" / "Ensure you do not see [element]"
**Piping**: "Ensure [variable value] is piped through" / "Ensure [variable value] is piped through in question text" / "Ensure [variable value] is piped through in R14 response option text"
**Question format**: "Ensure multi select in C1 and C2" / "Ensure single select" / "Ensure question is a [N] point scale" / "Ensure question is a [N] point agreement scale"
**Anchoring**: "Ensure [option text] is anchored at bottom and mutually exclusive" / "Ensure [option text] is anchored to the bottom and open-end"
**Grouping**: "Ensure R1 & R2 are together" / "Ensure R3-R8 are together"
**Assignment**: "Ensure assigned [variable]" / "Ensure assigned [variable] = [value]"
**Looping**: "Ensure you are looped through Q503-Q507 for each response to Q502" / "Ensure all possible questions in Q201-Q229 are looped up to two times for all assigned [brand]"
**Formatting**: "Ensure '[text]' is bolded" / "Ensure '[text]' is underlined"

## Common Question Types and How to Handle Them

### Single-select questions
Selection: "Select R[x]" — one option only
Checks: "Ensure single-select", anchoring, randomization, mutual exclusivity on "None of the above" type options

### Multi-select questions
Selection: "Select R[x] and R[y]" — can select multiple
Checks: "Ensure multi-select", anchoring, randomization, mutual exclusivity on exclusive options

### Grid/matrix questions (multi-column)
Selection: "Select R[x] in C1, R[y] in C2"
Checks: Column labels correct, must-select-in-C1-before-C2 logic works, proper piping per column

### Carousel/scale questions
Selection: "Select [value] for [item]"
Checks: All items appear, scale labels correct, randomization of items (not scale)

### Open-ended questions
Selection: "Type '[specific text]'" when piping matters, or "Type any response" when it doesn't
Checks: Text field appears, character limits if specified

### Looped questions
These repeat for each assigned category/brand. Expand them fully — write out each iteration with the specific category/brand piped in.
Selection: Specify for each iteration
Checks: Correct number of iterations, correct piping per iteration

### Conditional display questions
For paths where the question SHOULD appear: Write normal selection and checks
For paths where the question should NOT appear: "Ensure you do not see this question" (use exact phrasing)

### Messages
No selection. Verification only: "Ensure you see message" or "Ensure you do not see message"
If piped: "Ensure you see message with [actual piped value] piped through"
