# Angle Extraction Framework

## The Core Elements

For each ad, extract these six elements:

| Element | Definition | Question to Ask |
|---------|------------|-----------------|
| **Angle** | Persuasion lens / testable hypothesis | What's the core belief this ad wants me to adopt? |
| **Hook** | First 1-3 seconds that earns attention | What stops the scroll? |
| **Promise** | What the customer gets | What transformation/benefit is offered? |
| **Pain** | Problem being addressed | What frustration/desire does this tap into? |
| **Proof** | Evidence shown | Why should I believe this works? |
| **Offer** | CTA / discount / bundle | What's the deal? |
| **Objection** | Concern being addressed (optional) | What doubt does this overcome? |

---

## Angle Types by Category

### Functional Angles
Focus on what the product *does*:
- Solves a specific problem
- Saves time/money/effort
- Outperforms alternatives

### Emotional Angles
Focus on how the product makes you *feel*:
- Stress relief / relaxation
- Confidence / pride
- Connection / bonding

### Identity Angles
Focus on who you *become*:
- Creative person
- Good parent
- Mindful adult

### Social Angles
Focus on how others *perceive* you:
- Impressive gift-giver
- Aesthetic home owner
- Eco-conscious consumer

---

## Hook Patterns

### Question Hooks
"Tired of [pain point]?"
"What if you could [promise]?"
"Did you know [surprising fact]?"

### Statement Hooks
"This changed everything about my [routine]"
"I never thought I'd [unexpected benefit]"
"[Authority figure] recommends this"

### Visual Hooks
- Satisfying process (ASMR, transformation)
- Before/after contrast
- Unexpected use case
- Kid/pet reaction shot

### Pattern Interrupt
- Counter-intuitive claim
- Controversy or hot take
- Breaking fourth wall

---

## Proof Types

| Type | Example | Strength |
|------|---------|----------|
| **Demo** | Product in action, test | High - seeing is believing |
| **Testimonial** | Customer quote, review screenshot | High - social proof |
| **Stats** | "10,000+ sold", "4.9★ rating" | Medium - quantifiable |
| **Authority** | "As seen on [media]", expert endorsement | Medium - borrowed trust |
| **Comparison** | Side-by-side vs competitor | Medium - relative value |
| **Guarantee** | "30-day money back" | Low - risk reversal |
| **Specs** | Technical details, materials | Low - for detail-oriented buyers |

---

## Extraction Examples

### Example 1: Pottery Wheel Ad

**Ad Creative**: Video of stressed mom, transitions to peaceful pottery scene with child

| Element | Extraction |
|---------|------------|
| **Angle** | Screen-free family bonding (emotional + identity) |
| **Hook** | "Another rainy day at home..." (relatable pain visual) |
| **Promise** | Let kids unleash creativity, not screen time |
| **Pain** | Bored kids glued to tablets |
| **Proof** | "Over 5,000 families tried it" + child holding finished mug |
| **Offer** | Starter Bundle with free shipping |
| **Objection** | "Too messy?" - shows easy cleanup scene |

### Example 2: Travel Mug Ad

**Ad Creative**: Quick cuts of mug in car cupholder, pour test, morning routine

| Element | Extraction |
|---------|------------|
| **Angle** | Leakproof commute (functional) |
| **Hook** | "Cold coffee... never again" (text over coffee shop scene) |
| **Promise** | Keeps coffee hot for hours, no spills |
| **Pain** | Burnt lips or cold coffee in morning commute |
| **Proof** | Customer review screenshot: "KEEPS IT HOT ALL DAY!" |
| **Offer** | Free lid with each mug + 15% off first order |
| **Objection** | "Plastic taste?" - shows 100% ceramic lining close-up |

### Example 3: Gift-Focused Ad

**Ad Creative**: Unwrapping scene, child hugging parent, "best gift ever" moment

| Element | Extraction |
|---------|------------|
| **Angle** | Unique gift & family bonding (emotional + social) |
| **Hook** | Scene of unwrapping pottery wheel, child's excited reaction |
| **Promise** | Memorable DIY gift for family/friends |
| **Pain** | Generic gifts lack personal touch |
| **Proof** | Text overlay "As featured on Today Show" + user photo |
| **Offer** | Holiday Special: Gift bundle + gift wrap |
| **Objection** | "Too late for Xmas?" - shows "Order by Dec 20th for delivery" |

---

## Mapping to Brand Taxonomy

After extracting elements, map to your brand's predefined enums:

1. **Match angle** to brand's angle taxonomy
2. **Identify persona** the ad targets
3. **Note proof type** used
4. **Flag objections** being addressed
5. **Tag offer type** (bundle, discount, free shipping, etc.)

This enables:
- Querying: "Show all competitor ads targeting [persona] with [proof type]"
- Gap analysis: "Which angles are competitors using that we haven't tested?"
- Pattern recognition: "What proof types correlate with long-running ads?"

---

## Quick Extraction Template

Copy this for each ad analyzed:

```
## [Brand Name] - Ad #[X]
**Date Found**:
**Format**: video / static / carousel
**Running Since**:
**Low Count?**: yes / no

### Elements
- **Angle**:
- **Hook**:
- **Promise**:
- **Pain**:
- **Proof**:
- **Offer**:
- **Objection**:

### Brand Mapping
- Angle enum:
- Persona:
- Proof type:
- Objection target:

### Notes
[Any observations about variants, creative family, or testing signals]
```
