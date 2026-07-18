"""
Prepare a portrait photo for clean ASCII conversion:
  1. remove the background (rembg) so the subject is isolated
  2. boost LOCAL contrast (CLAHE) so a flatly-lit face gains highlights and
     shadows -- this is what turns a dark blob into a recognizable face
  3. composite the subject onto pure white so the background reads as blank
     (white -> spaces in the ascii ramp)

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
Run once whenever the source photo changes; the ascii SVG itself is static.

    python scripts/prep_photo.py <input.jpg> [output.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

# 1. cut out the subject
cut = remove(Image.open(INP).convert("RGBA"))

# Crop to subject bounding box with padding, maintaining square aspect ratio to avoid distortion
bbox = cut.getbbox()
if bbox:
    x0, y0, x1, y1 = bbox
    w, h = cut.size
    
    bw = x1 - x0
    bh = y1 - y0
    side = int(max(bw, bh) * 1.1)  # 10% padding
    
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    
    cx0 = max(0, cx - side // 2)
    cy0 = max(0, cy - side // 2)
    cx1 = min(w, cx0 + side)
    cy1 = min(h, cy0 + side)
    
    if cx1 - cx0 < side:
        cx0 = max(0, cx1 - side)
    if cy1 - cy0 < side:
        cy0 = max(0, cy1 - side)
        
    cut = cut.crop((cx0, cy0, cx1, cy1))

rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])                 # 0 = background

# 2. local-contrast the luminance (Bilateral Filter + CLAHE)
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
gray = cv2.bilateralFilter(gray, 9, 75, 75)
clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# a touch of global lift so the face sits in the sparse end of the ramp
gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

# 3. paste onto white using the alpha mask (feathered a hair to avoid a halo)
mask = (alpha.astype(np.float32) / 255.0)
mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out, mode="L").save(OUT)
print("wrote", OUT, out.shape)
