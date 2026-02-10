---
name: survey-document-builder
description: |
  Transform survey wireframes into fully programmed quantitative survey documents. Use when user mentions "wireframe to survey", "survey document", "build survey", "expand wireframe", "quant survey", or needs to create a professional survey document from a wireframe blueprint. Handles CPG consulting survey workflows including Path to Purchase, Category Expansion, Shopper Journey, Segmentation, and other quantitative research projects. Expects: (1) a wireframe document with objectives, quotas, and high-level questions, (2) optionally past survey examples for format reference, and (3) optionally discovery/inputs decks for context.
---

# Survey Document Builder

Transform wireframes into fully programmed survey documents.

## Quick Reference

| Input | Output |
|-------|--------|
| Wireframe + Past Example | Full Survey Document (.docx) |

## Workflow

### Step 1: Gather Inputs

Required:
- **Wireframe** (.docx): Contains objectives, quotas, survey structure, high-level questions with rationale

Recommended:
- **Past Example** (.docx): A completed survey document from a similar project type to learn formatting patterns
- **Discovery/Inputs Decks** (.pptx): For context on brand lists, response options, market specifics

Ask user for these if not provided.

### Step 2: Analyze the Wireframe

Extract and confirm:
1. **Survey Overview**: Objectives, learning areas, sample size, quotas
2. **Section Structure**: Identify sections (Screener, main body sections, Demographics)
3. **Question Inventory**: List all questions with their objectives
4. **Variable Logic**: Identify <piped variables> and assignment rules
5. **Quota Requirements**: Brand mins, segment mins, termination criteria

### Step 3: Learn from Past Example

If past example provided, extract:
- Document header format (logos, title styling)
- Table structure for questions (columns, widths, borders)
- Programming instruction conventions
- Response list formatting (with/without images)
- "NEW SCREEN" and section header patterns
- Hidden variable naming conventions
- Termination message wording

If no example provided, use patterns from [document-structure.md](references/document-structure.md).

### Step 4: Build the Survey Document

For each wireframe question, expand into full survey format:

1. **Question Text**: Rewrite for consumer clarity (8th-grade reading level)
2. **Response Options**: Build complete lists (MECE, parallel phrasing, 15 max)
3. **Programming Instructions**: Add randomization, select type, display logic
4. **Skip/Display Logic**: Convert wireframe notes to formal logic
5. **Variable Assignments**: Define hidden variables and quota tracking

Apply best practices from [survey-best-practices.md](references/survey-best-practices.md).

### Step 5: Format as .docx

Use the docx skill to create the final document:
- Match header/footer from example
- Use consistent table formatting throughout
- Include "NEW SCREEN" markers between questions
- Add blue topic header bars for each question
- Include programming notes in appropriate cells

## Key Conventions

### Question Table Structure

Standard 3-column layout:
| Column | Content |
|--------|---------|
| Q# | Question number or "Message" |
| Question | Full text + response options + programming notes |
| Notes | Objective/rationale OR display logic |

### Programming Instructions

Common patterns:
- `*Please select one.*` — Single select
- `*Please select all that apply.*` — Multi-select
- `*Select up to X.*` — Limited multi-select
- `Randomize.` / `Do not randomize.` — Response order
- `Anchor.` — Keep option at end (e.g., "None of the above")
- `Mutually Exclusive.` — Cannot combine with other options
- `Terminate immediately if...` — Screen-out logic

### Variable Naming

Use angle brackets for piped content:
- `<brand>`, `<category>`, `<retailer>`, `<pet name>`
- `<qualified category>`, `<form>`, `<species>`

### Response List Guidelines

- 15 options maximum per question
- Include "Other (Please Specify)" when appropriate
- Include "None of the above" as anchored, mutually exclusive option
- For brand lists: include images/logos when available

## Reference Files

- [survey-best-practices.md](references/survey-best-practices.md) — Bias avoidance, question writing rules, review checklists
- [document-structure.md](references/document-structure.md) — Standard sections and formatting patterns
- [programming-patterns.md](references/programming-patterns.md) — Common logic patterns and variable assignments
