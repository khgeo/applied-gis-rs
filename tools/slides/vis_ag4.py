"""Book 4 · Chapter 4 figures (Lessons 10–12).

Real data: Sentinel-2 over Sihanoukville 2015 vs 2021 (docs/assets/data/shv_change.json,
display-stretched bands + real NDVI) and Landsat 8 Phnom Penh 2019 (l8_pp_scene.json).
Hansen-style loss maps, Sentinel-1 rice series and LST fields are SIMULATED and say so.
"""
from vis_core import *
from rs_chart import chart, bars
from vis_ag2 import scene, nd, ramp, pal, box, code, KHF, CLS_COL, CLS_KH, MON, MSTART, DOY
import base64
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC_SHV = "Sentinel-2 · ក្រុងព្រះសីហនុ · ២០១៥ និង ២០២១ · Copernicus"
def shv():
    d = gj("shv_change.json"); w, h = d["w"], d["h"]
    f = lambda k: np.frombuffer(base64.b64decode(d[k]), np.uint8)
    b15 = f("y2015").reshape(6, h, w).astype(float); b21 = f("y2021").reshape(6, h, w).astype(float)
    return b15, b21, f("ndvi2015").reshape(h, w) / 127.5 - 1, f("ndvi2021").reshape(h, w) / 127.5 - 1
def rgb8(b):
    return Image.fromarray(np.dstack([b[2], b[1], b[0]]).astype(np.uint8))

# ---------------- Lesson 10 ----------------
def sim_forest(seed=12):
    """Hansen-like layers on the real Phnom Penh tree class: treecover2000 %, lossyear (0 = none)."""
    B, C = scene(); rng = np.random.default_rng(seed)
    base = np.where(C == 1, 85, np.where(C == 2, 25, 5)).astype(float) + ndi.gaussian_filter(rng.normal(0, 25, C.shape), 2)
    tc = np.clip(base, 0, 100)
    roads = np.zeros(C.shape, bool); roads[:, 110] = True; roads[150, :170] = True; roads[150:, 40] = True
    dist = ndi.distance_transform_edt(~roads)
    p = np.exp(-dist / 18) * (tc > 30); ly = np.zeros(C.shape, int)
    for y in range(1, 24):
        field = ndi.gaussian_filter(rng.random(C.shape), 3)
        new = (field > .5 + .08 * np.exp(-((y - 13) / 5) ** 2) * -1) & (rng.random(C.shape) < p * (.008 + .012 * np.exp(-((y - 12) / 4) ** 2))) & (ly == 0)
        ly[ndi.binary_dilation(new, iterations=1) & (tc > 30) & (ly == 0)] = y
    return tc, ly, C

PA_BOX = (175, 290, 185, 295)   # r0 r1 c0 c1 of a simulated protected area
def L10():
    SIM = "ស្រទាប់ក្លែងធ្វើតាមទម្រង់ Hansen GFC លើគម្របដីពិតនៃភ្នំពេញ (សម្រាប់បង្រៀន)"
    tc, ly, C = sim_forest()
    # 1 Hansen layers
    f = Fig(1000, 450).title("Hansen Global Forest Change៖ ក្រុមរលកសំខាន់", SIM)
    f.img(ramp(tc, ["#f7fcf5", "#74c476", "#00441b"], 0, 100), 30, 90, 280, 280)
    lyc = np.dstack([np.full(C.shape, 240, np.uint8)] * 3); cols = ramp(np.linspace(1, 23, 23)[None, :], ["#ffeda0", "#fd8d3c", "#bd0026"], 1, 23)
    cc = np.array(cols)[0]
    for y in range(1, 24): lyc[ly == y] = cc[y - 1]
    lyc[(ly == 0) & (tc > 30)] = (116, 196, 118)
    f.img(Image.fromarray(lyc), 360, 90, 280, 280, fmt="PNG")
    f.text(170, 395, "treecover2000 (%)", 14, INK, "middle", "bold", extra='font-family="monospace"'); f.text(500, 395, "lossyear (១–២៣ = ២០០១–២០២៣)", 14, INK, "middle", "bold")
    rows = [("treecover2000", "% គម្របដើមឈើ ឆ្នាំ ២០០០"), ("loss", "១ = បាត់បង់ ២០០១–…"), ("lossyear", "ឆ្នាំបាត់បង់ (១ = ២០០១)"), ("gain", "១ = កើនឡើង ២០០០–២០១២"), ("datamask", "១ ដី · ២ ទឹក")]
    for i, (a, b) in enumerate(rows):
        f.text(680, 120 + i * 52, a, 15, IND, weight="bold", extra='font-family="monospace"'); f.text(680, 142 + i * 52, b, 13, INK)
    entry(10, f.save("a10-hansen"), "ផែនទីការបាត់បង់ព្រៃ ៣០ ម ចាប់ពីឆ្នាំ ២០០១",
          ["treecover2000 ជាគម្របដើមឈើ (%) មិនមែន «ព្រៃ» ទេ៖ អ្នកប្រើត្រូវជ្រើសកម្រិត (ឧ. ≥ ៣០%)។", "lossyear ប្រាប់ឆ្នាំដែលដើមឈើត្រូវបាត់ (ជម្រះ ឬស្លាប់) ក្នុងក្រឡា ៣០ ម។",
           "gain គ្របតែ ២០០០–២០១២ ហើយមិនអាចដកពី loss ដើម្បីបាន «ការផ្លាស់ប្ដូរសុទ្ធ» បានទេ។"], .05)
    # 2 tree cover vs forest
    f = Fig(1000, 430).title("គម្របដើមឈើ ≠ ព្រៃ", "អ្វីដែល Hansen រាប់ជា «ដើមឈើ»")
    items = [("ព្រៃធម្មជាតិ", "ព្រៃស្រោង · ព្រៃរបោះស្លឹក", "#1b5e20"), ("ចម្ការកៅស៊ូ", "ដាំជាជួរ · ច្រូតរៀងរាល់ ២៥–៣០ ឆ្នាំ", "#558b2f"), ("ចម្ការស្វាយចន្ទី", "ដើមឈើ > ៥ ម", "#7cb342"), ("ឈើអាកាស្យា · ប្រេងដូង", "ដាំ និងកាប់ជាវដ្ដ", "#9ccc65")]
    for i, (a, b, col) in enumerate(items):
        x = 30 + i * 240; box(f, x, 100, 215, 120, a, b, col, 17)
        for k in range(5): f.circle(x + 40 + k * 35, 280, 14, col); f.rect(x + 37 + k * 35, 294, 6, 20, "#6d4c41")
    f.text(500, 370, "ការកាប់ចម្ការកៅស៊ូចាស់ ក៏រាប់ជា «loss» ដែរ៖ មិនមែនការបាត់បង់ព្រៃធម្មជាតិទេ", 16, "#c62828", "middle", "bold")
    entry(10, f.save("a10-treecover"), "Hansen វាស់ដើមឈើ មិនមែនប្រភេទព្រៃ",
          ["Hansen កំណត់ «ដើមឈើ» ថាជារុក្ខជាតិខ្ពស់ជាង ៥ ម៉ែត្រ ដោយមិនបែងចែកព្រៃធម្មជាតិ និងចម្ការទេ។", "នៅកម្ពុជា ចម្ការកៅស៊ូ ស្វាយចន្ទី និងអាកាស្យា មានច្រើន៖ loss ខ្លះគឺជាការច្រូតចម្ការ។",
           "ដើម្បីនិយាយពី «ព្រៃធម្មជាតិ» ត្រូវរួមជាមួយផែនទីព្រៃថ្នាក់ជាតិ ឬទិន្នន័យចម្ការ។"], .2)
    # 3 threshold effect (computed on simulated layer)
    ths = [10, 20, 30, 40, 50, 60, 70]; area = [(tc >= t).sum() * 900 / 1e6 for t in ths]
    f = Fig(1000, 430).title("កម្រិតគម្របដើមឈើ ប្ដូរផ្ទៃព្រៃ", SIM)
    X, Y = chart(f, 90, 90, 520, 280, [(ths, area, "#2e7d32", "ផ្ទៃ", 3)], (10, 70), (0, max(area) * 1.1), "កម្រិត treecover2000 (%)", "ផ្ទៃ «ព្រៃ» (គម²)", xt=ths, legend=False)
    for a, b in zip(ths, area): f.circle(X(a), Y(b), 5, "#2e7d32")
    code(f, 650, 100, 320, ["var forest2000 = gfc", "  .select('treecover2000')", "  .gte(30);        // ≥ ៣០%", "var lossArea = gfc.select('loss')", "  .updateMask(forest2000);"], 13)
    f.text(650, 280, "FAO៖ ≥ ១០% · ≥ ០,៥ ហិកតា", 14, INK); f.text(650, 308, "GFW លំនាំដើម៖ ≥ ៣០%", 14, INK)
    entry(10, f.save("a10-threshold"), "និយមន័យ ជាការសម្រេចចិត្ត",
          [f"ពីកម្រិត ១០% ទៅ ៥០% ផ្ទៃ «ព្រៃ» ថយពី {KHF(area[0], 1)} ទៅ {KHF(area[4], 1)} គម² លើតំបន់ដដែល។", "ការបាត់បង់ក៏ប្ដូរតាម៖ loss ត្រូវវាស់តែក្នុងក្រឡាដែលជា «ព្រៃ» ឆ្នាំ ២០០០ តាមកម្រិតដែលបានជ្រើស។",
           "រាយការណ៍កម្រិតជានិច្ច ហើយប្រើកម្រិតដូចគ្នាពេលប្រៀបធៀបខេត្ត ឬឆ្នាំ។"], .35)
    # 4 loss by year (computed on simulated layer)
    yrs = list(range(2001, 2024)); lk = [((ly == y - 2000) & (tc >= 30)).sum() * 900 / 1e6 for y in yrs]
    f = Fig(1000, 440).title("ការបាត់បង់ព្រៃតាមឆ្នាំ៖ reducer ជាក្រុម", SIM)
    for i, v in enumerate(lk):
        x = 70 + i * 26; h = v / max(lk) * 250; f.rect(x, 350 - h, 20, h, "#c62828")
        if i % 4 == 0: f.text(x + 10, 372, kh(yrs[i]), 11, "#546e7a", "middle")
    code(f, 680, 90, 300, ["var a = ee.Image.pixelArea()", "  .divide(1e6).addBands(", "   gfc.select('lossyear'))", "  .updateMask(loss30)", "  .reduceRegion({reducer:", "   ee.Reducer.sum().group(", "    {groupField: 1}), ...});"], 13)
    entry(10, f.save("a10-lossyear"), "ពេលវេលានៃការបាត់បង់",
          ["pixelArea + lossyear + group() ផ្ដល់ផ្ទៃបាត់បង់ក្នុងឆ្នាំនីមួយៗ ក្នុងការហៅតែមួយ (មេរៀនទី៤)។", "ក្រាបលំនាំនេះជាស៊េរីក្លែងធ្វើ៖ លំហាត់ទី១០ គណនាតួលេខពិតសម្រាប់ខេត្តរបស់អ្នក។",
           "Hansen ប្ដូរវិធីសាស្ត្របន្តិចតាមកំណែ៖ ការប្រៀបធៀបឆ្នាំដំបូង និងចុងក្រោយ ត្រូវធ្វើដោយប្រុងប្រយ័ត្ន។"], .5)
    # 5 protected area inside / buffer / outside (computed)
    r0, r1, c0, c1 = PA_BOX; pa = np.zeros(C.shape, bool); pa[r0:r1, c0:c1] = True
    buf = ndi.binary_dilation(pa, iterations=30) & ~pa; out_ = ~pa & ~buf
    f30 = tc >= 30; rate = lambda m: ((ly > 0) & f30 & m).sum() / max(1, (f30 & m).sum()) * 100
    rs = [rate(pa), rate(buf), rate(out_)]
    f = Fig(1000, 450).title("ក្នុង ជិត និងក្រៅតំបន់ការពារ", SIM)
    img = np.array(Image.fromarray(lyc)); img[buf & (np.indices(C.shape).sum(0) % 6 == 0)] = (120, 120, 120)
    f.img(Image.fromarray(img), 30, 85, 330, 330, fmt="PNG"); s = 330 / 300
    f.rect(30 + c0 * s, 85 + r0 * s, (c1 - c0) * s, (r1 - r0) * s, "none", "#1565c0", 3); f.text(30 + c0 * s + 6, 85 + r0 * s + 20, "តំបន់ការពារ", 14, "#1565c0", weight="bold", extra='stroke="#fff" stroke-width="3" paint-order="stroke"')
    bars(f, 400, 110, 480, 200, ["ក្នុងតំបន់ការពារ", "តំបន់ទ្រនាប់ ១ គម", "ក្រៅ"], rs, ["#1565c0", "#78909c", "#c62828"], fmt=lambda v: KHF(v, 1) + "%", lw=170)
    f.text(680, 350, "% នៃព្រៃ ២០០០ ដែលបាត់បង់ ២០០១–២០២៣", 14, INK, "middle")
    entry(10, f.save("a10-protected"), "ប្រៀបធៀបអត្រា មិនមែនផ្ទៃ",
          ["ប្រៀបធៀប % នៃព្រៃឆ្នាំ ២០០០ ដែលបាត់បង់ ព្រោះតំបន់មានទំហំខុសគ្នា។", "តំបន់ទ្រនាប់ (buffer) ជុំវិញតំបន់ការពារ បង្ហាញថាសម្ពាធនៅជិតព្រំដែនខ្ពស់ប៉ុណ្ណា។",
           "អត្រាទាបក្នុងតំបន់ការពារ មិនមែនភស្តុតាងថាវាមានប្រសិទ្ធភាពទេ៖ តំបន់ទាំងនោះច្រើនតែឆ្ងាយពីផ្លូវ និងភ្នំ (ការលំអៀងទីតាំង)។"], .65)
    # 6 real NDVI loss, Sihanoukville
    b15, b21, n15, n21 = shv(); lost = (n15 > .5) & (n21 < .3); gained = (n15 < .3) & (n21 > .5)
    f = Fig(1000, 440).title("ការបាត់បង់រុក្ខជាតិ ពីរូបភាពពិតពីរឆ្នាំ", SRC_SHV)
    f.img(rgb8(b15), 20, 85, 230, 220); f.img(rgb8(b21), 265, 85, 230, 220)
    m = np.dstack([np.clip(b21[2] * .6 + 60, 0, 255)] * 3).astype(np.uint8); m[lost] = (211, 47, 47); m[gained] = (46, 125, 50)
    f.img(Image.fromarray(m), 510, 85, 230, 220, fmt="PNG")
    f.text(135, 330, "២០១៥", 15, INK, "middle", "bold"); f.text(380, 330, "២០២១", 15, INK, "middle", "bold"); f.text(625, 330, "NDVI > ០,៥ → < ០,៣ (ក្រហម)", 13, INK, "middle", "bold")
    f.text(760, 120, f"បាត់រុក្ខជាតិ៖ {KHF(lost.sum() * 900 / 1e6, 2)} គម²", 16, "#c62828", weight="bold"); f.text(760, 150, f"កើនរុក្ខជាតិ៖ {KHF(gained.sum() * 900 / 1e6, 2)} គម²", 16, "#2e7d32", weight="bold")
    f.text(760, 180, f"តំបន់សរុប៖ {KHF(n15.size * 900 / 1e6, 1)} គម²", 14, INK)
    f.text(760, 230, "ក្រឡា ៣០ ម (resample)", 13, "#607d8b")
    entry(10, f.save("a10-ndvi-loss"), "វិធីផ្ទាល់ខ្លួន៖ ប្រៀបធៀប NDVI",
          ["នៅពេលត្រូវការឆ្នាំថ្មីជាង Hansen ឬតំបន់តូច ប្រៀបធៀប NDVI ពី composite ពីរឆ្នាំ ក្នុងរដូវដូចគ្នា។", "ក្រហម = រុក្ខជាតិក្រាស់ក្នុងឆ្នាំ ២០១៥ ក្លាយជាដីទទេ ឬសំណង់នៅឆ្នាំ ២០២១ (ការពង្រីកទីក្រុង)។",
           "តួលេខគណនាពីរូបភាព Sentinel-2 ពិត។ កម្រិត ០,៥ និង ០,៣ ជាការជ្រើសរើស ហើយត្រូវរាយការណ៍។"], .8)
    # 7 workflow
    f = Fig(1000, 380).title("លំហូរការវិភាគការបាត់បង់ព្រៃ")
    steps = [("ព្រៃ ២០០០", "treecover2000 ≥ កម្រិត", "#2e7d32"), ("បាត់បង់", "loss · lossyear", "#c62828"), ("តំបន់", "ខេត្ត · WDPA · buffer", "#1565c0"), ("ស្ថិតិ", "ផ្ទៃ · អត្រា · តាមឆ្នាំ", "#6a1b9a"), ("ផ្ទៀងផ្ទាត់", "Sentinel-2 · Google Earth", "#ef6c00")]
    for i, (a, b, c) in enumerate(steps):
        x = 25 + i * 195; box(f, x, 120, 175, 120, a, b, c, 17)
        if i < 4: f.line(x + 177, 180, x + 193, 180, "#607d8b", 2, arrow=True)
    f.text(500, 300, "រាយការណ៍៖ កំណែ Hansen · កម្រិតគម្របដើមឈើ · ឯកតាផ្ទៃ (pixelArea) · ដែនកំណត់", 15, "#607d8b", "middle")
    entry(10, f.save("a10-workflow"), "ប្រាំជំហាន",
          ["កំណត់ព្រៃឆ្នាំ ២០០០ ដោយកម្រិតដែលបានជ្រើស មុនគណនាការបាត់បង់ណាមួយ។", "គណនាផ្ទៃ និងអត្រាតាមតំបន់ និងតាមឆ្នាំ ដោយ pixelArea និង group()។",
           "ពិនិត្យគំរូក្រឡាបាត់បង់ជាមួយរូបភាពគុណភាពខ្ពស់ ដើម្បីដឹងថាវាជាព្រៃធម្មជាតិ ឬចម្ការ។"], .95)

# ---------------- Lesson 11 ----------------
def vh_curve(kind, t):
    if kind == "wet": return -16.5 - 7 * np.exp(-((t - 205) / 14) ** 2) + 3.5 * np.exp(-((t - 265) / 30) ** 2) / (1 + np.exp(-(t - 200) / 4)) - 1.5 / (1 + np.exp(-(t - 320) / 5))
    if kind == "dry": return -16.5 - 7 * np.exp(-((t - 345) / 14) ** 2) - 7 * np.exp(-((t + 20) / 14) ** 2) + 3.5 * np.exp(-((t - 45) / 30) ** 2)
    if kind == "forest": return -13 + .4 * np.sin(t / 50)
    if kind == "urban": return -9 + .3 * np.sin(t / 40)
    if kind == "water": return -25 + .8 * np.sin(t / 30)
    if kind == "crop": return -17 + 2 * np.exp(-((t - 250) / 45) ** 2)
def L11():
    SIM = "ស៊េរីក្លែងធ្វើតាមលំនាំ Sentinel-1 VH លើស្រែកម្ពុជា (សម្រាប់បង្រៀន)"
    # 1 rice calendar
    f = Fig(1000, 400).title("ប្រតិទិនស្រូវនៅកម្ពុជា", "ប្រហាក់ប្រហែល · ខុសគ្នាតាមខេត្ត និងពូជ")
    rows = [("ស្រូវវស្សា", [(5, 11.8)], "#2e7d32"), ("ស្រូវប្រាំង", [(11, 12), (0, 3.5)], "#f9a825"), ("ស្រូវវស្សាដំបូង", [(4, 8)], "#8bc34a"), ("ស្រូវទឹកស្រក", [(0, 4)], "#1565c0")]
    for i, m in enumerate(MON): f.text(220 + i * 62 + 31, 100, m, 13, "#546e7a", "middle")
    for r, (a, spans, col) in enumerate(rows):
        y = 120 + r * 60; f.text(200, y + 28, a, 16, INK, "end", "bold"); f.rect(220, y, 744, 44, "#fafafa", "#eceff1")
        for s, e in spans: f.rect(220 + s * 62, y + 6, (e - s) * 62, 32, col, rx=8)
    f.rect(220 + 4.5 * 62, 360, 5.5 * 62, 10, "#90caf9"); f.text(220 + 7.2 * 62, 392, "រដូវវស្សា (ពពកច្រើន)", 13, "#1565c0", "middle")
    entry(11, f.save("a11-calendar"), "ស្រូវច្រើនប្រភេទ ច្រើនរដូវ",
          ["ស្រូវវស្សា គ្របដណ្ដប់ផ្ទៃធំជាងគេ ហើយដាំក្នុងពេលពពកច្រើនបំផុត។", "ស្រូវប្រាំង និងស្រូវទឹកស្រក នៅតំបន់ធារាសាស្ត្រ និងជុំវិញបឹង៖ អុបទិកមើលឃើញបានល្អជាង។",
           "ប្រតិទិននេះប្រហាក់ប្រហែល៖ ត្រូវកែតាមខេត្ត ដើម្បីជ្រើសរយៈពេលស្ទូងដែលត្រឹមត្រូវ។"], .05)
    # 2 VH signatures
    t = np.arange(1, 366); kinds = [("wet", "ស្រែវស្សា", "#2e7d32"), ("crop", "ដំណាំដទៃ", "#ff9800"), ("forest", "ព្រៃ", "#1b5e20"), ("urban", "ទីក្រុង", "#e53935"), ("water", "ទឹកអចិន្ត្រៃយ៍", "#1e88e5")]
    f = Fig(1000, 450).title("ហត្ថលេខា VH របស់ស្រូវ", SIM)
    X, Y = chart(f, 80, 90, 640, 290, [(list(t), list(vh_curve(k, t)), c, l, 3) for k, l, c in kinds], (1, 365), (-28, -6), "", "VH (dB)", yt=[-25, -20, -15, -10], lx=750, ly=120)
    month_x = [X(d + 14) for d in MSTART]
    for x, m in zip(month_x, MON): f.text(x, 404, m, 12, "#546e7a", "middle")
    f.line(X(205), Y(-24.5), X(205), Y(-26.5), "#2e7d32", 0); f.circle(X(205), Y(float(vh_curve("wet", np.array([205.]))[0])), 7, "none", "#2e7d32", 2.5)
    f.text(X(205) + 10, Y(-24.2), "ស្ទូង (ទឹក)", 13, "#2e7d32", weight="bold"); f.text(X(265), Y(-12.2), "ស្រូវលូតលាស់", 13, "#2e7d32", "middle", weight="bold")
    entry(11, f.save("a11-vh"), "ទាបពេលស្ទូង ខ្ពស់ពេលស្រូវធំ",
          ["ពេលស្ទូង វាលស្រែមានទឹក៖ VH ធ្លាក់ទាបដូចទឹក (−២២ ដល់ −២៥ dB)។", "ពេលស្រូវលូតលាស់ ដើមស្រូវបង្កើនការចាំងត្រឡប់៖ VH ឡើង ៥–៩ dB។",
           "ទឹកអចិន្ត្រៃយ៍ទាបជានិច្ច ព្រៃ និងទីក្រុងខ្ពស់ជានិច្ច៖ មិនមានទម្រង់ «ចុះ រួចឡើង» ទេ។"], .15)
    # 3 rule scatter (simulated pixels)
    rng = np.random.default_rng(5); pts = []
    for k, l, c in kinds:
        for _ in range(60):
            cv0 = vh_curve(k, t); s = cv0.mean() + (cv0 - cv0.mean()) * rng.uniform(.45, 1.4) + rng.normal(0, 1.5, t.size) + rng.normal(0, 1.8); s = np.convolve(s, np.ones(12) / 12, 'same'); win = s[150:260]; pts.append((win.min(), s[180:330].max() - win.min(), c, k))
    f = Fig(1000, 470).title("ក្បួនសាមញ្ញ៖ អប្បបរមា និងការឡើងវិញ", "ក្រឡាក្លែងធ្វើ ៣០០ · មធ្យមរំកិល ១២ ថ្ងៃ · VH អប្បបរមា (មិថុនា–កញ្ញា) និងការកើនឡើងបន្ទាប់ · " + SIM)
    X, Y = chart(f, 90, 90, 560, 320, [], (-30, -8), (0, 14), "VH អប្បបរមា (dB)", "ការកើនឡើងបន្ទាប់ (dB)", xt=[-30, -25, -20, -15, -10], yt=[0, 4, 8, 12], legend=False)
    f.rect(X(-30), Y(14), X(-19) - X(-30), Y(5) - Y(14), "#2e7d32", "none", 0, extra='opacity=".08"')
    f.line(X(-19), Y(0), X(-19), Y(14), "#2e7d32", 2, "6 4"); f.line(X(-30), Y(5), X(-8), Y(5), "#2e7d32", 2, "6 4")
    for a, b, c, k in pts: f.circle(X(min(-8.3, max(-30, a))), Y(min(14, max(0, b))), 3.5, c, op=.8)
    ok = sum(1 for a, b, c, k in pts if (a < -19 and b > 5) == (k == "wet")) / len(pts)
    for i, (k, l, c) in enumerate(kinds): f.circle(690, 120 + i * 28, 6, c); f.text(704, 125 + i * 28, l, 14)
    f.text(690, 290, "ស្រែ = min < −១៩ dB", 14, "#2e7d32", weight="bold"); f.text(690, 314, "និង ការកើនឡើង > ៥ dB", 14, "#2e7d32", weight="bold")
    f.text(690, 360, f"ត្រឹមត្រូវ {kh(round(ok * 100))}% (ក្លែងធ្វើ)", 15, INK, weight="bold")
    entry(11, f.save("a11-rules"), "លក្ខខណ្ឌពីរ បែងចែកស្រែបាន",
          ["ទឹកអចិន្ត្រៃយ៍មាន min ទាប ប៉ុន្តែមិនឡើងវិញ៖ លក្ខខណ្ឌទីពីរកាត់វាចេញ។", "ដំណាំដទៃ និងព្រៃមិនធ្លាក់ដល់ −១៩ dB៖ លក្ខខណ្ឌទីមួយកាត់វាចេញ។",
           "កម្រិតក្នុងរូបនេះជាឧទាហរណ៍៖ ត្រូវកែតាមតំបន់ ដោយប្រើចំណុចស្រែដែលដឹង។"], .3)
    # 4 monthly S1 RGB concept
    f = Fig(1000, 420).title("Composite ប្រចាំខែ ជាក្រុមរលកពណ៌", "VH កក្កដា · សីហា · តុលា ជា RGB")
    for i, (m, lab) in enumerate([("កក្កដា", "R"), ("សីហា", "G"), ("តុលា", "B")]):
        box(f, 40 + i * 160, 120, 140, 90, m, "VH median → " + lab, ["#e53935", "#43a047", "#1e88e5"][i], 16)
    f.line(520, 165, 570, 165, "#607d8b", 2.5, arrow=True)
    for i, (lab, col, why) in enumerate([("ស្រែ (ស្ទូងកក្កដា)", "#1e88e5", "ទាបកក្កដា ខ្ពស់តុលា → ខៀវ"), ("ទឹកអចិន្ត្រៃយ៍", "#000000", "ទាបគ្រប់ខែ → ខ្មៅ"), ("ព្រៃ/ទីក្រុង", "#bdbdbd", "ខ្ពស់គ្រប់ខែ → ស/ប្រផេះ")]):
        f.rect(590, 100 + i * 80, 50, 50, col, "#90a4ae"); f.text(655, 120 + i * 80, lab, 15, INK, weight="bold"); f.text(655, 142 + i * 80, why, 13, "#607d8b")
    entry(11, f.save("a11-rgb"), "មើលស្រែក្នុងរូបភាពតែមួយ",
          ["ដាក់ VH បីខែជា RGB៖ ពណ៌ប្រាប់ពីការប្ដូរតាមពេលវេលា មិនមែនពណ៌ពិតទេ។", "ស្រែដែលស្ទូងយឺត ឬលឿន បង្ហាញពណ៌ខុសគ្នា (ក្រហម បៃតង ខៀវ)។",
           "Composite ប្រចាំខែ ក៏អាចជាលក្ខណៈសម្រាប់ Random Forest (មេរៀនទី៦)។"], .45)
    # 5 optical flooding signal (LSWI vs EVI)
    lswi = -.05 + .45 * np.exp(-((t - 215) / 22) ** 2) + .2 * np.exp(-((t - 270) / 45) ** 2) * (t > 200); evi = .15 + .45 * np.exp(-((t - 280) / 38) ** 2) * (t > 190)
    f = Fig(1000, 440).title("វិធីអុបទិក៖ LSWI + ០,០៥ ≥ EVI", "ស៊េរីក្លែងធ្វើ · Xiao et al. (២០០៥)")
    X, Y = chart(f, 80, 90, 820, 280, [(list(t), list(evi), "#2e7d32", "EVI", 3), (list(t), list(lswi + .05), "#1565c0", "LSWI + ០,០៥", 3)], (1, 365), (-.1, .8), "", "", yt=[0, .2, .4, .6, .8], lx=700, ly=112)
    fl = (lswi + .05 >= evi) & (t > 190) & (t < 240)
    if fl.any(): f.rect(X(t[fl].min()), 90, X(t[fl].max()) - X(t[fl].min()), 280, "#1565c0", extra='opacity=".1"'); f.text((X(t[fl].min()) + X(t[fl].max())) / 2, 108, "សញ្ញាលិចទឹក", 13, "#1565c0", "middle", "bold")
    for x, m in zip([X(d + 14) for d in MSTART], MON): f.text(x, 394, m, 12, "#546e7a", "middle")
    entry(11, f.save("a11-optical"), "ទឹកមុន បៃតងក្រោយ (អុបទិក)",
          ["ក្នុងរយៈពេលស្ទូង LSWI ឡើងជិត ឬលើស EVI៖ ផ្ទៃមានទឹក និងរុក្ខជាតិតិច។", "បន្ទាប់ពីសញ្ញាលិចទឹក EVI ត្រូវឡើងខ្ពស់ក្នុងរយៈពេល ២–៣ ខែ ដើម្បីបញ្ជាក់ថាជាស្រូវ។",
           "វិធីនេះល្អសម្រាប់ស្រូវប្រាំង ប៉ុន្តែក្នុងរដូវវស្សា ពពកធ្វើឲ្យខកសញ្ញាលិចទឹកញឹកញាប់។"], .6)
    # 6 validation vs statistics (illustrative)
    f = Fig(1000, 440).title("ផ្ទៀងផ្ទាត់ពីរកម្រិត", "ភាពត្រឹមត្រូវតាមចំណុច និងផ្ទៃធៀបនឹងស្ថិតិ · តម្លៃគំរូ")
    f.rect(40, 90, 440, 300, "#fafafa", "#cfd8dc", 1, 10); f.text(260, 125, "១. ចំណុចផ្ទៀងផ្ទាត់", 17, IND, "middle", "bold")
    for i, (a, b) in enumerate([("ចំណុចស្រែ / មិនមែនស្រែ", "ពីការស្ទង់វាល ឬ Google Earth"), ("តារាងកំហុស ២ × ២", "PA · UA · OA (មេរៀនទី៦)"), ("បំបែកតាមខេត្ត", "ភាពត្រឹមត្រូវខុសគ្នាតាមតំបន់")]):
        f.text(70, 170 + i * 70, a, 15, INK, weight="bold"); f.text(70, 194 + i * 70, b, 13, "#607d8b")
    f.rect(520, 90, 440, 300, "#fafafa", "#cfd8dc", 1, 10); f.text(740, 125, "២. ផ្ទៃធៀបនឹងស្ថិតិ", 17, IND, "middle", "bold")
    rng = np.random.default_rng(2); st = rng.uniform(20, 300, 12); mp = st * rng.normal(1.05, .12, 12)
    for a, b in zip(st, mp): f.circle(560 + a * 1.2, 360 - b * .75, 5, "#2e7d32")
    f.line(560, 360, 560 + 330 * 1.2, 360 - 330 * .75, "#90a4ae", 1.5, "5 4"); f.text(570, 380, "ស្ថិតិក្រសួង (ពាន់ ហិកតា)", 12, "#607d8b"); f.text(560, 160, "ផែនទី", 12, "#607d8b")
    entry(11, f.save("a11-validation"), "ផែនទីត្រឹមត្រូវតាមចំណុច មិនធានាផ្ទៃត្រឹមត្រូវទេ",
          ["ភាពត្រឹមត្រូវតាមចំណុច វាស់ថាផែនទីដាក់ស្លាកត្រឹមត្រូវប៉ុណ្ណា នៅកន្លែងដែលមានចំណុច។", "ការប្រៀបធៀបផ្ទៃតាមខេត្តជាមួយស្ថិតិក្រសួងកសិកម្ម បង្ហាញលំអៀងជាប្រព័ន្ធ (ច្រើន ឬតិចពេក)។",
           "ស្ថិតិក៏មានកំហុសដែរ៖ ភាពខុសគ្នាធំ ត្រូវពិនិត្យទាំងពីរផ្នែក។ ចំណុចក្នុងក្រាបជាតម្លៃគំរូ។"], .75)
    # 7 workflow
    f = Fig(1000, 380).title("លំហូរការធ្វើផែនទីស្រែដោយ Sentinel-1")
    steps = [("S1 VH", "IW · គន្លងតែមួយ", "#1565c0"), ("Composite ១២ ថ្ងៃ", "ស៊េរីរដូវ", "#1e88e5"), ("លក្ខណៈ", "min · ការឡើង · ពេល", "#43a047"), ("ក្បួន ឬ RF", "កម្រិត · ចំណុចគំរូ", "#2e7d32"), ("Mask", "ទឹក JRC · ជម្រាល · ទីក្រុង", "#6d4c41"), ("ផ្ទៀងផ្ទាត់", "ចំណុច · ស្ថិតិ", "#ef6c00")]
    for i, (a, b, c) in enumerate(steps):
        x = 20 + i * 163; box(f, x, 120, 148, 120, a, b, c, 15)
        if i < 5: f.line(x + 150, 180, x + 161, 180, "#607d8b", 2, arrow=True)
    entry(11, f.save("a11-workflow"), "ពីស៊េរី VH ទៅផែនទីស្រែ",
          ["ស៊េរីត្រូវមកពីគន្លងតែមួយ ដើម្បីកុំឲ្យការប្ដូរមុំមើលធ្វើឲ្យ VH ឡើងចុះ។", "លក្ខណៈពីស៊េរី (min ការឡើង ពេលវេលា) សំខាន់ជាងរូបភាពណាមួយ។",
           "Mask ដកទឹកអចិន្ត្រៃយ៍ តំបន់ភ្នំ និងទីក្រុង មុនគណនាផ្ទៃ។"], .9)

# ---------------- Lesson 12 ----------------
def L12():
    b15, b21, n15, n21 = shv()
    ndbi = lambda b: (b[4] - b[3]) / (b[4] + b[3] + 1e-9)
    # 1 real true colour 2015 vs 2021
    f = Fig(1000, 440).title("ក្រុងព្រះសីហនុ ២០១៥ និង ២០២១", SRC_SHV)
    f.img(rgb8(b15), 30, 85, 300, 287); f.img(rgb8(b21), 350, 85, 300, 287)
    f.text(180, 400, "២០១៥", 16, INK, "middle", "bold"); f.text(500, 400, "២០២១", 16, INK, "middle", "bold")
    for i, (a, b) in enumerate([("ក្រឡា", f"{kh(b15.shape[2])} × {kh(b15.shape[1])} · ៣០ ម"), ("ផ្ទៃ", f"{KHF(n15.size * 900 / 1e6, 1)} គម²"), ("ក្រុមរលក", "B2 B3 B4 B8 B11 B12")]):
        f.text(680, 120 + i * 60, a, 14, "#607d8b"); f.text(680, 145 + i * 60, b, 16, INK, weight="bold")
    f.text(680, 330, "ពណ៌ពិត (ពង្រីកពន្លឺសម្រាប់មើល)", 13, "#607d8b")
    entry(12, f.save("a12-shv"), "ការពង្រីកទីក្រុងរហ័ស",
          ["ក្រុងព្រះសីហនុបានសាងសង់ច្រើនក្នុងរយៈពេល ២០១៦–២០២០។ រូបភាពពីរឆ្នាំបង្ហាញដីទទេ និងអគារថ្មី។", "ទីក្រុងជាគម្របដីដែលប្ដូរលឿនបំផុត ហើយការប្ដូរនេះកម្របញ្ច្រាសវិញ។",
           "រូបភាពពិត Sentinel-2 ដែលបានពង្រីកពន្លឺតាមក្រុមរលក សម្រាប់ការបង្ហាញ។"], .05)
    # 2 NDBI/NDVI change (real)
    d_ndvi = n21 - n15; nb15, nb21 = ndbi(b15), ndbi(b21)
    new_built = (d_ndvi < -.2) & (n21 < .3) & (nb21 > nb15 + .05)
    f = Fig(1000, 440).title("រកទីក្រុងថ្មី៖ NDVI ធ្លាក់ + NDBI ឡើង", SRC_SHV + " · NDBI ប្រហាក់ប្រហែល")
    f.img(ramp(d_ndvi, ["#b2182b", "#f7f7f7", "#1a9850"], -.6, .6), 30, 85, 300, 287)
    img = np.dstack([np.clip(b21[2] * .55 + 70, 0, 255)] * 3).astype(np.uint8); img[new_built] = (211, 47, 47)
    f.img(Image.fromarray(img), 350, 85, 300, 287, fmt="PNG")
    f.text(180, 400, "ΔNDVI ២០២១ − ២០១៥", 15, INK, "middle", "bold"); f.text(500, 400, "សំណង់/ដីទទេថ្មី (ក្រហម)", 15, INK, "middle", "bold")
    f.text(680, 120, f"ផ្ទៃ៖ {KHF(new_built.sum() * 900 / 1e6, 2)} គម²", 18, "#c62828", weight="bold"); f.text(680, 150, f"({KHF(new_built.mean() * 100, 1)}% នៃតំបន់)", 14, INK)
    code(f, 680, 190, 300, ["dNDVI < -0.2", "NDVI_2021 < 0.3", "dNDBI > 0.05"], 14)
    entry(12, f.save("a12-change"), "លក្ខខណ្ឌបី ដើម្បីកាត់កំហុស",
          ["NDVI ធ្លាក់តែមួយ អាចជាដំណាំច្រូត ឬរដូវខុសគ្នា៖ ត្រូវការ NDVI ទាបក្នុងឆ្នាំថ្មី និង NDBI ឡើង។", "NDBI នៅកម្ពុជាច្រឡំរវាងដីទទេ និងអគារ៖ ផ្ទៃនេះរួមទាំងដីចាក់បំពេញដែលមិនទាន់សាងសង់។",
           "តួលេខគណនាពីរូបភាពពិត ប៉ុន្តែកម្រិតជាការជ្រើសរើស៖ ត្រូវផ្ទៀងផ្ទាត់ដោយចំណុច (មេរៀនទី៦)។"], .2)
    # 3 global built-up datasets
    f = Fig(1000, 460).title("ទិន្នន័យទីក្រុងសកលក្នុង Earth Engine", "ជ្រើសតាមសំណួរ និងឆ្នាំ")
    rows = [("GHSL GHS-BUILT-S", "JRC/GHSL/P2023A/GHS_BUILT_S", "១០០ ម · ១៩៧៥–២០៣០ (៥ ឆ្នាំ)"), ("Dynamic World · built", "GOOGLE/DYNAMICWORLD/V1", "១០ ម · ប្រចាំរូបភាព ២០១៥–"),
            ("ESA WorldCover", "ESA/WorldCover/v200", "១០ ម · ២០២០ ២០២១"), ("World Settlement Footprint", "DLR/WSF/WSF2015/v1", "១០ ម · ២០១៥"),
            ("Open Buildings", "GOOGLE/Research/open-buildings/v3/polygons", "ពហុកោណអគារ"), ("VIIRS ពន្លឺពេលយប់", "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG", "~៥០០ ម · ប្រចាំខែ ២០១២–")]
    for i, (a, b, c) in enumerate(rows):
        y = 95 + i * 56; f.rect(30, y, 940, 48, "#f3e5f5" if i % 2 == 0 else "#fff"); f.text(44, y + 30, a, 15, INK, weight="bold"); f.text(330, y + 30, b, 12, INK, extra='font-family="monospace"'); f.text(730, y + 30, c, 13)
    entry(12, f.save("a12-datasets"), "កុំចាប់ផ្ដើមពីសូន្យ",
          ["GHSL ផ្ដល់ស៊េរីវែង (១៩៧៥–២០៣០) សម្រាប់និន្នាការ ប៉ុន្តែក្រឡា ១០០ ម និងឆ្នាំក្រោយ ២០២០ ជាការព្យាករ។", "Dynamic World និង WorldCover មានក្រឡា ១០ ម សម្រាប់ព័ត៌មានលម្អិតថ្មីៗ។",
           "ពន្លឺពេលយប់ វាស់សកម្មភាព និងអគ្គិសនី មិនមែនអគារទេ៖ ប្រើជាមួយ ដើម្បីបំពេញគ្នា។"], .35)
    # 4 Landsat LST pipeline
    f = Fig(1000, 400).title("សីតុណ្ហភាពផ្ទៃដីពី Landsat Collection 2", "LANDSAT/LC08/C02/T1_L2 · ក្រុមរលក ST_B10")
    steps = [("ST_B10", "DN (uint16)", "#6d4c41"), ("× ០,០០៣៤១៨០២", "+ ១៤៩,០", "#8d6e63"), ("កែលវិន (K)", "រួមបញ្ចូល emissivity រួច", "#ef6c00"), ("− ២៧៣,១៥", "", "#e65100"), ("°C", "LST", "#c62828")]
    for i, (a, b, c) in enumerate(steps):
        x = 25 + i * 195; box(f, x, 110, 175, 110, a, b, c, 16)
        if i < 4: f.line(x + 177, 165, x + 193, 165, "#607d8b", 2, arrow=True)
    f.text(500, 280, "var lst = img.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15);", 14, INK, "middle", extra='font-family="monospace"')
    f.text(500, 320, "ថតប្រហែលម៉ោង ១០:៣០ ព្រឹក · mask ពពកដោយ QA_PIXEL · ក្រឡាដើម ១០០ ម (resample ៣០ ម)", 14, "#607d8b", "middle")
    entry(12, f.save("a12-lst"), "LST រួចជាស្រេចក្នុង Collection 2",
          ["Landsat Collection 2 Level-2 មាន ST_B10 ដែលបានកែបរិយាកាស និង emissivity រួច៖ យើងគ្រាន់តែបម្លែងឯកតា។", "ត្រូវ mask ពពកជានិច្ច៖ ពពកត្រជាក់ខ្លាំង ហើយធ្វើឲ្យ LST ទាបខុសប្រក្រតី។",
           "LST ជាសីតុណ្ហភាពផ្ទៃ (ដំបូល ផ្លូវ ស្លឹក) មិនមែនសីតុណ្ហភាពខ្យល់ដែលមនុស្សមានអារម្មណ៍ទេ។"], .5)
    # 5 LST vs NDVI (simulated from real land cover)
    B, C = scene(); ndv = nd(B[3], B[2]); rng = np.random.default_rng(4)
    base = np.choose(C, [29.0, 33.0, 36.0, 42.0, 40.0]); lst = base - 6 * np.clip(ndv, 0, 1) + ndi.gaussian_filter(rng.normal(0, 3, C.shape), 2)
    f = Fig(1000, 450).title("LST និង NDVI", "LST ក្លែងធ្វើពីគម្របដីពិត និង NDVI ពិត នៃ Landsat 8 ភ្នំពេញ (សម្រាប់បង្រៀន)")
    f.img(ramp(lst, ["#313695", "#74add1", "#ffffbf", "#f46d43", "#a50026"], 26, 46), 30, 85, 300, 300)
    idx = rng.choice(C.size, 900, replace=False)
    X, Y = chart(f, 400, 90, 520, 290, [], (-.3, .7), (24, 48), "NDVI", "LST (°C)", xt=[-.2, 0, .2, .4, .6], yt=[25, 30, 35, 40, 45], legend=False)
    for i in idx: f.circle(X(min(.7, max(-.3, float(ndv.ravel()[i])))), Y(min(48, max(24, float(lst.ravel()[i])))), 2.5, CLS_COL[C.ravel()[i]], op=.7)
    ok = C.ravel()[idx] != 0; b1, b0 = np.polyfit(ndv.ravel()[idx][ok], lst.ravel()[idx][ok], 1)
    f.line(X(-.1), Y(b0 + b1 * -.1), X(.65), Y(b0 + b1 * .65), INK, 2, "6 4")
    f.text(180, 410, "LST (°C)", 14, INK, "middle", "bold"); f.text(930, 110, f"ជម្រាល {KHF(b1, 1)} °C / ១ NDVI (ដី)", 13, INK, "end")
    entry(12, f.save("a12-lst-ndvi"), "រុក្ខជាតិធ្វើឲ្យត្រជាក់",
          ["តំបន់សាងសង់ (ក្រហម) និងដីទទេក្ដៅបំផុត ទឹក (ខៀវ) ត្រជាក់បំផុត។", "ក្នុងចំណោមដី LST ថយនៅពេល NDVI កើន៖ ការបញ្ចេញចំហាយពីស្លឹកធ្វើឲ្យផ្ទៃត្រជាក់។",
           "LST ក្នុងរូបនេះត្រូវបានក្លែងធ្វើពីគម្របដីពិត ដើម្បីបង្ហាញទំនាក់ទំនង៖ លំហាត់ទី១២ ប្រើ ST_B10 ពិត។"], .65)
    # 6 UHI transect (simulated)
    xs = np.linspace(-20, 20, 200); lstT = 33 + 8 * np.exp(-(xs / 7) ** 2) - 5 * np.exp(-((xs - 4) / 1.8) ** 2) + np.random.default_rng(1).normal(0, .4, xs.size)
    f = Fig(1000, 420).title("កោះកំដៅទីក្រុង (UHI)", "ផ្នែកកាត់ LST ក្លែងធ្វើ ពីជនបទ ឆ្លងកាត់ទីក្រុង · ទន្លេនៅ +៤ គម")
    X, Y = chart(f, 80, 90, 820, 260, [(list(xs), list(lstT), "#c62828", "LST", 2.5)], (-20, 20), (28, 44), "ចម្ងាយពីកណ្ដាលទីក្រុង (គម)", "LST (°C)", xt=[-20, -10, 0, 10, 20], yt=[30, 35, 40], legend=False)
    f.rect(X(-7), 90, X(7) - X(-7), 260, "#e53935", extra='opacity=".07"'); f.text(X(0), 110, "ទីក្រុង", 14, "#c62828", "middle", "bold"); f.text(X(4), Y(31), "ទន្លេ", 13, "#1565c0", "middle", "bold")
    f.line(X(-18), Y(33), X(18), Y(33), "#1565c0", 1.5, "6 4"); f.text(X(-18), Y(33) - 6, "ជនបទ", 13, "#1565c0")
    f.line(X(-1), Y(33), X(-1), Y(41), "#6a1b9a", 2.5, arrow=True); f.text(X(-1) - 8, Y(37), "UHI ≈ ៨ °C", 14, "#6a1b9a", "end", "bold")
    entry(12, f.save("a12-uhi"), "ទីក្រុងក្ដៅជាងជនបទជុំវិញ",
          ["UHI = LST មធ្យមក្នុងទីក្រុង − LST មធ្យមក្នុងជនបទជុំវិញ។", "ទន្លេ បឹង និងឧទ្យាន បង្កើត «កោះត្រជាក់» ក្នុងទីក្រុង។",
           "តម្លៃ UHI អាស្រ័យលើរបៀបកំណត់ «ជនបទ»៖ ស្រែស្ងួតក្នុងរដូវប្រាំងក៏ក្ដៅដែរ។ ផ្នែកកាត់នេះជាការក្លែងធ្វើ។"], .8)
    # 7 heat exposure workflow
    f = Fig(1000, 380).title("ពី LST ទៅការប៉ះពាល់កំដៅ")
    steps = [("Landsat C2 L2", "រដូវក្ដៅ · mask ពពក", "#6d4c41"), ("LST median", "°C", "#ef6c00"), ("ទីក្រុង", "GHSL · WorldCover", "#e53935"), ("UHI", "ទីក្រុង − ជនបទ", "#c62828"), ("ប្រជាជន · សាលា", "WorldPop · OSM", "#6a1b9a")]
    for i, (a, b, c) in enumerate(steps):
        x = 25 + i * 195; box(f, x, 120, 175, 120, a, b, c, 16)
        if i < 4: f.line(x + 177, 180, x + 193, 180, "#607d8b", 2, arrow=True)
    f.text(500, 300, "reduceRegions តាមខណ្ឌ ឬសង្កាត់ → ផែនទីអាទិភាពសម្រាប់ដើមឈើ និងម្លប់", 15, "#607d8b", "middle")
    entry(12, f.save("a12-workflow"), "កំដៅ + មនុស្ស = ហានិភ័យ",
          ["LST តែមួយប្រាប់ថាកន្លែងណាក្ដៅ។ ការឆ្លងជាមួយប្រជាជន សាលា ឬមន្ទីរពេទ្យ ប្រាប់ថាកន្លែងណាសំខាន់។", "Composite median រដូវក្ដៅ (មីនា–ឧសភា) ច្រើនឆ្នាំ កាត់បន្ថយឥទ្ធិពលថ្ងៃតែមួយ។",
           "លទ្ធផលជួយកំណត់អាទិភាពសម្រាប់ដាំដើមឈើ ដំបូលពណ៌ស ឬម្លប់។"], .95)
