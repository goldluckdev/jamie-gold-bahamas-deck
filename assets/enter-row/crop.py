#!/usr/bin/env python3
"""Pre-crop portrait Drive-sourced photos to the .enter-photos tile aspect ratio
(1.738:1, landscape) so object-fit:cover has nothing left to remove and faces
stay fully in frame. Mirrors the technique from the Winner's Journey photo-row memory."""
from PIL import Image
import os

SRC = os.path.dirname(os.path.abspath(__file__))
TILE_AR = 1.738  # 339/195

def crop_to_ar(im, ar, y_center_frac=0.5):
    w, h = im.size
    target_h = w / ar
    if target_h <= h:
        # crop height
        y0 = max(0, min(h - target_h, h * y_center_frac - target_h / 2))
        box = (0, round(y0), w, round(y0 + target_h))
    else:
        target_w = h * ar
        x0 = max(0, min(w - target_w, w * 0.5 - target_w / 2))
        box = (round(x0), 0, round(x0 + target_w), h)
    return im.crop(box)

jobs = [
    # (src, dst, y_center_frac)
    ("src-selfie.jpg", "tile-1-selfie.jpg", 0.42),
    ("src-bbotable.jpg", "tile-2-bbotable.jpg", 0.38),
    ("src-philanthropist.jpg", "tile-3-philanthropist.jpg", 0.32),
    ("src-tips.jpg", "tile-4-tips.jpg", 0.40),
    ("src-behind.jpg", "tile-5-behind.jpg", 0.38),
]

for src, dst, yc in jobs:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    cropped = crop_to_ar(im, TILE_AR, yc)
    # upscale to a consistent 2x render width for sharpness (678x390)
    out = cropped.resize((678, 390), Image.LANCZOS)
    out.save(os.path.join(SRC, dst), "JPEG", quality=92)
    print(dst, out.size)
