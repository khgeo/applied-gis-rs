"""Front and back cover for Book 4 · Applied GIS and Remote Sensing (A4, full bleed).

Same layout and typography as Books 1–2 (vector SVG). The artwork is Cambodia drawn as
a stack of three raster "images" in time (an Earth Engine ImageCollection): dry season,
rising water and the 2011 flood peak. Outline, lake and roads come from the simplified real
layers in coverdata.json. The top layer's water is the real 2011 flood extent (author's
data, UTM 48N, rasterized to the 64 × 64 grid in coverdata.json["flood2011"]); the middle
layer is that extent shrunk inward; vegetation colours are an illustrative field.
"""
import json, os, html
import numpy as np
import qrcode
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "coverdata.json")))
W, H = 794, 1123
SITE = "https://khgeo.github.io/applied-gis-rs/"
TITLE1, TITLE2 = "អនុវត្តន៍ GIS", "និងការយកព័ត៌មានពីចម្ងាយ"
BG0, BG1, BG2, ACC, ACC2, PALE = "#0b2418", "#123d27", "#1b5e20", "#ffb300", "#ffe082", "#c8e6c9"

def proj(u, v, ox, oy, w, h, sk):
    return (ox + u * w + (1 - v) * sk, oy + (1 - v) * h)

# ---------------------------------------------------------------- raster layers
N = 64
def _mask(key, n=N):
    im = Image.new("L", (n, n), 0); dr = ImageDraw.Draw(im)
    for poly in D[key]:
        for ring in poly:
            dr.polygon([(u * n, (1 - v) * n) for u, v in ring], fill=255)
    return np.array(im) > 0
LAKE = _mask("lake"); LAND = ndi.binary_fill_holes(ndi.binary_closing(_mask("prov") | LAKE, iterations=1))
FLOOD = np.array([[c == "1" for c in row] for row in D["flood2011"]]) & LAND   # real 2011 flood extent
rng = np.random.default_rng(4)
yy, xx = np.mgrid[0:N, 0:N] / N
field = ndi.gaussian_filter(rng.normal(size=(N, N)), 3) * 4
forest = np.clip(.35 + .45 * np.exp(-((xx - .9) ** 2 + (yy - .15) ** 2) / .08) + .45 * np.exp(-((xx - .12) ** 2 + (yy - .7) ** 2) / .06)
                 + .3 * np.exp(-((xx - .55) ** 2 + (yy - .12) ** 2) / .05) + .08 * field, 0, 1)
lowland = np.exp(-((xx - .45) ** 2 / .05 + (yy - .55) ** 2 / .09))           # around Tonle Sap / Mekong
def _poly_mask(poly, n=N):
    im = Image.new("L", (n, n), 0); dr = ImageDraw.Draw(im)
    for ring in poly: dr.polygon([(u * n, (1 - v) * n) for u, v in ring], fill=255)
    return np.array(im) > 0
# Phnom Penh = the province polygon centred near (0.478, 0.278) in coverdata.json
_pp = min(D["prov"], key=lambda poly: sum((u - .478) ** 2 + (v - .278) ** 2 for u, v in poly[0]) / len(poly[0]))
city = _poly_mask(_pp)

def layer(season):
    """0 dry · 1 wet · 2 flood — returns (value 0–1, kind) arrays; kind 0 land · 1 water · 2 city."""
    v = forest * (.55 if season == 0 else 1.0) + (1 - forest) * lowland * (0 if season == 0 else .55)
    water = LAKE.copy()
    if season == 2: water = LAKE | FLOOD
    elif season == 1: water = LAKE | ndi.binary_erosion(FLOOD, iterations=2)
    kind = np.where(water, 1, 0); kind[city & LAND] = 2
    return np.clip(v + .06 * field, 0, 1), kind

GREENS = [(56, 44, 20), (120, 96, 40), (174, 150, 60), (140, 180, 70), (70, 150, 60), (27, 110, 50)]
def green(t):
    t = t * (len(GREENS) - 1); i = min(len(GREENS) - 2, int(t)); f = t - i
    return "#%02x%02x%02x" % tuple(int(a + (b - a) * f) for a, b in zip(GREENS[i], GREENS[i + 1]))

def raster_svg(ox, oy, w, h, sk, season, alpha):
    val, kind = layer(season); out = []
    cw, ch = 1 / N, 1 / N
    for r in range(N):
        for c in range(N):
            if not LAND[r, c]: continue
            u0, u1 = c * cw, (c + 1) * cw; v1, v0 = 1 - r * ch, 1 - (r + 1) * ch
            pts = [proj(u0, v1, ox, oy, w, h, sk), proj(u1, v1, ox, oy, w, h, sk), proj(u1, v0, ox, oy, w, h, sk), proj(u0, v0, ox, oy, w, h, sk)]
            col = "#4fc3f7" if kind[r, c] == 1 else "#ff7043" if kind[r, c] == 2 else green(val[r, c])
            out.append(f'<path d="M{pts[0][0]:.1f} {pts[0][1]:.1f}L{pts[1][0]:.1f} {pts[1][1]:.1f}L{pts[2][0]:.1f} {pts[2][1]:.1f}L{pts[3][0]:.1f} {pts[3][1]:.1f}Z" fill="{col}"/>')
    return f'<g opacity="{alpha}" stroke="rgba(11,36,24,.55)" stroke-width=".35">' + "".join(out) + "</g>"

def outline(ox, oy, w, h, sk, key="prov", stroke="rgba(255,255,255,.55)", sw=.7, fill="none"):
    d = []
    for poly in D[key]:
        for ring in poly:
            pts = [proj(u, v, ox, oy, w, h, sk) for u, v in ring]
            d.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
    return f'<path d="{" ".join(d)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-rule="evenodd"/>'

def plate(ox, oy, w, h, sk):
    a = proj(-.05, 1.06, ox, oy, w, h, sk); b = proj(1.05, 1.06, ox, oy, w, h, sk); c = proj(1.05, -.06, ox, oy, w, h, sk); d = proj(-.05, -.06, ox, oy, w, h, sk)
    return f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{c[0]:.1f} {c[1]:.1f}L{d[0]:.1f} {d[1]:.1f}Z" fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.3)"/>'

def art(ox, oy, w, h, sk, gap):
    L = []
    labels = [("មករា · រដូវប្រាំង", 0), ("សីហា · ទឹកកំពុងឡើង", 1), ("តុលា ២០១១ · ទឹកជំនន់", 2)]
    for i, (lab, season) in enumerate(labels):
        y = oy - i * gap
        L.append(plate(ox, y, w, h, sk))
        L.append(raster_svg(ox, y, w, h, sk, season, .96))
        L.append(outline(ox, y, w, h, sk))
        px, py = proj(1.08, .5, ox, y, w, h, sk)
        L.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px + 40:.1f}" y2="{py:.1f}" stroke="rgba(255,255,255,.5)" stroke-dasharray="3 3"/>'
                 f'<text x="{px + 46:.1f}" y="{py + 5:.1f}" class="lab">{lab}</text>')
    # time axis
    a = proj(-.12, .1, ox, oy, w, h, sk); b = proj(-.12, .1, ox, oy - 2 * gap, w, h, sk)
    L.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1] - 18:.1f}" stroke="{ACC}" stroke-width="2" marker-end="url(#ar)"/>')
    L.append(f'<text x="{a[0] - 10:.1f}" y="{(a[1] + b[1]) / 2:.1f}" class="lab" text-anchor="end" fill="{ACC2}">ពេលវេលា</text>')
    return "".join(L)

CSS = """<style>
@page{size:A4;margin:0} html,body{margin:0;padding:0}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always}
svg{display:block;width:210mm;height:297mm}
text{font-family:'Battambang',sans-serif;fill:#fff}
.moul{font-family:'Moul',serif}
.lab{font-size:13px;fill:rgba(255,255,255,.88)}
.en{font-family:'Georgia','DejaVu Serif',serif}
</style>"""

def front():
    defs = (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset=".55" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>'
            '<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="rgba(255,255,255,.04)"/></pattern>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{ACC}"/></marker></defs>')
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs}<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>']
    s.append(f'<rect x="0" y="0" width="{W}" height="8" fill="{ACC}"/>')
    s.append('<text x="60" y="70" font-size="15" fill="rgba(255,255,255,.8)">ស៊េរីសៀវភៅ GIS និងការយកព័ត៌មានពីចម្ងាយ</text>')
    s.append(f'<text x="{W - 60}" y="70" font-size="15" text-anchor="end" fill="{ACC2}" font-weight="700">សៀវភៅទី ៤</text>')
    s.append('<line x1="60" y1="88" x2="734" y2="88" stroke="rgba(255,255,255,.25)"/>')
    s.append(f'<text x="60" y="165" class="moul" font-size="40">{TITLE1}</text>')
    s.append(f'<text x="60" y="232" class="moul" font-size="40">{TITLE2}</text>')
    s.append(f'<rect x="60" y="258" width="90" height="4" fill="{ACC}"/>')
    s.append(f'<text x="60" y="300" class="en" font-size="23" fill="{PALE}" font-style="italic">Applied GIS and Remote Sensing</text>')
    s.append(f'<text x="60" y="338" font-size="17" fill="{PALE}">Google Earth Engine · ទឹកជំនន់ · គ្រោះរាំងស្ងួត · ព្រៃឈើ · ស្រែ · ទីក្រុង</text>')
    s.append(art(100, 675, 430, 205, 90, 148))
    s.append(f'<rect x="0" y="{H - 190}" width="{W}" height="190" fill="rgba(0,0,0,.30)"/>')
    s.append(f'<text x="60" y="{H - 128}" font-size="26" font-weight="700">យាំ សារដ្ឋ</text><text x="190" y="{H - 128}" font-size="20" class="en" fill="{PALE}">YAM Sarath</text>')
    s.append(f'<text x="60" y="{H - 96}" font-size="15" fill="{PALE}">ថ្នាក់បរិញ្ញាបត្រ ឆ្នាំទី៣ ឆមាសទី២ · ដេប៉ាតឺម៉ង់ភូមិវិទ្យា និងរៀបចំដែនដី</text>')
    s.append(f'<text x="60" y="{H - 58}" font-size="14" fill="rgba(255,255,255,.75)">១៥ មេរៀន · ១៥ លំហាត់ Earth Engine · បោះពុម្ពលើកទី១ · ២០២៦</text>')
    s.append(f'<text x="{W - 60}" y="{H - 58}" font-size="13" text-anchor="end" fill="rgba(255,255,255,.75)" class="en">CC BY-SA 4.0</text>')
    s.append("</svg>")
    return "".join(s)

def qr_svg(url, size):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(url); q.make(fit=True); m = q.get_matrix(); n = len(m); c = size / n
    rects = "".join(f'<rect x="{j * c:.2f}" y="{i * c:.2f}" width="{c + .2:.2f}" height="{c + .2:.2f}"/>' for i in range(n) for j in range(n) if m[i][j])
    return f'<g fill="{BG0}">{rects}</g>'

def back():
    items = ["១៥ មេរៀន ពីការគណនាលើពពក ដល់កម្មវិធីវេប Earth Engine", "១៥ លំហាត់ Earth Engine ជាមួយកូដដែលរត់បាន និងប្រអប់ពិនិត្យខ្លួនឯង",
             "១៦ ពិសោធន៍អន្តរកម្ម · ស្លាយបង្រៀន ១៥ ឈុត", "ទឹកជំនន់ Sentinel-1 · គ្រោះរាំងស្ងួត CHIRPS និង VHI · អាងទន្លេ",
             "ព្រៃឈើ Hansen · ស្រែ Sentinel-1 · ទីក្រុង និង LST", "MCDA · ក្រមសីលធម៌ទិន្នន័យ · គម្រោងបញ្ចប់វគ្គ"]
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="{BG1}"/><rect x="0" y="{H - 8}" width="{W}" height="8" fill="{ACC}"/>']
    s.append('<text x="60" y="120" class="moul" font-size="22">អំពីសៀវភៅនេះ</text>')
    para = ["សៀវភៅនេះជាក្បាលទីបួន និងចុងក្រោយនៃស៊េរី។ វាបង្រៀនការវិភាគរូបភាព",
            "ផ្កាយរណបរាប់ពាន់ផ្ទាំងលើកម្ពុជា ដោយ Google Earth Engine ហើយអនុវត្ត",
            "លើបញ្ហាពិត៖ ទឹកជំនន់ គ្រោះរាំងស្ងួត ព្រៃឈើ ស្រែ ទីក្រុង និងកំដៅ។",
            "មេរៀននីមួយៗបញ្ចប់ដោយ «អ្វីដែលយើងមិនអាចសន្និដ្ឋាន»។"]
    for i, t in enumerate(para): s.append(f'<text x="60" y="{175 + i * 32}" font-size="16.5" fill="#e8f5e9">{html.escape(t)}</text>')
    s.append(f'<text x="60" y="340" font-size="18" font-weight="700" fill="{ACC2}">អ្វីដែលមាននៅក្នុងសៀវភៅ</text>')
    for i, t in enumerate(items):
        y = 385 + i * 40; s.append(f'<rect x="60" y="{y - 13}" width="10" height="10" fill="{ACC}"/><text x="84" y="{y - 3}" font-size="15.5">{html.escape(t)}</text>')
    s.append(f'<text x="60" y="660" font-size="18" font-weight="700" fill="{ACC2}">ស៊េរីសៀវភៅ</text>')
    series = [("១", "ផែនទីវិទ្យា", "ឆ្នាំទី២ ឆមាសទី១", False), ("២", "មូលដ្ឋានគ្រឹះនៃ GIS", "ឆ្នាំទី២ ឆមាសទី២", False),
              ("៣", "មូលដ្ឋានគ្រឹះនៃការយកព័ត៌មានពីចម្ងាយ", "ឆ្នាំទី៣ ឆមាសទី១", False), ("៤", "អនុវត្តន៍ GIS និងការយកព័ត៌មានពីចម្ងាយ", "ឆ្នាំទី៣ ឆមាសទី២", True)]
    for i, (n_, t, y_, cur) in enumerate(series):
        y = 700 + i * 44
        s.append(f'<rect x="60" y="{y - 26}" width="674" height="36" rx="4" fill="{"rgba(255,179,0,.22)" if cur else "rgba(255,255,255,.06)"}"/>')
        s.append(f'<text x="78" y="{y - 2}" font-size="15" font-weight="700" fill="{ACC2}">សៀវភៅទី{n_}</text><text x="185" y="{y - 2}" font-size="15">{html.escape(t)}</text><text x="716" y="{y - 2}" font-size="13" text-anchor="end" fill="{PALE}">{y_}</text>')
    s.append(f'<g transform="translate(60 {H - 230})"><rect x="-8" y="-8" width="136" height="136" fill="#fff" rx="6"/>{qr_svg(SITE, 120)}</g>')
    s.append(f'<text x="215" y="{H - 190}" font-size="16" font-weight="700">អានកំណែអនឡាញអន្តរកម្ម</text><text x="215" y="{H - 162}" font-size="14" class="en" fill="{PALE}">{SITE}</text>')
    s.append(f'<text x="215" y="{H - 132}" font-size="14" fill="#e8f5e9">កូដ និងទិន្នន័យ៖ github.com/khgeo/applied-gis-rs</text>')
    s.append(f'<text x="215" y="{H - 104}" font-size="13" fill="rgba(255,255,255,.75)">ចេញផ្សាយក្រោមអាជ្ញាបណ្ណ CC BY-SA 4.0 · ចែកចាយដោយឥតគិតថ្លៃ</text>')
    s.append("</svg>")
    return "".join(s)

def wrap(pages, paper_mm=0.1, bleed=3):
    """Print-shop wraparound cover: bleed + back + spine + front + bleed (A4 trim)."""
    spine = round(pages / 2 * paper_mm, 1)
    wmm, hmm = 2 * 210 + spine + 2 * bleed, 297 + 2 * bleed
    sp = (f'<div style="position:absolute;left:{bleed + 210}mm;top:0;width:{spine}mm;height:{hmm}mm;background:{BG0};display:flex;align-items:center;justify-content:center">'
          f'<div style="transform:rotate(90deg);white-space:nowrap;color:#fff;font-family:Battambang;font-size:{min(11, spine * .9):.1f}pt;display:flex;gap:10mm;align-items:center">'
          f'<span style="font-family:Moul">{TITLE1} {TITLE2}</span><span style="font-weight:700">យាំ សារដ្ឋ</span><span style="color:{ACC2}">សៀវភៅទី ៤</span></div></div>')
    page = lambda x, svg: f'<div style="position:absolute;left:{x}mm;top:{bleed}mm;width:210mm;height:297mm">{svg}</div>'
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>@page{{size:{wmm}mm {hmm}mm;margin:0}}html,body{{margin:0}}"
            f"body{{width:{wmm}mm;height:{hmm}mm;position:relative;background:{BG1};overflow:hidden}}svg{{display:block;width:210mm;height:297mm}}"
            f"text{{font-family:'Battambang',sans-serif;fill:#fff}}.moul{{font-family:'Moul',serif}}.lab{{font-size:13px;fill:rgba(255,255,255,.88)}}.en{{font-family:Georgia,serif}}</style></head><body>"
            f"<div style='position:absolute;inset:0;background:{BG1}'></div>{page(bleed, back())}{sp}{page(bleed + 210 + spine, front())}</body></html>"), wmm, hmm, spine

def write(outdir):
    for name, fn in (("cover", front), ("backcover", back)):
        with open(os.path.join(outdir, name + ".html"), "w", encoding="utf-8") as f:
            f.write(f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body><div class='page'>{fn()}</div></body></html>")

if __name__ == "__main__":
    write(".")
