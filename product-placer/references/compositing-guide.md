# Compositing Guide — Technical Reference

Detailed technical reference for the image compositing workflow. This covers the Python/PIL techniques for each step of the placement process.

## Background Removal Techniques

### Method 1: rembg (Preferred)

```python
from rembg import remove
from PIL import Image
import io

input_image = Image.open('product_source.png')
output_image = remove(input_image)
output_image.save('product_cutout.png')
```

rembg uses a neural network trained specifically for foreground extraction. It handles complex edges (hair, fur, translucent materials) much better than threshold-based methods.

**When rembg struggles:**
- Very low contrast between product and background
- Translucent/glass products
- Products that are mostly white on a white background
- Very small images (<200px)

### Method 2: Color Threshold (White Background)

```python
from PIL import Image
import numpy as np

img = Image.open('product_source.png').convert('RGBA')
data = np.array(img)

# Define "white" threshold — pixels with R, G, B all above threshold
# become transparent
threshold = 240
white_mask = (data[:, :, 0] > threshold) & \
             (data[:, :, 1] > threshold) & \
             (data[:, :, 2] > threshold)

# Set alpha to 0 for white pixels
data[:, :, 3] = np.where(white_mask, 0, 255)

# Clean up edges with slight feathering
result = Image.fromarray(data)
result.save('product_cutout.png')
```

**Improvements:**
- Use adaptive threshold based on the actual background color (sample corners)
- Apply morphological operations (erode then dilate) to clean edges
- Use anti-aliased alpha by computing distance from threshold rather than hard cutoff

### Method 3: GrabCut-style (OpenCV)

If OpenCV is available:
```python
import cv2
import numpy as np

img = cv2.imread('product_source.png')
mask = np.zeros(img.shape[:2], np.uint8)

# Define a rectangle around the product (leave margin)
rect = (margin, margin, img.shape[1]-2*margin, img.shape[0]-2*margin)

bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)

cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# Create alpha mask
alpha = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
```

## Scaling and Positioning

### Calculating Target Size

The product in the final ad should occupy approximately the same bounding box as the AI-generated product it replaces.

```python
# Measure the AI product's bounding box in the ad
# (manually identified from Phase 2 analysis)
ai_product_width = x2 - x1  # pixels
ai_product_height = y2 - y1  # pixels

# Get the real product cutout's dimensions
cutout_w, cutout_h = product_cutout.size

# Scale to fit the same bounding box while preserving aspect ratio
aspect_ratio = cutout_w / cutout_h
target_aspect = ai_product_width / ai_product_height

if aspect_ratio > target_aspect:
    # Product is wider relative to its height than the target box
    new_width = ai_product_width
    new_height = int(ai_product_width / aspect_ratio)
else:
    # Product is taller relative to its width than the target box
    new_height = ai_product_height
    new_width = int(ai_product_height * aspect_ratio)

product_scaled = product_cutout.resize((new_width, new_height), Image.LANCZOS)
```

### Centering in the Bounding Box

```python
# Center the scaled product in the original bounding box
x_offset = x1 + (ai_product_width - new_width) // 2
y_offset = y1 + (ai_product_height - new_height) // 2
```

## Color Matching

### Analyzing Ad Color Temperature

```python
from PIL import Image, ImageStat
import numpy as np

ad = Image.open('target_ad.png').convert('RGB')

# Sample the area around the product (but not the product itself)
# to understand the scene's color temperature
surrounding_box = (x1-50, y1-50, x2+50, y2+50)  # expand bounding box
surrounding = ad.crop(surrounding_box)

stat = ImageStat.Stat(surrounding)
mean_r, mean_g, mean_b = stat.mean

# Color temperature assessment
# Warm: mean_r > mean_b by significant margin
# Cool: mean_b > mean_r by significant margin
# Neutral: roughly equal
warmth = mean_r - mean_b  # positive = warm, negative = cool
```

### Applying Color Temperature Shift

```python
from PIL import ImageEnhance
import numpy as np

def adjust_warmth(image, warmth_factor):
    """
    warmth_factor > 0: warm up (add slight red/yellow, reduce blue)
    warmth_factor < 0: cool down (add slight blue, reduce red)
    Range: -0.3 to 0.3 for subtle adjustments
    """
    data = np.array(image).astype(float)

    # Adjust red channel
    data[:, :, 0] = np.clip(data[:, :, 0] * (1 + warmth_factor * 0.15), 0, 255)

    # Slightly adjust green for warmth
    data[:, :, 1] = np.clip(data[:, :, 1] * (1 + warmth_factor * 0.05), 0, 255)

    # Inversely adjust blue channel
    data[:, :, 2] = np.clip(data[:, :, 2] * (1 - warmth_factor * 0.1), 0, 255)

    # Preserve alpha channel
    if image.mode == 'RGBA':
        alpha = np.array(image)[:, :, 3]
        result = np.dstack([data[:, :, :3].astype(np.uint8), alpha])
        return Image.fromarray(result, 'RGBA')
    return Image.fromarray(data.astype(np.uint8))
```

### Brightness and Contrast Matching

```python
def match_brightness(product, ad, product_region):
    """
    Match the product's overall brightness to the brightness
    level in the ad region where it will be placed.
    """
    # Measure ad brightness in the target region
    ad_region = ad.crop(product_region)
    ad_brightness = ImageStat.Stat(ad_region.convert('L')).mean[0]

    # Measure product brightness
    product_brightness = ImageStat.Stat(product.convert('L')).mean[0]

    # Calculate adjustment factor
    if product_brightness > 0:
        factor = ad_brightness / product_brightness
        # Clamp to reasonable range (0.5 to 1.5)
        factor = max(0.5, min(1.5, factor))
    else:
        factor = 1.0

    enhancer = ImageEnhance.Brightness(product)
    return enhancer.enhance(factor)
```

## Shadow Creation

### Simple Drop Shadow

```python
def create_drop_shadow(product_cutout, shadow_offset=(5, 8),
                        shadow_blur=15, shadow_opacity=0.4):
    """
    Create a soft drop shadow beneath the product.
    shadow_offset: (x, y) pixel offset for shadow direction
    shadow_blur: Gaussian blur radius for shadow softness
    shadow_opacity: 0.0 (invisible) to 1.0 (solid black)
    """
    # Create shadow from product alpha channel
    alpha = product_cutout.split()[-1]

    # Create solid dark shape matching product silhouette
    shadow = Image.new('RGBA', product_cutout.size, (0, 0, 0, 0))
    shadow_layer = Image.new('RGBA', product_cutout.size,
                              (0, 0, 0, int(255 * shadow_opacity)))
    shadow.paste(shadow_layer, mask=alpha)

    # Blur the shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))

    # Offset the shadow
    offset_shadow = Image.new('RGBA', product_cutout.size, (0, 0, 0, 0))
    offset_shadow.paste(shadow, shadow_offset)

    return offset_shadow
```

### Surface Contact Shadow

For products sitting on a surface, the shadow should be concentrated at the base:

```python
def create_contact_shadow(product_cutout, surface_y,
                           spread=20, opacity=0.5):
    """
    Create a contact shadow at the base of the product
    where it meets the surface.
    """
    alpha = np.array(product_cutout.split()[-1])

    # Find the bottom edge of the product
    rows_with_content = np.where(alpha.max(axis=1) > 0)[0]
    if len(rows_with_content) == 0:
        return Image.new('RGBA', product_cutout.size, (0, 0, 0, 0))

    bottom_row = rows_with_content[-1]

    # Create shadow concentrated at the bottom
    shadow = Image.new('RGBA', product_cutout.size, (0, 0, 0, 0))
    # Draw elliptical shadow at base
    # ... (use ImageDraw for ellipse at product base)

    shadow = shadow.filter(ImageFilter.GaussianBlur(spread))
    return shadow
```

## Edge Blending

### Anti-aliased Edge Feathering

```python
def feather_edges(cutout, feather_radius=1.5):
    """
    Soften the edges of a cutout to prevent harsh 'cut-out' appearance.
    Very subtle — 1-2px is usually enough.
    """
    alpha = cutout.split()[-1]

    # Slightly blur the alpha channel
    feathered_alpha = alpha.filter(
        ImageFilter.GaussianBlur(feather_radius)
    )

    # Recombine
    r, g, b, _ = cutout.split()
    return Image.merge('RGBA', (r, g, b, feathered_alpha))
```

### Scene Color Bleed

To make edges look natural, bleed a tiny amount of the surrounding scene color into the product edges:

```python
def apply_color_bleed(composite, product_mask, bleed_radius=2):
    """
    Blend a hint of surrounding colors into the product edges.
    This simulates how real objects pick up ambient color.
    """
    # Blur the composite heavily
    blurred = composite.filter(ImageFilter.GaussianBlur(bleed_radius * 3))

    # Create an edge-only mask (product boundary)
    edge_mask = product_mask.filter(ImageFilter.FIND_EDGES)
    edge_mask = edge_mask.filter(ImageFilter.GaussianBlur(bleed_radius))

    # Composite: use the blurred version at the edges,
    # original everywhere else
    return Image.composite(blurred, composite, edge_mask)
```

## Perspective Transform

When the product cutout angle doesn't match the ad:

```python
def apply_perspective(product, coefficients):
    """
    Apply a perspective transform to adjust the viewing angle.
    coefficients: 8 values for the perspective transform matrix

    Finding coefficients:
    - Define 4 source points (corners of the product)
    - Define 4 destination points (where they should map to)
    - Use numpy to solve for the transform matrix
    """
    return product.transform(
        product.size,
        Image.PERSPECTIVE,
        coefficients,
        Image.BICUBIC
    )

def find_perspective_coefficients(src_points, dst_points):
    """
    Calculate perspective transform coefficients from point pairs.
    src_points: [(x1,y1), (x2,y2), (x3,y3), (x4,y4)] — original corners
    dst_points: [(x1,y1), (x2,y2), (x3,y3), (x4,y4)] — target corners
    """
    import numpy as np

    matrix = []
    for s, d in zip(src_points, dst_points):
        matrix.append([s[0], s[1], 1, 0, 0, 0, -d[0]*s[0], -d[0]*s[1]])
        matrix.append([0, 0, 0, s[0], s[1], 1, -d[1]*s[0], -d[1]*s[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array([d for pair in dst_points for d in pair]).reshape(8)

    coefficients = np.array(np.dot(np.linalg.inv(A.T * A) * A.T, B)).flatten()
    return tuple(coefficients.tolist())
```

## Complete Pipeline Example

```python
from PIL import Image, ImageEnhance, ImageFilter, ImageStat
import numpy as np

def place_product(ad_path, cutout_path, output_path,
                  product_bbox, lighting_direction='left',
                  warmth_adjustment=0.0):
    """
    Full compositing pipeline.

    ad_path: path to the advertisement image
    cutout_path: path to the product cutout (PNG with alpha)
    output_path: where to save the final composite
    product_bbox: (x1, y1, x2, y2) where the product should go
    lighting_direction: 'left', 'right', 'top', 'bottom'
    warmth_adjustment: -0.3 to 0.3
    """
    # Load images
    ad = Image.open(ad_path).convert('RGBA')
    product = Image.open(cutout_path).convert('RGBA')

    # 1. Scale product to fit bounding box
    x1, y1, x2, y2 = product_bbox
    target_w = x2 - x1
    target_h = y2 - y1

    aspect = product.width / product.height
    if aspect > (target_w / target_h):
        new_w = target_w
        new_h = int(target_w / aspect)
    else:
        new_h = target_h
        new_w = int(target_h * aspect)

    product = product.resize((new_w, new_h), Image.LANCZOS)

    # 2. Color match
    product = match_brightness(product, ad, product_bbox)
    if warmth_adjustment != 0:
        product = adjust_warmth(product, warmth_adjustment)

    # 3. Feather edges
    product = feather_edges(product, 1.0)

    # 4. Create shadow
    shadow_offsets = {
        'left': (5, 8),
        'right': (-5, 8),
        'top': (0, 10),
        'bottom': (0, -5)
    }
    shadow = create_drop_shadow(
        product,
        shadow_offset=shadow_offsets.get(lighting_direction, (5, 8)),
        shadow_blur=12,
        shadow_opacity=0.35
    )

    # 5. Position in ad
    pos_x = x1 + (target_w - new_w) // 2
    pos_y = y1 + (target_h - new_h) // 2

    # Paste shadow first (behind product)
    ad.paste(shadow, (pos_x, pos_y), shadow)

    # Paste product
    ad.paste(product, (pos_x, pos_y), product)

    # 6. Save
    ad.save(output_path, 'PNG')

    return output_path
```
