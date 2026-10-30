"""Contact sheet builder — used for style refs and for per-batch frame QC.

Usage:
    python3 tools/contact_sheet.py out.png thumb_px img1.png img2.png ...
    python3 tools/contact_sheet.py out.png 380 frames/*.png
"""
import sys
from PIL import Image, ImageDraw

def build(out, thumb_w, paths, cols=4, pad=10, bg=(24, 28, 34), label_h=0):
    cols = min(cols, max(1, len(paths)))
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        r = thumb_w / im.width
        thumbs.append(im.resize((thumb_w, max(1, int(im.height * r))), Image.LANCZOS))
    rows = (len(thumbs) + cols - 1) // cols
    th = max(t.height for t in thumbs)
    cw, ch = thumb_w + pad, th + pad + label_h
    sheet = Image.new("RGB", (pad + cols * cw, pad + rows * ch), bg)
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(thumbs):
        x = pad + (i % cols) * cw
        y = pad + (i // cols) * ch
        sheet.paste(t, (x, y))
        d.rectangle([x, y, x + t.width, y + t.height], outline=(90, 100, 112))
    sheet.save(out, optimize=True)
    return out

if __name__ == "__main__":
    out = sys.argv[1]
    tw = int(sys.argv[2])
    print(build(out, tw, sys.argv[3:]))
