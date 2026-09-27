"""Book 4 · Chapter 5 figures (Lessons 13–15).

Lesson 13 layers are built on the synthetic teaching DEM (dem_synthetic.json) plus
synthetic rainfall/soil; AHP weights and consistency ratio are real computations.
Lesson 14 water-area curve is illustrative. Lessons 15 figures are diagrams.
"""
from vis_core import *
from rs_chart import chart, bars
from vis_ag2 import ramp, box, code, KHF, MON
from vis_ag3 import synth_dem, fill_sinks, d8, flowacc, slope_aspect
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SYN = "ស្រទាប់ក្លែងធ្វើលើ DEM គំរូ (សម្រាប់បង្រៀន)"
def layers():
    z = synth_dem(); zf = fill_sinks(z); acc = flowacc(zf, d8(zf)); sl, _ = slope_aspect(z); n = z.shape[0]
    rng = np.random.default_rng(31); yy, xx = np.mgrid[0:n, 0:n] / n
    stream = acc > 400; dstr = ndi.distance_transform_edt(~stream) * 30
    rain = 1300 + 500 * yy + 80 * ndi.gaussian_filter(rng.normal(size=(n, n)), 12) * 10
    clay = np.clip(25 + 20 * (1 - xx) * .3 + 25 * ndi.gaussian_filter(rng.normal(size=(n, n)), 8) * 6, 5, 60)
    crop = (sl < 3) & (z < np.percentile(z, 55)); dcrop = ndi.distance_transform_edt(~crop) * 30
    forest = (sl > 8) | (z > np.percentile(z, 85)); village = np.zeros((n, n), bool)
    for cy, cx in ((40, 120), (110, 70), (130, 140)): village[cy - 3:cy + 3, cx - 3:cx + 3] = True
    return dict(z=z, slope=sl, dstr=dstr, rain=rain, clay=clay, dcrop=dcrop, forest=forest, water=stream & (acc > 3000), village=village)

def lin(a, lo, hi): return np.clip((a - lo) / (hi - lo), 0, 1)
def fuzzy_dec(a, a0, a1): return 1 - np.clip((a - a0) / (a1 - a0), 0, 1)

def ahp(M):
    M = np.array(M, float); w, v = np.linalg.eig(M); k = np.argmax(w.real); vec = np.abs(v[:, k].real); vec /= vec.sum()
    n = len(M); ci = (w[k].real - n) / (n - 1); ri = {3: .58, 4: .90, 5: 1.12}[n]; return vec, ci / ri

PAIR = [[1, 3, 2, 4], [1 / 3, 1, 1 / 2, 2], [1 / 2, 2, 1, 3], [1 / 4, 1 / 2, 1 / 3, 1]]
CRIT = ["ជម្រាល", "ចម្ងាយពីដំណាំ", "ដីឥដ្ឋ", "ទឹកភ្លៀង"]

def suitability(L, w):
    f = np.stack([fuzzy_dec(L["slope"], 1, 6), fuzzy_dec(L["dcrop"], 0, 1500), lin(L["clay"], 15, 45), lin(L["rain"], 1300, 1900)])
    s = np.tensordot(np.array(w) / sum(w), f, 1)
    cons = L["forest"] | L["water"] | ndi.binary_dilation(L["village"], iterations=4)
    return s, cons, f

def L13():
    L = layers(); w, cr = ahp(PAIR); s, cons, f = suitability(L, w); sm = np.where(cons, np.nan, s)
    # 1 workflow
    fg = Fig(1000, 400).title("លំហូរការវិភាគពហុលក្ខខណ្ឌ (MCDA)")
    steps = [("សំណួរ", "ទីតាំងអ្វី សម្រាប់អ្វី?", "#546e7a"), ("លក្ខខណ្ឌ", "កត្តា + ឧបសគ្គ", "#1565c0"), ("ស្តង់ដារ", "០–១ ដូចគ្នា", "#43a047"), ("ទម្ងន់", "ចំណាត់ថ្នាក់ · AHP", "#ef6c00"),
             ("បូកបញ្ចូល", "WLC · mask ឧបសគ្គ", "#6a1b9a"), ("ពិនិត្យ", "ភាពរសើប · វាល", "#c62828")]
    for i, (a, b, c) in enumerate(steps):
        x = 20 + i * 163; box(fg, x, 120, 148, 120, a, b, c, 16)
        if i < 5: fg.line(x + 150, 180, x + 161, 180, "#607d8b", 2, arrow=True)
    fg.text(500, 310, "S = Σ wᵢ · xᵢ  ×  Π cⱼ    (x = កត្តាស្តង់ដារ · c = ឧបសគ្គ ០/១)", 17, INK, "middle", "bold")
    entry(13, fg.save("a13-workflow"), "ប្រាំមួយជំហាន ពីសំណួរទៅទីតាំង",
          ["កត្តា (factor) មានកម្រិតល្អ–អាក្រក់ជាបន្ត៖ ជម្រាល ចម្ងាយ ទឹកភ្លៀង។ ឧបសគ្គ (constraint) ជា បាទ/ទេ៖ ព្រៃការពារ ទឹក ភូមិ។", "កត្តាត្រូវបម្លែងទៅជាមាត្រដ្ឋានដូចគ្នា (០–១) មុនបូកបញ្ចូល។",
           "Weighted Linear Combination (WLC) = ផលបូកមានទម្ងន់ ហើយឧបសគ្គគុណដើម្បីដកចេញ។"], .05)
    # 2 standardization curves
    fg = Fig(1000, 420).title("ស្តង់ដារកត្តា ទៅជា ០–១", "មុខងារសមាជិកភាព (membership)")
    x = np.linspace(0, 10, 200)
    X, Y = chart(fg, 80, 90, 380, 260, [(list(x), list(fuzzy_dec(x, 1, 6)), "#1565c0", "ជម្រាល (ថយ)", 3)], (0, 10), (0, 1), "ជម្រាល (°)", "ភាពសមស្រប", xt=[0, 2, 4, 6, 8, 10], yt=[0, .5, 1], legend=False)
    fg.text(X(6.5), Y(.85), "ល្អ ≤ ១° · អាក្រក់ ≥ ៦°", 13, "#1565c0")
    x2 = np.linspace(10, 60, 200); sig = 1 / (1 + np.exp(-(x2 - 30) / 4))
    X, Y = chart(fg, 560, 90, 380, 260, [(list(x2), list(lin(x2, 15, 45)), "#43a047", "លីនេអ៊ែរ", 3), (list(x2), list(sig), "#ef6c00", "sigmoid", 3)], (10, 60), (0, 1), "ដីឥដ្ឋ (%)", "", xt=[10, 20, 30, 40, 50, 60], yt=[0, .5, 1], lx=580, ly=110)
    entry(13, fg.save("a13-standardize"), "ឯកតាខុសគ្នា ត្រូវបម្លែងមុន",
          ["ដឺក្រេ ម៉ែត្រ mm និង % មិនអាចបូកគ្នាបានទេ៖ បម្លែងទាំងអស់ទៅ ០ (អាក្រក់) ដល់ ១ (ល្អ)។", "កត្តាខ្លះ «កាន់តែតិចកាន់តែល្អ» (ជម្រាល ចម្ងាយ)៖ ត្រូវបញ្ច្រាសទិស។",
           "ចំណុចបត់ (ឧ. ១° និង ៦°) មកពីអក្សរសិល្ប៍ ឬអ្នកជំនាញ៖ ត្រូវរាយការណ៍វា។ ក្នុង Earth Engine៖ unitScale() និង clamp()។"], .2)
    # 3 AHP (real computation)
    fg = Fig(1000, 440).title("ទម្ងន់ពី AHP", f"ការប្រៀបធៀបជាគូ Saaty (១–៩) · CR = {KHF(cr, 3)} {'< ០,១ ទទួលយកបាន' if cr < .1 else '≥ ០,១ ត្រូវកែ'}")
    x0, y0, c = 190, 110, 70
    for i in range(4):
        fg.text(x0 - 10, y0 + i * c + c / 2 + 5, CRIT[i], 13, INK, "end", "bold"); fg.text(x0 + i * c + c / 2, y0 - 10, CRIT[i], 11, INK, "middle", "bold")
        for j in range(4):
            v = PAIR[i][j]; t = kh(int(v)) if v >= 1 else "១/" + kh(int(round(1 / v)))
            fg.rect(x0 + j * c, y0 + i * c, c - 2, c - 2, "#eceff1" if i == j else ("#e8f5e9" if v > 1 else "#fff3e0")); fg.text(x0 + j * c + c / 2 - 1, y0 + i * c + c / 2 + 6, t, 16, INK, "middle", "bold")
    bars(fg, 540, 120, 420, 220, CRIT, [v * 100 for v in w], ["#1565c0", "#43a047", "#8d6e63", "#0288d1"], vmax=60, fmt=lambda v: kh(round(v)) + "%", lw=120)
    fg.text(750, 380, "ទម្ងន់ = eigenvector អតិបរមា (ធ្វើឲ្យផលបូក = ១)", 13, "#607d8b", "middle")
    entry(13, fg.save("a13-ahp"), "ប្រៀបធៀបម្ដងពីរ ងាយជាងប្រៀបធៀបទាំងអស់",
          ["«ជម្រាលសំខាន់ជាងទឹកភ្លៀង ៤ ដង»៖ ការសម្រេចពីរៗ ងាយជាងការដាក់ទម្ងន់ ៤ ក្នុងពេលតែមួយ។", f"ទម្ងន់ពី AHP៖ {', '.join(f'{c} {kh(round(v * 100))}%' for c, v in zip(CRIT, w))}។",
           "CR (consistency ratio) < ០,១៖ ការសម្រេចមិនផ្ទុយគ្នាខ្លាំង។ តួលេខគណនាពិតពីម៉ាទ្រីសនេះ។"], .35)
    # 4 WLC maps (computed on synthetic layers)
    fg = Fig(1000, 440).title("Weighted Linear Combination", SYN)
    cols = [["#f7fbff", "#08519c"], ["#f7fcf5", "#006d2c"], ["#fff5eb", "#7f2704"], ["#f7fbff", "#08306b"]]
    for k in range(4):
        fg.img(ramp(f[k], cols[k], 0, 1), 20 + k * 118, 90, 108, 108); fg.text(74 + k * 118, 216, f"{CRIT[k]} · {kh(round(w[k] * 100))}%", 11, INK, "middle")
    rgbm = np.array(ramp(np.nan_to_num(sm, nan=0), ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"], 0.2, .9)); rgbm[cons] = (200, 200, 200)
    fg.img(Image.fromarray(rgbm), 520, 85, 300, 300, fmt="PNG")
    fg.text(250, 260, "×  ទម្ងន់  →  បូក", 18, IND, "middle", "bold"); fg.line(480, 150, 510, 150, "#607d8b", 2.5, arrow=True)
    code(fg, 20, 290, 470, [f"var S = slopeF.multiply({w[0]:.2f})", f"  .add(cropF.multiply({w[1]:.2f}))", f"  .add(clayF.multiply({w[2]:.2f})).add(rainF.multiply({w[3]:.2f}))", "  .updateMask(notForest).updateMask(notWater);"], 13)
    fg.text(840, 120, "ប្រផេះ = ឧបសគ្គ", 13, "#607d8b"); fg.text(840, 145, "បៃតង = សមស្រប", 13, "#1a9641"); fg.text(840, 170, "ក្រហម = មិនសម", 13, "#d7191c")
    entry(13, fg.save("a13-wlc"), "ផែនទីភាពសមស្រប",
          ["ក្រឡានីមួយៗទទួលពិន្ទុ ០–១៖ ផលបូកមានទម្ងន់នៃកត្តាស្តង់ដារ។", "ពិន្ទុខ្ពស់នៅកន្លែងដែលរាបស្មើ ជិតដំណាំ និងដីឥដ្ឋច្រើន៖ ប៉ុន្តែកត្តាខ្សោយមួយអាចត្រូវបានទូទាត់ដោយកត្តាល្អ (compensation)។",
           "ប្រសិនបើកត្តាណាមួយមិនអាចទូទាត់បាន (ឧ. ជម្រាល > ១០°) វាត្រូវតែជាឧបសគ្គ មិនមែនកត្តាទេ។"], .5)
    # 5 constraints
    fg = Fig(1000, 400).title("ឧបសគ្គ (constraints)", "ក្រឡាដែលមិនអាចប្រើ ទោះបីពិន្ទុខ្ពស់ក៏ដោយ · " + SYN)
    items = [("ព្រៃ / ជម្រាលខ្លាំង", L["forest"], "#2e7d32"), ("ទឹក / ទន្លេ", L["water"], "#1e88e5"), ("ភូមិ + ១២០ ម", ndi.binary_dilation(L["village"], iterations=4), "#e53935"), ("រួម", cons, "#616161")]
    for k, (lab, m, col) in enumerate(items):
        im = np.full(m.shape + (3,), 245, np.uint8); im[m] = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5)); fg.img(Image.fromarray(im), 30 + k * 240, 90, 210, 210, fmt="PNG"); fg.text(135 + k * 240, 325, lab, 14, INK, "middle", "bold")
    fg.text(500, 370, f"ផ្ទៃដែលនៅសល់៖ {kh(round((~cons).mean() * 100))}% នៃតំបន់", 15, "#607d8b", "middle")
    entry(13, fg.save("a13-constraints"), "ឧបសគ្គជា ០ ឬ ១",
          ["ឧបសគ្គមកពីច្បាប់ (តំបន់ការពារ) រូបវិទ្យា (ទឹក ជម្រាល) ឬសង្គម (ចម្ងាយពីភូមិ ផ្លូវ)។", "ក្នុង Earth Engine៖ updateMask() ជាមួយរូបភាព ០/១ ឬ where() ដើម្បីដាក់ពិន្ទុ ០។",
           "ឧបសគ្គច្រើនពេក អាចមិនសល់ទីតាំងណាទេ៖ ពិនិត្យផ្ទៃដែលនៅសល់ជានិច្ច។"], .6)
    # 6 sensitivity (computed)
    base_top = np.nan_to_num(sm, nan=-1) >= np.nanpercentile(sm, 90); res = []
    for k in range(4):
        for d in (-.2, .2):
            ww = w.copy(); ww[k] *= 1 + d; s2, _, _ = suitability(L, ww); s2 = np.where(cons, np.nan, s2); top = np.nan_to_num(s2, nan=-1) >= np.nanpercentile(s2, 90)
            res.append((CRIT[k], d, (top & base_top).sum() / base_top.sum() * 100))
    fg = Fig(1000, 420).title("ការវិភាគភាពរសើប", "ប្ដូរទម្ងន់ម្ដងមួយ ±២០% · % នៃទីតាំងល្អបំផុត ១០% ដែលនៅដដែល · " + SYN)
    for i, (c, d, v) in enumerate(res):
        x = 80 + i * 105; h = v / 100 * 240; col = "#43a047" if v > 85 else "#ef6c00" if v > 70 else "#c62828"
        fg.rect(x, 340 - h, 70, h, col); fg.text(x + 35, 330 - h, kh(round(v)) + "%", 13, INK, "middle", "bold"); fg.text(x + 35, 360, c, 11, INK, "middle"); fg.text(x + 35, 378, ("−" if d < 0 else "+") + "២០%", 11, "#607d8b", "middle")
    entry(13, fg.save("a13-sensitivity"), "ទីតាំងល្អ មិនគួរពឹងលើលេខទម្ងន់មួយ",
          ["ប្រសិនបើប្ដូរទម្ងន់តិចតួច ហើយទីតាំងល្អប្ដូរទាំងស្រុង លទ្ធផលមិនរឹងមាំទេ។", f"នៅទីនេះ ទីតាំងល្អបំផុតនៅដដែល {kh(round(min(r[2] for r in res)))}–{kh(round(max(r[2] for r in res)))}%៖ លទ្ធផលរឹងមាំ។ ការប្ដូរ «{min(res, key=lambda r: r[2])[0]}» ប៉ះពាល់ច្រើនបំផុត។",
           "រាយការណ៍ទីតាំងដែលល្អក្នុងគ្រប់សេណារីយ៉ូ ជាការណែនាំដែលរឹងមាំជាងគេ។"], .75)
    # 7 from map to candidate sites
    lab_, nlab = ndi.label(np.nan_to_num(sm, nan=0) > np.nanpercentile(sm, 95)); sizes = ndi.sum(np.ones_like(sm), lab_, range(1, nlab + 1)); good = np.argsort(-sizes)[:5] + 1
    fg = Fig(1000, 420).title("ពីផែនទី ទៅទីតាំងបេក្ខភាព", "ក្រុមក្រឡាល្អបំផុត ៥% · ៥ ក្រុមធំជាងគេ · " + SYN)
    rgb2 = rgbm.copy(); rgb2[np.isin(lab_, good)] = (106, 27, 154); fg.img(Image.fromarray(rgb2), 30, 85, 300, 300, fmt="PNG")
    for r, g in enumerate(good):
        cy, cx = ndi.center_of_mass(lab_ == g); fg.circle(30 + cx * 300 / 160, 85 + cy * 300 / 160, 11, "#fff", "#6a1b9a", 2); fg.text(30 + cx * 300 / 160, 90 + cy * 300 / 160, kh(r + 1), 12, "#6a1b9a", "middle", "bold")
        fg.text(380, 130 + r * 40, f"{kh(r + 1)}. ផ្ទៃ {KHF(sizes[g - 1] * 900 / 1e4, 1)} ហិកតា · ពិន្ទុមធ្យម {KHF(np.nanmean(sm[lab_ == g]), 2)}", 15, INK)
    fg.text(380, 350, "→ ពិនិត្យវាល · ពិគ្រោះសហគមន៍ · កម្មសិទ្ធិដី", 15, "#c62828", weight="bold")
    entry(13, fg.save("a13-candidates"), "ផែនទីជួយតម្រង មិនមែនសម្រេច",
          ["connectedPixelCount() និង reduceToVectors() បម្លែងក្រឡាល្អ ទៅជាតំបន់បេក្ខភាពដែលមានផ្ទៃ។", "ដកតំបន់តូចពេក ហើយតម្រៀបតាមផ្ទៃ និងពិន្ទុ។",
           "ទីតាំងបេក្ខភាពត្រូវតែពិនិត្យនៅវាល ហើយពិភាក្សាជាមួយសហគមន៍ និងអាជ្ញាធរ មុនសម្រេច។"], .9)

def L14():
    # 1 app anatomy
    f = Fig(1000, 460).title("រចនាសម្ព័ន្ធកម្មវិធី Earth Engine")
    f.rect(40, 90, 920, 330, "#fafafa", "#90a4ae", 2, 10)
    f.rect(55, 105, 250, 300, "#e3f2fd", "#64b5f6", 1.5, 8); f.text(180, 130, "ui.Panel (ផ្ទាំងបញ្ជា)", 15, "#1565c0", "middle", "bold")
    for i, (a, b) in enumerate([("ui.Label", "ចំណងជើង · ការពន្យល់"), ("ui.Select", "ជ្រើសខេត្ត"), ("ui.Slider", "ជ្រើសឆ្នាំ"), ("ui.Button", "គណនា"), ("ui.Chart", "ក្រាប")]):
        f.rect(70, 145 + i * 50, 220, 40, "#fff", "#90caf9", 1, 6); f.text(82, 170 + i * 50, a, 13, INK, weight="bold", extra='font-family="monospace"'); f.text(180, 170 + i * 50, b, 12, "#607d8b")
    f.rect(320, 105, 625, 300, "#e8f5e9", "#81c784", 1.5, 8); f.text(632, 130, "ui.Map (ផែនទី)", 15, "#2e7d32", "middle", "bold")
    f.path("M420 330 C 480 250, 560 280, 620 230 S 760 200, 860 260", "none", "#1e88e5", 5); f.circle(700, 240, 8, "#c62828"); f.text(712, 234, "Map.onClick", 13, "#c62828", weight="bold", extra='font-family="monospace"')
    f.text(500, 445, "ui.root.clear() · ui.root.add(panel) · ui.root.add(map)  ឬ  ui.SplitPanel", 14, INK, "middle", extra='font-family="monospace"')
    entry(14, f.save("a14-anatomy"), "ផ្ទាំងបញ្ជា + ផែនទី",
          ["កម្មវិធីភាគច្រើនមានផ្ទាំងបញ្ជា (widgets) នៅម្ខាង និងផែនទីធំនៅម្ខាងទៀត។", "Widgets ទាំងអស់ជាវត្ថុ ui.* ដែលដាក់ក្នុង ui.Panel។",
           "អ្នកប្រើមិនឃើញកូដទេ៖ ពួកគេឃើញតែផ្ទាំង ផែនទី និងក្រាប។"], .05)
    # 2 widgets table
    f = Fig(1000, 470).title("Widgets សំខាន់ៗ")
    rows = [("ui.Label", "អត្ថបទ · តំណ", "value · style"), ("ui.Button", "ចុចដើម្បីរត់មុខងារ", "onClick"), ("ui.Select", "បញ្ជីជម្រើស", "items · onChange"), ("ui.Slider", "លេខក្នុងចន្លោះ", "min · max · step · onChange"),
            ("ui.DateSlider", "ជ្រើសកាលបរិច្ឆេទ", "start · end · onChange"), ("ui.Checkbox", "បើក/បិទស្រទាប់", "onChange"), ("ui.Chart", "ក្រាបពី ui.Chart.*", "setOptions"), ("ui.Thumbnail", "រូបភាពតូច · GIF", "image · params")]
    for i, (a, b, c) in enumerate(rows):
        y = 90 + i * 45; f.rect(40, y, 920, 38, "#f5f5f5" if i % 2 == 0 else "#fff"); f.text(56, y + 25, a, 14, IND, weight="bold", extra='font-family="monospace"'); f.text(290, y + 25, b, 14, INK); f.text(620, y + 25, c, 13, "#607d8b", extra='font-family="monospace"')
    entry(14, f.save("a14-widgets"), "ប្លុកសាងសង់នៃកម្មវិធី",
          ["Widget នីមួយៗមាន style (ទំហំ ពណ៌ ពុម្ពអក្សរ) និង callback (មុខងារដែលរត់ពេលអ្នកប្រើធ្វើអ្វីមួយ)។", "ui.Chart.* ដដែលក្នុង Console អាចដាក់ក្នុង Panel បាន។",
           "ពុម្ពអក្សរខ្មែរបង្ហាញបានក្នុងកម្មវិធី ប៉ុន្តែទំហំ និងចន្លោះបន្ទាត់ត្រូវកែតាម style។"], .2)
    # 3 events flow
    f = Fig(1000, 400).title("ព្រឹត្តិការណ៍ និង callback")
    steps = [("អ្នកប្រើ", "ជ្រើសឆ្នាំ ២០២៤", "#546e7a"), ("onChange", "callback(value)", "#1565c0"), ("គណនា", "filterDate · median · Otsu", "#43a047"), ("ធ្វើបច្ចុប្បន្នភាព", "map.layers().set()", "#ef6c00"), ("ក្រាប", "panel.widgets().set()", "#6a1b9a")]
    for i, (a, b, c) in enumerate(steps):
        x = 25 + i * 195; box(f, x, 120, 175, 110, a, b, c, 16)
        if i < 4: f.line(x + 177, 175, x + 193, 175, "#607d8b", 2, arrow=True)
    f.text(500, 300, "yearSlider.onChange(function(y) { map.layers().set(0, ui.Map.Layer(water(y), vis, 'water ' + y)); });", 13, INK, "middle", extra='font-family="monospace"')
    entry(14, f.save("a14-events"), "កម្មវិធីរង់ចាំ ហើយឆ្លើយតប",
          ["callback គឺជាមុខងារដែលយើងផ្ដល់ឲ្យ widget៖ វារត់តែនៅពេលអ្នកប្រើធ្វើសកម្មភាព។", "ប្ដូរស្រទាប់ដោយ layers().set() ជំនួស addLayer() ម្ដងទៀត ដើម្បីកុំឲ្យស្រទាប់ជាន់គ្នារាប់សិប។",
           "គណនាតែអ្វីដែលត្រូវការ៖ កម្មវិធីដែលរង់ចាំយូរ ធ្វើឲ្យអ្នកប្រើចាកចេញ។"], .35)
    # 4 client vs server
    f = Fig(1000, 420).title("getInfo() ឬ evaluate()?")
    box(f, 60, 110, 330, 120, "getInfo()", "កម្មវិធីរុករក «ជាប់គាំង» រហូតដល់ម៉ាស៊ីនមេឆ្លើយ", "#c62828", 18)
    box(f, 610, 110, 330, 120, "evaluate(callback)", "កម្មវិធីនៅតែដំណើរការ · callback រត់ពេលមានចម្លើយ", "#2e7d32", 18)
    f.text(225, 280, "var n = col.size().getInfo();", 14, INK, "middle", extra='font-family="monospace"'); f.text(775, 280, "col.size().evaluate(function(n) {", 14, INK, "middle", extra='font-family="monospace"'); f.text(775, 305, "  label.setValue('images: ' + n); });", 14, INK, "middle", extra='font-family="monospace"')
    f.text(500, 370, "ក្នុងកម្មវិធី៖ ប្រើ evaluate() ជានិច្ច · រក្សាវត្ថុ ee.* នៅលើម៉ាស៊ីនមេឲ្យបានយូរបំផុត", 15, "#607d8b", "middle")
    entry(14, f.save("a14-evaluate"), "កុំឲ្យកម្មវិធីគាំង",
          ["getInfo() ទាញលទ្ធផលមកម៉ាស៊ីនភ្ញៀវ ហើយរង់ចាំ៖ ក្នុងកម្មវិធី វាធ្វើឲ្យផ្ទាំងទាំងមូលកក។", "evaluate() ស្នើលទ្ធផល ហើយបន្តដំណើរការ៖ ពេលចម្លើយមកដល់ callback ធ្វើបច្ចុប្បន្នភាព Label ឬ Chart។",
           "បង្ហាញ «កំពុងគណនា…» មុន evaluate ដើម្បីឲ្យអ្នកប្រើដឹងថាកម្មវិធីកំពុងធ្វើការ (មេរៀនទី២៖ client ធៀប server)។"], .5)
    # 5 split panel
    f = Fig(1000, 400).title("ផែនទីពីរភ្ជាប់គ្នា៖ ui.SplitPanel", "មុន ធៀបនឹង ក្រោយ")
    f.rect(60, 90, 880, 250, "#fafafa", "#90a4ae", 1.5, 8); f.rect(62, 92, 438, 246, "#e3f2fd"); f.rect(500, 92, 438, 246, "#fff3e0"); f.line(500, 92, 500, 338, INK, 4)
    f.text(280, 215, "រដូវប្រាំង", 20, "#1565c0", "middle", "bold"); f.text(720, 215, "រដូវទឹកឡើង", 20, "#e65100", "middle", "bold")
    f.text(500, 375, "var linker = ui.Map.Linker([left, right]);  ui.root.widgets().reset([ui.SplitPanel({firstPanel: left, secondPanel: right, wipe: true})]);", 12, INK, "middle", extra='font-family="monospace"')
    entry(14, f.save("a14-split"), "ប្រៀបធៀបដោយអូស",
          ["ui.Map.Linker ធ្វើឲ្យផែនទីទាំងពីរ zoom និងរំកិលជាមួយគ្នា។", "wipe: true បង្កើតរបារអូស ដូចពិសោធន៍ក្រុងព្រះសីហនុ ក្នុងមេរៀនទី១២។",
           "ល្អសម្រាប់ទឹកជំនន់ មុន/ក្រោយ ការបាត់បង់ព្រៃ និងការពង្រីកទីក្រុង។"], .65)
    # 6 illustrative Tonle Sap water area series
    rng = np.random.default_rng(8); m = np.arange(12 * 5); area = 2700 + 7500 * ((1 + np.cos(2 * np.pi * (m % 12 - 9) / 12)) / 2) ** 1.5 + rng.normal(0, 250, m.size)
    f = Fig(1000, 420).title("ក្រាបក្នុងកម្មវិធីតាមដានទឹក", "ផ្ទៃទឹកទន្លេសាបប្រចាំខែ · តម្លៃគំរូ (លំហាត់ទី១៤ គណនាតម្លៃពិត)")
    X, Y = chart(f, 90, 90, 820, 260, [(list(m), list(area), "#1565c0", "ផ្ទៃទឹក", 2.5)], (0, 59), (0, 12000), "", "គម²", yt=[0, 4000, 8000, 12000], legend=False)
    for k in range(5): f.text(X(k * 12 + 6), 375, kh(2020 + k), 13, "#546e7a", "middle")
    entry(14, f.save("a14-chart"), "ពីកូដ ទៅឧបករណ៍ដែលអ្នកដទៃប្រើបាន",
          ["កម្មវិធីតាមដានទឹក ទាញផ្ទៃទឹកប្រចាំខែ ហើយបង្ហាញក្រាប និងផែនទីនៃខែដែលអ្នកប្រើចុច។", "ក្រាបត្រូវគណនាលើម៉ាស៊ីនមេ៖ ក្រាបដែលមានច្រើនខែ ច្រើនឆ្នាំ អាចយឺត ដូច្នេះគណនាទុកមុនជា Asset បាន។",
           "តម្លៃក្នុងក្រាបនេះជាគំរូ ដើម្បីបង្ហាញទម្រង់។"], .8)
    # 7 publishing steps
    f = Fig(1000, 400).title("ការបោះពុម្ពកម្មវិធី")
    steps = [("Cloud Project", "ចុះឈ្មោះ Earth Engine", "#546e7a"), ("Apps → New App", "ជ្រើសស្គ្រីប", "#1565c0"), ("សិទ្ធិ Asset", "Anyone can read", "#43a047"), ("URL សាធារណៈ", "…/view/app-name", "#ef6c00"), ("ធ្វើបច្ចុប្បន្នភាព", "Publish ម្ដងទៀត", "#6a1b9a")]
    for i, (a, b, c) in enumerate(steps):
        x = 25 + i * 195; box(f, x, 120, 175, 110, a, b, c, 16)
        if i < 4: f.line(x + 177, 175, x + 193, 175, "#607d8b", 2, arrow=True)
    f.text(500, 300, "អ្នកប្រើកម្មវិធីមិនត្រូវការគណនី Earth Engine ទេ · ការគណនាគិតលើ Cloud Project របស់អ្នកបោះពុម្ព", 14, "#607d8b", "middle")
    entry(14, f.save("a14-publish"), "ចែករំលែកដោយតំណមួយ",
          ["កម្មវិធីត្រូវភ្ជាប់ជាមួយ Cloud Project ដែលបានចុះឈ្មោះ Earth Engine (មិនមែនពាណិជ្ជកម្ម ឬពាណិជ្ជកម្ម)។", "Asset ដែលកម្មវិធីប្រើ (ចំណុច ព្រំដែន) ត្រូវតែអាចអានបានដោយកម្មវិធី។",
           "ពិនិត្យលក្ខខណ្ឌប្រើប្រាស់ និងកូតាជាប្រចាំ៖ ច្បាប់ទាំងនេះប្ដូរតាមពេលវេលា។"], .92)

def L15():
    # 1 project cycle
    f = Fig(1000, 440).title("វដ្ដគម្រោងអនុវត្ត")
    steps = [("សំណួរ", "ច្បាស់ · តូចល្មម · មានអ្នកប្រើ"), ("ទិន្នន័យ", "ប្រភព · ឆ្នាំ · ក្រឡា · អាជ្ញាបណ្ណ"), ("វិធីសាស្ត្រ", "មេរៀន ៣–១៣"), ("ផ្ទៀងផ្ទាត់", "ចំណុច · ស្ថិតិ · ភាពរសើប"), ("ទំនាក់ទំនង", "ផែនទី · របាយការណ៍ · កម្មវិធី")]
    cx, cy, r = 500, 275, 140
    for i, (a, b) in enumerate(steps):
        ang = -np.pi / 2 + i * 2 * np.pi / 5; x, y = cx + 2.3 * r * np.cos(ang), cy + 1.15 * r * np.sin(ang)
        box(f, x - 95, y - 38, 190, 76, a, b, ["#1565c0", "#43a047", "#ef6c00", "#c62828", "#6a1b9a"][i], 16)
    f.text(cx, cy + 6, "ឆ្លុះបញ្ចាំង", 16, "#607d8b", "middle", "bold")
    entry(15, f.save("a15-cycle"), "ចាប់ផ្ដើមពីសំណួរ មិនមែនពីទិន្នន័យ",
          ["សំណួរល្អ មានអ្នកប្រើច្បាស់ (អ្នកណានឹងប្រើចម្លើយ) និងតូចល្មមសម្រាប់ ៤–៦ សប្ដាហ៍។", "ជំហាននីមួយៗអាចត្រឡប់ក្រោយ៖ ការផ្ទៀងផ្ទាត់អាចបង្ហាញថាត្រូវប្ដូរទិន្នន័យ ឬវិធីសាស្ត្រ។",
           "ទំនាក់ទំនងជាផ្នែកនៃគម្រោង៖ លទ្ធផលដែលគ្មាននរណាយល់ គ្មានផលប៉ះពាល់ទេ។"], .05)
    # 2 proposal template
    f = Fig(1000, 470).title("ពុម្ពសំណើគម្រោង (១ ទំព័រ)")
    rows = [("១. ចំណងជើង", "ខ្លី ច្បាស់ មានទីកន្លែង និងពេលវេលា"), ("២. បញ្ហា និងអ្នកប្រើ", "ហេតុអ្វីសំខាន់ · អ្នកណានឹងប្រើ"), ("៣. សំណួរស្រាវជ្រាវ", "១–២ សំណួរ ដែលអាចឆ្លើយបាន"), ("៤. តំបន់ និងរយៈពេល", "AOI · ឆ្នាំ · រដូវ"),
            ("៥. ទិន្នន័យ", "ID Earth Engine · ក្រឡា · អាជ្ញាបណ្ណ"), ("៦. វិធីសាស្ត្រ", "ជំហាន ៥–៨ · មេរៀនដែលពាក់ព័ន្ធ"), ("៧. ការផ្ទៀងផ្ទាត់", "ចំណុច · ស្ថិតិ · ការពិនិត្យដោយភ្នែក"), ("៨. លទ្ធផល និងកាលវិភាគ", "ផែនទី · តារាង · កម្មវិធី · ប្រចាំសប្ដាហ៍")]
    for i, (a, b) in enumerate(rows):
        y = 88 + i * 46; f.rect(60, y, 880, 40, "#f5f5f5" if i % 2 == 0 else "#fff"); f.text(80, y + 26, a, 15, IND, weight="bold"); f.text(380, y + 26, b, 14, INK)
    entry(15, f.save("a15-proposal"), "សំណើល្អ = គម្រោងពាក់កណ្ដាលរួច",
          ["ការសរសេរសំណើ បង្ខំឲ្យកំណត់ទិន្នន័យ និងវិធីសាស្ត្រ មុនចំណាយពេលសរសេរកូដ។", "គ្រូពិនិត្យសំណើ ដើម្បីធានាថាវិសាលភាពសមរម្យ ហើយទិន្នន័យមានពិតប្រាកដ។",
           "ពុម្ពនេះក៏ប្រើជាក្បាលនៃរបាយការណ៍ចុងក្រោយបានដែរ។"], .2)
    # 3 reproducibility checklist
    f = Fig(1000, 440).title("បញ្ជីពិនិត្យភាពអាចធ្វើឡើងវិញ (reproducibility)")
    items = ["ស្គ្រីបមួយ ឬច្រើន ដែលរត់ពីដើមដល់ចប់ ដោយគ្មានការកែដោយដៃ", "ID និងកំណែទិន្នន័យ (ឧ. Hansen v1.11) · កាលបរិច្ឆេទ · scale · CRS", "seed សម្រាប់ randomColumn និង classifier",
             "Asset ដែលប្រើ ចែករំលែក «Anyone can read»", "កម្រិត និងទម្ងន់ទាំងអស់ ជាអថេរនៅដើមស្គ្រីប", "README៖ របៀបរត់ · លទ្ធផល · ដែនកំណត់", "រក្សាទុកក្នុង Git (GitHub) ជាមួយកំណែ"]
    for i, t in enumerate(items):
        y = 100 + i * 45; f.rect(60, y, 30, 30, "#e8f5e9", "#43a047", 2, 6); f.text(75, y + 22, "✓", 18, "#2e7d32", "middle", "bold"); f.text(110, y + 22, t, 15, INK)
    entry(15, f.save("a15-reproducible"), "អ្នកដទៃអាចធ្វើតាមបានទេ?",
          ["ការសាកល្បងល្អបំផុត៖ ឲ្យមិត្តភក្ដិរត់ស្គ្រីបរបស់អ្នក ដោយគ្មានការពន្យល់ ហើយមើលថាបានលទ្ធផលដូចគ្នាឬទេ។", "Earth Engine ធ្វើបច្ចុប្បន្នភាពទិន្នន័យ៖ កាលបរិច្ឆេទ និងកំណែ ជាផ្នែកនៃលទ្ធផល។",
           "សៀវភៅទាំង ៤ ក្បាលនេះ ក៏រក្សាទុកក្នុង GitHub ដូចគ្នាដែរ។"], .35)
    # 4 uncertainty communication
    f = Fig(1000, 420).title("ការទំនាក់ទំនងភាពមិនប្រាកដ")
    items = [("លេខ ± ចន្លោះ", "ផ្ទៃទឹកជំនន់ ៣២០ ± ៤០ គម²", "#1565c0"), ("ភាពត្រឹមត្រូវ", "OA ៨៥% · PA ស្រែ ៧៨%", "#43a047"), ("សេណារីយ៉ូ", "កម្រិត ១០% ធៀប ៣០%", "#ef6c00"), ("ដែនកំណត់", "«អ្វីដែលយើងមិនអាចសន្និដ្ឋាន»", "#c62828")]
    for i, (a, b, c) in enumerate(items):
        x = 30 + i * 240; box(f, x, 110, 215, 150, a, b, c, 18)
    f.text(500, 320, "ផែនទីដែលមើលទៅ «ប្រាកដ» ពេក អាចនាំឲ្យសម្រេចចិត្តខុស", 17, INK, "middle", "bold")
    entry(15, f.save("a15-uncertainty"), "និយាយពីអ្វីដែលមិនដឹង ដោយស្មោះត្រង់",
          ["គ្រប់មេរៀនក្នុងសៀវភៅនេះ បញ្ចប់ដោយ «អ្វីដែលយើងមិនអាចសន្និដ្ឋាន»៖ គម្រោងរបស់អ្នកក៏ត្រូវតែមានដែរ។", "រាយការណ៍ភាពត្រឹមត្រូវតាមថ្នាក់ មិនមែនតែ OA ទេ ហើយបង្ហាញលទ្ធផលពីកម្រិត ឬទម្ងន់ខុសគ្នា។",
           "ប្រើពាក្យដូចជា «ទំនង» «ប្រហែល» «សញ្ញា» នៅពេលទិន្នន័យមិនអាចបញ្ជាក់ច្បាស់។"], .5)
    # 5 ethics principles
    f = Fig(1000, 460).title("ក្រមសីលធម៌ទិន្នន័យភូមិសាស្ត្រ", "ប្រាំគោលការណ៍")
    items = [("ឯកជនភាព", "ផ្ទះ · មនុស្ស", "#1565c0"), ("គ្មានគ្រោះថ្នាក់", "ទីតាំងរសើប", "#2e7d32"), ("យុត្តិធម៌", "អ្នកដែលខកក្នុងទិន្នន័យ", "#ef6c00"),
             ("តម្លាភាព", "វិធី · ដែនកំណត់", "#6a1b9a"), ("ការគោរព", "អាជ្ញាបណ្ណ · ការយល់ព្រម", "#c62828")]
    for i, (a, b, c) in enumerate(items):
        x = 25 + i * 192; box(f, x, 110, 175, 170, a, b, c, 18)
    f.text(500, 350, "សំណួរមុនចែករំលែក៖ «ផែនទីនេះអាចធ្វើឲ្យនរណាម្នាក់រងគ្រោះបានទេ?»", 17, INK, "middle", "bold")
    entry(15, f.save("a15-ethics"), "ផែនទីមានអំណាច",
          ["ផែនទីនៃការតាំងលំនៅក្រៅផ្លូវការ ឬទីតាំងសត្វព្រៃកម្រ អាចជួយ ឬធ្វើឲ្យមានគ្រោះថ្នាក់ អាស្រ័យលើអ្នកណាប្រើ។", "ទិន្នន័យសកល (WorldPop Open Buildings) អាចខកសហគមន៍ជនបទ ឬជនជាតិដើមភាគតិច៖ ពិនិត្យថាអ្នកណាមិនមាននៅក្នុងទិន្នន័យ។",
           "ពិភាក្សាលទ្ធផលជាមួយអ្នកដែលរងផលប៉ះពាល់ មុនបោះពុម្ពផ្សាយ។"], .65)
    # 6 licences
    f = Fig(1000, 440).title("អាជ្ញាបណ្ណ និងការដកស្រង់ទិន្នន័យ", "សង្ខេប · ពិនិត្យលក្ខខណ្ឌពេញលេញលើទំព័រទិន្នន័យនីមួយៗ")
    rows = [("Landsat (USGS/NASA)", "សាធារណៈ", "ដកស្រង់ USGS"), ("Sentinel (Copernicus)", "ឥតគិតថ្លៃ · បើកចំហ", "«Contains modified Copernicus Sentinel data [ឆ្នាំ]»"), ("Hansen GFC", "CC BY 4.0", "ដកស្រង់ Hansen et al. ២០១៣"),
            ("ESA WorldCover · Dynamic World", "CC BY 4.0", "ដកស្រង់អ្នកផលិត"), ("WDPA", "មិនមែនពាណិជ្ជកម្ម · លក្ខខណ្ឌពិសេស", "ពិនិត្យលក្ខខណ្ឌ UNEP-WCMC"), ("សៀវភៅនេះ", "CC BY-SA 4.0", "យាំ សារដ្ឋ · github.com/khgeo")]
    for i, (a, b, c) in enumerate(rows):
        y = 95 + i * 52; f.rect(30, y, 940, 44, "#f5f5f5" if i % 2 == 0 else "#fff"); f.text(46, y + 28, a, 15, INK, weight="bold"); f.text(380, y + 28, b, 14, IND); f.text(610, y + 28, c, 13, "#607d8b")
    entry(15, f.save("a15-licences"), "ឥតគិតថ្លៃ មិនមានន័យថាគ្មានលក្ខខណ្ឌ",
          ["ទិន្នន័យភាគច្រើនក្នុង Earth Engine ឥតគិតថ្លៃ ប៉ុន្តែមានលក្ខខណ្ឌដកស្រង់ ហើយខ្លះហាមការប្រើពាណិជ្ជកម្ម។", "ដកស្រង់ទិន្នន័យ (និងកំណែ) ក្នុងផែនទី របាយការណ៍ និងកម្មវិធី។",
           "Earth Engine ខ្លួនឯងក៏មានលក្ខខណ្ឌប្រើប្រាស់៖ ការប្រើពាណិជ្ជកម្មត្រូវការអាជ្ញាបណ្ណពាណិជ្ជកម្ម។"], .8)
    # 7 rubric
    f = Fig(1000, 440).title("លក្ខណៈវិនិច្ឆ័យវាយតម្លៃគម្រោង", "សរុប ១០០ ពិន្ទុ")
    crit = [("សំណួរ និងភាពពាក់ព័ន្ធ", 15), ("ទិន្នន័យ និងវិធីសាស្ត្រ", 25), ("ការផ្ទៀងផ្ទាត់ និងភាពមិនប្រាកដ", 20), ("ផែនទី និងក្រាប", 15), ("ភាពអាចធ្វើឡើងវិញ", 10), ("ការបង្ហាញ", 10), ("ក្រមសីលធម៌", 5)]
    bars(f, 60, 90, 880, 300, [a for a, b in crit], [b for a, b in crit], ["#1565c0", "#43a047", "#c62828", "#ef6c00", "#6a1b9a", "#00838f", "#6d4c41"], vmax=30, fmt=lambda v: kh(int(v)) + " ពិន្ទុ", lw=260)
    entry(15, f.save("a15-rubric"), "វិធីសាស្ត្រ និងការផ្ទៀងផ្ទាត់ មានទម្ងន់ច្រើនជាងគេ",
          ["ផែនទីស្អាតតែមួយ មិនគ្រប់គ្រាន់ទេ៖ ពិន្ទុភាគច្រើនមកពីការជ្រើសទិន្នន័យ វិធីសាស្ត្រ និងការផ្ទៀងផ្ទាត់។", "ភាពអាចធ្វើឡើងវិញ៖ គ្រូរត់ស្គ្រីបរបស់អ្នក ហើយត្រូវបានលទ្ធផលដូចគ្នា។",
           "លក្ខណៈវិនិច្ឆ័យពេញលេញមានក្នុងលំហាត់ទី១៥។"], .95)
