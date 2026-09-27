"""Book 4 · Chapter 2 figures (Lessons 4–6).

Real data: Landsat 8 OLI TOA, Phnom Penh, 11 Feb 2019, 300 × 300 px at 30 m
(docs/assets/data/l8_pp_scene.json, shared with Book 3). Its reference classes were
derived from index thresholds for teaching, not field survey, and figures say so.
NDVI time series (Lesson 5) and the province table (Lesson 4) are illustrative and
are labelled as such on the figure.
"""
from vis_core import *
from rs_chart import chart, bars
import base64
import numpy as np
from PIL import Image

KHF = lambda v, d=2: kh(f"{v:.{d}f}".replace(".", ","))
CLS_KH = ["ទឹក", "ដើមឈើ", "ដំណាំ/ស្មៅ", "តំបន់សាងសង់", "ដីទទេ"]
CLS_COL = ["#1e88e5", "#1b5e20", "#9ccc65", "#e53935", "#d7ccc8"]
SRC_L8 = "Landsat 8 OLI · ភ្នំពេញ · ១១ កុម្ភៈ ២០១៩ · USGS"

def scene():
    d = gj("l8_pp_scene.json")
    B = np.frombuffer(base64.b64decode(d["data"]), np.uint8).reshape(6, 300, 300).astype(float) * d["scale"]
    C = np.frombuffer(base64.b64decode(d["cls"]), np.uint8).reshape(300, 300)
    return B, C
def nd(a, b): return (a - b) / (a + b + 1e-9)
def stretch(a, lo=2, hi=98):
    l, h = np.percentile(a, lo), np.percentile(a, hi); return (np.clip((a - l) / (h - l + 1e-12), 0, 1) * 255).astype(np.uint8)
def rgb(r, g, b): return Image.fromarray(np.dstack([stretch(r), stretch(g), stretch(b)]))
def ramp(a, cols, vmin, vmax):
    t = np.clip((a - vmin) / (vmax - vmin), 0, 1) * (len(cols) - 1); lo = np.floor(t).astype(int).clip(0, len(cols) - 2); fr = (t - lo)[..., None]
    P = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in cols], float)
    return Image.fromarray((P[lo] * (1 - fr) + P[lo + 1] * fr).astype(np.uint8))
def pal(idx, cols):
    P = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in cols], np.uint8); return Image.fromarray(P[idx])
NDVI_PAL = ["#a50026", "#f46d43", "#fee08b", "#d9ef8b", "#66bd63", "#006837"]

def box(f, x, y, w, h, t, sub="", c=IND, fs=17, tc="#fff"):
    f.rect(x, y, w, h, c, rx=12); f.text(x + w / 2, y + h / 2 + (-4 if sub else 6), t, fs, tc, "middle", "bold")
    if sub: f.text(x + w / 2, y + h / 2 + 20, sub, 13, tc, "middle")
def code(f, x, y, w, lines, fs=14):
    f.rect(x, y, w, 24 + len(lines) * 22, "#263238", rx=8)
    for i, l in enumerate(lines): f.text(x + 16, y + 28 + i * 22, l, fs, "#a5d6a7" if l.strip().startswith("//") else "#80cbc4", extra='font-family="monospace" xml:space="preserve"')
def grid(f, x, y, n, s, cols):
    for i in range(n):
        for j in range(n): f.rect(x + j * s, y + i * s, s - 1, s - 1, cols[(i * 7 + j * 3) % len(cols)])

# Three teaching zones inside the Phnom Penh scene (pixel rectangles: r0, r1, c0, c1)
ZONES = [("តំបន់ ក", (30, 110, 20, 120), "#ef6c00"), ("តំបន់ ខ", (150, 250, 170, 280), "#1565c0"), ("តំបន់ គ", (120, 190, 40, 130), "#6a1b9a")]

def zstats(ndvi, z, k=1):
    """Mean NDVI of zone z at scale k × 30 m: block-average, then keep blocks whose centre is inside."""
    r0, r1, c0, c1 = z; H = 300 // k * k
    a = ndvi[:H, :H].reshape(H // k, k, H // k, k).mean((1, 3))
    rr, cc = np.mgrid[0:H // k, 0:H // k]; yc, xc = rr * k + k / 2, cc * k + k / 2
    m = (yc >= r0) & (yc < r1) & (xc >= c0) & (xc < c1)
    return a[m].mean(), int(m.sum())

def L04():
    B, C = scene(); b2, b3, b4, b5, b6, b7 = B; ndvi = nd(b5, b4)
    # 1 four directions of reduction
    f = Fig(1000, 470).title("Reducer បង្រួមតម្លៃច្រើនទៅជាតម្លៃតិច", "បួនទិសដៅនៃការបង្រួម")
    items = [("តាមពេលវេលា", "collection.reduce() · median()", "#43a047"), ("តាមតំបន់មួយ", "image.reduceRegion()", "#ef6c00"),
             ("តាមតំបន់ច្រើន", "image.reduceRegions()", "#6d4c41"), ("តាមក្រឡាជិតខាង", "image.reduceNeighborhood()", "#1565c0")]
    for i, (a, b, c) in enumerate(items):
        x = 30 + i * 240; f.rect(x, 90, 220, 330, "#fafafa", "#cfd8dc", 1.2, 12); f.text(x + 110, 124, a, 18, c, "middle", "bold")
        if i == 0:
            for t in range(4): grid(f, x + 40 + t * 12, 150 + t * 12, 5, 18, ["#a5d6a7", "#81c784", "#c8e6c9", "#66bb6a"])
            f.line(x + 110, 300, x + 110, 330, INK, 2, arrow=True); grid(f, x + 65, 340, 5, 18, ["#66bb6a", "#81c784"])
        elif i == 1:
            grid(f, x + 35, 150, 8, 19, ["#a5d6a7", "#fff59d", "#81c784", "#c8e6c9"]); f.rect(x + 73, 188, 95, 76, "none", c, 3)
            f.line(x + 110, 310, x + 110, 336, INK, 2, arrow=True); f.rect(x + 40, 345, 140, 50, "#fff3e0", c, 1.5, 6); f.text(x + 110, 376, "{NDVI: ០,៦២}", 15, INK, "middle")
        elif i == 2:
            grid(f, x + 35, 150, 8, 19, ["#a5d6a7", "#fff59d", "#81c784", "#c8e6c9"])
            f.path(f"M{x+35} {x*0+150} L{x+111} 150 L{x+111} 302 L{x+35} 302Z", "none", c, 3); f.path(f"M{x+111} 150 L{x+187} 150 L{x+187} 302 L{x+111} 302Z", "none", c, 3)
            f.line(x + 110, 310, x + 110, 336, INK, 2, arrow=True)
            for k, v in enumerate(["ស្រុក ១ · ០,៥៤", "ស្រុក ២ · ០,៧១"]): f.text(x + 110, 360 + k * 24, v, 14, INK, "middle")
        else:
            grid(f, x + 35, 150, 8, 19, ["#a5d6a7", "#fff59d", "#81c784", "#c8e6c9"]); f.rect(x + 92, 207, 57, 57, "none", c, 3); f.rect(x + 111, 226, 19, 19, c)
            f.line(x + 110, 310, x + 110, 336, INK, 2, arrow=True); f.text(x + 110, 370, "រូបភាពថ្មី (ផ្ទៃរលោង)", 14, INK, "middle")
    entry(4, f.save("a04-directions"), "Reducer មួយ ប្រើបានបួនបែប",
          ["មេរៀនទី៣៖ បង្រួមតាមពេលវេលា (median) ដើម្បីបានរូបភាពមួយ។", "មេរៀននេះ៖ បង្រួមតាមលំហ ដើម្បីបានលេខ ឬតារាង (reduceRegion · reduceRegions)។",
           "ee.Reducer ដដែល (mean · sum · count · percentile) ប្រើបានក្នុងទិសដៅទាំងបួន។"], .08)

    # 2 reduceRegion on a real NDVI image
    r0, r1, c0, c1 = ZONES[0][1]; v = ndvi[r0:r1, c0:c1].ravel()
    f = Fig(1000, 470).title("reduceRegion() លើរូបភាព NDVI ពិត", SRC_L8)
    f.img(ramp(ndvi, NDVI_PAL, -.1, .6), 30, 85, 360, 360); s = 360 / 300
    f.rect(30 + c0 * s, 85 + r0 * s, (c1 - c0) * s, (r1 - r0) * s, "none", "#fff", 4); f.rect(30 + c0 * s, 85 + r0 * s, (c1 - c0) * s, (r1 - r0) * s, "none", AMB, 2.5)
    f.text(30 + c0 * s + 6, 85 + r0 * s + 22, "geometry", 15, "#fff", weight="bold", extra='stroke="#000" stroke-width="3" paint-order="stroke"')
    code(f, 420, 90, 540, ["var stats = ndvi.reduceRegion({", "  reducer: ee.Reducer.mean(),", "  geometry: zone,", "  scale: 30,", "  maxPixels: 1e9", "});", "print(stats);   // Dictionary"], 14)
    rows = [("mean", v.mean()), ("median", np.median(v)), ("stdDev", v.std()), ("min", v.min()), ("max", v.max())]
    f.rect(420, 285, 540, 160, "#fff8e1", "#ffcc80", 1.2, 8); f.text(440, 312, f"លទ្ធផល (ក្រឡា ៣០ ម · {khn(v.size)} ក្រឡា)", 15, INK, weight="bold")
    for i, (a, b) in enumerate(rows): f.text(450 + (i % 3) * 170, 350 + (i // 3) * 40, f"{a}: {KHF(b)}", 16, INK, extra='font-family="monospace"')
    entry(4, f.save("a04-region"), "ពីក្រឡារាប់ពាន់ ទៅជាលេខមួយ",
          [f"តំបន់នេះមាន {khn(v.size)} ក្រឡា Landsat ៣០ ម៖ reduceRegion ត្រឡប់ Dictionary មួយ។", "reducer ផ្សេងគ្នា ផ្ដល់ចម្លើយខុសគ្នា៖ mean និង median មិនដូចគ្នាទេ ពេលទិន្នន័យលំអៀង។",
           "តួលេខគណនាពីរូបភាព Landsat 8 ពិតលើភ្នំពេញ (TOA · មិនបានកែបរិយាកាស)។"], .22)

    # 3 scale matters (real computation)
    ks = [1, 3, 10, 30]; lab = ["៣០ ម", "៩០ ម", "៣០០ ម", "៩០០ ម"]
    def zall(z, k):
        r0, r1, c0, c1 = z; H = 300 // k * k
        a = ndvi[:H, :H].reshape(H // k, k, H // k, k).mean((1, 3)); rr, cc = np.mgrid[0:H // k, 0:H // k]; yc, xc = rr * k + k / 2, cc * k + k / 2
        vv = a[(yc >= r0) & (yc < r1) & (xc >= c0) & (xc < c1)]; return vv.mean(), vv.std(), vv.max(), (vv < 0).mean(), vv.size
    R = [zall(ZONES[0][1], k) for k in ks]
    f = Fig(1000, 470).title("ប៉ារ៉ាម៉ែត្រ scale ប្ដូរចម្លើយ", "តំបន់ ក ដដែល គណនាលើមាត្រដ្ឋានបួន · " + SRC_L8)
    X, Y = chart(f, 90, 100, 460, 280, [(list(range(4)), [r[0] for r in R], "#2e7d32", "mean", 3), (list(range(4)), [r[1] for r in R], "#6a1b9a", "stdDev", 3),
                                        (list(range(4)), [r[2] for r in R], "#ef6c00", "max", 3)], (0, 3), (0, .8), "scale", "NDVI", yt=[0, .2, .4, .6, .8], lx=470, ly=118)
    for i, t in enumerate(lab): f.text(X(i), 404, t, 13, "#546e7a", "middle")
    for r in R:
        pass
    for j, c in enumerate(["#2e7d32", "#6a1b9a", "#ef6c00"]):
        for i, r in enumerate(R): f.circle(X(i), Y(r[j]), 5, c)
    f.rect(600, 100, 370, 280, "#fafafa", "#cfd8dc", 1, 8); f.text(620, 128, "តំបន់ ក តាមមាត្រដ្ឋាន", 16, INK, weight="bold")
    f.text(620, 162, "scale", 13, "#78909c"); f.text(720, 162, "ក្រឡា", 13, "#78909c"); f.text(820, 162, "ទឹក (NDVI < ០)", 13, "#78909c")
    for i, r in enumerate(R):
        f.text(620, 198 + i * 40, lab[i], 15, INK); f.text(720, 198 + i * 40, khn(r[4]), 15, INK, weight="bold"); f.text(820, 198 + i * 40, kh(round(r[3] * 100)) + "%", 15, "#1565c0", weight="bold")
    entry(4, f.save("a04-scale"), "scale គឺជាការសម្រេចចិត្ត មិនមែនលម្អិតតូចទេ",
          [f"mean ស្ទើរមិនប្ដូរ ({KHF(R[0][0])} → {KHF(R[3][0])}) ប៉ុន្តែ max និង stdDev ធ្លាក់ ហើយផ្ទៃទឹកថយពី {kh(round(R[0][3]*100))}% ទៅ {kh(round(R[3][3]*100))}%។",
           "scale ធំលាយក្រឡាតូចៗចូលគ្នា៖ វត្ថុតូច និងគែមតំបន់បាត់ ហើយចំនួនក្រឡាថយពីរាប់ពាន់ទៅតិចជាងដប់។",
           "scale កំណត់ទំហំក្រឡាដែល Earth Engine ប្រើក្នុងការគណនា៖ សរសេរវាជានិច្ច ហើយរាយការណ៍វាជាមួយលទ្ធផល។"], .4)

    # 4 combined reducers + histogram (real)
    f = Fig(1000, 470).title("បន្សំ reducer៖ ស្ថិតិច្រើនក្នុងការហៅតែមួយ", "អ៊ីស្តូក្រាម NDVI នៃតំបន់ ក · " + SRC_L8)
    h, e = np.histogram(v, bins=39, range=(-.6, .7)); x0, y0, w, hh = 60, 100, 460, 270; mx = h.max()
    for i, c in enumerate(h): f.rect(x0 + i * w / 39, y0 + hh - hh * c / mx, w / 39 - 1, hh * c / mx, "#64b5f6" if e[i] < 0 else "#81c784")
    f.line(x0, y0 + hh, x0 + w, y0 + hh, INK, 1)
    for t in (-.6, -.3, 0, .3, .6): f.text(x0 + (t + .6) / 1.3 * w, y0 + hh + 20, KHF(t, 1), 12, "#546e7a", "middle")
    for p, lab_, col in [(10, "p10", "#6d4c41"), (50, "p50", "#c62828"), (90, "p90", "#6d4c41")]:
        q = np.percentile(v, p); xx = x0 + (q + .6) / 1.3 * w; f.line(xx, y0, xx, y0 + hh, col, 2, "5 4"); f.text(xx, y0 - 6, lab_, 12, col, "middle", "bold")
    code(f, 550, 100, 420, ["var red = ee.Reducer.mean()", "  .combine({reducer2: ee.Reducer.stdDev(),", "            sharedInputs: true})", "  .combine({reducer2:", "    ee.Reducer.percentile([10,50,90]),", "            sharedInputs: true});"], 13)
    q10, q50, q90 = np.percentile(v, [10, 50, 90])
    f.text(560, 300, f"NDVI_mean {KHF(v.mean())} · NDVI_stdDev {KHF(v.std())}", 14, INK, extra='font-family="monospace"')
    f.text(560, 328, f"NDVI_p10 {KHF(q10)} · p50 {KHF(q50)} · p90 {KHF(q90)}", 14, INK, extra='font-family="monospace"')
    f.text(560, 370, "ឈ្មោះលទ្ធផល = ក្រុមរលក + _ + reducer", 14, "#607d8b")
    entry(4, f.save("a04-combine"), "មធ្យមតែមួយ លាក់ការបែងចែក",
          ["អ៊ីស្តូក្រាមមានពីរក្រុម៖ ទឹក (NDVI អវិជ្ជមាន ពណ៌ខៀវ) និងដី/រុក្ខជាតិ (NDVI វិជ្ជមាន)។ មធ្យមធ្លាក់នៅចន្លោះ ដែលគ្មានក្រឡាច្រើន។", "combine() គណនា mean stdDev និង percentile ក្នុងការឆ្លងកាត់ទិន្នន័យតែម្ដង។",
           "ឈ្មោះគន្លឹះក្នុងលទ្ធផល ប្ដូរទៅជា NDVI_mean NDVI_p50 … ត្រូវប្រើឈ្មោះនេះពេល get()។"], .5)

    # 5 reduceRegions → table → map (illustrative values)
    rnk = {"Mondul Kiri": .74, "Ratanak Kiri": .73, "Koh Kong": .75, "Preah Vihear": .68, "Stung Treng": .70, "Kratie": .66, "Pursat": .63, "Kampong Speu": .55, "Kampong Thom": .58,
           "Oddar Meanchey": .60, "Siemreap": .52, "Preah Sihanouk": .62, "Kampot": .57, "Pailin": .61, "Battambang": .45, "Banteay Meanchey": .40, "Kampong Chhnang": .44, "Kampong Cham": .50,
           "Tboung Khmum": .53, "Kandal": .41, "Takeo": .38, "Prey Veng": .36, "Svay Rieng": .37, "Kep": .52, "Phnom Penh": .20}
    br = [0, .40, .50, .60, .70]; pl = ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"]; cf = classify(None, br, pl)
    f = Fig(1000, 500).title("reduceRegions()៖ តម្លៃមួយក្នុងមួយខេត្ត", "តម្លៃគំរូ សម្រាប់បង្ហាញទម្រង់លទ្ធផលប៉ុណ្ណោះ (មិនមែនលទ្ធផលពិត)")
    prov_map(f, 30, 80, 1.55, fill=lambda p: cf(rnk.get(p["en"], .5)), stroke="#fff", sw=.8)
    f.legend_boxes(30, 470, pl, ["< ០,៤០", "០,៤០–០,៥០", "០,៥០–០,៦០", "០,៦០–០,៧០", "≥ ០,៧០"], horizontal=True)
    f.rect(530, 90, 440, 300, "#fff", "#cfd8dc", 1, 8); f.text(550, 118, "FeatureCollection លទ្ធផល (៥ ជួរដំបូង)", 15, INK, weight="bold")
    f.text(550, 150, "ADM1_NAME", 14, "#607d8b", weight="bold"); f.text(830, 150, "mean", 14, "#607d8b", weight="bold")
    for i, k in enumerate(["Banteay Meanchey", "Battambang", "Kampong Cham", "Kampong Chhnang", "Kampong Speu"]):
        f.text(550, 182 + i * 32, k, 14, INK, extra='font-family="monospace"'); f.text(830, 182 + i * 32, KHF(rnk[k]), 14, INK, extra='font-family="monospace"')
    f.text(550, 360, "→ Export.table.toDrive (CSV) → QGIS", 14, AMB, weight="bold")
    entry(4, f.save("a04-regions"), "តារាងស្ថិតិ ក្លាយជាផែនទី",
          ["reduceRegions បន្ថែមលក្ខណៈ (ឧ. mean) ទៅលើ Feature នីមួយៗ ក្នុង FeatureCollection ដើម។", "លទ្ធផលជាតារាង៖ នាំចេញជា CSV ឬ SHP ហើយធ្វើផែនទី choropleth ក្នុង QGIS (សៀវភៅទី១)។",
           "តម្លៃក្នុងរូបនេះជាគំរូ៖ លំហាត់ទី៤ គណនាតម្លៃពិតសម្រាប់ខេត្តទាំង ២៥។"], .62)

    # 6 area with pixelArea + grouped reducer (real class counts of the teaching scene)
    cnt = np.bincount(C.ravel(), minlength=5); km2 = cnt * 900 / 1e6
    f = Fig(1000, 470).title("គណនាផ្ទៃ៖ pixelArea() + reducer ជាក្រុម", "ផែនទីគម្របដីគំរូ (បានពីកម្រិតសន្ទស្សន៍ មិនមែនការស្ទង់វាល) · " + SRC_L8)
    f.img(pal(C, CLS_COL), 30, 85, 330, 330, fmt="PNG")
    code(f, 390, 88, 580, ["var area = ee.Image.pixelArea().divide(1e6)   // km²", "  .addBands(classified)", "  .reduceRegion({", "    reducer: ee.Reducer.sum().group({", "      groupField: 1, groupName: 'class'}),", "    geometry: aoi, scale: 30, maxPixels: 1e10});"], 13)
    bars(f, 390, 262, 480, 170, CLS_KH, list(km2), CLS_COL, fmt=lambda x: KHF(x, 1) + " គម²", lw=130)
    entry(4, f.save("a04-area"), "ផ្ទៃពិត មិនមែនចំនួនក្រឡា",
          ["pixelArea() ផ្ដល់ផ្ទៃ (ម²) របស់ក្រឡានីមួយៗ តាមទីតាំងពិត មិនមែនលេខថេរទេ។", "group() បំបែកផលបូកតាមថ្នាក់៖ ផ្ទៃដីមួយថ្នាក់ៗ ក្នុងការគណនាតែមួយ។",
           f"រូបភាពគំរូ ៣០០ × ៣០០ ក្រឡា ៣០ ម = {KHF(km2.sum(), 0)} គម²។ ផ្ទៃនេះជាលទ្ធផលគណនាពិតពីផែនទីគំរូ។"], .78)

    # 7 print vs export
    f = Fig(1000, 470).title("print() ឬ Export?")
    box(f, 40, 100, 280, 110, "print() · Chart", "លឿន · តូច · អន្តរកម្ម", "#43a047"); box(f, 40, 260, 280, 110, "Export (Tasks)", "ធំ · យូរ · រត់នៅផ្ទៃក្រោយ", AMB)
    rows = [("Export.table.toDrive", "CSV · SHP · GeoJSON · KML", "តារាងស្ថិតិ → Excel · QGIS"), ("Export.image.toDrive", "GeoTIFF", "រ៉ាស្ទ័រ → QGIS"),
            ("Export.image.toAsset", "Earth Engine Asset", "ប្រើបន្តក្នុងស្គ្រីបផ្សេង"), ("Export.table.toAsset", "FeatureCollection", "ចំណុចបណ្ដុះបណ្ដាល · ព្រំដែន")]
    for i, (a, b, c) in enumerate(rows):
        y = 100 + i * 70; f.rect(360, y, 600, 58, "#fff3e0" if i % 2 == 0 else "#fff8e1", "#ffcc80", 1, 6)
        f.text(376, y + 25, a, 15, INK, weight="bold", extra='font-family="monospace"'); f.text(376, y + 47, b, 13, "#607d8b"); f.text(700, y + 36, c, 14, INK)
    f.text(500, 420, "ប្រសិនបើ print() បង្ហាញ «Computation timed out» ឬ «memory limit» → ប្ដូរទៅ Export", 15, "#c62828", "middle")
    entry(4, f.save("a04-export"), "ពេលណាត្រូវនាំចេញ",
          ["print() និង Chart ដំណើរការក្នុងកម្មវិធីរុករក ហើយមានកំណត់ពេល (ប្រហែល ៥ នាទី)។", "Export រត់ជា Task នៅម៉ាស៊ីនមេ អាចចំណាយពេលរាប់ម៉ោង ហើយមិនពឹងលើកម្មវិធីរុករកទេ។",
           "លទ្ធផលស្ថិតិជាតារាង៖ ប្រើ Export.table ជាមួយ selectors ដើម្បីរក្សាតែជួរឈរដែលត្រូវការ។"], .92)

# ---------------- Lesson 5 ----------------
DOY = np.arange(1, 366)
def rice_wet(t):   # wet-season rice: transplant Jul, peak Sep–Oct, harvest late Nov
    return .18 + .58 * np.exp(-((t - 280) / 38) ** 2) * (t > 190) + .05 * np.exp(-((t - 60) / 40) ** 2)
def rice_double(t):   # dry-season + wet-season rice (irrigated lowland)
    return .16 + .56 * np.exp(-((t - 50) / 30) ** 2) + .55 * np.exp(-((t - 250) / 30) ** 2)
def forest_ev(t): return .80 + .03 * np.cos(2 * np.pi * (t - 250) / 365)
def forest_dec(t): return .55 + .22 * np.cos(2 * np.pi * (t - 260) / 365)
def urban(t): return .15 + .02 * np.cos(2 * np.pi * (t - 260) / 365)
MON = ["មក", "កម", "មន", "មស", "ឧស", "មថ", "កក", "សហ", "កញ", "តល", "វច", "ធន"]
MSTART = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
def month_axis(f, X, y):
    for m, d in zip(MON, MSTART): f.text(X(d + 14), y, m, 12, "#546e7a", "middle")
def s2_obs(fn, seed=3, cloud_wet=.55, cloud_dry=.15, n_year=73):
    rng = np.random.default_rng(seed); t = np.sort(rng.choice(np.arange(1, 366), n_year, replace=False)).astype(float)
    wet = (t > 135) & (t < 305); p = np.where(wet, cloud_wet, cloud_dry); cl = rng.random(t.size) < p
    y = fn(t) + rng.normal(0, .025, t.size); y_obs = np.where(cl, y * rng.uniform(.05, .6, t.size), y)
    return t, y_obs, cl

def harmonic_fit(t, y, order=2, w=None):
    cols = [np.ones_like(t)]
    for k in range(1, order + 1): cols += [np.cos(2 * np.pi * k * t / 365), np.sin(2 * np.pi * k * t / 365)]
    A = np.stack(cols, 1); beta = np.linalg.lstsq(A, y, rcond=None)[0]
    def pred(tt):
        c = [np.ones_like(tt)]
        for k in range(1, order + 1): c += [np.cos(2 * np.pi * k * tt / 365), np.sin(2 * np.pi * k * tt / 365)]
        return np.stack(c, 1) @ beta
    return beta, pred

def L05():
    ILL = "ស៊េរីក្លែងធ្វើតាមលំនាំពិតនៅកម្ពុជា (សម្រាប់បង្រៀន)"
    # 1 temporal signatures
    f = Fig(1000, 470).title("គម្របដីនីមួយៗ មាន «ហត្ថលេខាពេលវេលា» ខុសគ្នា", "NDVI ក្នុងមួយឆ្នាំ · " + ILL)
    ser = [(rice_double, "#f9a825", "ស្រែពីរដង (ប្រាំង + វស្សា)"), (rice_wet, "#ef6c00", "ស្រែវស្សា"), (forest_ev, "#1b5e20", "ព្រៃស្រោងទាប"),
           (forest_dec, "#8d6e63", "ព្រៃរបោះស្លឹក"), (urban, "#e53935", "ទីក្រុង")]
    X, Y = chart(f, 80, 90, 620, 300, [(list(DOY), list(fn(DOY)), c, l, 3) for fn, c, l in ser], (1, 365), (0, 1), "", "NDVI", yt=[0, .2, .4, .6, .8, 1], lx=730, ly=120)
    month_axis(f, X, 412)
    f.rect(X(135), 90, X(305) - X(135), 300, "#90caf9", extra='opacity=".18"'); f.text(X(220), 108, "រដូវវស្សា (ពពកច្រើន)", 13, "#1565c0", "middle")
    entry(5, f.save("a05-signatures"), "រូបភាពមួយផ្ទាំង មិនអាចបែងចែកបានទេ",
          ["នៅខែមករា ស្រែវស្សា និងទីក្រុង មាន NDVI ស្រដៀងគ្នា (ទាប)។ នៅខែតុលា ស្រែ និងព្រៃស្រដៀងគ្នា (ខ្ពស់)។", "ទម្រង់ក្រាបពេញមួយឆ្នាំ បែងចែកបានច្បាស់៖ ចំនួនកំពូល ពេលកំពូល និងកម្ពស់។",
           "ខ្សែទាំងនេះជាស៊េរីក្លែងធ្វើតាមប្រតិទិនដំណាំនៅកម្ពុជា មិនមែនការវាស់ពិតទេ។"], .1)

    # 2 raw vs masked
    t, yo, cl = s2_obs(rice_wet)
    f = Fig(1000, 470).title("ពពកធ្វើឲ្យ NDVI ធ្លាក់ចុះ", "ស្រែវស្សាមួយ · ការសង្កេត Sentinel-2 ប្រហែល ៧៣ ដង/ឆ្នាំ · " + ILL)
    X, Y = chart(f, 80, 90, 820, 300, [(list(DOY), list(rice_wet(DOY)), "#bdbdbd", "", 2)], (1, 365), (0, 1), "", "NDVI", yt=[0, .2, .4, .6, .8, 1], legend=False)
    month_axis(f, X, 412)
    for a, b, c in zip(t, yo, cl): f.circle(X(a), Y(b), 5, "#90a4ae" if c else "#2e7d32", "#fff", .8)
    f.circle(640, 448, 6, "#2e7d32"); f.text(652, 453, "ស្អាត", 13); f.circle(720, 448, 6, "#90a4ae"); f.text(732, 453, "មានពពក (រត់ចួល)", 13)
    f.line(840, 448, 870, 448, "#bdbdbd", 3); f.text(876, 453, "សញ្ញាពិត", 13)
    entry(5, f.save("a05-noise"), "ស៊េរីឆៅមានសំឡេងរំខាន",
          [f"ក្នុងរដូវវស្សា ការសង្កេត {kh(int(cl[(t>135)&(t<305)].sum()))} ក្នុងចំណោម {kh(int(((t>135)&(t<305)).sum()))} មានពពក៖ NDVI ធ្លាក់ខ្លាំងជាងតម្លៃពិត។", "ពពកតែងធ្វើឲ្យ NDVI ទាបជាងពិត មិនដែលខ្ពស់ជាងទេ។",
           "ដំណោះស្រាយ៖ mask ពពក (SCL · Cloud Score+) រួច composite ប្រចាំខែ ឬ smooth។"], .25)

    # 3 monthly median composites
    f = Fig(1000, 470).title("Composite ប្រចាំខែ ធ្វើឲ្យស៊េរីរលោង", "ស្រែវស្សាដដែល · mask ពពក រួច median ក្នុងខែនីមួយៗ · " + ILL)
    X, Y = chart(f, 80, 90, 820, 300, [(list(DOY), list(rice_wet(DOY)), "#bdbdbd", "", 2)], (1, 365), (0, 1), "", "NDVI", yt=[0, .2, .4, .6, .8, 1], legend=False)
    month_axis(f, X, 412)
    clear = ~cl
    for a, b in zip(t[clear], yo[clear]): f.circle(X(a), Y(b), 3.5, "#a5d6a7")
    mm = []
    for i, d in enumerate(MSTART):
        e = MSTART[i + 1] if i < 11 else 366; sel = clear & (t >= d) & (t < e)
        mm.append((d + 14, float(np.median(yo[sel])) if sel.any() else None))
    pts = [(X(a), Y(b)) for a, b in mm if b is not None]
    f.path("M" + " L".join(f"{p:.1f} {q:.1f}" for p, q in pts), "none", "#2e7d32", 3)
    for (a, b) in mm:
        if b is None: f.text(X(a), Y(.05), "?", 18, "#c62828", "middle", "bold")
        else: f.circle(X(a), Y(b), 6, "#2e7d32", "#fff", 1.5)
    nmiss = sum(1 for a, b in mm if b is None)
    f.circle(560, 448, 4, "#a5d6a7"); f.text(570, 453, "ការសង្កេតស្អាត", 13); f.circle(690, 448, 6, "#2e7d32"); f.text(702, 453, "median ប្រចាំខែ", 13); f.text(820, 453, "? ខែគ្មានទិន្នន័យ", 13, "#c62828")
    entry(5, f.save("a05-monthly"), "១២ តម្លៃ ជំនួសរាប់សិប",
          ["ee.List.sequence(1, 12).map() បង្កើត composite មួយក្នុងមួយខែ ហើយកំណត់ system:time_start។", "median ក្នុងខែ ដកតម្លៃពពកដែលរត់ចួលភាគច្រើន។",
           f"ខែខ្លះក្នុងរដូវវស្សាអាចគ្មានការសង្កេតស្អាតទាល់តែសោះ ({kh(nmiss)} ខែក្នុងឧទាហរណ៍នេះ)៖ ត្រូវការ Sentinel-1 ឬ harmonic។"], .38)

    # 4 rice stages with LSWI
    lswi = lambda tt: -.05 + .45 * np.exp(-((tt - 215) / 22) ** 2) + .25 * np.exp(-((tt - 270) / 45) ** 2) * (tt > 200)
    f = Fig(1000, 490).title("ដំណាក់កាលស្រូវវស្សា ក្នុងស៊េរីពេលវេលា", ILL)
    X, Y = chart(f, 80, 90, 820, 300, [(list(DOY), list(rice_wet(DOY)), "#2e7d32", "NDVI", 3), (list(DOY), list(lswi(DOY)), "#1565c0", "LSWI (ទឹក/សំណើម)", 3)], (1, 365), (-.1, 1), "", "តម្លៃសន្ទស្សន៍", yt=[0, .2, .4, .6, .8, 1], lx=620, ly=112)
    month_axis(f, X, 412)
    for d, t1, t2 in [(200, "បញ្ចូលទឹក ស្ទូង", "LSWI > NDVI"), (245, "លូតលាស់", "NDVI ឡើង"), (285, "ចេញផ្កា", "NDVI កំពូល"), (330, "ច្រូត", "NDVI ធ្លាក់")]:
        f.line(X(d), 90, X(d), 390, "#ef6c00", 1.5, "5 4"); f.text(X(d), 440, t1, 13, INK, "middle", "bold"); f.text(X(d), 462, t2, 12, "#607d8b", "middle")
    entry(5, f.save("a05-rice"), "ទឹកមុន បៃតងក្រោយ",
          ["ពេលបញ្ចូលទឹក និងស្ទូង វាលស្រែមានទឹកច្រើន៖ LSWI ឡើងលើស NDVI មួយរយៈខ្លី។", "បន្ទាប់មក NDVI ឡើងដល់កំពូលពេលចេញផ្កា ហើយធ្លាក់ពេលទុំ និងច្រូត។",
           "សញ្ញា «ទឹកមុន បៃតងក្រោយ» នេះ ប្រើសម្រាប់ធ្វើផែនទីស្រែក្នុងមេរៀនទី១១។"], .5)

    # 5 linear trend on annual maximum NDVI
    rng = np.random.default_rng(11); yrs = np.arange(2016, 2025); ymax = .78 - .018 * (yrs - 2016) + rng.normal(0, .02, yrs.size)
    b1, b0 = np.polyfit(yrs - 2016, ymax, 1)
    f = Fig(1000, 450).title("និន្នាការលីនេអ៊ែរ៖ linearFit()", "NDVI អតិបរមាប្រចាំឆ្នាំ នៃក្រឡាមួយដែលព្រៃត្រូវបានកាប់បន្តិចម្ដងៗ · " + ILL)
    X, Y = chart(f, 90, 90, 520, 280, [(list(yrs), list(b0 + b1 * (yrs - 2016)), "#c62828", "និន្នាការ", 2.5)], (2016, 2024), (.5, .9), "ឆ្នាំ", "NDVI អតិបរមា", xt=list(range(2016, 2025, 2)), yt=[.5, .6, .7, .8, .9], legend=False)
    for a, b in zip(yrs, ymax): f.circle(X(a), Y(b), 6, "#2e7d32", "#fff", 1.5)
    code(f, 640, 100, 330, ["var withT = col.map(function(img){", "  var t = img.date().difference(", "     '2016-01-01', 'year');", "  return img.select('NDVI')", "     .addBands(ee.Image(t)", "     .rename('t').float());});", "var fit = withT.select(['t','NDVI'])", "  .reduce(ee.Reducer.linearFit());", "// bands: scale (slope), offset"], 13)
    f.text(640, 360, f"ជម្រាល = {KHF(b1, 3)} NDVI/ឆ្នាំ", 16, "#c62828", weight="bold")
    entry(5, f.save("a05-trend"), "ជម្រាលមួយក្នុងមួយក្រឡា",
          ["linearFit() ត្រូវការក្រុមរលកពីរ តាមលំដាប់ [x, y]៖ ពេលវេលា t មុន NDVI។", "លទ្ធផលមានក្រុមរលក scale (ជម្រាល) និង offset៖ ជម្រាលអវិជ្ជមាន = រុក្ខជាតិថយចុះ។",
           "ប្រើតម្លៃប្រចាំឆ្នាំ (ឧ. អតិបរមា ឬរដូវតែមួយ) ដើម្បីកុំឲ្យរដូវកាលលាក់និន្នាការ។"], .62)

    # 6 harmonic regression
    t, yo, cl = s2_obs(rice_double, seed=5, cloud_wet=.35, cloud_dry=.1); keep = ~cl
    _, p1 = harmonic_fit(t[keep], yo[keep], 1); _, p2 = harmonic_fit(t[keep], yo[keep], 2)
    f = Fig(1000, 470).title("តំរែតំរង់ harmonic", "ស្រែពីរដង · ការសង្កេតស្អាត និងខ្សែសម · " + ILL)
    X, Y = chart(f, 80, 90, 600, 300, [(list(DOY), list(p1(DOY.astype(float))), "#ef6c00", "លំដាប់ ១", 3), (list(DOY), list(p2(DOY.astype(float))), "#6a1b9a", "លំដាប់ ២", 3)], (1, 365), (0, 1), "", "NDVI", yt=[0, .2, .4, .6, .8, 1], lx=330, ly=112)
    month_axis(f, X, 412)
    for a, b in zip(t[keep], yo[keep]): f.circle(X(a), Y(b), 4, "#2e7d32")
    f.rect(705, 95, 270, 300, "#f3e5f5", "#ce93d8", 1, 8)
    f.text(720, 125, "NDVI(t) =", 15, INK, weight="bold", extra='font-family="monospace"'); f.text(720, 152, "β₀ + β₁·t", 15, INK, extra='font-family="monospace"')
    f.text(720, 179, "+ a₁·cos(2πt) + b₁·sin(2πt)", 13, INK, extra='font-family="monospace"'); f.text(720, 204, "+ a₂·cos(4πt) + b₂·sin(4πt)", 13, INK, extra='font-family="monospace"')
    f.text(720, 244, "t គិតជាឆ្នាំ", 13, "#607d8b"); f.text(720, 274, "ទំហំ  = √(a₁² + b₁²)", 13, INK); f.text(720, 300, "ដំណាក់ = atan2(b₁, a₁)", 13, INK)
    f.text(720, 340, "reducer៖", 13, "#607d8b"); f.text(720, 364, "ee.Reducer.linearRegression", 12, INK, extra='font-family="monospace"')
    entry(5, f.save("a05-harmonic"), "ខ្សែកោងរលោង ពីការសង្កេតមិនទៀងទាត់",
          ["លំដាប់ ១ (cos និង sin មួយគូ) មានកំពូលតែមួយ/ឆ្នាំ៖ វាខកកំពូលទាំងពីរនៃស្រែពីរដង។ លំដាប់ ២ ចាប់បានទាំងពីរ។", "ខ្សែសមបំពេញចន្លោះពពក ហើយផ្ដល់តម្លៃនៅថ្ងៃណាក៏បាន។",
           "ទំហំ (amplitude) និងដំណាក់ (phase) ក្លាយជាក្រុមរលកថ្មី សម្រាប់ផែនទី និងការចាត់ថ្នាក់។"], .75)

    # 7 phenology metrics
    y = rice_wet(DOY.astype(float)); base, peak = y[150:250].min(), y.max(); thr = base + .5 * (peak - base)
    sos = int(DOY[200:][np.argmax(y[200:] > thr)]); pos = int(DOY[np.argmax(y)]); eos = int(DOY[pos:][np.argmax(y[pos:] < thr)])
    f = Fig(1000, 470).title("រង្វាស់រដូវកាល (phenology metrics)", "វិធីកម្រិត ៥០% នៃទំហំ · ស្រែវស្សា · " + ILL)
    X, Y = chart(f, 80, 90, 820, 300, [(list(DOY), list(y), "#2e7d32", "", 3)], (1, 365), (0, 1), "", "NDVI", yt=[0, .2, .4, .6, .8, 1], legend=False)
    month_axis(f, X, 412)
    f.line(X(1), Y(thr), X(365), Y(thr), "#90a4ae", 1.5, "6 4"); f.text(X(20), Y(thr) - 6, "កម្រិត ៥០%", 12, "#607d8b")
    for d, t1 in [(sos, "SOS ចាប់ផ្ដើម"), (pos, "POS កំពូល"), (eos, "EOS បញ្ចប់")]:
        yy = Y(thr if d != pos else peak); f.circle(X(d), yy, 7, AMB, "#fff", 2); f.text(X(d), yy - 14, t1, 13, INK, "middle", "bold")
    f.line(X(pos) - 30, Y(base), X(pos) - 30, Y(peak), "#6a1b9a", 2, arrow=True); f.text(X(pos) - 38, Y((base + peak) / 2 - .05), "ទំហំ", 13, "#6a1b9a", "end", weight="bold")
    f.line(X(sos), Y(.08), X(eos), Y(.08), "#ef6c00", 2, arrow=True); f.text((X(sos) + X(eos)) / 2, Y(.08) - 8, f"រយៈពេលរដូវ ≈ {kh(eos - sos)} ថ្ងៃ", 13, "#ef6c00", "middle", weight="bold")
    entry(5, f.save("a05-metrics"), "ពីខ្សែកោង ទៅជាលេខដែលអ្នកកសិកម្មយល់",
          ["SOS POS EOS ប្រាប់ពេលចាប់ផ្ដើម កំពូល និងបញ្ចប់រដូវ ជាថ្ងៃក្នុងឆ្នាំ (DOY)។", "កម្រិត ៥០% នៃទំហំ ធន់ជាងកម្រិត NDVI ថេរ ព្រោះវាសម្របតាមក្រឡានីមួយៗ។",
           "SOS ដែលយឺតជាងធម្មតា អាចបង្ហាញភ្លៀងយឺត ឬរាំងស្ងួតដើមរដូវ (មេរៀនទី៨)។"], .88)

# ---------------- Lesson 6 ----------------
def rf_data():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import confusion_matrix, accuracy_score, cohen_kappa_score
    B, C = scene(); b2, b3, b4, b5, b6, b7 = B
    ndvi, ndbi, mndwi = nd(b5, b4), nd(b6, b5), nd(b3, b6); bsi = ((b6 + b4) - (b5 + b2)) / ((b6 + b4) + (b5 + b2) + 1e-9)
    names = ["B2", "B3", "B4", "B5", "B6", "B7", "NDVI", "NDBI", "MNDWI", "BSI"]
    F = np.stack(list(B) + [ndvi, ndbi, mndwi, bsi], -1).reshape(-1, 10); y = C.ravel()
    rng = np.random.default_rng(7)
    idx = np.concatenate([rng.choice(np.flatnonzero(y == k), 150, replace=False) for k in range(5)]); rng.shuffle(idx)
    tr, te = idx[:525], idx[525:]
    sets = {"RGB (B2 B3 B4)": [0, 1, 2], "+ NIR SWIR (B2–B7)": list(range(6)), "+ សន្ទស្សន៍ ៤": list(range(10))}
    out = {}
    for k, cols in sets.items():
        m = RandomForestClassifier(50, random_state=1).fit(F[tr][:, cols], y[tr]); p = m.predict(F[te][:, cols])
        out[k] = dict(model=m, oa=accuracy_score(y[te], p), kappa=cohen_kappa_score(y[te], p), cm=confusion_matrix(y[te], p, labels=range(5)), cols=cols)
    return B, C, F, y, tr, te, names, out

def L06():
    B, C, F, y, tr, te, names, out = rf_data(); b2, b3, b4, b5, b6, b7 = B
    main = out["+ NIR SWIR (B2–B7)"]
    # 1 workflow
    f = Fig(1000, 420).title("លំហូរការងារចាត់ថ្នាក់ក្នុង Earth Engine")
    steps = [("Composite", "median · លុបពពក"), ("លក្ខណៈ", "ក្រុមរលក · សន្ទស្សន៍ · DEM"), ("ចំណុចគំរូ", "landcover = ០ ១ ២…"), ("sampleRegions", "តារាងបណ្ដុះបណ្ដាល"),
             ("train", "smileRandomForest"), ("classify", "ផែនទី"), ("errorMatrix", "ភាពត្រឹមត្រូវ"), ("ផ្ទៃ · Export", "pixelArea · Drive")]
    for i, (a, b) in enumerate(steps):
        x = 30 + (i % 4) * 240; yy = 95 + (i // 4) * 150; c = ["#a5d6a7", "#81c784", "#66bb6a", "#43a047", "#2e7d32", "#1b5e20", "#ef6c00", "#e65100"][i]
        box(f, x, yy, 210, 100, a, b, c, 17, INK if i < 2 else "#fff")
        if i % 4 < 3: f.line(x + 212, yy + 50, x + 236, yy + 50, "#607d8b", 2, arrow=True)
    f.path("M 945 245 C 985 245, 985 290, 945 290 L 150 290 C 110 290, 110 245, 135 245", "none", "#607d8b", 2, extra='marker-end="url(#arrow)"'); f.defs.add("arrow")
    f.text(500, 400, "ទ្រឹស្ដីចាត់ថ្នាក់ (សញ្ញាណស្ពិចត្រាល់ ការចាត់ថ្នាក់ត្រួតពិនិត្យ) មានក្នុងសៀវភៅទី៣", 14, "#607d8b", "middle")
    entry(6, f.save("a06-workflow"), "ប្រាំបីជំហាន ពីរូបភាពទៅផែនទីគម្របដី",
          ["ជំហាន ១–២៖ រៀបចំរូបភាព និងលក្ខណៈ (features) ដែល classifier នឹងមើល។", "ជំហាន ៣–៦៖ ចំណុចគំរូ → តារាង → បណ្ដុះបណ្ដាល → ចាត់ថ្នាក់រូបភាពទាំងមូល។",
           "ជំហាន ៧–៨៖ វាយតម្លៃភាពត្រឹមត្រូវ មុនគណនាផ្ទៃ ឬចែករំលែកផែនទី។"], .05)

    # 2 real spectral signatures
    f = Fig(1000, 470).title("សញ្ញាណស្ពិចត្រាល់នៃថ្នាក់ទាំងប្រាំ", "មធ្យម ± គម្លាតស្តង់ដារ · " + SRC_L8 + " · ថ្នាក់បានពីកម្រិតសន្ទស្សន៍")
    wl = [482, 561, 655, 865, 1609, 2201]
    ser = []
    for k in range(5):
        m = [float(B[i][C == k].mean()) for i in range(6)]; ser.append((wl, m, CLS_COL[k] if k != 4 else "#8d6e63", CLS_KH[k], 3))
    X, Y = chart(f, 90, 90, 620, 300, ser, (450, 2250), (0, .4), "រលកពន្លឺ (nm)", "ការចាំងផ្លាត TOA", xt=[500, 1000, 1500, 2000], yt=[0, .1, .2, .3, .4], lx=740, ly=120)
    for k in range(5):
        for i in range(6):
            s = float(B[i][C == k].std()); m = float(B[i][C == k].mean()); f.line(X(wl[i]), Y(m - s), X(wl[i]), Y(m + s), CLS_COL[k] if k != 4 else "#8d6e63", 1.2)
    for i, b in enumerate(["B2", "B3", "B4", "B5", "B6", "B7"]): f.text(X(wl[i]), 385, b, 11, "#90a4ae", "middle")
    entry(6, f.save("a06-signatures"), "Classifier រៀនពីភាពខុសគ្នានេះ",
          ["ទឹកទាបនៅ NIR និង SWIR (B5–B7)៖ ងាយបែងចែកបំផុត។", "តំបន់សាងសង់ និងដីទទេ ស្រដៀងគ្នានៅក្រុមរលកមើលឃើញ៖ ត្រូវការ SWIR ដើម្បីបែងចែក។",
           "របារបញ្ឈរ (± គម្លាតស្តង់ដារ) ត្រួតគ្នា៖ ដូច្នេះការចាត់ថ្នាក់មិនដែលល្អឥតខ្ចោះទេ។"], .2)

    # 3 training samples on real image
    f = Fig(1000, 470).title("ចំណុចគំរូ (training points)", "១៥០ ចំណុច/ថ្នាក់ · ៧០% បណ្ដុះបណ្ដាល · ៣០% ផ្ទៀងផ្ទាត់ · " + SRC_L8)
    f.img(rgb(b6, b5, b4), 30, 85, 360, 360); f.img(pal(C, CLS_COL), 420, 85, 360, 360, fmt="PNG")
    s = 360 / 300
    for j, i in enumerate(np.concatenate([tr, te])):
        r, c = divmod(int(i), 300); isTr = j < len(tr); x, yy = 30 + c * s, 85 + r * s
        if isTr: f.circle(x, yy, 3.2, CLS_COL[y[i]], "#fff", .9)
        else: f.rect(x - 3, yy - 3, 6, 6, CLS_COL[y[i]], "#000", .8)
    f.text(210, 462, "ពណ៌មិនពិត SWIR-NIR-Red + ចំណុច", 13, INK, "middle"); f.text(600, 462, "ផែនទីយោង (បានពីកម្រិតសន្ទស្សន៍)", 13, INK, "middle")
    f.legend_boxes(810, 110, CLS_COL, CLS_KH, "ថ្នាក់")
    f.circle(823, 300, 4, "#9e9e9e", "#fff"); f.text(844, 305, "បណ្ដុះបណ្ដាល", 13); f.rect(819, 322, 8, 8, "#9e9e9e", "#000"); f.text(844, 331, "ផ្ទៀងផ្ទាត់", 13)
    entry(6, f.save("a06-samples"), "ចំណុចគំរូ គឺជាគ្រូរបស់ classifier",
          ["ចំណុចត្រូវរាយពេញតំបន់ មិនប្រមូលផ្ដុំនៅកន្លែងតែមួយ។", "ថ្នាក់នីមួយៗត្រូវការចំណុចគ្រប់គ្រាន់ (៥០–១០០ ឡើងទៅ) និងតំណាងភាពខុសគ្នាក្នុងថ្នាក់ (ទឹកថ្លា ទឹកល្អក់…)។",
           "ចំណុចផ្ទៀងផ្ទាត់ ត្រូវតែដាច់ដោយឡែក៖ classifier មិនដែលឃើញវាពេលបណ្ដុះបណ្ដាលទេ។"], .35)

    # 4 random forest concept
    f = Fig(1000, 470).title("Random Forest៖ ដើមឈើសម្រេចចិត្តច្រើន បោះឆ្នោត")
    box(f, 30, 180, 180, 110, "ចំណុចគំរូ", "៥២៥ ចំណុច", "#546e7a")
    for i in range(4):
        yy = 90 + i * 85; f.line(212, 235, 262, yy + 30, "#90a4ae", 1.5, arrow=True)
        f.rect(265, yy, 170, 60, "#eceff1", "#b0bec5", 1, 8); f.text(350, yy + 25, f"គំរូចៃដន្យ {kh(i+1)}", 14, INK, "middle", "bold"); f.text(350, yy + 46, "bootstrap · √ លក្ខណៈ", 12, "#607d8b", "middle")
        cx = 520; f.line(437, yy + 30, 478, yy + 30, "#90a4ae", 1.5, arrow=True)
        f.circle(cx, yy + 12, 8, "#2e7d32"); f.line(cx, yy + 20, cx - 22, yy + 44, "#2e7d32", 2); f.line(cx, yy + 20, cx + 22, yy + 44, "#2e7d32", 2)
        f.circle(cx - 22, yy + 50, 7, "#66bb6a"); f.circle(cx + 22, yy + 50, 7, "#66bb6a")
        vote = [CLS_KH[3], CLS_KH[4], CLS_KH[3], CLS_KH[3]][i]; f.line(560, yy + 30, 640, 235, "#90a4ae", 1.5, arrow=True); f.text(600, yy + 25, vote, 13, CLS_COL[3] if vote == CLS_KH[3] else "#8d6e63", "middle", "bold")
    box(f, 645, 175, 150, 120, "បោះឆ្នោត", "៣ ធៀប ១", AMB); f.line(797, 235, 830, 235, "#607d8b", 2.5, arrow=True)
    box(f, 835, 185, 140, 100, CLS_KH[3], "លទ្ធផល", CLS_COL[3], 18)
    f.text(500, 440, "ee.Classifier.smileRandomForest(numberOfTrees, variablesPerSplit, minLeafPopulation, bagFraction)", 13, INK, "middle", extra='font-family="monospace"')
    entry(6, f.save("a06-rf"), "ហេតុអ្វី Random Forest ជាជម្រើសលំនាំដើម",
          ["ដើមឈើនីមួយៗរៀនពីគំរូចៃដន្យ (bootstrap) ហើយពិនិត្យតែផ្នែកនៃលក្ខណៈនៅការបំបែកនីមួយៗ។", "ដើមឈើខុសគ្នា ធ្វើកំហុសខុសគ្នា៖ ការបោះឆ្នោតភាគច្រើនកាត់បន្ថយកំហុសទាំងនោះ។",
           "ធន់នឹងលក្ខណៈច្រើន និងមិនត្រូវការ normalize ទិន្នន័យ៖ ៥០–១៥០ ដើមគ្រប់គ្រាន់ជាទូទៅ។"], .5)

    # 5 classified map vs reference (real)
    pred = main["model"].predict(F[:, main["cols"]]).reshape(300, 300)
    agree = (pred == C).mean()
    f = Fig(1000, 470).title("លទ្ធផល Random Forest ធៀបនឹងផែនទីយោង", "៥០ ដើម · លក្ខណៈ B2–B7 · " + SRC_L8)
    f.img(pal(pred, CLS_COL), 30, 85, 330, 330, fmt="PNG"); f.img(pal(C, CLS_COL), 380, 85, 330, 330, fmt="PNG")
    diff = np.where(pred == C, 255, 0).astype(np.uint8); dimg = Image.fromarray(np.dstack([np.full_like(diff, 255), diff, diff]))
    f.img(dimg, 730, 85, 240, 240, fmt="PNG")
    f.text(195, 440, "ចាត់ថ្នាក់ (RF)", 15, INK, "middle", "bold"); f.text(545, 440, "យោង", 15, INK, "middle", "bold"); f.text(850, 350, "ក្រហម = មិនត្រូវគ្នា", 14, "#c62828", "middle", "bold")
    f.text(850, 378, f"ត្រូវគ្នា {kh(round(agree*100))}% នៃក្រឡា", 14, INK, "middle")
    entry(6, f.save("a06-map"), "កំហុសមិនរាយស្មើទេ",
          ["កំហុសប្រមូលផ្ដុំនៅគែមទីក្រុង និងរវាងដំណាំ/ស្មៅ ជាមួយដើមឈើ និងដីទទេ។", "ទឹក (ទន្លេមេគង្គ និងទន្លេសាប) ត្រឹមត្រូវស្ទើរទាំងស្រុង។",
           "នេះជាការចាត់ថ្នាក់ពិតលើរូបភាព Landsat 8 ពិត ប៉ុន្តែផែនទីយោងបានពីកម្រិតសន្ទស្សន៍ មិនមែនការស្ទង់វាលទេ។"], .62)

    # 6 confusion matrix (real)
    cm = main["cm"]; n = cm.sum(); pa = cm.diagonal() / cm.sum(1); ua = cm.diagonal() / cm.sum(0)
    f = Fig(1000, 520).title("តារាងកំហុស (confusion matrix)", f"ចំណុចផ្ទៀងផ្ទាត់ {kh(int(n))} · Random Forest ៥០ ដើម · B2–B7")
    x0, y0, s = 250, 120, 62
    f.text(x0 + 2.5 * s, 100, "ចាត់ថ្នាក់ (classification)", 15, INK, "middle", "bold")
    f.text(x0 - 150, y0 + 2.5 * s, "យោង (landcover)", 15, INK, "middle", "bold", f'transform="rotate(-90 {x0-150} {y0+2.5*s})"')
    for i in range(5):
        f.text(x0 - 8, y0 + i * s + s / 2 + 5, CLS_KH[i], 12, INK, "end"); f.text(x0 + i * s + s / 2, y0 + 5 * s + 20, CLS_KH[i], 11, INK, "middle")
        for j in range(5):
            v = int(cm[i, j]); c = "#2e7d32" if i == j else ("#ffcdd2" if v > 0 else "#fafafa")
            f.rect(x0 + j * s, y0 + i * s, s - 2, s - 2, c, "#e0e0e0"); f.text(x0 + j * s + s / 2, y0 + i * s + s / 2 + 6, kh(v), 17, "#fff" if i == j else INK, "middle", "bold")
        f.text(x0 + 5 * s + 36, y0 + i * s + s / 2 + 6, kh(round(pa[i] * 100)) + "%", 14, "#1565c0", "middle", "bold")
        f.text(x0 + i * s + s / 2, y0 + 5 * s + 48, kh(round(ua[i] * 100)) + "%", 14, "#ef6c00", "middle", "bold")
    f.text(x0 + 5 * s + 36, y0 - 8, "PA", 14, "#1565c0", "middle", "bold"); f.text(x0 - 30, y0 + 5 * s + 48, "UA", 14, "#ef6c00", "end", weight="bold")
    f.rect(680, 130, 290, 230, "#fff8e1", "#ffcc80", 1.2, 10)
    f.text(700, 168, f"OA = {kh(round(main['oa']*100))}%", 22, INK, weight="bold"); f.text(700, 206, f"Kappa = {KHF(main['kappa'])}", 20, INK, weight="bold")
    f.text(700, 250, "PA៖ ពីទស្សនៈអ្នកផលិត", 14, "#1565c0"); f.text(700, 276, "(ភាគរយនៃយោងដែលរកឃើញ)", 13, "#607d8b")
    f.text(700, 308, "UA៖ ពីទស្សនៈអ្នកប្រើ", 14, "#ef6c00"); f.text(700, 334, "(ភាគរយនៃផែនទីដែលត្រឹមត្រូវ)", 13, "#607d8b")
    worst = int(np.argmin(pa))
    entry(6, f.save("a06-confusion"), "OA មួយលេខ មិនប្រាប់រឿងទាំងអស់ទេ",
          [f"OA {kh(round(main['oa']*100))}% ប៉ុន្តែ PA នៃ «{CLS_KH[worst]}» មានត្រឹម {kh(round(pa[worst]*100))}%៖ ថ្នាក់នេះច្រឡំច្រើនបំផុត។",
           "ជួរ = យោង · ជួរឈរ = ចាត់ថ្នាក់។ ក្រឡាក្រៅអង្កត់ទ្រូង ប្រាប់ថាថ្នាក់ណាច្រឡំជាមួយថ្នាក់ណា។",
           "ក្នុង Earth Engine៖ test.errorMatrix('landcover', 'classification') រួច .accuracy() .kappa() .producersAccuracy() .consumersAccuracy()។"], .78)

    # 7 feature sets + importance (real)
    f = Fig(1000, 470).title("លក្ខណៈបន្ថែម ជួយបង្កើនភាពត្រឹមត្រូវ", "OA លើចំណុចផ្ទៀងផ្ទាត់ដដែល · ភាពសំខាន់នៃលក្ខណៈពី Random Forest · " + SRC_L8)
    ks = list(out.keys()); bars(f, 30, 100, 440, 200, ks, [out[k]["oa"] * 100 for k in ks], ["#bdbdbd", "#66bb6a", "#2e7d32"], vmax=100, fmt=lambda v: kh(round(v)) + "%", lw=190)
    full = out["+ សន្ទស្សន៍ ៤"]; imp = full["model"].feature_importances_; order = np.argsort(-imp)
    f.text(520, 100, "ភាពសំខាន់ (ម៉ូដែលមាន ១០ លក្ខណៈ)", 15, INK, weight="bold")
    bars(f, 520, 115, 400, 300, [names[i] for i in order], [imp[i] * 100 for i in order], ["#ef6c00" if names[i] in ("NDVI", "NDBI", "MNDWI", "BSI") else "#43a047" for i in order], fmt=lambda v: kh(round(v)) + "%", lw=80)
    f.text(250, 345, "ក្នុង Earth Engine៖ classifier.explain()", 13, "#607d8b", "middle")
    f.text(250, 372, "ផ្ដល់ importance តាមលក្ខណៈ", 13, "#607d8b", "middle")
    entry(6, f.save("a06-features"), "អ្វីដែល classifier មើលឃើញ សំខាន់ដូចក្បួនដោះស្រាយ",
          [f"ក្រុមរលកមើលឃើញតែបី៖ OA {kh(round(out[ks[0]]['oa']*100))}%។ បន្ថែម NIR និង SWIR៖ {kh(round(out[ks[1]]['oa']*100))}%។",
           f"សន្ទស្សន៍បន្ថែម {kh(round((out[ks[2]]['oa']-out[ks[1]]['oa'])*100))} ពិន្ទុទៀត ប៉ុន្តែផែនទីយោងនេះបានពីសន្ទស្សន៍ ដូច្នេះការកើនឡើងនេះលំអៀង៖ ក្នុងការងារពិត ត្រូវប្រើយោងឯករាជ្យ។",
           "ក្នុងលំហាត់ទី៦ អ្នកនឹងបន្ថែម NDVI NDBI MNDWI BSI និងរយៈកម្ពស់ ជម្រាល ពី DEM ទៅ composite។"], .88)

    # 8 spatial leakage (real): 60 training polygons of 7 × 7 px, split by pixel vs by polygon
    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(3); cols = main["cols"]; P = []
    for k in range(5):
        n = 0
        while n < 12:
            r, c = rng.integers(4, 296, 2); blk = C[r - 3:r + 4, c - 3:c + 4]
            if (blk == k).mean() >= .8: P.append((int(r), int(c), k)); n += 1
    rng.shuffle(P); trP, teP = P[:42], P[42:]
    px = lambda Ps: np.array([(r + dr) * 300 + c + dc for r, c, k in Ps for dr in range(-3, 4) for dc in range(-3, 4)])
    tri, tei = px(trP), px(teP); allp = np.concatenate([tri, tei]); rng.shuffle(allp); a_, b_ = allp[:int(.7 * len(allp))], allp[int(.7 * len(allp)):]
    mA = RandomForestClassifier(50, random_state=1).fit(F[a_][:, cols], y[a_]); accA = (mA.predict(F[b_][:, cols]) == y[b_]).mean()
    mB = RandomForestClassifier(50, random_state=1).fit(F[tri][:, cols], y[tri]); accB = (mB.predict(F[tei][:, cols]) == y[tei]).mean()
    accT = (mA.predict(F[:, cols]) == y).mean()
    f = Fig(1000, 450).title("ចំណុចផ្ទៀងផ្ទាត់ជិតពេក បំប៉ោងភាពត្រឹមត្រូវ", "ពហុកោណបណ្ដុះបណ្ដាល ៦០ (៧ × ៧ ក្រឡា) · Random Forest ៥០ ដើម · " + SRC_L8)
    bars(f, 60, 100, 860, 230, ["បំបែកតាមក្រឡា (ពហុកោណដដែល)", "បំបែកតាមពហុកោណ", "ភាពត្រឹមត្រូវពិត (៩០ ០០០ ក្រឡា)"], [accA * 100, accB * 100, accT * 100],
         ["#e57373", "#43a047", "#1e88e5"], vmax=100, fmt=lambda v: kh(round(v)) + "%", lw=280)
    f.text(500, 385, "ក្រឡាក្នុងពហុកោណតែមួយ ស្រដៀងគ្នាខ្លាំង (spatial autocorrelation)៖ វាមិនមែនការសាកល្បងឯករាជ្យទេ", 15, "#c62828", "middle")
    entry(6, f.save("a06-leak"), "បំបែកពហុកោណ មិនមែនក្រឡា",
          [f"បំបែកក្រឡាដោយចៃដន្យ៖ ក្រឡាផ្ទៀងផ្ទាត់មានបងប្អូននៅក្នុងពហុកោណបណ្ដុះបណ្ដាល ហើយ OA ឡើងដល់ {kh(round(accA*100))}%។",
           f"បំបែកពហុកោណមុន (randomColumn លើ FeatureCollection) ផ្ដល់ {kh(round(accB*100))}% ជិតភាពត្រឹមត្រូវពិត {kh(round(accT*100))}%។",
           "កុំបំបែកដោយ lt(0.7) និង gte(0.3)៖ ចំណុច ៤០% នឹងនៅក្នុងក្រុមទាំងពីរ។ ត្រូវប្រើ lt(0.7) និង gte(0.7)។"], .8)
