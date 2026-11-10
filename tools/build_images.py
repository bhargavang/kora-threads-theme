"""
Draws the demo product illustrations as SVG.

For every product in catalogue.py it writes one flat-lay picture per
colour and one close-up of the print, plus the two theme illustrations
(homepage hero and the Shop the look image). render_images.mjs then
turns them into JPEGs.

    python3 tools/build_images.py      # writes tools/.build/svg/*.svg
    node tools/render_images.mjs       # writes the JPEGs

Everything is drawn from code: no stock photos, nothing to license.
"""

import json
import math
import random
from pathlib import Path

from catalogue import PRODUCTS, detail_name, image_name

ROOT = Path(__file__).resolve().parent
OUT = ROOT / ".build" / "svg"

W, H = 1000, 1250  # product images are 4:5
BG = "#ECE4D6"


# ---------------------------------------------------------------- colour


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    ra, ga, ba = hex_to_rgb(a)
    rb, gb, bb = hex_to_rgb(b)
    return "#{:02X}{:02X}{:02X}".format(
        round(ra + (rb - ra) * t), round(ga + (gb - ga) * t), round(ba + (bb - ba) * t)
    )


def darker(c, t=0.25):
    return mix(c, "#000000", t)


def lighter(c, t=0.25):
    return mix(c, "#FFFFFF", t)


def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def pt(p):
    return f"{f(p[0])} {f(p[1])}"


# ------------------------------------------------------------- symmetry


def mirror(p):
    return (W - p[0], p[1])


def sym_path(start, segments, neck_depth=0.0, neck_type="curve"):
    """
    Build a left-right symmetric outline.
    `segments` trace the left half from `start` (left neck point) down to a
    point on the centre line. The right half is mirrored back up, and the
    neckline closes the shape.
    """
    d = [f"M {pt(start)}"]
    points = [start]
    for seg in segments:
        kind, *ps = seg
        d.append(kind + " " + " ".join(pt(p) for p in ps))
        points.append(ps[-1])
    for i in range(len(segments) - 1, -1, -1):
        kind, *ps = segments[i]
        prev = points[i]
        if kind == "L":
            d.append(f"L {pt(mirror(prev))}")
        elif kind == "C":
            d.append(f"C {pt(mirror(ps[1]))} {pt(mirror(ps[0]))} {pt(mirror(prev))}")
        elif kind == "Q":
            d.append(f"Q {pt(mirror(ps[0]))} {pt(mirror(prev))}")
    end = mirror(start)
    if neck_type == "v":
        d.append(f"L {pt((W / 2, start[1] + neck_depth))} L {pt(start)}")
    else:
        k = (end[0] - start[0]) * 0.2
        d.append(
            f"C {pt((end[0] - k, start[1] + neck_depth))} {pt((start[0] + k, start[1] + neck_depth))} {pt(start)}"
        )
    d.append("Z")
    return " ".join(d)


def both(points):
    """A polyline and its mirror image, as two path strings."""
    left = "M " + " L ".join(pt(p) for p in points)
    right = "M " + " L ".join(pt(mirror(p)) for p in points)
    return [left, right]


# -------------------------------------------------------------- patterns


def petal_flower(cx, cy, r, fill, centre=None, petals=5, rot=0):
    out = []
    for i in range(petals):
        a = rot + i * 360 / petals
        out.append(
            f'<ellipse cx="{f(cx)}" cy="{f(cy - r * 0.55)}" rx="{f(r * 0.34)}" ry="{f(r * 0.5)}" '
            f'transform="rotate({f(a)} {f(cx)} {f(cy)})" fill="{fill}"/>'
        )
    if centre:
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * 0.2)}" fill="{centre}"/>')
    return "".join(out)


def paisley(x, y, s, fill, rot=0, inner=None):
    d = (
        f"M 0 {-18*s} C {12*s} {-18*s} {17*s} {-2*s} {9*s} {10*s} "
        f"C {3*s} {18*s} {-10*s} {19*s} {-13*s} {8*s} "
        f"C {-15*s} {-1*s} {-9*s} {-6*s} {-3*s} {-6*s} "
        f"C {3*s} {-6*s} {5*s} {1*s} {1*s} {4*s} "
        f"C {-2*s} {-3*s} {-6*s} {-12*s} 0 {-18*s} Z"
    )
    g = f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)})"><path d="{d}" fill="{fill}"/>'
    if inner:
        g += f'<circle cx="{f(-4*s)}" cy="{f(6*s)}" r="{f(3*s)}" fill="{inner}"/>'
    return g + "</g>"


def pattern(pid, size, content, w=None):
    w = w or size
    return f'<pattern id="{pid}" width="{f(w)}" height="{f(size)}" patternUnits="userSpaceOnUse">{content}</pattern>'


def make_print(kind, pid, ground, motif, accent, scale=1.0):
    """Returns a <pattern> drawn over the fabric colour."""
    s = scale
    if kind == "booti":
        size = 66 * s
        c = petal_flower(16 * s, 16 * s, 15 * s, motif, centre=accent)
        c += petal_flower(49 * s, 49 * s, 15 * s, motif, centre=accent, rot=36)
        c += f'<circle cx="{f(49*s)}" cy="{f(16*s)}" r="{f(2.2*s)}" fill="{motif}"/>'
        c += f'<circle cx="{f(16*s)}" cy="{f(49*s)}" r="{f(2.2*s)}" fill="{motif}"/>'
        return pattern(pid, size, c)
    if kind == "dabu":
        size = 30 * s
        c = f'<circle cx="{f(7*s)}" cy="{f(7*s)}" r="{f(3.4*s)}" fill="{motif}" opacity=".9"/>'
        c += f'<circle cx="{f(22*s)}" cy="{f(22*s)}" r="{f(2.6*s)}" fill="{motif}" opacity=".8"/>'
        return pattern(pid, size, c)
    if kind == "buta":
        size = 72 * s
        c = paisley(20 * s, 22 * s, 0.85 * s, motif, rot=-20, inner=accent)
        c += paisley(56 * s, 58 * s, 0.85 * s, motif, rot=160, inner=accent)
        c += f'<circle cx="{f(56*s)}" cy="{f(18*s)}" r="{f(2*s)}" fill="{motif}"/>'
        c += f'<circle cx="{f(18*s)}" cy="{f(56*s)}" r="{f(2*s)}" fill="{motif}"/>'
        return pattern(pid, size, c)
    if kind == "floral":
        size = 120 * s
        c = petal_flower(32 * s, 32 * s, 28 * s, motif, centre=accent, petals=6)
        c += f'<circle cx="{f(32*s)}" cy="{f(32*s)}" r="{f(3*s)}" fill="{motif}"/>'
        for a in (35, 215):
            c += (
                f'<ellipse cx="{f(32*s)}" cy="{f(2*s)}" rx="{f(5*s)}" ry="{f(11*s)}" fill="{motif}" opacity=".85" '
                f'transform="rotate({a} {f(32*s)} {f(32*s)}) translate(0 {f(-8*s)})"/>'
            )
        c += petal_flower(92 * s, 90 * s, 16 * s, motif, centre=accent, petals=5, rot=20)
        c += f'<circle cx="{f(92*s)}" cy="{f(32*s)}" r="{f(3*s)}" fill="{motif}"/>'
        c += f'<circle cx="{f(32*s)}" cy="{f(92*s)}" r="{f(3*s)}" fill="{motif}"/>'
        return pattern(pid, size, c)
    if kind == "kalamkari":
        size = 170 * s
        c = petal_flower(45 * s, 45 * s, 40 * s, motif, centre=None, petals=8)
        c += petal_flower(45 * s, 45 * s, 22 * s, accent, centre=motif, petals=8, rot=22)
        c += paisley(125 * s, 120 * s, 2.1 * s, motif, rot=35, inner=accent)
        c += paisley(125 * s, 30 * s, 1.0 * s, accent, rot=-60)
        c += paisley(40 * s, 135 * s, 1.0 * s, accent, rot=120)
        for x, y in ((95 * s, 70 * s), (150 * s, 165 * s), (10 * s, 100 * s), (80 * s, 160 * s)):
            c += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(3*s)}" fill="{motif}"/>'
        return pattern(pid, size, c)
    if kind == "ajrakh":
        size = 76 * s
        h = size / 2
        sq = 15 * s
        c = (
            f'<rect x="{f(h-sq)}" y="{f(h-sq)}" width="{f(2*sq)}" height="{f(2*sq)}" fill="{motif}"/>'
            f'<rect x="{f(h-sq)}" y="{f(h-sq)}" width="{f(2*sq)}" height="{f(2*sq)}" fill="{motif}" transform="rotate(45 {f(h)} {f(h)})"/>'
            f'<circle cx="{f(h)}" cy="{f(h)}" r="{f(8*s)}" fill="{accent}"/>'
            f'<circle cx="{f(h)}" cy="{f(h)}" r="{f(3.5*s)}" fill="{ground}"/>'
        )
        for x, y in ((0, 0), (size, 0), (0, size), (size, size)):
            c += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(9*s)}" fill="{accent}"/>'
            c += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(4*s)}" fill="{motif}"/>'
        for x, y in ((h, 0), (0, h), (size, h), (h, size)):
            c += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(2.2*s)}" fill="{accent}"/>'
        return pattern(pid, size, c)
    if kind == "chikan":
        size = 110 * s
        vine = f"M {f(10*s)} {f(100*s)} C {f(40*s)} {f(70*s)} {f(20*s)} {f(40*s)} {f(55*s)} {f(20*s)} S {f(95*s)} {f(10*s)} {f(100*s)} {f(-5*s)}"
        c = f'<path d="{vine}" fill="none" stroke="{motif}" stroke-width="{f(2*s)}" stroke-linecap="round"/>'
        for x, y, a in ((26 * s, 70 * s, -30), (34 * s, 42 * s, 40), (62 * s, 18 * s, -50), (84 * s, 12 * s, 30)):
            c += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(3*s)}" ry="{f(7*s)}" fill="none" stroke="{motif}" stroke-width="{f(1.6*s)}" transform="rotate({a} {f(x)} {f(y)})"/>'
        c += petal_flower(78 * s, 72 * s, 13 * s, "none", centre=motif)
        for i in range(5):
            a = i * 72
            c += (
                f'<ellipse cx="{f(78*s)}" cy="{f(64.8*s)}" rx="{f(4*s)}" ry="{f(6*s)}" fill="none" stroke="{motif}" stroke-width="{f(1.6*s)}" '
                f'transform="rotate({a} {f(78*s)} {f(72*s)})"/>'
            )
        for x, y in ((12 * s, 22 * s), (20 * s, 28 * s), (16 * s, 34 * s)):
            c += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(1.8*s)}" fill="{motif}"/>'
        return pattern(pid, size, c)
    if kind == "herringbone":
        size = 22 * s
        c = (
            f'<path d="M 0 0 L {f(11*s)} {f(11*s)} L 0 {f(22*s)} M {f(11*s)} 0 L {f(22*s)} {f(11*s)} L {f(11*s)} {f(22*s)}" '
            f'fill="none" stroke="{motif}" stroke-width="{f(1.6*s)}" opacity=".9"/>'
        )
        return pattern(pid, size, c)
    if kind == "slub":
        size = 180 * s
        rnd = random.Random(pid)
        c = ""
        for _ in range(44):
            y = rnd.uniform(0, size)
            x = rnd.uniform(-20, size)
            ln = rnd.uniform(20, 90) * s
            op = rnd.uniform(0.25, 0.7)
            sw = rnd.uniform(1.2, 2.6) * s
            c += f'<path d="M {f(x)} {f(y)} h {f(ln)}" stroke="{motif}" stroke-width="{f(sw)}" stroke-linecap="round" opacity="{op:.2f}"/>'
        return pattern(pid, size, c)
    if kind == "border":
        size = 44 * s
        c = (
            f'<rect width="{f(size)}" height="{f(size)}" fill="{accent}"/>'
            f'<path d="M 0 {f(30*s)} L {f(11*s)} {f(14*s)} L {f(22*s)} {f(30*s)} L {f(33*s)} {f(14*s)} L {f(44*s)} {f(30*s)}" fill="none" stroke="{motif}" stroke-width="{f(3*s)}"/>'
            f'<circle cx="{f(11*s)}" cy="{f(36*s)}" r="{f(2.4*s)}" fill="{motif}"/>'
            f'<circle cx="{f(33*s)}" cy="{f(36*s)}" r="{f(2.4*s)}" fill="{motif}"/>'
            f'<rect y="{f(4*s)}" width="{f(size)}" height="{f(2.4*s)}" fill="{motif}"/>'
        )
        return pattern(pid, size, c)
    raise ValueError(kind)


def common_defs():
    return f"""
    <filter id="soft-shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="16"/>
      <feOffset dx="8" dy="18" result="o"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.30"/></feComponentTransfer>
    </filter>
    <filter id="tight-shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
      <feOffset dx="1" dy="3"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.25"/></feComponentTransfer>
    </filter>
    <linearGradient id="shade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity=".16"/>
      <stop offset=".45" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".16"/>
    </linearGradient>
    <radialGradient id="vignette" cx=".5" cy=".42" r=".75">
      <stop offset=".55" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".10"/>
    </radialGradient>
    <pattern id="linen" width="6" height="6" patternUnits="userSpaceOnUse">
      <path d="M 0 0.5 H 6 M 0.5 0 V 6" stroke="#6B5A44" stroke-width=".6" opacity=".10"/>
    </pattern>
    """


def background(w, h, colour=BG):
    return (
        f'<rect width="{w}" height="{h}" fill="{colour}"/>'
        f'<rect width="{w}" height="{h}" fill="url(#linen)"/>'
        f'<rect width="{w}" height="{h}" fill="url(#vignette)"/>'
    )


# ------------------------------------------------------------ garment kit


class Kit:
    """Collects <defs> and drawing for one picture."""

    def __init__(self, uid):
        self.uid = uid
        self.defs = []
        self.n = 0

    def id(self, name):
        self.n += 1
        return f"{self.uid}-{name}-{self.n}"

    def piece(self, d, colour, print_fill=None, details="", band=None, edge_band=None, shadow=True):
        """One garment piece: shadow, fabric, print, optional bands, shading, details."""
        clip = self.id("clip")
        self.defs.append(f'<clipPath id="{clip}"><path d="{d}"/></clipPath>')
        out = []
        if shadow:
            out.append(f'<path d="{d}" fill="#000" filter="url(#soft-shadow)"/>')
        out.append(f'<path d="{d}" fill="{colour}"/>')
        if print_fill:
            out.append(f'<path d="{d}" fill="{print_fill}"/>')
        if band:
            out.append(f'<g clip-path="url(#{clip})">{band}</g>')
        if edge_band:
            out.append(
                f'<path d="{d}" fill="none" stroke="{edge_band}" stroke-width="40" clip-path="url(#{clip})"/>'
            )
        out.append(f'<path d="{d}" fill="url(#shade)"/>')
        if details:
            out.append(f'<g clip-path="url(#{clip})">{details}</g>')
        out.append(f'<path d="{d}" fill="none" stroke="{darker(colour, 0.35)}" stroke-width="1.4" opacity=".45"/>')
        return "".join(out)

    def print_fill(self, kind, colour, scale=1.0):
        if not kind:
            return None
        pid = self.id(kind)
        self.defs.append(make_print(kind, pid, colour["hex"], colour["motif"], colour["accent"], scale))
        return f"url(#{pid})"

    def border_fill(self, colour, scale=1.0):
        pid = self.id("border")
        self.defs.append(make_print("border", pid, colour["hex"], colour["motif"], colour["accent"], scale))
        return f"url(#{pid})"


def strokes(paths, colour, width=2.0, opacity=0.18, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return "".join(
        f'<path d="{p}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" opacity="{opacity}"{dash_attr}/>'
        for p in paths
    )


def buttons(xs_ys, colour, r=6.5):
    return "".join(
        f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{colour}" filter="url(#tight-shadow)"/>'
        f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{colour}"/>'
        f'<circle cx="{f(x - 1.8)}" cy="{f(y)}" r="1" fill="{darker(colour, .4)}"/>'
        f'<circle cx="{f(x + 1.8)}" cy="{f(y)}" r="1" fill="{darker(colour, .4)}"/>'
        for x, y in xs_ys
    )


# ---------------------------------------------------------------- garments


def kurta(kit, c, kind, hem=1075, neck_buttons=True, yoke=False):
    start = (452, 190)
    segs = [
        ("L", (358, 208)),
        ("C", (330, 280), (268, 400), (236, 468)),
        ("L", (306, 500)),
        ("C", (330, 440), (362, 380), (386, 338)),
        ("C", (384, 420), (380, 500), (382, 560)),
        ("L", (336, hem)),
        ("Q", (420, hem + 10), (500, hem + 12)),
    ]
    d = sym_path(start, segs, neck_depth=62)
    fabric = c["hex"]
    line = darker(fabric, 0.45)
    pf = kit.print_fill(kind, c)
    band = f'<rect x="0" y="{hem - 46}" width="{W}" height="70" fill="{kit.border_fill(c)}"/>'
    # cuff bands follow the sleeve end
    for cuff in (((236, 468), (306, 500)), (mirror((236, 468)), mirror((306, 500)))):
        (x1, y1), (x2, y2) = cuff
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        band += (
            f'<rect x="{f(x1 - 10)}" y="{f(y1 - 34)}" width="{f(math.dist(cuff[0], cuff[1]) + 20)}" height="38" '
            f'fill="{kit.border_fill(c)}" transform="rotate({f(ang)} {f(x1)} {f(y1)})"/>'
        )
    det = strokes(both([(392, 620), (380, 900), (372, 1040)]) + both([(300, 300), (280, 400)]), line, 2.2, 0.16)
    # side slits
    det += strokes(both([(347, hem - 210), (336, hem + 4)]), BG, 4, 1)
    # neck facing
    det += f'<path d="M 446 186 C 470 262 530 262 554 186" fill="none" stroke="{line}" stroke-width="2" opacity=".35"/>'
    if neck_buttons:
        det += strokes(["M 500 250 L 500 372"], line, 2, 0.35)
        det += buttons([(500, 276), (500, 312), (500, 348)], c["accent"], 5.5)
    if yoke:
        det += f'<path d="M 396 214 C 440 330 560 330 604 214" fill="none" stroke="{c["motif"]}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" opacity=".9"/>'
        det += f'<path d="M 410 226 C 450 312 550 312 590 226" fill="none" stroke="{c["motif"]}" stroke-width="2" opacity=".8"/>'
    return kit.piece(d, fabric, pf, det, band=band if kind in ("booti", "dabu") else None)


def straight_pants(kit, c, kind, colour_hex=None):
    fabric = colour_hex or c["hex"]
    start = (395, 230)
    segs = [
        ("L", (390, 290)),
        ("C", (375, 600), (368, 900), (360, 1110)),
        ("L", (480, 1118)),
        ("L", (500, 540)),
    ]
    d = sym_path(start, segs, neck_depth=0)
    line = darker(fabric, 0.4)
    det = f'<rect x="380" y="226" width="240" height="44" fill="{darker(fabric, .06)}"/>'
    det += strokes([f"M {x} 232 L {x + 3} 266" for x in range(398, 604, 14)], line, 1.6, 0.25)
    det += strokes(both([(430, 320), (420, 1000)]), line, 2, 0.14)
    pf = kit.print_fill(kind, c) if kind else None
    return kit.piece(d, fabric, pf, det)


def palazzo(kit, c, kind):
    fabric = c["hex"]
    start = (352, 230)
    segs = [
        ("L", (348, 300)),
        ("C", (300, 600), (260, 900), (232, 1110)),
        ("L", (480, 1120)),
        ("L", (502, 580)),
    ]
    d = sym_path(start, segs, neck_depth=0)
    line = darker(fabric, 0.45)
    det = f'<rect x="330" y="226" width="340" height="62" fill="{darker(fabric, .07)}"/>'
    det += strokes([f"M {x} 232 L {x + 4} 282" for x in range(356, 650, 13)], line, 1.6, 0.25)
    det += strokes(both([(400, 320), (330, 1080)]) + both([(450, 330), (420, 1090)]) + both([(360, 520), (300, 1000)]), line, 2.2, 0.15)
    pf = kit.print_fill(kind, c, 0.9)
    out = kit.piece(d, fabric, pf, det)
    # drawstring with tassels, drawn outside the clip
    tie = c["accent"]
    out += (
        f'<path d="M 488 262 C 470 320 460 360 452 410" fill="none" stroke="{tie}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M 512 262 C 520 320 540 360 548 420" fill="none" stroke="{tie}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M 452 410 l -8 36 M 452 410 l 0 38 M 452 410 l 8 36" stroke="{tie}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 548 420 l -8 36 M 548 420 l 0 38 M 548 420 l 8 36" stroke="{tie}" stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="452" cy="410" r="7" fill="{tie}"/><circle cx="548" cy="420" r="7" fill="{tie}"/>'
    )
    return out


def coord_top(kit, c, kind):
    fabric = c["hex"]
    start = (450, 190)
    segs = [
        ("L", (335, 212)),
        ("C", (300, 250), (268, 300), (240, 360)),
        ("L", (316, 398)),
        ("C", (330, 372), (350, 350), (372, 338)),
        ("L", (360, 610)),
        ("Q", (430, 618), (500, 620)),
    ]
    d = sym_path(start, segs, neck_depth=52)
    line = darker(fabric, 0.4)
    det = strokes(both([(400, 400), (392, 590)]) + both([(272, 330), (300, 372)]), line, 2.2, 0.18)
    det += f'<path d="M 444 186 C 468 250 532 250 556 186" fill="none" stroke="{line}" stroke-width="2" opacity=".35"/>'
    det += strokes(both([(245, 350), (320, 388)]), line, 2, 0.3, dash="1 6")
    det += strokes(["M 362 590 Q 500 602 638 590"], line, 2, 0.3, dash="1 6")
    return kit.piece(d, fabric, kit.print_fill(kind, c), det)


def maxi(kit, c, kind):
    fabric = c["hex"]
    start = (455, 195)
    segs = [
        ("L", (382, 212)),
        ("C", (350, 232), (318, 262), (298, 300)),
        ("C", (330, 316), (362, 320), (390, 312)),
        ("L", (392, 470)),
        ("L", (366, 678)),
        ("L", (356, 683)),
        ("L", (326, 898)),
        ("L", (314, 903)),
        ("L", (272, 1140)),
        ("Q", (380, 1152), (500, 1156)),
    ]
    d = sym_path(start, segs, neck_depth=86, neck_type="v")
    line = darker(fabric, 0.45)
    det = ""
    for y, x0, x1 in ((470, 392, 608), (681, 356, 644), (901, 314, 686)):
        det += strokes([f"M {x0 - 20} {y} L {x1 + 20} {y}"], line, 2.4, 0.35)
        det += strokes([f"M {x} {y + 4} L {x + 2} {y + 38}" for x in range(x0 + 8, x1 - 4, 16)], line, 1.6, 0.22)
    det += strokes(both([(420, 720), (400, 880)]) + both([(400, 940), (370, 1120)]) + both([(460, 950), (450, 1130)]), line, 2, 0.14)
    det += strokes(both([(300, 302), (330, 314), (360, 316)]), line, 2, 0.3, dash="1 6")
    det += f'<path d="M 455 195 L 500 281 L 545 195" fill="none" stroke="{line}" stroke-width="2" opacity=".35"/>'
    return kit.piece(d, fabric, kit.print_fill(kind, c), det)


def wrap_dress(kit, c, kind):
    fabric = c["hex"]
    start = (455, 195)
    segs = [
        ("L", (372, 214)),
        ("C", (345, 300), (300, 400), (276, 470)),
        ("L", (344, 496)),
        ("C", (360, 440), (380, 390), (396, 350)),
        ("L", (402, 500)),
        ("C", (370, 700), (325, 900), (288, 1110)),
        ("Q", (390, 1128), (500, 1132)),
    ]
    d = sym_path(start, segs, neck_depth=170, neck_type="v")
    line = darker(fabric, 0.5)
    det = f'<path d="M 545 195 C 520 300 470 430 404 500" fill="none" stroke="{line}" stroke-width="3" opacity=".45"/>'
    det += f'<path d="M 404 500 C 420 700 430 900 410 1120" fill="none" stroke="{line}" stroke-width="3" opacity=".4"/>'
    det += f'<rect x="380" y="488" width="240" height="26" fill="{darker(fabric, .1)}"/>'
    det += strokes(both([(560, 600), (600, 1100)]) + both([(470, 560), (480, 1110)]), line, 2, 0.14)
    det += strokes(both([(282, 452), (348, 478)]), line, 2, 0.3, dash="1 6")
    out = kit.piece(d, fabric, kit.print_fill(kind, c, 0.85), det)
    # waist tie: knot and two tails, on top of the dress
    tie_d = "M 388 500 C 350 560 330 640 340 720 L 362 716 C 356 640 372 570 404 512 Z M 396 504 C 380 580 400 660 430 730 L 450 720 C 422 660 408 590 410 510 Z"
    out += kit.piece(tie_d, fabric, kit.print_fill(kind, c, 0.85), shadow=True)
    out += f'<ellipse cx="398" cy="502" rx="20" ry="16" fill="{darker(fabric, .12)}"/>'
    return out


def dupatta(kit, c, kind):
    fabric = c["hex"]
    d = "M 332 118 L 668 136 C 690 420 650 760 690 1128 L 350 1146 C 318 800 356 460 332 118 Z"
    line = darker(fabric, 0.45)
    pf = kit.print_fill(kind, c, 0.8)
    bf = kit.border_fill(c, 1.3)
    band = f'<rect x="250" y="80" width="520" height="110" fill="{bf}" transform="rotate(3 500 130)"/>'
    band += f'<rect x="250" y="1062" width="520" height="110" fill="{bf}" transform="rotate(-3 500 1120)"/>'
    det = strokes(["M 430 200 C 450 500 420 800 450 1060", "M 580 210 C 560 500 600 800 590 1060"], line, 2.4, 0.15)
    det += f'<path d="M 332 118 L 668 136 L 640 300 C 560 250 430 260 332 118 Z" fill="#fff" opacity=".08"/>'
    out = kit.piece(d, fabric, pf, det, band=band, edge_band=c["accent"])
    # tassels along the bottom edge
    for i in range(14):
        t = i / 13
        x = 352 + (688 - 352) * t
        y = 1146 + (1128 - 1146) * t
        out += f'<path d="M {f(x)} {f(y)} l 0 34" stroke="{c["motif"]}" stroke-width="3" stroke-linecap="round"/>'
        out += f'<circle cx="{f(x)}" cy="{f(y + 38)}" r="5" fill="{c["accent"]}"/>'
    return out


def shirt(kit, c, kind, collar="band"):
    fabric = c["hex"]
    hem = 940
    start = (442, 214)
    segs = [
        ("L", (316, 240)),
        ("C", (286, 400), (236, 620), (192, 800)),
        ("L", (266, 828)),
        ("C", (300, 680), (338, 520), (366, 392)),
        ("L", (362, hem - 56)),
        ("C", (390, hem + 10), (450, hem + 20), (500, hem + 20)),
    ]
    d = sym_path(start, segs, neck_depth=30)
    line = darker(fabric, 0.45)
    pf = kit.print_fill(kind, c, 0.8 if kind == "ajrakh" else 1.0)
    det = f'<rect x="486" y="236" width="28" height="{hem}" fill="{darker(fabric, .05)}"/>'
    det += strokes([f"M 486 236 L 486 {hem + 30}", f"M 514 236 L 514 {hem + 30}"], line, 1.6, 0.3)
    det += strokes(both([(200, 768), (274, 794)]), line, 2.2, 0.35)
    det += strokes(both([(400, 430), (392, 900)]) + both([(296, 480), (262, 700)]), line, 2, 0.14)
    det += f'<path d="M 560 420 h 74 v 78 q -37 12 -74 0 Z" fill="{darker(fabric, .04)}" stroke="{line}" stroke-width="1.6" stroke-opacity=".4"/>'
    det += strokes(both([(316, 240), (340, 380)]), line, 1.6, 0.25, dash="1 6")
    out = kit.piece(d, fabric, pf, det)
    btn = c["accent"] if kind == "ajrakh" else lighter(c["accent"], 0.1)
    out += buttons([(500, y) for y in range(300, hem, 104)], btn, 6)
    out += buttons([(232, 806), (768, 806)], btn, 5)
    if collar == "band":
        band = "M 438 218 L 434 190 C 466 204 534 204 566 190 L 562 218 C 540 246 460 246 438 218 Z"
        out += kit.piece(band, fabric, pf, shadow=False)
        out += buttons([(500, 228)], btn, 5.5)
    else:
        stand = "M 438 218 L 436 194 C 466 206 534 206 564 194 L 562 218 C 540 244 460 244 438 218 Z"
        out += kit.piece(stand, darker(fabric, .08), pf, shadow=False)
        left = "M 440 210 L 498 268 L 466 312 L 398 236 Z"
        right = "M 560 210 L 502 268 L 534 312 L 602 236 Z"
        out += kit.piece(left, fabric, pf, shadow=True)
        out += kit.piece(right, fabric, pf, shadow=True)
    return out


def men_kurta(kit, c, kind):
    fabric = c["hex"]
    hem = 1040
    start = (442, 200)
    segs = [
        ("L", (322, 226)),
        ("C", (292, 400), (240, 640), (196, 830)),
        ("L", (270, 856)),
        ("C", (304, 700), (340, 530), (370, 380)),
        ("L", (362, hem)),
        ("Q", (430, hem + 8), (500, hem + 8)),
    ]
    d = sym_path(start, segs, neck_depth=30)
    line = darker(fabric, 0.45)
    pf = kit.print_fill(kind, c)
    det = f'<rect x="488" y="226" width="24" height="250" fill="{darker(fabric, .05)}"/>'
    det += strokes(["M 488 226 L 488 476 L 512 476 L 512 226"], line, 1.6, 0.3)
    det += strokes(both([(370, hem - 230), (362, hem + 4)]), BG, 4, 1)
    det += strokes(both([(204, 798), (278, 822)]), line, 2.2, 0.35)
    det += strokes(both([(404, 420), (396, 1000)]) + both([(300, 480), (266, 720)]), line, 2, 0.14)
    out = kit.piece(d, fabric, pf, det)
    btn = c["accent"]
    out += buttons([(500, y) for y in (270, 330, 390, 446)], btn, 6)
    band = "M 438 204 L 434 174 C 466 188 534 188 566 174 L 562 204 C 540 232 460 232 438 204 Z"
    out += kit.piece(band, fabric, pf, shadow=False)
    return out


def nehru(kit, c, kind):
    fabric = c["hex"]
    start = (452, 200)
    segs = [
        ("L", (362, 222)),
        ("C", (352, 280), (360, 330), (392, 360)),
        ("C", (384, 470), (380, 600), (378, 840)),
        ("Q", (440, 862), (500, 902)),
    ]
    d = sym_path(start, segs, neck_depth=28)
    line = darker(fabric, 0.5)
    pf = kit.print_fill(kind, c)
    det = strokes(["M 500 226 L 500 902"], line, 2.4, 0.45)
    det += f'<path d="M 396 692 h 80 v 12 h -80 Z M 524 692 h 80 v 12 h -80 Z M 544 424 h 62 v 10 h -62 Z" fill="{darker(fabric, .18)}"/>'
    det += strokes(both([(420, 380), (410, 830)]), line, 2, 0.14)
    det += strokes(["M 380 830 Q 440 852 496 890", "M 620 830 Q 560 852 504 890"], line, 1.6, 0.3, dash="1 6")
    out = kit.piece(d, fabric, pf, det)
    out += buttons([(500, y) for y in range(260, 860, 84)], c["accent"], 7)
    band = "M 446 204 L 442 172 C 470 186 530 186 558 172 L 554 204 C 535 230 465 230 446 204 Z"
    out += kit.piece(band, fabric, pf, shadow=False)
    return out


def garment(kit, product, colour):
    kind = product["print"]
    g = product["garment"]
    if g == "kurta":
        return kurta(kit, colour, kind)
    if g == "kurti":
        return kurta(kit, colour, kind, hem=860, neck_buttons=False, yoke=True)
    if g == "kurta_set":
        pants = straight_pants(kit, colour, None, colour_hex=darker(colour["hex"], 0.06))
        top = kurta(kit, colour, kind, hem=990)
        return (
            f'<g transform="translate(300 150) scale(.8)">{pants}</g>'
            f'<g transform="translate(-40 70) scale(.84)">{top}</g>'
        )
    if g == "coord":
        top = coord_top(kit, colour, kind)
        pants = palazzo_like_pants(kit, colour, kind)
        return (
            f'<g transform="translate(170 400) scale(.66)">{pants}</g>'
            f'<g transform="translate(90 -40) scale(.82)">{top}</g>'
        )
    if g == "palazzo":
        return palazzo(kit, colour, kind)
    if g == "maxi":
        return maxi(kit, colour, kind)
    if g == "wrap":
        return wrap_dress(kit, colour, kind)
    if g == "dupatta":
        return dupatta(kit, colour, kind)
    if g == "shirt_band":
        return shirt(kit, colour, kind, "band")
    if g == "shirt_classic":
        return shirt(kit, colour, kind, "classic")
    if g == "men_kurta":
        return men_kurta(kit, colour, kind)
    if g == "nehru":
        return nehru(kit, colour, kind)
    raise ValueError(g)


def palazzo_like_pants(kit, c, kind):
    """Wide-leg pants for the co-ord set (no tassels)."""
    fabric = c["hex"]
    start = (360, 230)
    segs = [
        ("L", (356, 300)),
        ("C", (318, 600), (290, 900), (268, 1110)),
        ("L", (482, 1118)),
        ("L", (502, 570)),
    ]
    d = sym_path(start, segs, neck_depth=0)
    line = darker(fabric, 0.4)
    det = f'<rect x="340" y="226" width="320" height="56" fill="{darker(fabric, .06)}"/>'
    det += strokes(both([(410, 320), (350, 1080)]) + both([(455, 330), (430, 1090)]), line, 2.2, 0.15)
    return kit.piece(d, fabric, kit.print_fill(kind, c, 1.3), det)


# ------------------------------------------------------------------ props


def marigold(x, y, r, rot=0):
    out = [f'<g transform="translate({f(x)} {f(y)}) rotate({rot})">']
    out.append(f'<circle r="{f(r)}" fill="#000" filter="url(#soft-shadow)" opacity=".6"/>')
    for ring, colour in ((1.0, "#D9771F"), (0.78, "#E8902A"), (0.55, "#F0A738"), (0.32, "#F5B947")):
        n = int(18 * ring) + 6
        for i in range(n):
            a = i * 360 / n + ring * 40
            out.append(
                f'<ellipse cx="0" cy="{f(-r * ring * 0.62)}" rx="{f(r * 0.17)}" ry="{f(r * ring * 0.42)}" '
                f'fill="{colour}" transform="rotate({f(a)})"/>'
            )
    out.append(f'<circle r="{f(r * 0.12)}" fill="#B85A14"/>')
    out.append("</g>")
    return "".join(out)


def print_block(x, y, s, rot=0):
    """A carved wooden printing block, seen from above at an angle."""
    wood, dark = "#A2683C", "#6E4524"
    return (
        f'<g transform="translate({f(x)} {f(y)}) rotate({rot}) scale({s})">'
        f'<rect x="-90" y="-70" width="180" height="140" rx="10" fill="#000" filter="url(#soft-shadow)"/>'
        f'<rect x="-90" y="-70" width="180" height="140" rx="10" fill="{wood}"/>'
        f'<rect x="-90" y="-70" width="180" height="140" rx="10" fill="url(#shade)"/>'
        f'<rect x="-74" y="-54" width="148" height="108" rx="6" fill="{dark}" opacity=".35"/>'
        + petal_flower(-30, 0, 44, dark, centre=wood)
        + petal_flower(38, -18, 26, dark, centre=wood, rot=30)
        + f'<circle cx="40" cy="28" r="6" fill="{dark}"/>'
        f'<ellipse cx="0" cy="0" rx="34" ry="24" fill="#8A5530" opacity=".0"/>'
        f'<rect x="-22" y="-112" width="44" height="58" rx="14" fill="{dark}" opacity=".9"/>'
        f'<ellipse cx="0" cy="-112" rx="28" ry="16" fill="{wood}"/>'
        f'<ellipse cx="0" cy="-112" rx="28" ry="16" fill="url(#shade)"/>'
        "</g>"
    )


# ----------------------------------------------------------------- scenes


def svg_doc(w, h, defs, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<defs>{common_defs()}{''.join(defs)}</defs>{body}</svg>"
    )


def product_image(product, colour):
    kit = Kit(product["handle"][:10])
    body = background(W, H) + f'<g transform="translate(0 0)">{garment(kit, product, colour)}</g>'
    return svg_doc(W, H, kit.defs, body)


def detail_image(product):
    colour = product["colours"][0]
    kit = Kit("detail")
    kind = product["print"]
    fill = kit.print_fill(kind, colour, 3.2 if kind in ("dabu", "herringbone", "booti") else 2.4)
    cloth = "M -40 -40 L 1040 -40 L 1040 1290 L -40 1290 Z"
    fold = "M 600 1290 C 700 1100 860 1010 1040 960 L 1040 1290 Z"
    body = background(W, H)
    body += f'<path d="{cloth}" fill="{colour["hex"]}"/>'
    if fill:
        body += f'<path d="{cloth}" fill="{fill}"/>'
    body += f'<path d="{cloth}" fill="url(#shade)"/>'
    body += strokes(["M -40 380 C 300 330 700 420 1040 360", "M -40 820 C 280 870 640 780 1040 840"], "#000", 18, 0.05)
    body += strokes(["M -40 370 C 300 320 700 410 1040 350"], "#fff", 10, 0.07)
    body += f'<path d="{fold}" fill="#000" filter="url(#soft-shadow)"/>'
    body += f'<path d="{fold}" fill="{lighter(colour["hex"], 0.12)}"/>'
    body += f'<path d="{fold}" fill="url(#shade)"/>'
    return svg_doc(W, H, kit.defs, body)


def by_handle(handle):
    return next(p for p in PRODUCTS if p["handle"] == handle)


def place(content, cx, cy, scale, rot=0):
    return (
        f'<g transform="translate({f(cx)} {f(cy)}) rotate({rot}) scale({scale}) translate({-W / 2} {-H / 2})">'
        f"{content}</g>"
    )


def look_image():
    """Shop the look: kurta, palazzo and dupatta. Hotspots in index.json match these positions."""
    w, h = 1200, 1500
    kit = Kit("look")
    kurta_p = by_handle("neel-block-print-kurta")
    pal = by_handle("handloom-cotton-palazzo")
    dup = by_handle("kalamkari-cotton-dupatta")
    body = background(w, h)
    body += place(garment(kit, pal, pal["colours"][0]), 880, 800, 0.8, 5)
    body += place(garment(kit, kurta_p, kurta_p["colours"][0]), 420, 600, 0.9, -4)
    body += place(garment(kit, dup, dup["colours"][0]), 470, 1290, 0.6, -82)
    body += marigold(1060, 210, 46) + marigold(985, 300, 30, 20) + marigold(130, 1065, 34)
    return svg_doc(w, h, kit.defs, body), (w, h)


def hero_image():
    w, h = 1500, 1200
    kit = Kit("hero")
    a = by_handle("neel-block-print-kurta")
    b = by_handle("bagru-print-wrap-dress")
    dup = by_handle("kalamkari-cotton-dupatta")
    body = background(w, h, "#E9E0D0")
    body += place(garment(kit, dup, dup["colours"][1]), 760, 640, 0.86, -8)
    body += place(garment(kit, a, a["colours"][1]), 420, 620, 0.88, -7)
    body += place(garment(kit, b, b["colours"][0]), 1090, 640, 0.88, 6)
    body += print_block(760, 1040, 0.95, -12)
    body += marigold(230, 1080, 44) + marigold(330, 1130, 28, 15) + marigold(1330, 150, 40) + marigold(1400, 230, 26)
    return svg_doc(w, h, kit.defs, body), (w, h)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for product in PRODUCTS:
        for colour in product["colours"]:
            name = image_name(product, colour)
            (OUT / name.replace(".jpg", ".svg")).write_text(product_image(product, colour))
            manifest.append({"svg": name.replace(".jpg", ".svg"), "jpg": f"demo-data/images/{name}", "width": W, "height": H})
        name = detail_name(product)
        (OUT / name.replace(".jpg", ".svg")).write_text(detail_image(product))
        manifest.append({"svg": name.replace(".jpg", ".svg"), "jpg": f"demo-data/images/{name}", "width": W, "height": H})

    for svg_name, jpg, (doc, (w, h)) in (
        ("kora-hero.svg", "assets/kora-hero.jpg", hero_image()),
        ("kora-look.svg", "assets/kora-look.jpg", look_image()),
    ):
        (OUT / svg_name).write_text(doc)
        manifest.append({"svg": svg_name, "jpg": jpg, "width": w, "height": h})

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(manifest)} SVGs to {OUT}")


if __name__ == "__main__":
    main()
