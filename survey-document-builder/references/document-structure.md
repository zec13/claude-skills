# Survey Document Structure

## Table of Contents
1. Document Header
2. Survey Overview Section
3. Section Structure
4. Question Table Format
5. Screen Markers and Headers

---

## 1. Document Header

### Standard Elements
- Client logo (left)
- Consulting firm logo (right)
- Project title (centered, bold)
- Subtitle: "Quant Survey Document"
- Date/version

### Example Header Format
```
[Client Logo]                                    [Firm Logo]

            **Client Name Project Title**
               Quant Survey Document
                   Month Year
```

---

## 2. Survey Overview Section

### Required Components

**Objectives** (bullet list)
- Map the [target] journey across [behaviors], identifying [key variables]
- Understand how [factor] impacts [outcome]
- Quantify opportunity spaces within [channels/segments]
- Understand differences among [subgroups]

**Quotas** (structured list)
- Total N
- Market/Geography
- Demographics (age, gender, income)
- Category-specific quotas (brand users, segments, etc.)
- Min/max specifications for key groups

**Survey Structure** (numbered list describing each section)
1. **Screener**: Ensure qualified respondents, capture key screening variables
2. **Section Name**: Section objective description
3. **Section Name**: Section objective description
...
N. **Demographics**: Capture respondent information for profiling

---

## 3. Section Structure

### Section Header Format
Each section begins with:
- Section title row (full-width, bold, shaded)
- Section objectives (bullet list in first table row)

### Standard Sections

**Screener**
- Qualification questions
- Termination logic
- Quota assignment
- Hidden variable definitions

**Main Body Sections** (vary by project type)
Examples:
- Plan / Shop / Buy / Use (Path to Purchase)
- Consumer / Category / Competition / Channels / Customer (5 Cs)
- Awareness / Consideration / Trial / Usage (Funnel)
- Segmentation / Jobs / Drivers (Segmentation studies)

**Switching / Future Behavior** (often included)
- Past switching behavior
- Future intent
- Triggers and barriers

**Demographics**
- Standard demos (age, gender, income, education, geography)
- Category-specific demos (household composition, pet ownership, etc.)

---

## 4. Question Table Format

### 3-Column Layout

| Column | Width | Content |
|--------|-------|---------|
| Q# | ~10% | Question number (e.g., "S1", "Q201") or "Message" |
| Question | ~60% | Full question text, response options, programming instructions |
| Notes | ~30% | Objective/rationale OR display logic |

### Question Cell Content Order
1. Topic header (blue bar, bold white text) — optional, at start of topic block
2. Question text (bold)
3. Instruction text (italic): "*Please select one.*"
4. Response options (bulleted or numbered list)
5. Programming notes (italic, often in brackets or parentheses)

### Response List Formatting

**Text-only options:**
```
- Option A
- Option B
- Option C
- Other (Please specify) [Anchor, Open-end]
- None of the above [Anchor, Mutually Exclusive]
```

**Options with images:**
```
| [Brand Logo] | Brand Name |
| [Brand Logo] | Brand Name |
| [Brand Logo] | Brand Name |
```

---

## 5. Screen Markers and Headers

### NEW SCREEN Marker
Insert between questions that should appear on separate screens:

```
| NEW SCREEN |  |  |
```

### Topic Header Bar
Blue shaded row with white bold text, spans question column:

```
| Q# | **TOPIC: Purchase Behavior** (blue background, white text) | Notes |
```

### Message Rows
For instruction screens or section intros:

```
| Message | Thank you for your responses so far! We are now going to ask about your shopping behavior. | |
```

---

## 6. Variable Assignment Patterns

### Piped Variables
Define in notes column or hidden variable section:

```
ASSIGN <brand> = [response from Q3]
ASSIGN <category> = [first qualified category from S2]
```

### Quota Tracking
Include in screener section:

```
QUOTA: Brand X users (min 200)
QUOTA: Gen Z 18-25 (min 300 per country)
QUOTA: New customers P6M (min 150)
```

### Termination Logic
Specify clearly in notes:

```
TERMINATE if none selected
TERMINATE if age < 18 or age > 65
TERMINATE if works in [sensitive industry]
```
