"""Build Reimu splash gif: 50 frames, compact loop, strict palette safety.
Kept small - user wants everything shorter/tighter.
"""
from PIL import Image

im = Image.open('/tmp/f_reimu.gif')
N = im.n_frames
W, H = im.size
print('src:', im.size, N, 'frames')

frames = []
for i in range(N):
    im.seek(i)
    dur = im.info.get('duration', 33)
    f = im.convert('RGBA')
    frames.append((f, dur))

def to_palette(rgba_frame):
    alpha = rgba_frame.split()[3]
    mask = alpha.point(lambda a: 255 if a <= 100 else 0)
    rgb = rgba_frame.convert('RGB')
    p = rgb.quantize(colors=255, method=Image.MEDIANCUT, dither=Image.NONE)
    pal = p.getpalette() or []
    pal = pal + [0] * (3 * 256 - len(pal))
    p.putpalette(pal)
    p.paste(255, mask)
    p.info['transparency'] = 255
    return p

out = [(to_palette(f), d) for f, d in frames]

# safety: all indices < 256
bad = 0
for p, _ in out:
    px = p.load()
    mx = max(px[x, y] for y in range(0, p.size[1], 3) for x in range(0, p.size[0], 3))
    if mx >= 256:
        bad += 1
print('frames with bad idx:', bad)
assert bad == 0

durs = [d for _, d in out]
print('loop:', sum(durs), 'ms,', len(out), 'frames, 200x112')
out[0][0].save('res/drawable/gif_1.gif', save_all=True,
               append_images=[f for f, _ in out[1:]], duration=durs, loop=0,
               transparency=255, disposal=2, optimize=False)
import shutil, os
shutil.copy('res/drawable/gif_1.gif', 'res/drawable/gif_2.gif')
shutil.copy('res/drawable/gif_1.gif', 'res/drawable/gif_3.gif')
print('size:', os.path.getsize('res/drawable/gif_1.gif'))
