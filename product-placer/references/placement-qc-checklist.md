# Placement QC Checklist

Use this checklist after every product placement to verify the composite looks natural and the product is accurately represented. Score each dimension and make a ship/fix decision.

## Dimension 1: Product Fidelity (HIGHEST PRIORITY)

The whole point of this skill is replacing an AI approximation with the real thing. If the real product doesn't look right in the final image, the skill has failed.

**Check:**
- [ ] The product in the composite is recognizably the same item from the website
- [ ] Shape matches using geometric classification (tapered/conical, cylindrical, barrel, tulip, bell, hourglass) — compare silhouette top-to-bottom, not vibes
- [ ] Proportions match: rim-to-base width ratio and height-to-width ratio are correct (not stretched, squished, or distorted)
- [ ] Colors are accurate — the sage green is sage green, not teal or olive or gray
- [ ] Texture/finish is preserved — matte stays matte, speckle stays speckled
- [ ] The handmade character is visible (slight variations, not perfectly uniform)
- [ ] No features have been lost in the cutout (lid, sleeve, rim, base all present if they should be)
- [ ] No background remnants clinging to the product edges

**Common failures:**
- Wrong geometric profile (e.g., tapered cup rendered as barrel/egg — silhouette is the most common NanoBanana failure)
- Color shift from aggressive color-matching (product becomes a different hue)
- Over-smoothing from too much blur (product loses its texture)
- Edge clipping where part of the product was cut off during background removal
- Perspective distortion making the product look warped

**Scoring:**
- **Pass**: Customer would recognize this as the product they'd receive
- **Needs Fix**: Close but something is slightly off (minor color shift, small edge artifact)
- **Fail**: Product looks wrong, distorted, or unrecognizable — redo the cutout or placement

## Dimension 2: Natural Placement

The product should look like it was photographed in the scene, not pasted on top.

**Check:**
- [ ] Edges are smooth, no visible "halo" or jagged cutout lines
- [ ] Product has a shadow that matches the scene's lighting direction
- [ ] Shadow is soft and natural, not a harsh dark outline
- [ ] Product sits ON the surface (not floating above it)
- [ ] Scale is correct relative to the scene (product isn't too big or too small)
- [ ] Product base aligns with the surface plane

**Common failures:**
- Hard edges where the cutout meets the background (no feathering)
- Missing shadow making the product look like it's floating
- Shadow going the wrong direction (doesn't match scene lighting)
- Product scale mismatch (a mug the size of a coffee table, or vice versa)

**Scoring:**
- **Pass**: At a quick glance, looks like the product was photographed there
- **Needs Fix**: Looks placed but not jarring — a specific issue can be fixed
- **Fail**: Obvious paste job — shadow, edges, or scale completely wrong

## Dimension 3: Lighting Harmony

The product's lighting should match the scene's lighting.

**Check:**
- [ ] Brightness of the product matches the brightness of the scene
- [ ] Highlights on the product are on the correct side (matching the scene's light source)
- [ ] Color temperature matches — product isn't cool-toned in a warm scene (or vice versa)
- [ ] Contrast level of the product matches the scene's contrast
- [ ] If the scene has dramatic lighting, the product reflects that drama

**Common failures:**
- Product is brighter/darker than everything else in the scene
- Product has highlights on the left but scene light comes from the right
- Product looks "flat" while the scene has dramatic shadows
- Product has a blue cast in a warm golden scene

**Scoring:**
- **Pass**: Product lighting blends seamlessly with the scene
- **Needs Fix**: Slightly off — can be corrected with brightness/color adjustment
- **Fail**: Obviously different lighting — product looks pasted from a different photo

## Dimension 4: Composition Integrity

The ad should still work as an ad after the product swap.

**Check:**
- [ ] Visual hierarchy is preserved (eye flows correctly through the ad)
- [ ] Text overlays are still legible and properly positioned
- [ ] Icon badges or graphic elements are not covered or disrupted
- [ ] The product is the focal point (or maintains its original prominence)
- [ ] Whitespace/breathing room is preserved around the product
- [ ] The overall ad layout feels balanced

**Common failures:**
- Product is positioned slightly off from where the AI product was, breaking the layout
- Text overlay is now partially behind the product or awkwardly placed
- Icon badges are covered by the new product placement
- The product is bigger/smaller than expected, throwing off balance

**Scoring:**
- **Pass**: Ad still reads well and looks professionally composed
- **Needs Fix**: Minor positioning adjustment needed
- **Fail**: Composition is broken — product covers important elements or creates visual chaos

## Dimension 5: Honesty and Accuracy

The ad must not mislead customers about what they're buying.

**Check:**
- [ ] The product shown is what the customer will receive
- [ ] No color enhancement beyond what's real
- [ ] No size exaggeration
- [ ] Accessories shown are included with the product (or clearly optional)
- [ ] The product's handmade character is preserved, not smoothed to perfection
- [ ] If the product has visible variations (glaze inconsistencies), they're not hidden

**This dimension cannot "Need Fix" — it either passes or fails.**

**Scoring:**
- **Pass**: Customer would not feel deceived when receiving this product
- **Fail**: Product is misrepresented — fix immediately

## QC Report Format

```
PLACEMENT QC — [Ad Name]
=========================
Overall: [X/5 passing]

1. Product Fidelity:  [Pass/Needs Fix/Fail] — [notes]
2. Natural Placement: [Pass/Needs Fix/Fail] — [notes]
3. Lighting Harmony:  [Pass/Needs Fix/Fail] — [notes]
4. Composition:       [Pass/Needs Fix/Fail] — [notes]
5. Honesty:           [Pass/Fail] — [notes]

Decision: [SHIP / FIX (specific action) / REDO CUTOUT / REDO PLACEMENT]
```

## Decision Tree

```
All 5 pass → Ship it
     |
Product Fidelity fails → Get better source image or redo cutout
     |
Natural Placement fails → Adjust shadows, edges, or scale (Phase 3C)
     |
Lighting fails → Adjust color matching and brightness (Phase 3A)
     |
Composition fails → Reposition product (Phase 3B)
     |
Honesty fails → STOP — do not ship. Identify the misleading element and fix it.
```
