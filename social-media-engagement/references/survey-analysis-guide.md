# Survey Analysis Guide

This document describes how to systematically analyze a survey document before writing test paths. Thorough analysis here prevents cascading errors in the test paths.

## Step 1: Full Read-Through

Read the entire survey document end to end. Don't take notes yet—just absorb the overall structure, flow, and scope. Pay attention to:
- How many sections exist (Screener, Main Body sections, Demographics, etc.)
- Approximately how many questions total
- The general complexity level (simple linear flow vs. heavy branching)
- Whether there are loops, carousels, or repeated question blocks

## Step 2: Variable Inventory

Go through the survey document again, this time cataloging every variable. Create a structured inventory with these fields for each:

### Variable Entry Format
```
Variable Name: <exact name as written in survey doc, including angle brackets if used>
Created At: <question number where this variable is first assigned>
Assignment Logic: <exact conditions for assignment>
Possible Values: <all possible values this variable can take>
Used At: <list of question numbers where this variable affects display, piping, or routing>
Type: <assignment | hidden | quota | routing | piping>
```

### Types of Variables to Look For

**Assignment variables** — Created by explicit "Assign <variable> if..." instructions
- Example: `Assign <Myself> if respondent selects R1 Myself in S12 C1`
- These are the most common and most important for test paths

**Hidden/computed variables** — Created by "Create hidden variable..." instructions
- Example: `Create hidden variable <age group> according to...`
- These often drive downstream conditional logic

**Quota variables** — Variables used for quota management
- Example: `Assign <category quota> using least fill`
- Important because they affect which path a respondent takes

**Piping variables** — Variables whose values get inserted into question/response text
- Example: `<brand>`, `<retailer>`, `<product>`, `<category>`
- Critical for pipe verification in test paths

**Routing variables** — Variables that determine which questions appear
- Example: `Only show if <Purchasing for child(ren)>`
- Essential for skip logic verification

## Step 3: Termination Map

Create a complete map of every termination point:

### Termination Entry Format
```
Question: <question number>
Trigger: <exact condition that triggers termination>
Type: Immediate | Held (until end of screener)
Response Options: <specific R# values that trigger it>
Notes: <any special handling, e.g., "send to S25 before terminating">
```

### What to Look For
- "Terminate immediately" — respondent exits survey right away
- "Terminate" without "immediately" — usually held until end of screener
- "Hold until end of screener" — explicit held termination
- Conditional terminations — "Terminate if [condition]" (e.g., "Terminate if not <student>")
- Look in both the question instruction boxes AND the response option annotation columns

## Step 4: Conditional Display Map

Catalog every conditional display rule:

### Conditional Display Entry Format
```
Question: <question number>
Condition: <exact condition for display>
Affects: Question | Response options | Question text | Column
Details: <what specifically appears/changes>
```

### Types of Conditional Display
- **Entire question conditional**: "Only show if <variable>" — question appears or doesn't
- **Response options conditional**: "Only show R[x] if <variable>" — specific options appear/disappear
- **Question text conditional**: "If <Myself>: [text A] / If <Purchasing for child(ren)>: [text B]" — different wording based on variable
- **Column conditional**: "Only show C2 if respondent is assigned <variable>" — entire grid column appears/disappears
- **Selective response option display**: "Show response options according to <channel>" — different options for different variable values

## Step 5: Piping Map

Catalog every instance where variable values are inserted into text:

### Piping Entry Format
```
Question: <question number>
Location: Question text | Response option | Column header
Variable(s): <which variable(s) are piped>
Template: <the text with variables marked, e.g., "How often do you drink <brand> juice?">
```

### Piping Resolution
For each piped variable, trace back to where it was assigned and document what the actual text would be for each possible value. This is critical because the test path must specify the ACTUAL expected text, not the variable placeholder.

Example:
- Variable `<brand>` = "Ocean Spray" (assigned in S14 based on C2 selection)
- Piped in S15: "How often do you drink <brand> shelf-stable juice?"
- Expected text for this path: "How often do you drink Ocean Spray shelf-stable juice?"

## Step 6: Looping and Carousel Logic

Identify questions that repeat for multiple items:

### Loop Entry Format
```
Question(s): <question number range>
Loops For: <what drives the loop, e.g., "each assigned <priority category>">
Max Iterations: <maximum number of loops>
Content Changes: <what changes per iteration, e.g., category-specific brand lists>
```

### Key Details
- How many times does the loop execute for each path?
- What content changes per iteration (response options, question text, etc.)?
- Is there a specific order to the iterations?
- Are there sub-loops (loops within loops)?

## Step 7: Randomization and Grouping Rules

Catalog display rules that testers need to verify:

### Randomization Entry Format
```
Question: <question number>
What Randomizes: Rows | Columns | Items in carousel
What Doesn't: <anchored items, grouped items>
Grouping: <"Keep R[x] and R[y] together" instructions>
Anchoring: <"Anchor" items that stay at top/bottom>
Mutual Exclusivity: <options that are mutually exclusive>
```

## Step 8: Question-by-Question Reference Table

After completing steps 2-7, create a master reference table that lists, for each question:

| Question | Type | Variables Affected | Conditional Display | Terminations | Piping | Notes |
|----------|------|-------------------|-------------------|-------------|--------|-------|
| S1 | Message | None | None | None | None | Show all |
| S2 | Dropdown | `<age group>` | None | Immediate if <18 or >70 | None | Create hidden variable |
| ... | ... | ... | ... | ... | ... | ... |

This table becomes your primary reference when writing test paths. For each question in a path, you can quickly look up what matters.

## Verification

After completing the analysis, verify completeness:
- [ ] Every variable in the survey is cataloged
- [ ] Every termination point is mapped
- [ ] Every conditional display rule is captured
- [ ] Every piping instance is documented
- [ ] Every loop/carousel is identified
- [ ] Every randomization/grouping/anchoring rule is noted
- [ ] The master question reference table is complete
