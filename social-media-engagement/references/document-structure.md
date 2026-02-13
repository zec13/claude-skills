# Document Structure Guide

This document specifies the exact formatting and structure for the test path .docx output. The output must be visually indistinguishable from the hand-written reference examples (BIAH, Henkel, Ocean Spray, Unreal). Any deviation from this format is a failure.

## CRITICAL FORMAT RULES — READ FIRST

**DO NOT** use any of the following in the output document:
- Tables for individual test path content (test paths use paragraph + bullet format ONLY)
- Color formatting (no blue headers, no shading, no colored text, no alternating row colors)
- Title pages or cover pages
- Table of Contents
- Logos or images in the header/footer
- Page breaks between test paths (content flows continuously)
- Topic names or descriptions after question IDs (just the bare ID — "S1" NOT "S1: Age" or "S1 – Age")
- Colons after question IDs (use "S1" NOT "S1:")
- **"Derived Variables" sections** — NEVER add a variable summary or "Derived Variables" block at the start of each path
- "Path Profile" or similar summary lines
- Variable summary tables at the start of each test path
- Custom heading styles or fancy formatting
- "Test Path [N]" headings — use "Path [N]" only

The document should look like a **simple, clean Word document** with headings, numbered lists, bullets, and one table. Nothing more.

## Overall Document Structure

```
1. Title + Date (2 lines at top)
2. "Assignments:" (optional, if tester assignments provided)
3. General Checks (all) — Section (NUMBERED LIST)
4. Screener Termination Checks — Section (BOLD BULLETS)
5. Test Paths Table — Section (overview matrix as a proper Word table)
6. Path 1 — Section
7. Path 2 — Section
... (one section per path)
```

## Title Block

Two simple lines at the very top of the document. No special formatting beyond the heading style.

**Line 1** (Heading 1 style): "[Project Name] Survey Test Plan"
**Line 2** (Normal style): "Month Year"

Examples from real documents:
- "BIAH Survey Test Plan" + "September 2023"
- "Henkel Hair Care Insights Survey Test Plan" + "December 2025"
- "Ocean Spray SSJ Category Vision Quant Survey" + "July 2025"
- "Unreal Category Expansion Survey Test Plan" + "October 2025"

That's it. No subtitle, no version number, no logos, no table of contents.

## Section: Assignments (Optional)

If tester/builder assignments are provided, add a simple "Assignments:" heading (Heading 1 style) after the date line. This is where tester name assignments go. Keep it brief — just names and path assignments.

## Section: General Checks (all)

### Heading
Heading 1 style: "General Checks (all)"

### Content — NUMBERED LIST FORMAT
A standardized **numbered list** (1., 2., 3., ... 12.) using Word's numbered list formatting. This boilerplate is nearly identical across all projects. Use the EXACT wording from `references/general-checks-template.md`.

**CRITICAL**: Use **numbered bullets** (1., 2., 3., ...), NOT bullet characters (•). The General Checks section is the ONLY section that uses numbered bullets — all other sections use standard bullet characters.

Item 11 ("Put yourself in respondent's shoes") has sub-items using **lettered sub-bullets** (a., b., c., d.) indented one level deeper than the main numbered items.

### docx-js Implementation
```javascript
// General Checks use a SEPARATE numbered list config
numbering: {
  config: [
    {
      reference: "general-checks",
      levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.LOWER_LETTER, text: "%2.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
      ]
    },
    // ... other numbering configs for bullets
  ]
}

// Then for each general check item:
new Paragraph({
  numbering: { reference: "general-checks", level: 0 },
  children: [new TextRun("Ensure that instructions and question types are easy to understand and intuitive to use")]
})

// And for sub-items under item 11:
new Paragraph({
  numbering: { reference: "general-checks", level: 1 },
  children: [new TextRun("Overall, do question formats clearly reflect how to answer the questions?")]
})
```

## Section: Screener Termination Checks

### Heading
Heading 1 style: "Screener Termination Checks"

### Content Structure

**Opening paragraph(s)** (Normal style):
1-2 paragraphs of general instructions. Use this standard wording:

"For all termination checks – ensure all respondents see the disqualification message and are terminated at the end of the screener (skipping questions that do not make sense for them to see in programming notes)."

**BOLD PARAGRAPH** (Normal style, bold):
"Make sure that when testing these termination points, you only answer the specified question 'wrong' and all other responses in a qualifying way, in order to isolate termination to the specified question. For example, in the age termination, make sure to answer all other questions in the screener in such a way that would qualify a respondent, so you are sure age and not some other response created the termination."

**CRITICAL — ALL SCREENER TERMINATION CONTENT IS BOLD**: Unlike test path content (which is NOT bold), the screener termination bullets are ALL rendered in **bold text**. This includes:
- Question IDs (level 0 bullets): **S1**, **S4**, etc.
- Termination conditions (level 1 sub-bullets): **Terminate if respondent does not select between 21-74**
- Enumerated items (level 2 sub-bullets): **An advertising agency...**, **A retailer...**, etc.

**Then list each termination point using the BOLD bullet / sub-bullet format:**

Each termination entry uses the same stacked bullet structure as test path questions, but with ALL TEXT BOLD:
- **Question ID** as a level 0 bullet (ilvl=0): the bare question ID in bold, e.g., **S1**
- **Termination conditions** as level 1 sub-bullets (ilvl=1) stacked underneath in bold: one per condition
- **Enumerated items** as level 2 sub-bullets (ilvl=2) when listing specific response options that cause termination

Example (rendered format — all text is bold):
```
• S1
  ○ Terminate if respondent does not select between 21-74

• S4
  ○ Terminate if respondent selects any of the following (R1-R6):
    ▪ An advertising agency…
    ▪ A television or radio station…
    ▪ A marketing or market research firm…
    ▪ A manufacturer or distributor of pet food…
    ▪ A vet, pet breeder, or pet groomer
    ▪ A retailer…

• S7
  ○ Terminate if income <$30k (R1) and non-student (did not select R3 in S6)
  ○ Terminate if income <$30k (R1) and respondent is <multi-HH> (selected R2 or R3 in S5)
  ○ Terminate if income $30,000 to $49,000 (R2) and respondent is <multi-HH> (selected R2 or R3 in S5)

• S9
  ○ Terminate if respondent selects 0 for both Dog (R1) and Cat (R2)
  ○ Terminate if respondent selects 5 or more for Dog (R1) or Cat (R2)
  ○ Terminate if sum of Cats and Dogs (R1+R2) is greater than or equal to 5
```

**Be 100% inclusive** — list EVERY specific termination condition on its own sub-bullet. For questions where specific response options trigger termination, list each disqualifying response on its own line (as the S4 example shows with level 2 sub-bullets). Do NOT summarize multiple conditions into a single line.

### docx-js Implementation for Bold Screener Termination
```javascript
// Helper for bold bullet content in screener termination section
function addBoldBullet(level, text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: level },
    children: [new TextRun({ text: text, bold: true })]
  });
}

// Usage:
addBoldBullet(0, "S1"),
addBoldBullet(1, "Terminate if respondent does not select between 21-74"),
addBoldBullet(0, "S4"),
addBoldBullet(1, "Terminate if respondent selects any of the following (R1-R6):"),
addBoldBullet(2, "An advertising agency…"),
addBoldBullet(2, "A television or radio station…"),
// etc.
```

## Section: Test Paths Table

### Heading
Heading 1 style: "Test Paths Table"

### Content
A **proper Word table** reproducing the test matrix. The table MUST render as a visible grid with all content visible inside cells. Format:
- First column headers: "Question" and "Q#"
- Remaining columns: One per test path (labeled 1, 2, 3, 4, 5, 6, etc.)
- Each row: Variable name in first column, question reference in second column, values for each path
- Optional rows for "Builder", "Round 1 Tester", "Round 2 Tester" (assignment info)

Table formatting:
- Simple borders (thin black lines) — ALL borders must be visible
- Bold text in header cells (first row and first two columns)
- NO color fills, NO shading, NO alternating row colors
- Small font size is fine (8-9pt) to fit content
- All cell content MUST be visible — if text is long, allow word wrap (do NOT truncate)

### docx-js Implementation for Test Paths Table
```javascript
const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };

// Calculate column widths to fit all paths
// First two cols (Question + Q#) get more width, path columns split the rest
const contentWidth = 9360; // US Letter with 1" margins
const labelColWidth = 1600;
const qNumColWidth = 800;
const pathColWidth = Math.floor((contentWidth - labelColWidth - qNumColWidth) / numPaths);

new Table({
  width: { size: contentWidth, type: WidthType.DXA },
  columnWidths: [labelColWidth, qNumColWidth, ...Array(numPaths).fill(pathColWidth)],
  rows: [
    // Header row
    new TableRow({
      children: [
        makeCell("Question", labelColWidth, true),
        makeCell("Q#", qNumColWidth, true),
        ...pathNumbers.map(n => makeCell(String(n), pathColWidth, true))
      ]
    }),
    // Data rows
    ...matrixRows.map(row => new TableRow({
      children: [
        makeCell(row.label, labelColWidth, true),
        makeCell(row.qNum, qNumColWidth, true),
        ...row.values.map(v => makeCell(v, pathColWidth, false))
      ]
    }))
  ]
});

function makeCell(text, width, bold) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    margins: { top: 40, bottom: 40, left: 60, right: 60 },
    children: [new Paragraph({
      children: [new TextRun({ text, bold, size: 16 })] // 8pt font
    })]
  });
}
```

## Section: Individual Test Paths

### Path Heading
Heading 2 style: "Path [N]"

**CRITICAL**: Use "Path 1", "Path 2", etc. — NOT "Test Path 1" or "Test Path 1:". No description after the number. Just "Path 1". No variable summary table. No "Path Profile" line. **No "Derived Variables" section.**

### Survey Section Sub-Headings (REQUIRED)

Within each path, use **Heading 3** to mark each major survey section. This provides essential navigation within long test paths. The sub-headings should match the survey document's section structure. Common section names:

- Screener
- Plan
- Shop
- Buy
- Use
- Switching Behavior
- Future Behavior
- Demos & Psychographics

These section names may vary by project (e.g., "Awareness & Usage", "Category Assessment", "Brand Perceptions"). Use the section names from the survey document.

### Question-by-Question Content — BULLET / SUB-BULLET FORMAT

This is the core of each test path. Every question uses a **stacked bullet / sub-bullet structure** with up to THREE levels of depth:

- **Level 0 bullet** (ilvl=0): Question ID — "S1", "Q301", "D1". No colon, no topic name.
- **Level 1 sub-bullet** (ilvl=1): Instructions — "Ensure...", "Select...", "Ensure you only see the following brands:"
- **Level 2 sub-bullet** (ilvl=2): Enumerated list items — brand names, retailer names, DO see / do NOT see lists when they need their own indented block under a level 1 bullet

This creates a clear visual hierarchy:
```
• S18                                          ← Level 0 (question ID)
  ○ Ensure you only see the following brands:  ← Level 1 (instruction)
    ▪ Activate II                              ← Level 2 (list item)
    ▪ K9 Advantix II                           ← Level 2 (list item)
    ▪ Frontline                                ← Level 2 (list item)
    ▪ Frontline Gold                           ← Level 2 (list item)
  ○ Select Frontline and any others for C1     ← Level 1 (instruction)
  ○ Ensure assigned <OTC/Rx> is "OTC"          ← Level 1 (instruction)
```

**CRITICAL — Three levels of indentation**: Brand/retailer enumeration lists, DO see / do NOT see response blocks, and any other enumerated list under an instruction sub-bullet use **level 2 (ilvl=2)** bullets. This provides clear visual separation between instruction text and list items.

**For questions where multiple items share the same instruction**, you may combine them:
```
• S2-S3
  ○ Select any

• D1-D4
  ○ Select any
```

#### Format for regular questions:
```
• S2
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure "Prefer not to answer" is anchored at the bottom and mutually exclusive
  ○ Select R1 – Male
```

#### Format for messages:
Messages follow the same bullet / sub-bullet structure:

Simple message:
```
• M1
  ○ Ensure message reads: "We are conducting this survey..."
```

Message with piping:
```
• M3
  ○ Ensure message is shown
  ○ Ensure <brand> is piped through as <Axe>
  ○ Ensure <segment> is piped through as <styling products>
```

#### Format for hidden questions:
```
• S21
  ○ Should not see
```
Or:
```
• S24
  ○ Ensure you do not see
```

#### Format for questions with brand/retailer enumeration (THREE LEVELS):
```
• S18
  ○ Ensure you only see the following brands:
    ▪ Activate II
    ▪ K9 Advantix II
    ▪ Advantage XD
    ▪ Frontline
    ▪ Frontline Gold
    ▪ Frontline Plus
    ▪ Frontline Shield
    ▪ Hartz Ultra Gard
  ○ Select Frontline and any others for C1 and C2 and select Frontline for C3
  ○ Ensure assigned <OTC/Rx> is "OTC" and assigned <brand> is "Frontline"
```

#### Format for DO see / do NOT see blocks (THREE LEVELS):
```
• Q109
  ○ Select "Just wanted to make sure my pet had the proper parasite protection"
  ○ Ensure you DO see:
    ▪ Was worried that my pet might have fleas / ticks (e.g., saw pet scratching)
    ▪ My pet had a flea or tick related incident
    ▪ My home was infested with fleas
    ▪ Found a tick on myself / a family member
  ○ Ensure you do NOT see:
    ▪ Was worried my pet had heartworms...
  ○ Ensure assigned <proactive>
```

#### Format for questions with many checks:
```
• S14
  ○ Ensure <segment> is piped through as <styling products>
  ○ Ensure <retailer> is piped through as <Kroger>
  ○ Ensure shown brand list for <styling>
  ○ Ensure multi-select in C1 and C2
  ○ Ensure you do not see R3 – "Not Your Mother's"
  ○ Ensure you do not see R15 – "Miss Jessie's"
  ○ Ensure R29 & R30 are anchored at the bottom
  ○ Select any in C1 including R26 – Axe
  ○ Select R26 in C2
  ○ Ensure assigned <price tier> assigned as <mid tier>
  ○ Ensure <brand> assigned as <Axe>
```

### Key Style Rules for Test Path Content

1. **Question IDs are level 0 bullets** — "S1" or "Q301" as a bullet with ilvl=0. No colon, no topic names like "S1: Age" or "Q301 – High-level Needs".

2. **Instructions are level 1 sub-bullets** — each instruction is a bullet with ilvl=1, stacked underneath the parent question ID bullet.

3. **Enumerated lists are level 2 sub-bullets** — brand names, retailer names, DO see / do NOT see response option lists use ilvl=2, nested under the level 1 instruction that introduces them.

4. **No bold formatting in test path content** — test path question IDs, instructions, and list items are all regular (non-bold) text. Bold is ONLY used in the Screener Termination Checks section.

5. **Brief R# descriptions are OK** — "Select R1 – Male" or "Select R26 – Axe" is fine. But don't include verbose explanations like "Select R5 'Meijer' (visible since <Channel>='Grocery')".

6. **Content flows continuously** — no page breaks between questions or between test paths.

7. **Each test path covers EVERY question in the survey** — either with selection/ensure sub-bullets, or "Should not see" / "Ensure you do not see" for hidden questions.

8. **Combine simple questions** — When consecutive questions share the same instruction (e.g., "Select any"), combine them: "S2-S3" as one level 0 bullet with "Select any" as one sub-bullet.

9. **Be 100% completely inclusive** — include EVERY ensure check, EVERY selection instruction, EVERY piping verification, EVERY visibility check, and EVERY variable assignment. Do NOT summarize multiple checks into one line. Each discrete check gets its own sub-bullet. If a question has 10+ sub-bullets, that is fine — thoroughness is more important than brevity.

## docx-js Generation Specifications

When generating the .docx file using the Node.js `docx` package (`npm install docx`):

- **Page size**: US Letter (8.5" x 11") — width: 12240, height: 15840 DXA
- **Margins**: 1 inch on all sides (1440 DXA)
- **Body font**: Calibri or Arial, 11pt (size: 22 in half-points)
- **Heading 1**: Document title AND top-level section headings (General Checks, Screener Termination Checks, Test Paths Table)
- **Heading 2**: Individual path headings (Path 1, Path 2, etc.)
- **Heading 3**: Survey section sub-headings within each path (Screener, Plan, Shop, Buy, etc.)
- **Normal**: Intro paragraphs, date line, and any non-bulleted text
- **Numbered list (level 0)**: General Checks main items (1., 2., 3., ... 12.)
- **Numbered list (level 1)**: General Checks sub-items (a., b., c., d.) under item 11
- **Bullet list (level 0)**: Screener termination question IDs AND test path question IDs
- **Bullet list (level 1)**: Screener termination conditions AND test path instructions (select/ensure)
- **Bullet list (level 2)**: Brand/retailer enumeration lists AND DO see / do NOT see response lists

### CRITICAL — Numbering Configuration

The document needs TWO separate numbering configurations:

1. **"general-checks"**: Decimal numbers at level 0 (1., 2., 3...) and lowercase letters at level 1 (a., b., c...)
2. **"bullets"**: Standard bullets at level 0 (•), open circles at level 1 (○), and small squares/dashes at level 2 (▪)

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, LevelFormat, BorderStyle, WidthType } = require('docx');

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "general-checks",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          },
          {
            level: 1,
            format: LevelFormat.LOWER_LETTER,
            text: "%2.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } }
          }
        ]
      },
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          },
          {
            level: 1,
            format: LevelFormat.BULLET,
            text: "\u25CB",  // ○ open circle
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } }
          },
          {
            level: 2,
            format: LevelFormat.BULLET,
            text: "\u2013",  // – dash
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 2160, hanging: 360 } } }
          }
        ]
      }
    ]
  },
  sections: [{ children: [/* all content */] }]
});
```

### Helper Functions

```javascript
// General Checks numbered items
function numberedItem(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "general-checks", level },
    children: [new TextRun(text)]
  });
}

// Standard bullet (for test path question IDs, termination question IDs)
function bullet(text, level = 0, bold = false) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    children: [new TextRun({ text, bold })]
  });
}

// Heading helpers
function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] });
}
function normal(text, bold = false) {
  return new Paragraph({ children: [new TextRun({ text, bold })] });
}
```

### Example Document Assembly

```javascript
const children = [
  // Title
  h1("BIAH Survey Test Plan"),
  normal("September 2023"),

  // General Checks
  h1("General Checks (all)"),
  numberedItem("Ensure that instructions and question types are easy to understand and intuitive to use"),
  numberedItem("Test that single selects, multi selects, and \"select up to specified number\" questions are working properly"),
  // ... items 3-10 ...
  numberedItem("Put yourself in respondent's shoes and think about:"),
  numberedItem("Overall, do question formats clearly reflect how to answer the questions?", 1),
  numberedItem("Is it difficult to scroll through all answer options for any of the questions?", 1),
  numberedItem("Is a particular question frustrating to answer? Why?", 1),
  numberedItem("Is survey easy to take and intuitive to use?", 1),
  numberedItem("Make sure that all pictures/logos are shown in an easy to see way"),

  // Screener Termination Checks
  h1("Screener Termination Checks"),
  normal("For all termination checks – ensure all respondents see the disqualification message..."),
  normal("Make sure that when testing these termination points, you only answer the specified question 'wrong'...", true),
  bullet("S1", 0, true),                    // Bold level 0
  bullet("Terminate if respondent does not select between 21-74", 1, true),  // Bold level 1
  bullet("S4", 0, true),
  bullet("Terminate if respondent selects any of the following (R1-R6):", 1, true),
  bullet("An advertising agency…", 2, true),    // Bold level 2
  bullet("A retailer…", 2, true),

  // Test Paths Table
  h1("Test Paths Table"),
  // ... table ...

  // Path 1
  h2("Path 1"),
  h3("Screener"),
  bullet("M1", 0),                           // NOT bold (test path content)
  bullet('Ensure message reads: "We are conducting this survey..."', 1),
  bullet("S1", 0),
  bullet("Select any age 21-74", 1),
  // ...
  bullet("S18", 0),
  bullet("Ensure you only see the following brands:", 1),
  bullet("Activate II", 2),                   // Level 2 for brand list
  bullet("K9 Advantix II", 2),
  bullet("Frontline", 2),
  bullet("Select Frontline and any others for C1 and C2", 1),
  bullet('Ensure assigned <OTC/Rx> is "OTC" and assigned <brand> is "Frontline"', 1),
];
```

**DO NOT use any of these in the generated document:**
- Custom styles beyond the standard heading/list styles
- Colored shading (RGBColor, cell fills, etc.) except in table borders
- Table-based layouts for test path content
- Headers/footers with logos
- Page breaks between paths
- Unicode bullet characters in TextRun content (always use numbering config)
- "Derived Variables" blocks
- Topic names after question IDs

The document should be creatable with basic docx-js: add headings, add paragraphs, add numbered/bullet lists, add one table (for the test matrix). That's it.
