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

Generate a .docx file using the docx skill. Read `references/document-structure.md` for the EXACT formatting specification. The format is simple paragraph + bullet — NO tables for test paths, NO color formatting, NO title pages.

The document has these sections, in order:

#### Section 1: Title
Two lines: project name + date. Nothing else. See `references/document-structure.md`.

#### Section 2: General Checks (all)
A standardized list of formatting and behavior checks that apply across all survey testing. These are consistent across projects. Read `references/general-checks-template.md` for the EXACT standard template — use the wording VERBATIM. Do NOT rewrite or "improve" this boilerplate.

#### Section 3: Screener Termination Checks
This is a GENERAL section (not per-path). It provides instructions for any tester checking termination points.

**Opening paragraph** (normal text): General instructions:
"For all termination checks – ensure all respondents see the disqualification message and are terminated at the end of the screener (skipping questions that do not make sense for them to see in programming notes)."

**Bold paragraph**: The isolation instruction is rendered in **bold**:
"Make sure that when testing these termination points, you only answer the specified question 'wrong' and all other responses in a qualifying way, in order to isolate termination to the specified question. For example, in the age termination, make sure to answer all other questions in the screener in such a way that would qualify a respondent, so you are sure age and not some other response created the termination."

**CRITICAL — ALL SCREENER TERMINATION BULLETS ARE BOLD**: The termination list uses the bullet / sub-bullet format with ALL TEXT IN BOLD. This distinguishes it from test path content (which is NOT bold). Use up to 3 levels:
- **Question ID** as a **bold level 0 bullet** (ilvl=0): the bare question ID, e.g., **S1**
- **Termination conditions** as **bold level 1 sub-bullets** (ilvl=1) stacked underneath
- **Enumerated items** as **bold level 2 sub-bullets** (ilvl=2) when listing specific response options that cause termination

Example (all text rendered bold):
```
• S1
  ○ Terminate if respondent does not select between 21-74

• S4
  ○ Terminate if respondent selects any of the following (R1-R6):
    ▪ An advertising agency…
    ▪ A television or radio station…
    ▪ A marketing or market research firm…
    ▪ A vet, pet breeder, or pet groomer
    ▪ A retailer…

• S7
  ○ Terminate if income <$30k (R1) and non-student
  ○ Terminate if income <$30k (R1) and respondent is <multi-HH>
```

**Be 100% inclusive** — list EVERY specific termination condition on its own sub-bullet. For questions where specific response options trigger termination, list each disqualifying response on its own level 2 sub-bullet line.

Generate this by scanning the survey document's screener section for every termination instruction.

#### Section 4: Test Paths Table
Reproduce the test matrix as a simple table. Rows = variables, columns = test path numbers. Include assignment rows (Builder, Tester) if provided. Simple borders, no color.

#### Section 5: Individual Test Paths (one per matrix column)

Each test path section uses Heading 2: "Path [N]" — just the number, no descriptive subtitle (e.g., "Path 1", "Path 2"). **NEVER** use "Test Path 1" — always "Path 1".

**CRITICAL — NO "Derived Variables" section**: Do NOT add a variable summary or "Derived Variables" block at the start of each path. Jump straight into the Heading 3 sub-heading ("Screener") and the first question.

**Within each path, add survey section sub-headings** using Heading 3 style to mark major survey sections: Screener, Plan, Shop, Buy, Use, Switching Behavior, Future Behavior, Demos & Psychographics (or whatever section names the survey document uses). These provide essential navigation within long test paths.

Then walk through every survey question using **bullet / sub-bullet format** (up to THREE levels deep):

**Question ID** as a **level 0 bullet** (ilvl=0): just "S1" or "Q301" — bare ID, no colon, no topic name. Consecutive questions with the same simple instruction can be combined: "S2-S3" as one bullet followed by "Select any" as one sub-bullet.

**Instructions** as **level 1 sub-bullets** (ilvl=1) stacked underneath the question ID bullet. Each sub-bullet covers one of:

**Enumerated lists** as **level 2 sub-bullets** (ilvl=2) nested under a level 1 instruction. Use level 2 for: brand name lists, retailer name lists, DO see / do NOT see response option lists, and any other enumerated items listed under an instruction sub-bullet.

Each level 1 sub-bullet covers one of:

**a) Selection instruction**: What the tester should select
- Use R# with a dash and the actual option text for specific selections: `Select R1 – Male`, `Select R6 – Kroger in C1 and C2`
- Use the full quoted text when the selection is critical for routing or variable assignment: `Select "Medicine that protects against Fleas and Ticks" and "Medicine that prevents Heartworm"`, `Select "Just wanted to make sure my pet had the proper parasite protection"`
- For "select any" scenarios, note exclusions: `Select any other than R1-R4`, `Select any EXCEPT R3 (termination)`
- For simple selections, bare text or values are fine: `Select 1 dog`, `Select 0 cats`, `Select any`, `Select "Yes"`

**b) Ensure checks**: What the tester should verify. **Always use "Ensure" — never use "Verify" or "Check".**
- Piping: `Ensure <brand> is piped through as <Axe>`, `Ensure "Ocean Spray cranberry" is piped through`
- Question text (when variables are piped into the question wording): `Ensure question reads "Did you do any research on flea and tick protection before the most recent trip you made to Banfield where you bought Frontline topical?"` — include the full expected question text with piped values filled in
- Conditional visibility: Use **DO see / do NOT see blocks** listing actual response option text when a question has options that are conditionally shown/hidden based on path variables. See `references/example-patterns.md` Pattern 13 for the full pattern. This is one of the most important checks — it tells the tester exactly which options should appear for their path.
- Format: `Ensure multi-select in C1 and C2`, `Ensure single select`, `Ensure single select per row`
- Anchoring: `Ensure "None of the above" is anchored at bottom and mutually exclusive`, `Ensure "Other, please specify" is anchored at the bottom`
- Grouping: `Ensure R1 & R2 are together`, `Ensure R4-R7 are kept together`
- Scale: `Ensure 5-point scale is shown`, `Ensure shown 4-point scale`
- Randomization: `Ensure responses are randomized`, `Ensure responses are not randomized`, `Ensure list is not randomized`

**c) Variable assignment**: `Ensure assigned <brand> is "Frontline"`, `Ensure <retailer> assigned <Kroger> and <channel> assigned as <grocery>`, `Ensure assigned <proactive>`

**d) Hidden questions**: `Should not see`, `Ensure you do not see`, or `Ensure not shown question`

**e) Messages**: Include the FULL message text when the message contains important piped values: `Ensure message reads: "Earlier you told us you recently bought Frontline topical at Banfield at a physical location. For the following questions, please think about that experience in particular."`

**f) Brand / retailer lists**: When a brand or retailer question has a conditional response list (different brands visible depending on category, OTC/Rx status, etc.), enumerate the full visible list so the tester knows exactly which options should appear. See `references/example-patterns.md` Pattern 14.

### Phase 4b: Build a Question Inventory

Before writing the test path, create a numbered list of EVERY question in the survey document (M1, S1, S2, ... S20, S21, M2, Q101, Q102, ... D5). This inventory ensures you don't skip questions. For each question, note:
- Its ID (M1, S7a, Q203, etc.)
- Whether it applies to this path (always shown, conditionally shown, or hidden)
- If hidden: include "Ensure you do not see this question" in the test path

This inventory is your checklist. Every question in the survey document must appear in the test path — either as a full entry with selections/ensures, or as "Ensure you do not see this question."

### Phase 5: Cross-Reference and Verify

After generating all paths, verify:

1. **Every matrix variable is exercised** — Each variable value in the matrix has at least one path that tests it
2. **No termination conflicts** — Selections in each path don't accidentally terminate the respondent
3. **Piping consistency** — Variables assigned early in the path are correctly referenced in later "Ensure" checks
4. **Response option accuracy** — Every R# reference matches the actual position in the survey document's response tables (R1 is the first option, R2 is the second, etc.)
5. **Skip logic completeness** — Every conditional display rule in the survey is verified in at least one path (either "should see" or "should NOT see")
6. **Loop/carousel handling** — Questions that loop for multiple categories are properly expanded with the right categories for each path
7. **No missing questions** — Cross-check every question in your inventory against the test path output. Every survey question must be accounted for.
8. **Hidden questions included** — Questions that should NOT appear for this path must still have an entry: "Ensure you do not see this question"

## Critical Rules

These rules exist because errors here have caused real problems in past test plans:

**Response option numbering**: R1 is always the first response option listed in the survey document's table for that question, R2 is the second, etc. Do not skip numbers, do not renumber. If the survey document's table shows 10 options, they are R1-R10 in order. Column numbering follows the same pattern (C1, C2, C3...).

**CRITICAL — R# numbering on conditional display questions**: When a question selectively shows response options based on a variable (e.g., "Only show if <channel>=Grocery"), the R# numbers are assigned from the FULL response table, NOT just the visible subset. For example, if a retailer question lists Target (R1), Walmart (R2), Other mass (R3), Publix (R4), Meijer (R5)... and only grocery options are visible for a given path, Meijer is still R5 — not R2. Count from the top of the complete response table in the survey document, regardless of which options are visible for the current path. This is the single most common R# error.

**Pipe verification must use actual values**: When checking piped text, don't write "Ensure question pipes correctly." Write the actual expected text: "Ensure 'Ocean Spray cranberry' is piped through" — using the exact words that should appear given the path's variable assignments.

**Termination awareness at every selection**: Before writing "Select any" for a question, check if ANY response option at that question triggers termination. If so, write "Select any EXCEPT R[x]" and explain why.

**Held vs. immediate terminations**: These are different and the test plan must distinguish them. Immediate terminations end the survey right away. Held terminations let the respondent continue through the screener (seeing all remaining screener questions) before terminating at the end.

**CRITICAL — Trust the test matrix over conditional display conflicts**: If the test matrix specifies a value (e.g., Channel=Grocery for a male respondent) but the survey document says that option is hidden for that respondent type (e.g., "HIDE IF <MALE>"), FOLLOW THE MATRIX. Select the matrix-specified value. Add a brief 1-line note flagging the conflict. Do NOT change the selection, debate alternatives, or write multiple scenarios. The test matrix may be intentionally testing that conditional logic, or the survey may have been updated since the conditional rule was written. The matrix is the source of truth for what to select.

**CRITICAL — Force non-qualifying selections for non-assigned segments**: When a respondent qualifies for multiple segments (e.g., Styling + Shampoo) but the matrix assigns only one (e.g., Styling), you must make the non-assigned segments fail to qualify. At the usage frequency question, select qualifying frequencies (R1-R3 typically) for the assigned segment and NON-qualifying frequencies (R4-R7 typically) for all other segments. This forces the survey's assignment logic to pick the intended segment. If you select qualifying frequencies for all segments, the wrong segment might be assigned.

**CRITICAL — Multi-value matrix rows**: When a matrix row lists multiple values separated by commas (e.g., Q201: "R1, R5, R8"), select ONLY the value that corresponds to the assignment in the related matrix row. For example, if Q201 says "R1, R5, R8" and Q202 says "Getting ready while traveling / on vacation" (which is R8), select ONLY R8 at Q201. The Q201 row documents what occasions the path *could* exercise, but the Q202 row determines which one is actually assigned. Select only what's needed to produce the assigned value.

**CRITICAL — R# verification for long tables**: When counting R# positions in tables with 20+ items, count carefully and document your count. For brand tables, list a few landmark positions to verify (e.g., "R10=American Crew, R15=Miss Jessie's, R20=Pantene, R26=Axe"). Miscounting by even 1 position in a 30-item table produces the wrong R#.

**Question numbering**: Use the question identifiers from the survey document (S1, S2, Q301, etc.). If the survey document uses custom numbering (like "S10" for screener question 10, or "Q503" for main survey question), mirror that exactly. Do NOT invent your own numbering. Do NOT renumber questions sequentially (e.g., Q204, Q205, Q206...) if the survey document numbers them differently (e.g., Q301, Q302, Q303...). The survey document's question identifiers are what appear in the programmed survey, and testers navigate by these exact IDs.

**CRITICAL — Deriving question IDs from the survey document**: Main survey questions are typically numbered with a hundreds-group pattern: Q101, Q102, Q103 for one battery, Q201, Q202, Q203 for the next, Q301-Q308 for another, etc. These IDs appear in section headers, question labels, or programming notes in the survey document. You MUST find and use these exact IDs. If the survey document doesn't explicitly label questions with IDs, derive them from the section structure using the hundreds-group convention. Never generate sequential IDs (Q204, Q205...) across battery boundaries.

## Output Format — CRITICAL

The output .docx must use the **paragraph + bullet format** described in `references/document-structure.md`. Read that file thoroughly before generating any output.

### Format Summary

The document uses ONLY these Word elements:
- **Heading 1**: Document title AND top-level section headings (General Checks, Screener Termination Checks, Test Paths Table)
- **Heading 2**: Individual path headings ("Path 1", "Path 2", etc.) — NOT "Test Path 1"
- **Heading 3**: Survey section sub-headings within each path (Screener, Plan, Shop, Buy, Use, Switching Behavior, Future Behavior, Demos & Psychographics)
- **Normal**: Intro/explanatory paragraphs and date line only
- **Numbered list (level 0)**: General Checks main items (1., 2., 3., ... 12.) — NOT bullet characters
- **Numbered list (level 1)**: General Checks sub-items (a., b., c., d.) under item 11
- **Bullet list (level 0)**: Screener termination question IDs (BOLD) AND test path question IDs (not bold)
- **Bullet list (level 1)**: Screener termination conditions (BOLD) AND test path instructions (not bold)
- **Bullet list (level 2)**: Brand/retailer enumerated lists, DO see / do NOT see response lists, and screener termination enumerated items
- **One table**: The test paths overview matrix (proper Word table with visible grid borders)

### CRITICAL Formatting Differences Between Sections:
1. **General Checks**: Uses NUMBERED format (1., 2., 3...) with lettered sub-items (a., b., c., d.)
2. **Screener Termination Checks**: Uses bullet format with ALL TEXT IN BOLD
3. **Test Paths**: Uses bullet format with regular (non-bold) text
4. **All three sections** use the stacked parent/child structure with up to 3 levels of depth

### What NOT to include:
- NO tables for individual test path content
- NO color formatting (no blue headers, no shading, no alternating rows)
- NO title page or cover page
- NO table of contents
- NO logos
- NO topic names or descriptions after question IDs (just bare "S1" NOT "S1: Age" or "S1 – Age")
- NO variable summary tables at path starts
- NO "Derived Variables" section — NEVER add a variable summary block at the start of each path
- NO "Path Profile" lines
- NO page breaks between paths
- NO [ ] checkboxes in general checks — use numbered list
- NO colons after question IDs (use "S1" not "S1:")
- NO "Test Path [N]" headings — use "Path [N]" only
- NO bullet characters (•) for General Checks — use numbers (1., 2., 3., ...)

The document should be a clean, simple Word doc with headings, paragraphs, numbered lists, bullet lists (3 levels deep), and one table. That's it.

### CRITICAL — docx-js Numbering Configuration

Use the Node.js `docx` package (npm install docx) with TWO separate numbering configurations:

1. **"general-checks"**: Decimal numbers at level 0 (1., 2., 3...) and lowercase letters at level 1 (a., b., c...)
2. **"bullets"**: Standard bullets at level 0 (•), open circles at level 1 (○), and dashes at level 2 (–)

See `references/document-structure.md` for the complete implementation with helper functions and code examples.

## Output Quality Standards

The finished document should be indistinguishable from one a senior researcher wrote by hand. This means:

- No placeholder text or TODO markers in the final output
- Every R#/C# reference has been verified against the survey document
- Piped text uses the actual variable values, not variable names
- The document is complete — no "continue pattern for remaining questions" shortcuts
- Formatting matches the reference examples exactly (paragraph + bullet, no tables/color)

## Writing Style — Specific, Action-Focused, and Complete

Test paths should be **specific and action-oriented**. Every sub-bullet should tell the tester exactly what to do or exactly what to look for — using actual response option text, actual piped values, and actual variable assignments. Never write vague or generic instructions.

**Selection instructions**: Use the actual text of what the tester should select — either R# with a dash and the option text, or the full quoted text. Bare R# alone is fine for grouping checks but not for selections where the tester needs to find a specific option.
- GOOD: `Select R1 – Male`
- GOOD: `Select "Medicine that protects against Fleas and Ticks" and "Medicine that prevents Heartworm"`
- GOOD: `Select Frontline and any others for C1 and C2 and select Frontline for C3`
- GOOD: `Select "Just wanted to make sure my pet had the proper parasite protection"`
- GOOD: `Select "$30,000 to $49,000"`
- GOOD: `Select any other than R1-R4`
- GOOD: `Select 1 dog` / `Select 0 cats`
- BAD: `Select R1 (F&T medicine), R2 (HW medicine)` — Don't use parenthetical shorthand; use the actual option text

**Piping checks — question text**: When a variable is piped into the question wording, include the full expected question text so the tester can verify it reads correctly. This is only needed when piping changes the question wording.
- GOOD: `Ensure question reads "Did you do any research on flea and tick protection before the most recent trip you made to Banfield where you bought Frontline topical?"`
- GOOD: `Ensure question reads "What type of flea and tick protection products have you purchased for your pet(s) in the past year?"`
- BAD: `Ensure question text pipes properly` — Too vague, doesn't tell the tester what to look for

**Piping checks — variable values**: Use the actual piped value text.
- GOOD: `Ensure "Ocean Spray cranberry" is piped through`
- GOOD: `Ensure <brand> is piped through as <Axe>`
- GOOD: `Ensure "flea and tick protection" is piped through in question text`
- BAD: `Ensure piping is correct` — What piping? What value?

**Conditional display — DO see / do NOT see blocks**: This is a CRITICAL pattern. When a question has response options that are conditionally shown or hidden based on path variables (channel, form, species, OTC/Rx, fulfillment method, etc.), create "Ensure you DO see" and "Ensure you do NOT see" blocks that list the actual response option text. These tell the tester exactly which options should be visible for their specific path.
- GOOD:
  ```
  Ensure you DO see:
      Do not have to pay for shipping
      Can get product(s) right away
      Convenient location
      Going there anyway for pet services (e.g., grooming)
  Ensure you do NOT see:
      Can read product reviews
      Subscription program
      Easy to re-order
  ```
- BAD: `Ensure conditional display options are correct` — Useless to the tester
- BAD: `Ensure path-specific options display` — Doesn't say WHICH options

**Grouping checks**: Use bare R# ranges.
- GOOD: `Ensure R2, R3, R4 are together`
- GOOD: `Ensure R14 & R15 are together`

**Question identifiers**: Bare ID as a level 0 bullet, no colon, no topic name.
- GOOD: `• S17` (level 0 bullet)
- GOOD: `• Q301` (level 0 bullet)
- BAD: `S17:` (colon after ID)
- BAD: `S17 – Products` (topic name after ID)

**Variable assignments**: Use "Ensure" with the actual assigned value.
- GOOD: `Ensure assigned <OTC/Rx> is "OTC" and assigned <brand> is "Frontline"`
- GOOD: `Ensure <retailer> assigned <Kroger> and <channel> assigned as <grocery>`
- GOOD: `Ensure assigned <low income>`
- GOOD: `Ensure assigned to <New Dog Owner>`
- BAD: `Ensure variables assigned correctly` — What variables? What values?

**Messages**: Include the FULL message text when the message contains piped values or important wording the tester should verify.
- GOOD: `Ensure message reads: "Earlier you told us you recently bought Frontline topical at Banfield at a physical location. For the following questions, please think about that experience in particular."`
- BAD: `Verify introduction message displays clearly` — Doesn't tell the tester what the message should say

**Brand / retailer enumeration**: When a brand or retailer selection question shows a conditional list (filtered by category, OTC/Rx, channel, etc.), enumerate the full visible list. See Pattern 14 in `references/example-patterns.md`.

**Combining simple questions**: When consecutive questions all have the same simple instruction (e.g., "Select any"), combine them: `S2-S3: Select any`, `D1-D4: Select any`. Do NOT give each one its own entry with generic sub-bullets.

**Explanations**: Only add notes when the reason is not obvious.
- GOOD: `Select any other than R1-R4`
- GOOD: `Do not select any other qualifying categories (R3 "Combination medicine…")`

Each question entry should be **100% completely inclusive** — include every ensure check, every selection instruction, every piping verification, every DO see / do NOT see block, every variable assignment, and every conditional display check as separate sub-bullets. If a question has 10+ sub-bullets, that's fine. Thoroughness and completeness are more important than brevity. Do NOT summarize multiple checks into one line.

## Reference Documents

Read these before generating output:

| Reference | When to Read | What It Contains |
|-----------|-------------|-----------------|
| `references/survey-analysis-guide.md` | Always, first | How to systematically extract variables, conditions, and logic from a survey document |
| `references/document-structure.md` | Before writing output | EXACT formatting spec for the .docx output — paragraph + bullet format, Word styles, what NOT to include |
| `references/general-checks-template.md` | Before writing General Checks section | EXACT standard boilerplate — use verbatim |
| `references/example-patterns.md` | When writing test path entries | Common patterns showing correct format for different question types |

## Messages vs. Questions

Survey documents contain two distinct element types. Treat them differently:

**Messages (M1, M2, M3, etc.)** are standalone display elements that appear between question batteries. They serve as transition markers and sometimes carry piped data. In test paths, messages use the same bullet / sub-bullet format as questions:
- Messages never have "Select" instructions — they are verification-only
- Simple: "• M2" (level 0 bullet) then "○ Ensure you see message" (level 1 sub-bullet)
- With piping: "• M7" (level 0 bullet) then sub-bullets for each piping check
- Hidden: "• M2" then "○ Ensure you do not see message"
- Messages signal section transitions (e.g., M2 often marks screener-to-main-survey transition)

**Questions (S1, Q301, D1, etc.)** always have both selection instructions and ensure checks.

## Survey Numbering Convention

Surveys follow a hierarchical numbering system. Mirror the survey document's exact numbering:

- **M-series (M1, M2, M3...)**: Messages — transition markers between sections, no selections. The introduction/welcome message at the start of the survey is always M1, NOT S1.
- **S-series (S1, S2, S10, S10A...)**: Screener questions — qualification, demographics, category engagement. S-series continues through ALL questions in the screener section.
- **Q-series with hundreds grouping**: Main survey questions grouped by battery (Q1xx, Q2xx, Q3xx, etc.). These appear AFTER the screener transition message.
- **D-series (D1, D2, D3...)**: Demographics — always at the end of the survey
- **Sub-questions (S10A, Q211A)**: Follow-ups or carousel continuations

**CRITICAL — Screener boundary**: ALL questions from S1 through the last screener question (before the main survey transition message, usually M3) are S-series, even if they cover topics like brands, products, channels, retailers, fulfillment methods, or attitudes.

**CRITICAL — Finding Q-series IDs**: Look for section headers, battery labels, or explicit Q### references in the survey document. Each named section typically corresponds to a hundreds group.

**CRITICAL — Don't skip batteries**: Every Q-series battery in the survey document must appear in the test path.

## Test Matrix Section in the Document

Between the Screener Termination Checks and the Test Paths, include the **Test Paths Table** as a reference table. This reproduces the matrix grid the user provided, formatted as a simple table in the .docx with:
- Rows = key survey variables being tested
- Columns = test path numbers (1, 2, 3, etc.)
- Cells = the assigned values for each variable in each path
- Optional rows for Builder/Tester assignments

Simple table formatting — thin borders, no color fills.

## Exact Language for "Ensure" Checks

Use these exact phrasings — they match the established standard. **Always use "Ensure" — never "Verify", "Check", or "Confirm".**

**Visibility — simple**: `Ensure you see R20` / `Ensure you do not see R20` / `Ensure R6 is not shown`
**Visibility — DO see / do NOT see blocks**: For questions with conditionally displayed response options, use multi-line blocks listing the actual option text:
```
Ensure you DO see:
    [actual response text]
    [actual response text]
Ensure you do NOT see:
    [actual response text]
    [actual response text]
```
Or with context: `Ensure you DO see responses shown to everyone (e.g., Easy to browse, Large selection) and:`
**Piping — values**: `Ensure "Ocean Spray cranberry" is piped through` / `Ensure <brand> is piped through as <Axe>`
**Piping — question text**: `Ensure question reads "What type of flea and tick protection products have you purchased for your pet(s) in the past year?"` — full question text with piped values filled in
**Question format**: `Ensure multi-select in C1 and C2` / `Ensure single select` / `Ensure shown 4-point scale` / `Ensure single select per row`
**Anchoring**: `Ensure "None of the above" is anchored at bottom and mutually exclusive` / `Ensure "Other, please specify" is anchored at the bottom`
**Grouping**: `Ensure R1 & R2 are together` / `Ensure R4-R7 are kept together`
**Assignment**: `Ensure assigned <brand> is "Frontline"` / `Ensure <retailer> assigned <Kroger> and <channel> assigned as <grocery>` / `Ensure assigned <low income>` / `Ensure assigned to <New Dog Owner>`
**Randomization**: `Ensure responses are randomized` / `Ensure responses are not randomized` / `Ensure list is not randomized`
**Looping**: `Ensure you are looped through Q503-Q507 for each response to Q502`
**Messages**: `Ensure message reads: "[full message text with piped values]"` / `Ensure message appears` / `Ensure you do not see message`
**Hidden questions**: `Should not see` / `Ensure you do not see` / `Ensure not shown question` / `Ensure you do not see the question`
**Brand lists**: `Ensure you only see the following brands:` followed by an indented list of brand names
**Enumerated response lists**: `Ensure you see all retailer options, including OTC-only options:` followed by an indented list

## Common Question Types and How to Handle Them

### Single-select questions
Selection: "Select R[x]" or "Select R[x] – [brief descriptor]"
Checks: "Ensure single select", anchoring, randomization

### Multi-select questions
Selection: "Select R[x] and R[y]"
Checks: "Ensure multi-select", anchoring, randomization, mutual exclusivity

### Grid/matrix questions (multi-column)
Selection: "Select R[x] in C1, R[y] in C2"
Checks: Column formats (multi-select vs single-select per column), piping per column

### Carousel/scale questions
Selection: "Select [value] for [item]" or "Select any"
Checks: Scale type, items appear, randomization of items

### Open-ended questions
Selection: "Type any response" or "Type '[specific text]'" when piping matters
Checks: Text field appears

### Looped questions
Expand fully — write out each iteration with the specific category/brand piped in.

### Conditional display questions
Visible: Normal selection and checks, plus DO see / do NOT see blocks listing which response options should/shouldn't appear for this path
Hidden: "Should not see" or "Ensure you do not see" or "Ensure not shown question"

### Messages
No selection. Include the FULL message text when the message contains piped values:
- `Ensure message reads: "Earlier you told us you recently bought Frontline topical at Banfield at a physical location."`
- For simple transition messages: `Ensure message appears` or `Ensure message is shown`
- For hidden messages: `Ensure you do not see message`
- When message has multiple piped values, list them: `Ensure <brand> is piped through as <Axe>`, `Ensure <segment> is piped through as <styling products>`
