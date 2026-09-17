"""Prepare the Aris (Blue Archive) dance sticker for the splash.
Source: transparent Tenor sticker, 180x139, 187 frames @ ~30ms.
Upscale to 2x, trim to content, keep every 3rd frame (~10fps smooth), compact palette.
"""
from PIL import Image

SRC = "/tmp/aris_st.gif"
im = Image.open(SRC)
N = im.n_frames
W, H = im.size

# trim window (content bbox + pad)
X0, Y0, X1, Y1 = 45, 7, 135, 133  # bbox (49,11,131,129) + pad
TW, TH = X1 - X0, Y1 - Y0
SCALE = 2  # upscale for crispness at 190dp
OW, OH = TW * SCALE, TH * SCALE

frames = []
total_src = 0
for i in range(N):
    im.seek(i)
    dur = im.info.get("duration", 30)
    total_src += dur
    f = im.convert("RGBA").crop((X0, Y0, X1, Y1)).resize((OW, OH), Image.LANCZOS)
    frames.append((f, dur))
print("loaded", len(frames), "frames; src loop", total_src, "ms")

# keep every 5th frame (0.15s cadence; 38 frames, smooth for a dance loop)
keep = frames[::5]
if keep[-1][0] is not frames[-1][0]:
    keep.append(frames[-1])

def to_palette(rgba_frame):
    alpha = rgba_frame.split()[3]
    mask = alpha.point(lambda a: 255 if a <= 100 else 0)
    p = rgba_frame.convert("RGB").quantize(colors=96, method=Image.FASTOCTREE,
                                           dither=Image.NONE)
    p.paste(255, mask)
    p.info["transparency"] = 255
    return p

out = [(to_palette(f), d) for f, d in keep]
durs = [d for _, d in out]
print("out:", OW, "x", OH, len(out), "frames, loop", sum(durs), "ms")

out[0][0].save("res/drawable/gif_1.gif", save_all=True,
               append_images=[f for f, _ in out[1:]], duration=durs, loop=0,
               transparency=255, disposal=2)
import shutil, os
shutil.copy("res/drawable/gif_1.gif", "res/drawable/gif_2.gif")
shutil.copy("res/drawable/gif_1.gif", "res/drawable/gif_3.gif")
print("size:", os.path.getsize("res/drawable/gif_1.gif"))

chk = Image.open("res/drawable/gif_1.gif")
chk.seek(0)
a = chk.convert("RGBA").split()[3]
px = a.load(); w, h = a.size
corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
n = sum(1 for y in range(0, h, 3) for x in range(0, w, 3) if px[x, y] > 90)
print("verify: corners", corners, "opaque %.0f%%" % (100.0 * n / ((w // 3 + 1) * (h // 3 + 1))))
