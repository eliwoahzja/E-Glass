"""Neo-brutalist launcher icon: pure black disc, thick red ring, massive red E
with hard offset shadow. No gradients, no glow - raw blocks of color.
Also regenerates ic_glow1/2 as brutalist pulse frames (red ring flash).
"""
from PIL import Image, ImageDraw

S = 512
RED = (220, 20, 40, 255)
BLACK = (8, 8, 10, 255)
DARK = (16, 14, 16, 255)

def base_icon():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S // 2, S // 2
    r = 244
    # black disc with hard red ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK, outline=RED, width=18)
    return img, d, cx, cy

def draw_e(d, cx, cy, scale, offset=(0, 0)):
    """Massive blocky E with hard offset shadow."""
    w = int(190 * scale)   # arm length
    t = int(52 * scale)    # bar thickness
    x0 = cx - int(w * 0.45) + offset[0]
    y0 = cy - int(w * 0.62) + offset[1]
    x1 = x0 + w
    y1 = y0 + int(w * 1.24)
    # hard shadow (dark red, offset)
    sx, sy = x0 + int(10 * scale), y0 + int(10 * scale)
    d.rectangle([sx, sy, sx + w, sy + t], fill=(90, 8, 16, 255))
    d.rectangle([sx, sy + t, sx + t, sy + int(w * 1.24)], fill=(90, 8, 16, 255))
    d.rectangle([sx, sy + int(w * 1.24) - t, sx + w, sy + int(w * 1.24)], fill=(90, 8, 16, 255))
    # main E (three bars + spine)
    d.rectangle([x0, y0, x1, y0 + t], fill=RED)
    d.rectangle([x0, y0 + t, x0 + t, y1 - t], fill=RED)
    d.rectangle([x0, y1 - t, x1 - int(w * 0.15), y1], fill=RED)
    d.rectangle([x0, y0 + int(w * 0.52) - t // 2, x1 - int(w * 0.3), y0 + int(w * 0.52) + t // 2], fill=RED)
    return x0, y0, x1, y1

# main icon
img, d, cx, cy = base_icon()
draw_e(d, cx, cy, 1.0)
img.save("res/drawable/ic_normal.png")

# brutalist pulse frames: ring flashes bright/dim
for name, ring, ecol in [
    ("ic_glow1", (255, 40, 60, 255), RED),
    ("ic_glow2", (120, 10, 20, 255), (150, 14, 30, 255)),
]:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S // 2, S // 2
    r = 244
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLACK, outline=ring, width=22)
    # E in this frame's color
    w = 190; t = 52
    x0, y0 = cx - int(w * 0.45), cy - int(w * 0.62)
    x1 = x0 + w
    y1 = y0 + int(w * 1.24)
    d.rectangle([x0, y0, x1, y0 + t], fill=ecol)
    d.rectangle([x0, y0 + t, x0 + t, y1 - t], fill=ecol)
    d.rectangle([x0, y1 - t, x1 - int(w * 0.15), y1], fill=ecol)
    d.rectangle([x0, y0 + int(w * 0.52) - t // 2, x1 - int(w * 0.3), y0 + int(w * 0.52) + t // 2], fill=ecol)
    img.save("res/drawable/%s.png" % name)

# launcher mipmaps
import os
for density, size in [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)]:
    img2 = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(img2)
    cx2, cy2 = S // 2, S // 2
    d2.ellipse([cx2 - 244, cy2 - 244, cx2 + 244, cy2 + 244], fill=BLACK, outline=RED, width=18)
    draw_e(d2, cx2, cy2, 1.0)
    img2.resize((size, size), Image.LANCZOS).save("res/mipmap-%s/ic_launcher.png" % density)
print("icons done")
