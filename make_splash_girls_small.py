"""Regenerate chibi dancing girls at reduced scale (fits smaller splash slot).
Same 8-frame loop + variants, rendered at 0.72x so they read 'cute small' in the 240dp view.
"""
import math
from PIL import Image, ImageDraw

W, H = 460, 430
S = 2
SS = W * S, H * S

VARIANTS = [
    ("gif_1", (156, 200, 255, 255), (110, 160, 230, 255)),
    ("gif_2", (255, 170, 195, 255), (235, 130, 165, 255)),
    ("gif_3", (150, 230, 190, 255), (110, 200, 160, 255)),
]

FLOOR = H - 26


def draw_girl(d, cx, t, main, dark):
    bounce = abs(math.sin(t * math.pi)) * 8
    sway = math.sin(t * 2 * math.pi) * 7
    hip = sway * 0.55
    by = -bounce

    skin = (255, 224, 214, 255)
    skin_d = (240, 200, 190, 255)
    white = (245, 248, 255, 255)
    glow = main[:3] + (200,)

    head_r = 56
    head_cy = FLOOR - 250 + by

    # twin tails (counter-sway)
    for side in (-1, 1):
        tx = cx + side * (head_r + 6)
        ty = head_cy - 18
        pts = []
        for k in range(7):
            f = k / 6.0
            px = tx + side * (10 + 18 * f) - sway * 0.8 * f
            py = ty + 20 + 58 * f + math.sin(t * 2 * math.pi + k) * 4
            pts.append((px, py, 15 - 9 * f))
        for px, py, pr in pts:
            d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=main)

    # head
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=skin)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], outline=skin_d, width=2)

    # hair cap + bangs
    d.pieslice([cx - head_r - 4, head_cy - head_r - 6, cx + head_r + 4, head_cy + head_r * 0.5],
               180, 360, fill=dark)

    # eyes (blink at frame 5)
    blink = (t > 0.55 and t < 0.72)
    ey = head_cy + 6
    if blink:
        d.line([cx - 26, ey, cx - 10, ey], fill=(70, 60, 70, 255), width=3)
        d.line([cx + 10, ey, cx + 26, ey], fill=(70, 60, 70, 255), width=3)
    else:
        for ex in (cx - 18, cx + 18):
            d.ellipse([ex - 7, ey - 9, ex + 7, ey + 9], fill=(60, 55, 75, 255))
            d.ellipse([ex - 3, ey - 7, ex + 1, ey - 2], fill=white)
    # blush + smile
    for bx in (cx - 30, cx + 30):
        d.ellipse([bx - 7, ey + 10, bx + 7, ey + 17], fill=(255, 170, 170, 160))
    d.arc([cx - 10, ey + 2, cx + 10, ey + 16], 15, 165, fill=(200, 110, 110, 255), width=3)

    # headphones
    d.arc([cx - head_r - 10, head_cy - head_r - 12, cx + head_r + 10, head_cy + head_r],
          200, 340, fill=(40, 46, 66, 255), width=9)
    for side in (-1, 1):
        hx = cx + side * (head_r + 2)
        d.rounded_rectangle([hx - 12, head_cy - 22, hx + 12, head_cy + 12], 10, fill=(40, 46, 66, 255))
        d.rounded_rectangle([hx - 7, head_cy - 16, hx + 7, head_cy + 6], 6, fill=glow)

    # body: hoodie
    sh_y = head_cy + head_r + 4
    d.rounded_rectangle([cx - 52 + hip, sh_y, cx + 52 + hip, sh_y + 92], 30, fill=dark)
    d.rounded_rectangle([cx - 44 + hip, sh_y + 8, cx + 44 + hip, sh_y + 84], 26, fill=(30, 36, 54, 255))
    # glow stripe
    d.rounded_rectangle([cx - 30 + hip, sh_y + 66, cx + 30 + hip, sh_y + 74], 4, fill=glow)

    # arms: alternating wave
    arm_phase = math.sin(t * 2 * math.pi)
    for side in (-1, 1):
        lift = arm_phase * side
        ax = cx + side * 52 + hip
        if lift > 0:
            sx, sy = ax, sh_y + 18
            ex_, ey_ = sx + side * 34, sy - 46 - 14 * lift
            d.line([sx, sy, ex_, ey_], fill=dark, width=17)
            d.ellipse([ex_ - 11, ey_ - 11, ex_ + 11, ey_ + 11], fill=skin)
        else:
            sx, sy = ax, sh_y + 26
            ex_, ey_ = sx + side * 26, sy + 40
            d.line([sx, sy, ex_, ey_], fill=dark, width=17)
            d.ellipse([ex_ - 10, ey_ - 10, ex_ + 10, ey_ + 10], fill=skin)

    # skirt
    sk_y = sh_y + 92
    d.polygon([(cx - 44 + hip, sk_y), (cx + 44 + hip, sk_y),
               (cx + 58 + hip * 0.5, sk_y + 46), (cx - 58 + hip * 0.5, sk_y + 46)], fill=main)
    d.polygon([(cx - 44 + hip, sk_y), (cx + 44 + hip, sk_y),
               (cx + 58 + hip * 0.5, sk_y + 10), (cx - 58 + hip * 0.5, sk_y + 10)], fill=dark)

    # legs + boots
    for side in (-1, 1):
        lx = cx + side * 18 + hip
        d.line([lx, sk_y + 44, lx, FLOOR - 12], fill=skin, width=13)
        d.rounded_rectangle([lx - 14, FLOOR - 16, lx + 14, FLOOR], 7, fill=(35, 40, 60, 255))


for name, main, dark in VARIANTS:
    frames = []
    for i in range(8):
        t = i / 8.0
        img = Image.new("RGBA", SS, (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # soft floor shadow
        d.ellipse([W * S / 2 - 120, FLOOR * S - 8, W * S / 2 + 120, FLOOR * S + 14],
                  fill=(10, 16, 30, 120))
        draw_girl(d, W / 2, t, main, dark)
        frames.append(img.resize((W, H), Image.LANCZOS))
    frames[0].save("res/drawable/%s.gif" % name, save_all=True,
                   append_images=frames[1:], duration=110, loop=0, transparency=0, disposal=2)
    print(name, W, "x", H, "8 frames")
