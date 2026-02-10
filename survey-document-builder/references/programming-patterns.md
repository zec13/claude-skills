# Survey Programming Patterns

## Table of Contents
1. Selection Types
2. Display Logic
3. Skip Logic
4. Piping and Variables
5. Randomization
6. Grid/Matrix Questions
7. Common Termination Patterns

---

## 1. Selection Types

### Single Select
```
*Please select one.*
```
Use when: Only one answer is valid (e.g., age range, primary brand)

### Multi-Select (Unlimited)
```
*Please select all that apply.*
```
Use when: Multiple answers are valid with no limit

### Multi-Select (Limited)
```
*Select up to 3.*
*Select your top 3.*
```
Use when: Want to force prioritization

### Ranking
```
*Please rank your top 5, where 1 = most important.*
```
Use when: Need ordered preferences

### Open-End
```
*Please type your response below.*
[Open-end, 500 character limit]
```
Use when: Qualitative input needed

---

## 2. Display Logic

### Show If
```
[SHOW IF Q3 = "Yes"]
[DISPLAY IF S2 includes "Brand X"]
```

### Show to Subset
```
[SHOW TO: Brand X users only]
[DISPLAY TO: Respondents who selected 3+ options in Q5]
```

### Conditional Text
```
You mentioned you use <brand> for your <pet type>.
[PIPE brand from Q4, pet type from S3]
```

---

## 3. Skip Logic

### Skip To
```
[IF "None of the above" SELECTED, SKIP TO Q15]
[IF Q7 < 3, SKIP TO SECTION 4]
```

### Skip Section
```
[IF NOT qualified for Brand section, SKIP Brand section entirely]
```

### Loop/Iterate
```
[ASK Q10-Q15 FOR EACH brand selected in Q9, max 3 brands]
[LOOP through top 3 selected categories]
```

---

## 4. Piping and Variables

### Variable Definition
```
ASSIGN <brand> = [first brand selected in Q4]
ASSIGN <category> = [qualified category from screener]
ASSIGN <retailer> = [primary retailer from Q12]
```

### Piping Syntax
```
You mentioned you typically purchase <brand> at <retailer>.
How satisfied are you with your experience buying <brand> there?
```

### Computed Variables
```
COMPUTE purchase_frequency_score = [Q5a * 0.5 + Q5b * 0.3 + Q5c * 0.2]
ASSIGN segment = [IF score > 7 THEN "High" ELSE IF score > 4 THEN "Medium" ELSE "Low"]
```

---

## 5. Randomization

### Randomize Options
```
Randomize.
[Randomize options 1-8]
```

### Anchor Specific Options
```
Randomize options 1-10.
Anchor: "None of the above"
Anchor: "Other (Please specify)"
```

### Do Not Randomize
```
Do not randomize. [Logical order required]
```

### Rotate Blocks
```
[Rotate order of Q10-Q12 and Q13-Q15 blocks]
```

### Randomize Scale Direction
```
[Randomize: 50% see scale left-to-right, 50% right-to-left]
```

---

## 6. Grid/Matrix Questions

### Standard Grid
```
*Please rate each of the following on a scale of 1-5.*
[GRID: Rows = brands from Q4, Columns = 1-5 scale]
[Randomize rows]
```

### Carousel/Loop
```
*For each brand you selected, please answer the following:*
[CAROUSEL: Loop through brands selected in Q4]
[Ask Q20a-Q20e for each brand]
```

### Dual-Column Grid
```
| Brand | Own | Purchased P12M |
[Two checkbox columns per row]
```

---

## 7. Common Termination Patterns

### Age Termination
```
TERMINATE if age < 18 or age > [max age]
TERMINATE MESSAGE: "Thank you for your interest. Unfortunately, you do not qualify for this study."
```

### Category Qualification
```
TERMINATE if none selected in S2 (category ownership)
TERMINATE if no qualified categories
```

### Sensitive Industry
```
TERMINATE if ANY selected:
- Market research
- Advertising/Marketing
- [Category-specific industry]
```

### Usage Frequency
```
TERMINATE if usage frequency = "Never" or "Less than once a month"
```

### Quota Full
```
TERMINATE if quota full for [segment]
TERMINATE MESSAGE: "Thank you for your interest. We have reached our target number of respondents in your category."
```

---

## 8. Special Programming Notes

### Mobile Optimization
```
[Mobile-friendly: max 10 options visible without scrolling]
[Use carousel on mobile for grid questions]
```

### Soft Launch Notes
```
[SOFT LAUNCH CHECK: Verify incidence at n=50]
[SOFT LAUNCH: Monitor for data quality issues]
```

### Quality Checks
```
[ATTENTION CHECK: Terminate if incorrect]
[SPEEDER CHECK: Flag if completion < 1/3 median LOI]
[STRAIGHTLINER CHECK: Flag if same response for all grid items]
```
