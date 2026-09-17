"""Extract the dancing girl via temporal median background + largest-blob isolation."""
from PIL import Image, ImageChops, ImageFilter

SRC = "/tmp/girl.gif"
im = Image.open(SRC)
N = im.n_frames
w, h = im.size
print("src:", im.size, N, "frames")

all_frames = []
for i in range(N):
    im.seek(i)
    all_frames.append(im.convert("RGB"))

# --- temporal median bg (sample every 3rd frame) ---
sample = all_frames[::3]
pxs = [f.load() for f in sample]
med = Image.new("RGB", (w, h))
mp = med.load()
for y in range(h):
    for x in range(w):
        rs = sorted(p[x, y][0] for p in pxs)
        gs = sorted(p[x, y][1] for p in pxs)
        bs = sorted(p[x, y][2] for p in pxs)
        m = len(sample) // 2
        mp[x, y] = (rs[m], gs[m], bs[m])
print("median bg built")

# --- temporal diff for static mask ---
mn = mx = None
for rgb in all_frames:
    mn = rgb if mn is None else ImageChops.darker(mn, rgb)
    mx = rgb if mx is None else ImageChops.lighter(mx, rgb)
stat = ImageChops.subtract(mx, mn).convert("L")
static_mask = stat.point(lambda v: 255 if v < 40 else 0)
static_mask = static_mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
static_mask = static_mask.filter(ImageFilter.MaxFilter(3))
print("static mask built")

def largest_blob(mask, scale=4):
    """Keep only the largest connected component (checked at 1/scale res)."""
    small = mask.resize((w // scale, h // scale), Image.BILINEAR)
    sp = small.load()
    sw, sh = small.size
    seen = [[False] * sw for _ in range(sh)]
    best = []
    for sy in range(sh):
        for sx in range(sw):
            if sp[sx, sy] > 110 and not seen[sy][sx]:
                comp = []
                stack = [(sx, sy)]
                seen[sy][sx] = True
                while stack:
                    cx, cy = stack.pop()
                    comp.append((cx, cy))
                    for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                        if 0 <= nx < sw and 0 <= ny < sh and not seen[ny][nx] and sp[nx, ny] > 110:
                            seen[ny][nx] = True
                            stack.append((nx, ny))
                if len(comp) > len(best):
                    best = comp
    out = Image.new("L", (sw, sh), 0)
    op = out.load()
    for cx, cy in best:
        op[cx, cy] = 255
    return out.resize((w, h), Image.BILINEAR)

frames = []
for i, rgb in enumerate(all_frames):
    diff = ImageChops.difference(rgb, med).convert("L")
    fg = diff.point(lambda v: 255 if v > 30 else 0)
    fg = ImageChops.subtract(fg.convert("RGB"), static_mask.convert("RGB")).convert("L")
    # kill scattered grain, close subject holes (gentler)
    fg = fg.filter(ImageFilter.MinFilter(3))
    fg = fg.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    fg = largest_blob(fg)
    fg = fg.filter(ImageFilter.GaussianBlur(1.0))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(fg)
    frames.append((rgba, im.info.get("duration", 40)))
    if i % 24 == 0:
        cov = sum(1 for v in fg.getdata() if v > 90)
        print("frame", i, "fg coverage:", cov)

# trim via percentile: rows/cols with <1.5% of peak coverage are limb outliers
import collections
rowc = collections.Counter()
colc = collections.Counter()
for f, _ in frames[::4]:
    a = f.split()[3].point(lambda v: 255 if v > 90 else 0)
    ap = a.load()
    for y in range(0, h, 2):
        n = sum(1 for x in range(0, w, 2) if ap[x, y] > 0)
        if n:
            rowc[y] += n
    for x in range(0, w, 2):
        n = sum(1 for y in range(0, h, 2) if ap[x, y] > 0)
        if n:
            colc[x] += n
maxr = max(rowc.values()); maxc = max(colc.values())
rows_ok = sorted(y for y, n in rowc.items() if n > maxr * 0.015)
cols_ok = sorted(x for x, n in colc.items() if n > maxc * 0.015)
ys, ye = rows_ok[0], rows_ok[-1]
xs, xe = cols_ok[0], cols_ok[-1]
print("travel bbox:", (xs, ys, xe, ye))

# --- per-frame tracking crop: window follows her centroid ---
WIN = 280  # source window size (square)

def centroid(f):
    a = f.split()[3]
    ap = a.load()
    sx = sy = n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if ap[x, y] > 90:
                sx += x; sy += y; n += 1
    if n == 0:
        return w // 2, h // 2
    return sx // n, sy // n

keep = frames[::4]
if keep[-1][0] is not frames[-1][0]:
    keep.append(frames[-1])

TH = 340
scale = 1.0  # replaced by tracking crop below

# (to_palette defined below, kept in place)

def to_palette(rgba_frame):
    """RGBA -> P mode with index 255 reserved for transparency."""
    alpha = rgba_frame.split()[3]
    mask = alpha.point(lambda a: 255 if a <= 120 else 0)
    p = rgba_frame.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
    p.paste(255, mask)
    p.info["transparency"] = 255
    return p

# alpha-repair: if a frame's silhouette collapsed (she pauses -> no temporal
# signal), inherit the previous good frame's alpha mask
def coverage(f):
    a = f.split()[3]
    return sum(1 for v in a.getdata() if v > 90)

MIN_COV = 3500
repaired = []
last_good_alpha = None
for f, dur in frames:
    cov = coverage(f)
    if cov < MIN_COV and last_good_alpha is not None:
        f = f.copy()
        f.putalpha(last_good_alpha)
        repaired.append(1)
    else:
        last_good_alpha = f.split()[3]
print("repaired frames:", len(repaired))
frames = [ (f, d) for (f, d), r in zip([(f, d) for (f, d) in frames], [0]*len(frames)) ]  # no-op keep structure

out = []
prev_cx = prev_cy = None
for f, dur in frames[::4]:
    cx, cy = centroid(f)
    if prev_cx is not None:
        cx = max(prev_cx - 30, min(prev_cx + 30, cx))
        cy = max(prev_cy - 30, min(prev_cy + 30, cy))
    prev_cx, prev_cy = cx, cy
    x0 = max(0, min(w - WIN, cx - WIN // 2))
    y0 = max(0, min(h - WIN, cy - WIN // 2))
    c = f.crop((x0, y0, x0 + WIN, y0 + WIN)).resize((TH, TH), Image.LANCZOS)
    out.append((to_palette(c), max(40, dur * 4)))
if out[-1][0] is not out[0][0] and len(out) < 2:
    pass

durs = [d for _, d in out]
print("out:", TH, "x", TH, len(out), "frames, loop", sum(durs), "ms")
out[0][0].save("res/drawable/gif_1.gif", save_all=True,
               append_images=[f for f, _ in out[1:]], duration=durs, loop=0,
               transparency=255, disposal=2)
import shutil, os
shutil.copy("res/drawable/gif_1.gif", "res/drawable/gif_2.gif")
shutil.copy("res/drawable/gif_1.gif", "res/drawable/gif_3.gif")
print("size:", os.path.getsize("res/drawable/gif_1.gif"), "bytes")

chk = Image.open("res/drawable/gif_1.gif"); chk.seek(6)
a = chk.convert("RGBA").split()[3]
px = a.load(); W, H = a.size
step = W // 8
for gy in range(0, H, step):
    row = ""
    for gx in range(0, W, step):
        n = sum(1 for y in range(gy, min(gy+step, H), 3) for x in range(gx, min(gx+step, W), 3) if px[x, y] > 90)
        tot = len(range(gy, min(gy+step, H), 3)) * len(range(gx, min(gx+step, W), 3))
        row += "##" if n > tot * 0.5 else ("++" if n > tot * 0.15 else "..")
    print(row)
