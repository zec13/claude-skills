# Example Patterns for Test Path Entries

These patterns show the EXACT format to use when writing test path entries. They are derived from real hand-written test plan documents. The format uses a **stacked bullet / sub-bullet structure**: question ID as a level 0 bullet, with instruction lines as level 1 sub-bullets stacked underneath.

**CRITICAL**: Do NOT use bold headers, tables, or descriptive names after question IDs. Question IDs should be bare (no colon). Match these patterns exactly.

**FORMAT**: In all examples below, `•` represents a level 0 bullet (List Paragraph, ilvl=0) and `○` represents a level 1 sub-bullet (List Paragraph, ilvl=1).

## Pattern 1: Simple Demographic Questions

```
• S1
  ○ Select any response 18-65

• S2
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure "Prefer not to answer" is anchored at the bottom and mutually exclusive
  ○ Select R1 – Male

• S3
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure "Prefer not to answer" is anchored at the bottom and mutually exclusive
  ○ Select R6 – Hispanic / Latino

• S4
  ○ Type any zip code
  ○ Ensure only can continue with valid zip code
```

## Pattern 1b: Combined Simple Questions

When consecutive questions share the same instruction (e.g., "Select any"), combine them into one entry:

```
• S2-S3
  ○ Select any

• D1-D3
  ○ Select any
```

## Pattern 2: Industry Screening (Immediate Termination)

```
• S5
  ○ Ensure "None of the above" is anchored at bottom and mutually exclusive
  ○ Select any other than R1-R4
```

## Pattern 3: Employment / Income (Conditional Termination)

```
• S5a
  ○ Select R3 – Student
  ○ Ensure assigned <student>
  ○ Ensure list is not randomized

• S6
  ○ Ensure "Prefer not to answer" is anchored at the bottom and mutually exclusive
  ○ Select R1 – Less than $25,000
  ○ Ensure list is not randomized
  ○ Ensure not terminated
```

## Pattern 4: Multi-Column Grid with Variable Assignment

```
• S7
  ○ Ensure "None of the above" is anchored at the bottom and mutually exclusive
  ○ Ensure multi-select in C1 and C2
  ○ Select R1 and R2 in C1
  ○ Select any in C2
  ○ Ensure assigned <styling> and <shampoo> as <segment>
```

## Pattern 5: Carousel / Looped Question

```
• S9
  ○ Ensure <segment> is piped through in carousel as <styling products> and <shampoo>
  ○ Select any R1-R2 for <styling products>
  ○ Select any R4-R7 for <shampoo>
  ○ Ensure response options are not randomized
  ○ Ensure <segment> is assigned <styling>
```

## Pattern 6: Channel / Retailer Selection

```
• S11
  ○ Ensure <segment> is piped through as <styling products>
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure "None of the above" is anchored at the bottom and mutually exclusive
  ○ Ensure multi-select in C1 and C2, single select in C3
  ○ Select R1 – grocery store in C1 and C2

• S12
  ○ Ensure <segment> is piped through as <styling products>
  ○ Ensure corresponding response list for <grocery> is shown
  ○ Ensure multi-select in C1 and C2, single select in C3
  ○ Select R6 – Kroger in C1 and C2
  ○ Ensure R4-R7 are kept together
  ○ Ensure <retailer> assigned <Kroger> and <channel> assigned as <grocery>
```

## Pattern 7: Brand Selection with Conditional Display

```
• S14
  ○ Ensure <segment> is piped through as <styling products>
  ○ Ensure <retailer> is piped through as <Kroger>
  ○ Ensure shown brand list for <styling>
  ○ Ensure multi-select in C1 and C2
  ○ Ensure you do not see R3 – "Not Your Mother's"
  ○ Ensure you do not see R15 – "Miss Jessie's"
  ○ Ensure you do not see R28 – "The Doux"
  ○ Ensure you DO see R10 "American Crew", R23 "Old Spice", and R26 "Axe"
  ○ Ensure R29 & R30 are anchored at the bottom
  ○ Select any in C1 including R26 – Axe
  ○ Select R26 in C2
  ○ Ensure assigned <price tier> assigned as <mid tier>
  ○ Ensure <brand> assigned as <Axe>
```

## Pattern 8: Form / Product Selection

```
• S15
  ○ Ensure <segment> is piped through as <styling products>
  ○ Ensure <brand> piped through as <Axe>
  ○ Ensure response list is shown for <styling>
  ○ Ensure responses are not randomized
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure multi-select
  ○ Select R2 – Mousse
  ○ Ensure <form> assigned <Mousse>
```

## Pattern 9: Scale / Attitude Questions

```
• S19
  ○ Ensure 5-point scale is shown
  ○ Ensure R6 is not shown
  ○ Ensure R7 is shown
  ○ Select 1 for R1 and R3
  ○ Select 4 for R2, R4, R5, and R7
  ○ Ensure assigned <LE consumer>
```

## Pattern 10: Messages

Simple intro message — include the FULL message text:
```
• M1
  ○ Ensure message reads: "We are conducting this survey to better understand how you shop for different types of products for your pets. We appreciate your honesty! Thank you in advance for your time."
```

Transition message with piped variable values filled in:
```
• M1
  ○ Ensure message reads: "Earlier you told us you recently bought Frontline topical at Banfield at a physical location. For the following questions, please think about that experience in particular."
```

Message with piping checks (when exact text is not critical but piped values matter):
```
• M3
  ○ Ensure message is shown
  ○ Ensure <brand> is piped through as <Axe>
  ○ Ensure <segment> is piped through as <styling products>
```

Message that should not appear:
```
• M2
  ○ Ensure you do not see message
```

## Pattern 11: Hidden / Skipped Questions

Use short, simple language:
```
• S21
  ○ Ensure not shown question

• S24
  ○ Should not see

• Q313
  ○ Ensure you do not see the question
```

## Pattern 12: Questions with Piped Question Text

When a variable is piped INTO the question wording, include the full expected question text so the tester can verify the piping:
```
• S14
  ○ Ensure question reads "What type of flea and tick protection products have you purchased for your pet(s) in the past year?"
  ○ Ensure there is only one column with the pet's name at the top
  ○ Select "Topical / Spot-on Treatments" and "Orals"

• S20
  ○ Ensure question reads: "In the past two years have you used a different brand of flea and tick protection for <pet name> other than Frontline?"
  ○ Ensure you DO see:
      Yes—Used a different brand of medicine that prevents Fleas and Ticks
      No
  ○ Ensure you do NOT see:
      Yes—Used a different brand of medicine that prevents Heartworm
      Yes—Used a different brand of Combination medicine that prevents fleas, ticks, and heartworms
  ○ Select "Yes—Used a different brand of medicine that prevents fleas and ticks"

• Q103
  ○ Ensure question reads "Did you do any research on flea and tick protection before the most recent trip you made to Banfield where you bought Frontline topical?"
  ○ Select R1 "Yes"
```

## Pattern 13: DO see / do NOT see Blocks (Conditional Response Visibility)

**This is a critical pattern.** When a question has response options that are conditionally shown or hidden based on path variables (channel, form, category, species, OTC/Rx, fulfillment method, etc.), use "Ensure you DO see" and "Ensure you do NOT see" blocks listing the actual response option text. These blocks tell the tester exactly which options should be visible for their path.

```
• Q109
  ○ Select "Just wanted to make sure my pet had the proper parasite protection"
  ○ Ensure you DO see:
      Was worried that my pet might have fleas / ticks (e.g., saw pet scratching)
      My pet had a flea or tick related incident (e.g., discovered fleas or ticks, or related signs on pet or at home)
      My home was infested with fleas
      Found a tick on myself / a family member
      Wanted to prevent a future flea or tick infestation in my home
      Needed it before leaving my pet with a pet sitting service (e.g., doggy daycare, overnight boarding, kennel, etc.)
  ○ Ensure you do NOT see:
      Was worried my pet had heartworms…
  ○ Ensure assigned <proactive>

• Q111
  ○ Ensure you DO see responses shown to everyone (e.g., Easy to browse, Large selection) and:
      Do not have to pay for shipping
      Can get product(s) right away
      Convenient location
      Going there anyway for pet services (e.g., grooming)
      The vet is my most trusted source
      Going there anyway for an appointment or checkup
  ○ Ensure you do NOT see:
      Easy to shop for other non-pet care items I need
      Can read product reviews
      Fast / Convenient shopping
      Subscription program
      Easy to re-order
      Don't have to leave my home
  ○ Select any
```

For simpler conditional visibility, a compact format is fine:
```
• Q202
  ○ Ensure you see R1-R3
  ○ Ensure you do not see R4
  ○ Ensure you see R12
  ○ Ensure you do not see R13-R14
  ○ Ensure R1 & R2 are together
  ○ Select any
```

## Pattern 14: Brand / Retailer Enumerated Lists

When a brand or retailer question shows different options depending on path variables, enumerate the full visible list so the tester knows exactly which brands/retailers should appear:
```
• S18
  ○ Ensure you only see the following brands:
      Activate II
      K9 Advantix II
      Advantage XD
      Advantage II
      Advecta
      Bravecto
      Cheristin
      First Act Plus
      Frontline
      Frontline Gold
      Frontline Plus
      Frontline Shield
      Hartz Ultra Gard
      Hartz Ultra Guard Pro
      Nextstar
      Pet Action
      Pet Armor
      Pet Armor Plus
      Vectra
      Vectra 3D
      Vet's Best
  ○ Select Frontline and any others for C1 and C2 and select Frontline for C3
  ○ Ensure assigned <OTC/Rx> is "OTC" and assigned <brand> is "Frontline"

• S21
  ○ Ensure you see all retailer options, including OTC-only options:
      Sam's Club
      BJ's
      Pet Supermarket
      Amazon
      Target
      Kmart
      Meijer
      Menards
      A drug store
      A grocery store (e.g., Kroger, Publix, Albertsons, Stop and Shop, etc.)
      A home improvement / outdoor supply store (e.g., Home Depot, Lowes, etc.)
  ○ Select Banfield
```

## Pattern 15: Multi-Select with Grouping Rules

```
• Q104
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure multi-select in C1, select up to 3 in C2
  ○ Ensure R1-R4 kept together
  ○ Ensure R12 & R13 kept together
  ○ Ensure R15 & R16 kept together
  ○ Select any
```

## Pattern 16: Occasion / Trigger Questions

```
• Q201
  ○ Ensure <brand> piped through as <Axe>
  ○ Ensure <segment> piped through as <styling products>
  ○ Ensure "Other, please specify" is anchored at the bottom
  ○ Ensure responses are randomized
  ○ Ensure multi-select
  ○ Select R8 – "Getting ready while traveling / on vacation"
  ○ Ensure <qualifying occasion> assigned <getting ready while traveling / on vacation>
```

## Pattern 17: Fulfillment Method

```
• S13
  ○ Ensure <retailer> is piped through as <Kroger>
  ○ Ensure <segment> is piped through as <styling products>
  ○ Ensure responses are not randomized
  ○ Ensure multi-select in C1, single select in C2
  ○ Select R1 in C1 and C2
  ○ Ensure <fulfillment method> is assigned <in-store>
```

## Pattern 18: Selection Using Quoted Text

When the selection matters for variable assignment or path routing, use the actual text in quotes rather than just an R# code:
```
• S12
  ○ Ensure you see it
  ○ Select R1 "Medicine that protects against Fleas and Ticks" and R2 "Medicine that prevents Heartworm"
  ○ Do not select any other qualifying categories (R3 "Combination medicine…")

• Q307
  ○ Select "Safest for my <pet name> (e.g., minimal/no side effects)"

• Q403
  ○ Select "3 = Satisfied"
  ○ Ensure hidden variable <satisfaction> = <satisfied>
```

## Pattern 19: Pet / Category Count Selection

```
• S9
  ○ Select 1 dog
  ○ Select 0 cats

• S10
  ○ Ensure you only see one row with two dropdown columns and one open space
  ○ Choose any option for C1 and C2 and select any name for C3

• S11
  ○ Ensure there is only one column for Dogs
  ○ Select "No…"
  ○ Ensure assigned to <New Dog Owner>
```

## Pattern 16: Screener Termination Check Entries

The screener termination checks section uses the bullet / sub-bullet format with **ALL TEXT IN BOLD**. When listing specific response options that trigger termination, use level 2 sub-bullets. This section is distinct from test path content because it uses bold text:

```
• S1                                                              [bold, level 0]
  ○ Terminate if respondent does not select between 21-74         [bold, level 1]

• S4                                                              [bold, level 0]
  ○ Terminate if respondent selects any of the following (R1-R6): [bold, level 1]
    ▪ An advertising agency…                                      [bold, level 2]
    ▪ A television or radio station…                              [bold, level 2]
    ▪ A marketing or market research firm…                        [bold, level 2]
    ▪ A manufacturer or distributor of pet food…                  [bold, level 2]
    ▪ A vet, pet breeder, or pet groomer                          [bold, level 2]
    ▪ A retailer…                                                 [bold, level 2]

• S7                                                              [bold, level 0]
  ○ Terminate if income <$30k (R1) and non-student                [bold, level 1]
  ○ Terminate if income <$30k (R1) and <multi-HH>                 [bold, level 1]
  ○ Terminate if income $30,000 to $49,000 (R2) and <multi-HH>   [bold, level 1]

• S9                                                              [bold, level 0]
  ○ Terminate if respondent selects 0 for both Dog and Cat        [bold, level 1]
  ○ Terminate if respondent selects 5+ for Dog or Cat             [bold, level 1]
  ○ Terminate if sum of Cats and Dogs is >= 5                     [bold, level 1]
```

## Pattern 20: Brand/Retailer Enumeration Lists (THREE LEVELS)

When a brand or retailer question shows different options depending on path variables, enumerate the full visible list using **level 2 sub-bullets** under the "Ensure you only see" instruction:

```
• S18                                                             [level 0]
  ○ Ensure you only see the following brands:                     [level 1]
    ▪ Activate II                                                 [level 2]
    ▪ K9 Advantix II                                              [level 2]
    ▪ Advantage XD                                                [level 2]
    ▪ Frontline                                                   [level 2]
    ▪ Frontline Gold                                              [level 2]
    ▪ Frontline Plus                                              [level 2]
    ▪ Frontline Shield                                            [level 2]
    ▪ Hartz Ultra Gard                                            [level 2]
    ▪ Hartz Ultra Guard Pro                                       [level 2]
    ▪ Vectra                                                      [level 2]
    ▪ Vectra 3D                                                   [level 2]
    ▪ Vet's Best                                                  [level 2]
  ○ Select Frontline and any others for C1 and C2...              [level 1]
  ○ Ensure assigned <OTC/Rx> is "OTC" and assigned <brand>...     [level 1]
```

Similarly for DO see / do NOT see blocks:
```
• Q109                                                            [level 0]
  ○ Select "Just wanted to make sure my pet had the proper..."    [level 1]
  ○ Ensure you DO see:                                            [level 1]
    ▪ Was worried that my pet might have fleas / ticks            [level 2]
    ▪ My pet had a flea or tick related incident                  [level 2]
    ▪ My home was infested with fleas                             [level 2]
    ▪ Found a tick on myself / a family member                    [level 2]
  ○ Ensure you do NOT see:                                        [level 1]
    ▪ Was worried my pet had heartworms...                        [level 2]
  ○ Ensure assigned <proactive>                                   [level 1]
```

## Anti-Patterns — DO NOT Use These Formats

**BAD — Bold headers with topic names:**
```
**S2 – Age**
- Select [age value, e.g., "32"] from dropdown
- Ensure dropdown displays ages from 1-100
```

**GOOD — Bare ID as level 0 bullet, instructions as level 1 sub-bullets:**
```
• S2
  ○ Select any response 18-65
```

**BAD — Question ID on Normal line, instructions on Normal lines (flat format):**
```
S2
Select any response 18-65
Ensure assigned to proper age group
```

**GOOD — Stacked bullet / sub-bullet format:**
```
• S2
  ○ Select any response 18-65
  ○ Ensure assigned to proper age group
```

**BAD — Question ID on Normal line with instructions as flat bullets:**
```
S2
• Select any response 18-65
• Ensure assigned to proper age group
```

**GOOD — Question ID IS the parent bullet, instructions are sub-bullets:**
```
• S2
  ○ Select any response 18-65
  ○ Ensure assigned to proper age group
```

**BAD — Adding explanatory parentheses that explain WHY something is visible:**
```
  ○ Select R5 'Meijer' (visible since <Channel>='Grocery')
  ○ Ensure R1 'Cranberry' and R2 'Cranberry blends (e.g., Cranberry-Apple)' are kept together
```

**GOOD — Clean notation. Use R# with brief text after a dash when the selection is specific; use plain R# for grouping checks:**
```
  ○ Select R5 – Meijer
  ○ Ensure R1 & R2 are together
```

**BAD — Generic/vague sub-bullets that don't tell the tester what to look for:**
```
  ○ Verify piped options match selections
  ○ Select appropriate response for this path
  ○ Check conditional display rules
```

**GOOD — Specific sub-bullets with actual values and text:**
```
  ○ Ensure "Ocean Spray cranberry" is piped through
  ○ Select "Topical / Spot-on Treatments"
  ○ Ensure you DO see R4 "For a scheduled vet appointment"
```

**BAD — Using "Verify" instead of "Ensure":**
```
  ○ Verify <brand> assigned correctly
  ○ Verify question text pipes properly
```

**GOOD — Always use "Ensure":**
```
  ○ Ensure <brand> assigned as <Frontline>
  ○ Ensure question reads "Did you do any research on flea and tick protection..."
```

**BAD — Table-based test path format:**
```
| Q# | Topic | Test Instructions |
| S1 | Age   | Select 32...      |
```

**GOOD — Bullet / sub-bullet format:**
```
• S1
  ○ Select any response 18-65
```

**BAD — "Derived Variables" section at start of test path:**
```
Test Path 1

Derived Variables:
<species> = dog
<brand> = Frontline
<channel> = vet
...

M1
• Ensure welcome message appears
```

**GOOD — Jump straight into questions after heading and section sub-heading:**
```
Path 1           ← Heading 2 (NOT "Test Path 1")

### Screener     ← Heading 3

• M1             ← Level 0 bullet (first question immediately)
  ○ Ensure message reads: "We are conducting this survey..."
• S1
  ○ Select any age 21-74
```

**BAD — "Test Path [N]" heading:**
```
Test Path 1
```

**GOOD — "Path [N]" heading:**
```
Path 1
```

**BAD — Topic names or colons after question IDs:**
```
• S1: Age
  ○ Select any age 21-74
• S4: Occupation/Industry
  ○ Select any non-sensitive industry
```

**GOOD — Bare question IDs, no colons, no topic names:**
```
• S1
  ○ Select any age 21-74
• S4
  ○ Select any R7-R13
```

**BAD — Flat brand list at level 1 (same indentation as instructions):**
```
• S18
  ○ Ensure you only see the following brands:
  ○ Activate II
  ○ K9 Advantix II
  ○ Frontline
```

**GOOD — Brand list at level 2 (deeper indentation under instruction):**
```
• S18
  ○ Ensure you only see the following brands:
    ▪ Activate II
    ▪ K9 Advantix II
    ▪ Frontline
```

**BAD — General Checks using bullet characters:**
```
• Ensure that instructions and question types are easy to understand
• Test that single selects, multi selects...
```

**GOOD — General Checks using NUMBERED list:**
```
1. Ensure that instructions and question types are easy to understand
2. Test that single selects, multi selects...
```
