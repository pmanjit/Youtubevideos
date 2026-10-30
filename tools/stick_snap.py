"""
cold_snap — deterministic flat-vector frame engine.

Reproduces the user's art reference (stick-figure explainer) in code:
  * thick uniform black outlines, rounded caps, no taper
  * flat solid fills, zero gradients, zero shading
  * the sampled palette, locked as constants

Why code instead of an image model: this style is geometry. Code cannot drift,
cannot hallucinate limbs, never trips moderation, and renders 200+ frames in
seconds. Every frame in the film is reproducible from this file alone.

CLI:  python3 tools/stick_snap.py refs      # style test refs
      python3 tools/stick_snap.py demo      # hook frame 01
"""
import math
from PIL import Image, ImageDraw

# ---------------------------------------------------------------- palette (sampled)
INK      = (0, 0, 0)
PAPER    = (252, 253, 248)   # ref 2 background / snow light
CREAM    = (248, 241, 216)   # ref 2 face
BEIGE    = (229, 211, 186)   # ref 3 wall
BROWN    = (117, 80, 59)     # ref 3 floor
SLATE    = (122, 135, 145)   # ref 3 sofa
NAVY     = (30, 45, 80)      # ref 1 night sky / coat
ROCK     = (94, 86, 83)      # ref 1 cave wall
MUSTARD  = (241, 199, 104)   # ref 3 blanket / scarf
ORANGE   = (255, 132, 33)    # ref 1 flame
AMBER    = (255, 175, 75)    # ref 1 flame core
SNOW_SH  = (206, 216, 224)   # flat snow shadow (blue-grey, no gradient)
NIGHT_IN = (52, 66, 96)      # interior wall at night
WOOD     = (150, 116, 82)    # table / door handle warm wood
STEEL    = (150, 180, 190)   # water bottles

W, H = 1920, 1080
SS = 3.0                      # supersample factor -> antialiasing on downsample
LW = 9.0                      # uniform outline width at 1920px (measured 4-12 @1180)


class Canvas:
    def __init__(self, w=W, h=H, bg=PAPER):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (int(w * SS), int(h * SS)), bg)
        self.d = ImageDraw.Draw(self.img)

    # -- primitives -------------------------------------------------
    def line(self, pts, w=LW, color=INK):
        p = [(x * SS, y * SS) for x, y in pts]
        if len(p) > 1:
            self.d.line(p, fill=color, width=int(round(w * SS)), joint="curve")
        r = w * SS / 2.0          # round caps
        for x, y in (p[0], p[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    def circle(self, cx, cy, r, fill=None, outline=INK, w=LW):
        box = [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS]
        self.d.ellipse(box, fill=fill,
                       outline=outline if (outline is not None and w > 0) else None,
                       width=int(round(w * SS)))

    def poly(self, pts, fill=None, outline=INK, w=LW, caps=True):
        p = [(x * SS, y * SS) for x, y in pts]
        self.d.polygon(p, fill=fill)
        if outline is not None and w > 0:
            self.d.line(p + [p[0]], fill=outline, width=int(round(w * SS)), joint="curve")
            if caps:
                r = w * SS / 2.0
                for x, y in p:                      # round the joints
                    self.d.ellipse([x - r, y - r, x + r, y + r], fill=outline)

    def outlined(self, pts, fill, w=LW):
        """Fill plus a uniform outline that survives concave contours.

        Stroking a dense closed path with joint='curve' plugs narrow notches
        (finger gaps). Drawing the shape fat in ink and then filling the exact
        interior leaves a clean ring of width `w` outside the contour.
        """
        self.poly(pts, fill=INK, outline=INK, w=2 * w, caps=False)
        self.poly(pts, fill=fill, outline=None, w=0)

    def rect(self, x0, y0, x1, y1, fill=None, outline=INK, w=LW):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, w)

    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=INK, w=LW):
        """Rounded rectangle = the reference's hand/finger/pocket vocabulary."""
        self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS],
                                 radius=r * SS, fill=fill,
                                 outline=outline if (outline is not None and w > 0) else None,
                                 width=int(round(w * SS)))

    def bar(self, x, y, w_=60, h_=40, r=12, fill=None, outline=INK, w=LW):
        self.rrect(x - w_ / 2, y - h_ / 2, x + w_ / 2, y + h_ / 2, r, fill, outline, w)

    def save(self, path):
        out = self.img.resize((self.w, self.h), Image.LANCZOS)
        out.save(path, optimize=True)
        return path


# ---------------------------------------------------------------- the character
def stick_figure(c, x, ground, height=460, coat=NAVY, scarf=True, face="flat",
                 lean=0.0, leg_splay=0.055, hand_l=None, hand_r=None,
                 arm_style="hang", silhouette=False, hair=None, show_scarf_end=True):
    """One consistent 'YOU'. Every proportion is a fraction of `height`, so the
    silhouette is identical in every frame of the film.

    height   full height, feet to top of head
    hand_l/r optional (x, y) world targets for the blob hands (pose control)
    """
    h = height
    head_r   = 0.115 * h
    head_cy  = ground - h + head_r
    chin_y   = head_cy + head_r
    shoulder = chin_y + 0.055 * h
    hip      = ground - 0.46 * h
    hem      = hip + 0.02 * h
    lx       = lean * h * 0.10          # torso lean offset

    ink = INK
    body_fill = INK if silhouette else coat
    head_fill = INK if silhouette else CREAM

    # ---- legs (always visible below the coat hem)
    for sgn in (-1, 1):
        kx = x + sgn * leg_splay * h * 0.55 + lx * 0.4
        fx = x + sgn * leg_splay * h + lx * 0.2
        c.line([(x + lx * 0.3, hip + 0.01 * h), (kx, ground - 0.20 * h), (fx, ground - 0.012 * h)],
               w=LW)
        c.bar(fx, ground - 0.012 * h, w_=0.075 * h, h_=0.030 * h, r=0.012 * h,
              fill=ink, outline=None, w=0)          # foot

    # ---- coat: flat outlined block, shoulders to mid-thigh
    sw, hw = 0.072 * h, 0.088 * h
    c.poly([(x + lx - sw, shoulder), (x + lx + sw, shoulder),
            (x + lx * 1.3 + hw, hem), (x + lx * 1.3 - hw, hem)],
           fill=body_fill, outline=ink)
    if not silhouette:
        c.line([(x + lx, shoulder + 0.01 * h), (x + lx * 1.15, hem - 0.02 * h)],
               w=LW * 0.7)                            # coat opening

    # ---- arms (drawn over the coat so hands are never buried)
    shoulders = [(x + lx - sw * 0.78, shoulder + 0.012 * h),
                 (x + lx + sw * 0.78, shoulder + 0.012 * h)]
    hands = []
    for i, sgn in enumerate((-1, 1)):
        sh = shoulders[i]
        if i == 0 and hand_l:
            hand = hand_l
        elif i == 1 and hand_r:
            hand = hand_r
        elif arm_style == "hang":
            hand = (sh[0] + sgn * 0.072 * h, sh[1] + 0.225 * h)
        elif arm_style == "up":
            hand = (sh[0] + sgn * 0.075 * h, sh[1] - 0.10 * h)
        elif arm_style == "point":
            hand = (sh[0] + sgn * 0.12 * h, sh[1] - 0.02 * h)
        else:
            hand = (sh[0] + sgn * 0.055 * h, sh[1] + 0.235 * h)
        elbow = ((sh[0] + hand[0]) / 2 + sgn * 0.020 * h, (sh[1] + hand[1]) / 2)
        c.line([sh, elbow, hand], w=LW)
        c.circle(hand[0], hand[1], 0.026 * h, fill=ink, outline=None)
        hands.append(hand)

    # ---- neck + head
    c.line([(x + lx, chin_y - 0.02 * h), (x + lx, shoulder + 0.02 * h)], w=LW)
    c.circle(x + lx, head_cy, head_r, fill=head_fill, outline=ink)

    if silhouette:
        return {"head": (x + lx, head_cy), "hand_l": hands[0], "hand_r": hands[1],
                "head_r": head_r}

    # ---- face: minimal, exactly the reference vocabulary
    ex = head_r * 0.32
    ey = head_cy - head_r * 0.06
    for sgn in (-1, 1):
        c.circle(x + lx + sgn * ex, ey, head_r * 0.078, fill=INK, outline=None)
        by = ey - head_r * 0.34
        tilt = -head_r * 0.09 if face == "worried" else 0.0
        c.line([(x + lx + sgn * ex - head_r * 0.15, by + tilt),
                (x + lx + sgn * ex + head_r * 0.15, by)], w=LW * 0.78)

    my = head_cy + head_r * 0.46
    if face == "flat":
        c.line([(x + lx - head_r * 0.15, my), (x + lx + head_r * 0.15, my)], w=LW * 0.78)
    elif face == "worried":
        c.line([(x + lx - head_r * 0.17, my + head_r * 0.06),
                (x + lx, my - head_r * 0.03),
                (x + lx + head_r * 0.17, my + head_r * 0.06)], w=LW * 0.78)
    elif face == "smug":
        c.line([(x + lx - head_r * 0.19, my - head_r * 0.02),
                (x + lx + head_r * 0.17, my - head_r * 0.11)], w=LW * 0.78)
    elif face == "open":
        c.circle(x + lx, my, head_r * 0.13, fill=INK, outline=None)

    # ---- scarf: the recurring continuity token, tucked under the chin
    if scarf:
        by0, by1 = chin_y - 0.014 * h, chin_y + 0.028 * h
        hw_ = head_r * 0.70
        c.poly([(x + lx - hw_, by0), (x + lx + hw_, by0),
                (x + lx + hw_ * 0.96, by1), (x + lx - hw_ * 0.96, by1)],
               fill=MUSTARD, outline=INK)
        if show_scarf_end:
            c.poly([(x + lx - hw_ * 0.46, by1 - 0.004 * h), (x + lx - hw_ * 0.02, by1 - 0.004 * h),
                    (x + lx - hw_ * 0.20, by1 + 0.150 * h), (x + lx - hw_ * 0.58, by1 + 0.138 * h)],
                   fill=MUSTARD, outline=INK)

    if hair:
        for i in range(9):
            a = math.radians(-155 + i * 16)
            c.line([(x + lx + head_r * 0.92 * math.cos(a), head_cy + head_r * 0.92 * math.sin(a)),
                    (x + lx + head_r * 1.34 * math.cos(a), head_cy + head_r * 1.34 * math.sin(a))],
                   w=LW * 0.85, color=hair)

    return {"head": (x + lx, head_cy), "hand_l": hands[0], "hand_r": hands[1],
            "head_r": head_r}



def _arc(cx, cy, r, a0, a1, n=10):
    """Point list along an arc, used to round the fingertips of drawn shapes."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1))))
            for i in range(n)]


def hand_contour(hx, hy, scale=1.0, flip=False):
    """One continuous contour: wrist -> thumb -> four fingers -> wrist.

    Drawn as a single filled+stroked polygon so the black line follows the
    real finger notches instead of outlining four separate sausages.
    """
    s = scale
    d = -1 if flip else 1
    def X(dx): return hx + d * dx * s
    def Y(dy): return hy + dy * s

    palm_l, palm_r = -125, 125
    palm_top = 140
    wrist = 420
    fw, gap = 48, 24
    tips = (120, 170, 158, 104)          # index -> pinky
    x = palm_l + 6
    pts = [(X(palm_l), Y(wrist)), (X(palm_l), Y(286))]

    # thumb: a clean wedge off the palm's left edge, tip rounded by the joint
    pts += [(X(-186), Y(248)), (X(-198), Y(186)), (X(-152), Y(146)), (X(palm_l), Y(160))]

    # fingers
    for i, t in enumerate(tips):
        fx0 = x + i * (fw + gap)
        fx1 = fx0 + fw
        pts.append((X(fx0), Y(palm_top - 6)))
        pts.append((X(fx0), Y(palm_top - t)))
        pts += _arc(X(fx0 + fw / 2), Y(palm_top - t), fw / 2, 180, 0)
        pts.append((X(fx1), Y(palm_top - t)))
        pts.append((X(fx1), Y(palm_top - 6)))

    pts += [(X(palm_r), Y(150)), (X(palm_r), Y(wrist))]
    return pts


def distant_person(c, x, ground, height, tilt=0.0):
    """Readable silhouette at distance: head, shoulders, coat, two legs. No face."""
    h = height
    hx = x + tilt
    c.circle(hx, ground - h + 0.12 * h, 0.115 * h, fill=INK, outline=None)
    c.poly([(hx - 0.085 * h, ground - h * 0.72), (hx + 0.085 * h, ground - h * 0.72),
            (hx + 0.105 * h, ground - h * 0.40), (hx - 0.105 * h, ground - h * 0.40)],
           fill=INK, outline=None, w=0)
    for sgn in (-1, 1):
        c.line([(hx + sgn * 0.03 * h, ground - h * 0.42), (hx + sgn * 0.075 * h, ground)],
               w=0.045 * h, color=INK)
    c.line([(hx - 0.02 * h, ground - h * 0.70), (hx - 0.02 * h, ground + 0.01 * h)], w=0.038 * h,
           color=INK)


# ---------------------------------------------------------------- scenes
def paste_layer(dst, layer, x, y):
    """Blit a sub-canvas at (x, y); the layer's own bounds clip its contents."""
    dst.img.paste(layer.img, (int(x * SS), int(y * SS)))
    return dst


def scene_window_hook(path, n_figures=3):
    """FRAME 01 — hook A2: POV inside, glass scraped clear, figures out in the yard.

    Draw order matters: the window slab is painted first, the glass layer is
    pasted over it, then mullion + outlines. Painting the slab last would cover
    the pane (learned the hard way).
    """
    c = Canvas(bg=NIGHT_IN)
    gx0, gy0 = 150, 110
    gw, gh = 1600, 820
    gx1, gy1 = gx0 + gw, gy0 + gh
    fw = 42

    # ---- interior: wall + floor, nothing else
    c.rect(0, 940, W, H, fill=(40, 52, 76), w=0)
    c.line([(0, 940), (W, 940)], w=LW)

    # ---- window slab (glass sits on top of this)
    c.rrect(gx0 - fw, gy0 - fw, gx1 + fw, gy1 + fw, 12, fill=SLATE)

    # ---------------- glass layer (local 0..gw, 0..gh)
    g = Canvas(gw, gh, bg=NAVY)
    SNOW = (219, 228, 235)
    horizon = gh * 0.60
    g.poly([(0, horizon), (gw, horizon), (gw, gh), (0, gh)], fill=SNOW, outline=None, w=0)
    g.line([(0, horizon), (gw, horizon)], w=LW * 0.8)
    for sx, sy in ((0.16, 0.14), (0.29, 0.08), (0.52, 0.11), (0.68, 0.19),
                   (0.83, 0.09), (0.41, 0.27), (0.92, 0.24)):
        g.circle(gw * sx, gh * sy, 6, fill=PAPER, outline=None)

    for px, ph in ((0.07, 0.21), (0.125, 0.155)):
        bx, by = gw * px, horizon + 6
        for k in range(3):
            wgt = (3 - k) / 3.0
            g.poly([(bx - 44 * wgt, by - k * 42), (bx + 44 * wgt, by - k * 42),
                    (bx, by - k * 42 - 88 * wgt)], fill=(18, 27, 52), outline=None, w=0)

    for i in range(8):
        g.circle(gw * (0.30 + i * 0.026), gh - 40 - i * 34, 9, fill=(214, 222, 226), outline=None)

    spots = ((0.25, 0.30, 5), (0.43, 0.335, 0), (0.60, 0.29, -4), (0.72, 0.29, 2))
    for px, ph, tl in spots[:n_figures]:
        distant_person(g, gw * px, horizon + gh * 0.22, gh * ph, tilt=tl)

    # ---- frost: blobs straddling the pane edge + a second inward row
    def rim(side, n, rmin, rmax, phase):
        for i in range(n):
            t = (i + 0.5) / n
            r = rmin + (rmax - rmin) * (((i * 0.618) + phase) % 1.0)
            if side == "top":
                cx, cy = t * gw, r * 0.25
            elif side == "bottom":
                cx, cy = t * gw, gh - r * 0.25
            elif side == "left":
                cx, cy = r * 0.25, t * gh
            else:
                cx, cy = gw - r * 0.25, t * gh
            g.circle(cx, cy, r, fill=PAPER, outline=None)
    rim("top", 20, 46, 94, 0.00)
    rim("left", 9, 38, 84, 0.62)
    rim("right", 9, 38, 84, 0.17)
    rim("top", 15, 22, 46, 0.47)
    rim("left", 6, 18, 40, 0.73)
    rim("right", 6, 18, 40, 0.29)
    for cx, cy in ((0, 0), (gw, 0)):
        g.circle(cx, cy, 132, fill=PAPER, outline=None)
        g.circle(cx, cy, 86, fill=PAPER, outline=None)
    g.rect(0, gh - 12, gw, gh, fill=PAPER, outline=None, w=0)      # thin sill frost

    for i in range(14):
        side = i % 4
        t = (i * 0.618) % 1.0
        if side == 0:
            cx, cy, a = t * gw, 96 + 22 * (i % 3), 68
        elif side == 1:
            cx, cy, a = 104 + 22 * (i % 3), t * gh, 20
        elif side == 2:
            cx, cy, a = gw - 104 - 22 * (i % 3), t * gh, 160
        else:
            cx, cy, a = t * gw, gh - 96 - 22 * (i % 3), -68
        L = 34 + (i * 43) % 54
        ar = math.radians(a + ((i * 17) % 20) - 10)
        g.line([(cx, cy), (cx + L * math.cos(ar), cy + L * math.sin(ar))], w=5, color=PAPER)

    paste_layer(c, g, gx0, gy0)

    # ---------------- frame detail on top of the glass
    c.rect(gx0, gy0, gx1, gy1, fill=None, w=5)                             # pane opening
    c.rrect(gx0 - fw, gy0 - fw, gx1 + fw, gy1 + fw, 12, fill=None, w=LW)   # outer edge
    mx = gx0 + gw * 0.5
    c.rect(mx - 24, gy0, mx + 24, gy1, fill=SLATE)                         # vertical mullion
    c.rrect(gx0 - fw, gy1 + fw * 0.55, gx1 + fw, gy1 + fw * 1.7, 8, fill=SLATE)  # sill

    # ---------------- your breath: three flat puffs on the dark interior band
    for (bx, by, br) in ((300, 1006, 54), (368, 1022, 42), (242, 1028, 38)):
        c.circle(bx, by, br, fill=(226, 234, 238), outline=None)

    return c.save(path)



def scene_character_ref(path):
    c = Canvas(bg=PAPER)
    joints = stick_figure(c, 700, 940, height=760, face="flat", arm_style="hang",
                          hand_r=(880, 700))
    hx, hy = joints["hand_r"]
    hy += 42          # hang the lantern below the fist so the hand reads
    c.line([(hx, hy - 92), (hx, hy - 118)], w=LW)                       # wire to the hand
    c.rrect(hx - 62, hy - 44, hx + 62, hy + 110, 8, fill=(58, 62, 70))  # cap
    c.rect(hx - 62, hy - 6, hx + 62, hy + 74, fill=AMBER)               # glass glow
    c.rect(hx - 62, hy - 6, hx + 62, hy + 74, fill=None, w=LW * 0.7)
    c.poly([(hx - 4, hy + 58), (hx + 4, hy + 58), (hx + 18, hy + 20), (hx - 18, hy + 20)],
           fill=ORANGE, outline=None, w=0)
    c.rrect(hx - 62, hy + 74, hx + 62, hy + 110, 6, fill=(58, 62, 70))
    return c.save(path)


def scene_room_ref(path):
    """Interior anchor: the one sealed room. Flat elevation, reference staging."""
    c = Canvas(bg=NIGHT_IN)
    c.rect(0, 0, W, H, fill=(44, 58, 88))              # back wall
    c.rect(0, 862, W, H, fill=BROWN)                   # floor
    c.line([(0, 862), (W, 862)], w=LW)

    # ---- left: door with the mattress dragged against it
    c.rect(96, 250, 430, 862, fill=(84, 66, 50))       # door slab
    c.rect(120, 274, 406, 838, fill=None, w=LW * 0.7)  # panel line
    c.circle(380, 560, 15, fill=WOOD)                  # handle
    c.poly([(64, 300), (424, 318), (436, 880), (52, 866)], fill=SLATE)   # mattress
    c.poly([(64, 300), (424, 318), (424, 366), (64, 350)], fill=PAPER)   # sheet stripe
    for by in (470, 590, 710):
        c.circle(246, by, 9, fill=(104, 116, 126), outline=None)

    # ---- centre: table with three candles
    c.rect(786, 552, 1128, 588, fill=WOOD)             # top
    c.line([(812, 588), (812, 862)], w=LW)             # legs
    c.line([(1102, 588), (1102, 862)], w=LW)
    c.rect(834, 700, 1082, 716, fill=WOOD, w=LW * 0.6)  # brace
    for i, cx in enumerate((856, 958, 1060)):
        top = 452 - i * 14
        c.rect(cx - 26, top, cx + 26, 552, fill=PAPER)
        c.poly([(cx - 3, top - 52), (cx + 3, top - 52), (cx + 32, top - 4), (cx - 32, top - 4)],
               fill=ORANGE, outline=None, w=0)
        c.poly([(cx - 2, top - 30), (cx + 2, top - 30), (cx + 15, top - 6), (cx - 15, top - 6)],
               fill=AMBER, outline=None, w=0)

    # ---- right: the frost window (the only view of the outside)
    wx0, wy0, wx1, wy1 = 1470, 238, 1836, 676
    c.rrect(wx0 - 30, wy0 - 30, wx1 + 30, wy1 + 30, 8, fill=SLATE)
    g = Canvas(wx1 - wx0, wy1 - wy0, bg=NAVY)
    gw, gh = wx1 - wx0, wy1 - wy0
    for (sx, sy) in ((0.22, 0.18), (0.52, 0.10), (0.78, 0.24)):
        g.circle(gw * sx, gh * sy, 6, fill=PAPER, outline=None)
    g.poly([(0, gh * 0.72), (gw, gh * 0.72), (gw, gh), (0, gh)], fill=(219, 228, 235), outline=None, w=0)
    for i in range(14):
        t = (i + 0.5) / 14
        r = 26 + 26 * ((i * 0.618) % 1.0)
        g.circle(t * gw, r * 0.3, r, fill=PAPER, outline=None)
        g.circle(r * 0.3, t * gh, r * 0.8, fill=PAPER, outline=None)
        g.circle(gw - r * 0.3, t * gh, r * 0.8, fill=PAPER, outline=None)
    g.rect(gw * 0.5 - 12, 0, gw * 0.5 + 12, gh, fill=SLATE)
    paste_layer(c, g, wx0, wy0)
    c.rect(wx0 - 30, wy0 - 30, wx1 + 30, wy1 + 30, fill=None, w=LW)

    # ---- wall: a real thermometer (tube + bulb + ticks), needle near the bottom
    tx, ty = 1196, 168
    c.rrect(tx - 20, ty, tx + 20, ty + 190, 20, fill=PAPER)
    c.circle(tx, ty + 200, 30, fill=PAPER)
    c.circle(tx, ty + 200, 18, fill=(196, 62, 48), outline=None)
    c.rrect(tx - 7, ty + 108, tx + 7, ty + 190, 7, fill=(196, 62, 48), outline=None)
    for i in range(6):
        c.line([(tx + 24, ty + 24 + i * 26), (tx + 44, ty + 24 + i * 26)], w=LW * 0.45)

    # ---- empty cupboard, doors hanging open
    c.rect(1252, 340, 1432, 862, fill=(96, 80, 64))
    c.line([(1342, 340), (1342, 862)], w=LW)
    c.circle(1298, 590, 11, fill=INK, outline=None)
    c.circle(1386, 590, 11, fill=INK, outline=None)
    c.rect(1252, 340, 1432, 862, fill=None, w=LW)

    # ---- water bottles on the floor
    for bx in (880, 936):
        c.rrect(bx, 742, bx + 48, 862, 10, fill=STEEL)

    # ---- you, standing in the cold room
    stick_figure(c, 596, 906, height=440, face="worried", leg_splay=0.05)
    return c.save(path)


if __name__ == "__main__":
    import sys, os
    os.makedirs("refs", exist_ok=True)
    os.makedirs("frames", exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        print(scene_window_hook("frames/beat01m01.png"))
    else:
        print(scene_character_ref("refs/ref01_character.png"))
        print(scene_window_hook("refs/ref02_window_hook.png"))
        print(scene_room_ref("refs/ref03_interior_room.png"))
