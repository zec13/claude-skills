# Table Clay Brand Context

## Brand Overview

**Table Clay** is a ceramics/pottery ecommerce brand selling pottery wheels, ceramic travel mugs, and aesthetic mugs.

**Brand Positioning**: Premium craftsmanship, handmade quality, creativity-enabling products

---

## Product Lines

| Product Line | Enum | Description |
|--------------|------|-------------|
| Mini Pottery Wheel | `mini_wheel` | Starter pottery wheels for beginners and kids |
| Ceramic Travel Mug | `travel_mug` | Handmade ceramic mugs for on-the-go |
| Aesthetic/Cute Mugs | `aesthetic_mugs` | Decorative ceramic mugs for home |

---

## Tag Taxonomy

### Angles by Product Line

**mini_wheel:**
- `pottery_therapy` - Stress relief, mindfulness through pottery
- `screen_free_family` - Alternative to screens for kids
- `beginner_confidence` - Anyone can do it, easy to start
- `mess_managed` - Clean, contained, not messy
- `giftable_date_night` - Couples activity, unique gift

**travel_mug:**
- `leakproof_commute` - Won't spill in your bag
- `keeps_hot` - Temperature retention
- `fits_cupholder` - Practical car fit
- `handmade_aesthetic` - Artisan quality, unique look
- `giftable_everyday` - Practical premium gift

**aesthetic_mugs:**
- `morning_ritual` - Elevate your coffee routine
- `cozy_home` - Home comfort aesthetic
- `desk_companion` - Work-from-home style
- `cute_gift` - Giftable adorable design
- `collectible_drops` - Limited editions, collecting

---

### Personas

| Persona | Enum | Description |
|---------|------|-------------|
| Apartment Adult | `apartment_adult` | Urban dweller, limited space |
| Beginner Maker | `beginner_maker` | New to crafts, wants easy start |
| Parent | `parent` | Looking for kid activities |
| Gift Seeker | `gift_seeker` | Shopping for others |
| Coffee Commuter | `coffee_commuter` | Daily commute, needs travel mug |
| Aesthetic Home | `aesthetic_home` | Cares about home décor |

**By Product Line:**
- mini_wheel: `adult_hobbyist`, `apartment_dweller`, `parent`, `gift_seeker`
- travel_mug: `commuter`, `office_worker`, `student`, `gift_seeker`, `coffee_person`
- aesthetic_mugs: `home_decor`, `coffee_person`, `gift_seeker`, `collector`

---

### Intent Context (Job-to-be-Done)

| Context | Enum |
|---------|------|
| Stress relief | `stress_reset` |
| Screen-free time | `screen_free_time` |
| Coffee ritual | `coffee_ritual` |
| Commute | `commute` |
| Gift shopping | `gift` |
| Home decoration | `home_decor` |

---

### Objection Targets by Product Line

**mini_wheel:**
| Objection | Enum | Counter |
|-----------|------|---------|
| Takes up space | `space` | Compact design, stores easily |
| Too messy | `mess` | Contained setup, easy cleanup |
| Hard to learn | `learning_curve` | Beginner-friendly, tutorials included |
| Is it real clay? | `is_it_real_clay` | Yes, air-dry clay included |
| Takes too long | `time` | Quick projects, 30-min sessions |

**travel_mug:**
| Objection | Enum | Counter |
|-----------|------|---------|
| Will it leak? | `leaks` | Leakproof seal guarantee |
| Won't stay hot | `heat_retention` | 6+ hour heat retention |
| Lid quality | `lid_quality` | Premium silicone seal |
| Fragile ceramic | `fragile` | Double-wall protection |
| Won't fit cupholder | `cupholder_fit` | Standard cupholder size |

**aesthetic_mugs:**
| Objection | Enum | Counter |
|-----------|------|---------|
| Will it break? | `breakage` | Durable stoneware |
| Too small/large | `size` | Multiple sizes available |
| Dishwasher safe? | `dishwasher_safe` | Yes, dishwasher safe |
| Too expensive | `price` | Handmade quality justifies |
| Shipping damage | `shipping` | Secure packaging guaranteed |

---

### Proof Types by Product Line

**mini_wheel:**
- `demo` - Product in action, throwing clay
- `outcome` - Finished pieces made by beginners
- `objection_kill` - Cleanup demo, space demo
- `social_proof` - Reviews, testimonials
- `specs` - What's included in kit

**travel_mug:**
- `test` - Leak test, temperature test
- `demo` - Using in car, commute scene
- `comparison` - vs other mugs
- `social_proof` - Reviews, "X sold"
- `specs` - Dimensions, materials

**aesthetic_mugs:**
- `social_proof` - Reviews, UGC photos
- `lifestyle` - In-situ home shots
- `ugc` - Customer photos
- `specs` - Dimensions, care instructions
- `risk_reversal` - Guarantee, return policy

---

### Other Enums

**Funnel Stage:**
- `tof` - Top of funnel (awareness)
- `mof` - Middle of funnel (consideration)
- `bof` - Bottom of funnel (decision)
- `rt` - Retargeting

**Format:**
- `video`
- `static`
- `carousel`

**Ratio:**
- `9x16` - Vertical (Stories/Reels)
- `4x5` - Portrait (Feed)
- `1x1` - Square

**Offer Type:**
- `none`
- `bundle`
- `free_shipping`
- `limited_drop`
- `giftable`
- `discount`

**Creative Type:**
- `paid_ugc` - Paid influencer/creator content
- `native_demo` - In-house demo video
- `product_cinematic` - Polished product shots
- `static_graphic` - Designed static image
- `carousel_micro_lp` - Multi-image mini landing page
- `long_form` - Extended video content

---

## Filename Convention

```
[Brand]_[ProductLine]_[Format]_[FunnelStage]_[Concept]_[Angle]_[ProofType]_[HookKey]_[V#]_[Ratio]
```

**Examples:**
- `TableClay_mini_wheel_video_tof_pottery_therapy_demo_asmr_calm_V3_9x16`
- `TableClay_travel_mug_video_tof_leakproof_test_demo_spillproof_V1_9x16`
- `TableClay_aesthetic_mugs_carousel_mof_morning_ritual_social_proof_cozy_V2_4x5`

---

## Using This Context in Analysis

When analyzing competitor ads:

1. **Match their angle** to Table Clay's angle enums
   - If competitor uses "relaxation" → maps to `pottery_therapy`
   - If competitor uses "kids activity" → maps to `screen_free_family`

2. **Identify persona overlap**
   - Which of Table Clay's personas would respond to this ad?

3. **Note proof type**
   - What evidence strategy are they using?
   - Does Table Clay use this proof type? Should we?

4. **Flag objection handling**
   - What objections are they preemptively addressing?
   - Are these objections in Table Clay's list?

5. **Gap analysis**
   - Angles competitors use that Table Clay hasn't tested
   - Objections competitors address that Table Clay ignores
   - Proof types that seem effective but underused
