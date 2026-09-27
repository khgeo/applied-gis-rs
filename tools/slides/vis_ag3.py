"""Book 4 · Chapter 3 figures (Lessons 7–9).

Lesson 7 SAR images are SIMULATED from the real Landsat 8 Phnom Penh land-cover
(water / land classes → typical Sentinel-1 VV backscatter + gamma speckle). Lesson 8
rainfall and NDVI series are illustrative. Lesson 9 uses a synthetic DEM. Every
figure states this on its subtitle; computations on them (Otsu, D8, slope) are real.
"""
from vis_core import *
from rs_chart import chart, bars
from vis_ag2 import scene, nd, ramp, pal, box, code, KHF, CLS_COL, CLS_KH, MON, MSTART
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SIM_SAR = "SAR ក្លែងធ្វើពីគម្របដីពិតនៃភ្នំពេញ (សម្រាប់បង្រៀន)"

def gray(a, lo, hi):
    return Image.fromarray((np.clip((a - lo) / (hi - lo), 0, 1) * 255).astype(np.uint8))

def sar_scene(seed=4):
    """Return (before_dB, after_dB, water_before, flood_truth) 300 × 300."""
    B, C = scene(); rng = np.random.default_rng(seed)
    water = C == 0
    dist = ndi.distance_transform_edt(~water)
    field = ndi.gaussian_filter(rng.normal(size=C.shape), 12); field = (field - field.min()) / (field.max() - field.min())
    flood = (~water) & (dist < 55) & np.isin(C, [2, 4]) & (field > .45)
    flood = ndi.binary_opening(flood, iterations=1)
    mean_db = {0: -21.0, 1: -7.5, 2: -12.0, 3: -5.0, 4: -14.0}
    def img(wmask, flooded):
        m = np.vectorize(mean_db.get)(C).astype(float)
        m[wmask] = -21.0; m[flooded] = -20.0
        lin = 10 ** (m / 10) * rng.gamma(4.4, 1 / 4.4, C.shape)   # ~4.4-look speckle
        return 10 * np.log10(lin)
    return img(water, np.zeros_like(water)), img(water, flood), water, flood

def otsu(v, bins=256):
    h, e = np.histogram(v, bins=bins); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); w2 = w[-1] - w
    m = np.cumsum(h * c); mu1 = m / np.maximum(w, 1); mu2 = (m[-1] - m) / np.maximum(w2, 1)
    return c[np.argmax(w * w2 * (mu1 - mu2) ** 2)]

def L07():
    before, after, water, flood = sar_scene()
    B, C = scene()
    # 1 optical vs SAR in the wet season
    f = Fig(1000, 450).title("ហេតុអ្វីប្រើ SAR ពេលទឹកជំនន់?", "ភាគរយពពកជាមធ្យមលើកម្ពុជា តាមខែ (ប្រហាក់ប្រហែល សម្រាប់បង្រៀន)")
    cl = [25, 20, 25, 40, 70, 85, 90, 90, 88, 75, 45, 30]
    bars(f, 60, 90, 560, 280, MON, cl, ["#90a4ae" if v < 60 else "#546e7a" for v in cl], vmax=100, fmt=lambda v: kh(v) + "%", horizontal=False)
    f.rect(660, 100, 310, 110, "#fff3e0", "#ffb74d", 1.5, 10); f.text(815, 138, "អុបទិក (Sentinel-2)", 16, "#e65100", "middle", "bold"); f.text(815, 170, "មើលមិនឃើញក្រោមពពក", 14, INK, "middle"); f.text(815, 194, "ទឹកជំនន់ = ខែដែលពពកច្រើនបំផុត", 13, "#607d8b", "middle")
    f.rect(660, 240, 310, 110, "#e3f2fd", "#64b5f6", 1.5, 10); f.text(815, 278, "រ៉ាដា (Sentinel-1)", 16, "#1565c0", "middle", "bold"); f.text(815, 310, "ឆ្លងកាត់ពពក ថ្ងៃ និងយប់", 14, INK, "middle"); f.text(815, 334, "រៀងរាល់ ៦–១២ ថ្ងៃ", 13, "#607d8b", "middle")
    entry(7, f.save("a07-clouds"), "ទឹកជំនន់ និងពពក មកជាមួយគ្នា",
          ["ទឹកជំនន់នៅកម្ពុជាកើតឡើងភាគច្រើនក្នុងខែកក្កដា–តុលា ពេលពពកគ្របដណ្ដប់ច្រើនបំផុត។", "SAR បញ្ចេញរលកមីក្រូផ្ទាល់ខ្លួន ហើយរលកនេះឆ្លងកាត់ពពកបាន។",
           "ភាគរយពពកក្នុងក្រាបជាតម្លៃប្រហាក់ប្រហែល សម្រាប់បង្ហាញលំនាំរដូវ។"], .05)
    # 2 backscatter mechanisms
    f = Fig(1000, 450).title("ទឹកងងឹតក្នុងរូបភាព SAR", "យន្តការចាំងត្រឡប់ (ទ្រឹស្ដីពេញមាននៅសៀវភៅទី៣)")
    items = [("ទឹកស្ងប់", "ចាំងឆ្ងាយពីផ្កាយរណប", "≈ −២០ dB · ងងឹត", "#1e88e5"), ("ដី/ស្រែស្ងួត", "ចាំងរាយគ្រប់ទិស", "≈ −១២ dB · ប្រផេះ", "#8d6e63"),
             ("រុក្ខជាតិលិចទឹក", "ចាំងពីរដង (ទឹក + ដើម)", "≈ −៥ dB · ភ្លឺ", "#2e7d32"), ("ទីក្រុង", "ចាំងពីរដង (ផ្លូវ + ជញ្ជាំង)", "> −៥ dB · ភ្លឺខ្លាំង", "#e53935")]
    for i, (a, b, c, col) in enumerate(items):
        x = 30 + i * 240; f.rect(x, 90, 220, 300, "#fafafa", "#cfd8dc", 1, 10); f.text(x + 110, 122, a, 17, col, "middle", "bold")
        f.line(x + 30, 150, x + 100, 250, "#ef6c00", 2.5, arrow=True)
        if i == 0: f.line(x + 100, 250, x + 180, 160, "#ef6c00", 2.5, arrow=True); f.rect(x + 20, 252, 180, 16, "#90caf9")
        elif i == 1:
            f.rect(x + 20, 252, 180, 16, "#bcaaa4")
            for d in (-60, -20, 20, 60): f.line(x + 100, 250, x + 100 + d, 190, "#ef6c00", 1.5, arrow=True)
        else:
            f.rect(x + 20, 252, 180, 16, "#90caf9" if i == 2 else "#9e9e9e"); f.rect(x + 120, 180, 10 if i == 2 else 40, 72, "#2e7d32" if i == 2 else "#757575")
            f.line(x + 100, 250, x + 118, 230, "#ef6c00", 2); f.line(x + 118, 230, x + 40, 150, "#ef6c00", 2.5, arrow=True)
        f.text(x + 110, 310, b, 13, INK, "middle"); f.text(x + 110, 340, c, 14, col, "middle", "bold")
    entry(7, f.save("a07-mechanisms"), "ផ្ទៃរលោងចាំងចេញ ផ្ទៃរដុបចាំងត្រឡប់",
          ["ទឹកស្ងប់ដូចកញ្ចក់៖ រលកចាំងចេញឆ្ងាយ ហើយត្រឡប់មកផ្កាយរណបតិចណាស់ (ងងឹត)។", "រុក្ខជាតិលិចទឹក និងទីក្រុងចាំងពីរដង៖ ភ្លឺ មិនមែនងងឹតទេ ដូច្នេះការកំណត់កម្រិតរំលងវា។",
           "ខ្យល់ខ្លាំងធ្វើឲ្យផ្ទៃទឹករដុប និងភ្លឺជាងធម្មតា៖ ជាប្រភពកំហុសមួយទៀត។"], .2)
    # 3 speckle and filtering (computed on simulated image)
    filt = 10 * np.log10(ndi.median_filter(10 ** (after / 10), 5))
    f = Fig(1000, 450).title("Speckle និងតម្រង", SIM_SAR)
    f.img(gray(after, -25, 0), 30, 85, 300, 300); f.img(gray(filt, -25, 0), 350, 85, 300, 300)
    f.text(180, 410, "ដើម (VV dB)", 15, INK, "middle", "bold"); f.text(500, 410, "focal_median ៥ × ៥", 15, INK, "middle", "bold")
    h1, e = np.histogram(after, 60, (-30, 5)); h2, _ = np.histogram(filt, 60, (-30, 5)); mx = max(h1.max(), h2.max())
    x0, y0, w, h = 690, 110, 280, 250
    for hh, col in ((h1, "#b0bec5"), (h2, "#1565c0")):
        f.path("M" + " L".join(f"{x0 + i * w / 60:.1f} {y0 + h - h * v / mx:.1f}" for i, v in enumerate(hh)), "none", col, 2.5)
    f.line(x0, y0 + h, x0 + w, y0 + h, INK, 1); f.text(x0, y0 + h + 18, "−៣០", 12, "#546e7a"); f.text(x0 + w, y0 + h + 18, "៥ dB", 12, "#546e7a", "end")
    f.text(x0 + 10, y0 - 8, "អ៊ីស្តូក្រាម៖ ប្រផេះ = ដើម · ខៀវ = បានតម្រង", 12, INK)
    entry(7, f.save("a07-speckle"), "តម្រងធ្វើឲ្យកំពូលពីរច្បាស់",
          ["Speckle ជាសំឡេងរំខានពីធម្មជាតិនៃ SAR៖ ក្រឡាជិតគ្នាលើផ្ទៃដូចគ្នា មានតម្លៃខុសគ្នាខ្លាំង។", "focal_median បន្ថយ speckle ហើយអ៊ីស្តូក្រាមក្លាយជាកំពូលពីរច្បាស់៖ ទឹក និងដី។",
           "តម្រងធំពេកធ្វើឲ្យប្រឡាយ និងស្រះតូចៗបាត់។ ២–៥ ក្រឡា (២០–៥០ ម) ជាទូទៅសមរម្យ។"], .38)
    # 4 histogram + Otsu (computed)
    t = otsu(filt); acc_otsu = ((filt < t) == (water | flood)).mean(); fixed = -16; acc_fixed = ((filt < fixed) == (water | flood)).mean()
    f = Fig(1000, 450).title("ជ្រើសកម្រិតដោយ Otsu", SIM_SAR + " · ក្រោយតម្រង")
    h, e = np.histogram(filt, 80, (-28, 2)); mx = h.max(); x0, y0, w, hh = 70, 100, 560, 270
    for i, v in enumerate(h): f.rect(x0 + i * w / 80, y0 + hh - hh * v / mx, w / 80 - .6, hh * v / mx, "#64b5f6" if e[i] < t else "#bcaaa4")
    X = lambda v: x0 + (v + 28) / 30 * w
    f.line(X(t), y0 - 5, X(t), y0 + hh, "#c62828", 2.5); f.text(X(t) + 6, y0 + 10, f"Otsu = {KHF(t, 1)} dB", 14, "#c62828", weight="bold")
    f.line(X(fixed), y0 + 30, X(fixed), y0 + hh, "#6a1b9a", 2, "6 4"); f.text(X(fixed) + 6, y0 + 44, "ថេរ −១៦ dB", 13, "#6a1b9a")
    for v in (-25, -20, -15, -10, -5, 0): f.text(X(v), y0 + hh + 20, kh(v), 12, "#546e7a", "middle")
    f.rect(670, 110, 300, 200, "#fafafa", "#cfd8dc", 1, 10); f.text(690, 145, "ភាពត្រឹមត្រូវ (ធៀបនឹងការពិតក្លែងធ្វើ)", 14, INK, weight="bold")
    f.text(690, 190, f"Otsu៖ {kh(round(acc_otsu * 100, 1)).replace('.', ',')}%", 18, "#c62828", weight="bold"); f.text(690, 230, f"ថេរ −១៦ dB៖ {kh(round(acc_fixed * 100, 1)).replace('.', ',')}%", 18, "#6a1b9a", weight="bold")
    f.text(690, 280, "ee.Reducer.histogram() + Otsu", 13, "#607d8b", extra='font-family="monospace"')
    entry(7, f.save("a07-otsu"), "កម្រិតដែលសមនឹងរូបភាពនីមួយៗ",
          [f"Otsu ជ្រើសកម្រិតដែលបំបែកកំពូលទាំងពីរល្អបំផុត៖ នៅទីនេះ {KHF(t, 1)} dB។", "កម្រិតថេរ (−១៥ ដល់ −១៨ dB) ងាយប្រើ ប៉ុន្តែអាចមិនសមនឹងរូបភាព មុំ ឬខ្យល់ផ្សេងៗ។",
           "Otsu ដំណើរការល្អ លុះត្រាតែតំបន់មានទាំងទឹក និងដីច្រើនគួរសម (ជ្រើស AOI ជុំវិញទឹកជំនន់)។"], .5)
    # 5 change detection
    fb = 10 * np.log10(ndi.median_filter(10 ** (before / 10), 5)); diff = filt - fb
    det = (diff < -3) & (filt < t); tp = (det & flood).sum(); fp = (det & ~flood).sum(); fn = (~det & flood).sum()
    f = Fig(1000, 450).title("ការរកការផ្លាស់ប្ដូរ៖ មុន និងក្រោយ", SIM_SAR)
    for k, (a, lab) in enumerate([(fb, "មុន (រដូវប្រាំង)"), (filt, "ក្រោយ (ទឹកជំនន់)")]): f.img(gray(a, -25, 0), 20 + k * 245, 85, 230, 230); f.text(135 + k * 245, 335, lab, 14, INK, "middle", "bold")
    f.img(ramp(diff, ["#08519c", "#6baed6", "#f7f7f7", "#fdae61", "#d7191c"], -10, 10), 510, 85, 230, 230); f.text(625, 335, "ក្រោយ − មុន (dB)", 14, INK, "middle", "bold")
    rgbm = np.full(C.shape + (3,), 235, np.uint8); rgbm[water] = (30, 136, 229); rgbm[det] = (229, 57, 53)
    f.img(Image.fromarray(rgbm), 755, 85, 230, 230, fmt="PNG"); f.text(870, 335, "ទឹកជំនន់ (ក្រហម) · ទឹកអចិន្ត្រៃយ៍ (ខៀវ)", 13, INK, "middle", "bold")
    f.text(500, 385, f"ក្រឡាទឹកជំនន់ពិតដែលរកឃើញ {kh(round(tp / (tp + fn) * 100))}% · ក្រឡាដែលរកឃើញខុស {kh(round(fp / max(1, tp + fp) * 100))}%", 15, "#607d8b", "middle")
    entry(7, f.save("a07-change"), "ទឹកជំនន់ = ទឹកថ្មី",
          ["ផ្ទៃទឹកក្រោយព្រឹត្តិការណ៍ រួមទាំងទន្លេ និងបឹងធម្មតា៖ វាមិនមែនទឹកជំនន់ទាំងអស់ទេ។", "ភាពខុសគ្នា (ក្រោយ − មុន) ធ្លាក់ខ្លាំង (−៣ dB ឬទាបជាង) នៅកន្លែងដែលដីក្លាយជាទឹក។",
           "ប្រើរូបភាពមុន និងក្រោយ ពីគន្លងដូចគ្នា (orbit + pass) ដើម្បីកុំឲ្យភាពខុសគ្នាមកពីមុំមើល។"], .65)
    # 6 false positives
    f = Fig(1000, 450).title("ដកកំហុសវិជ្ជមានក្លែងក្លាយ", "ស្រទាប់ mask បីដែលប្រើញឹកញាប់")
    rows = [("ទឹកអចិន្ត្រៃយ៍", "JRC Global Surface Water · occurrence > ៨០%", "ទន្លេ បឹង ដែលមានទឹកជានិច្ច", "#1e88e5"),
            ("ជម្រាល", "DEM · slope > ៥°", "ស្រមោលរ៉ាដានៅតំបន់ភ្នំ ងងឹតដូចទឹក", "#6d4c41"),
            ("HAND", "MERIT Hydro hnd > ១៥ ម", "ទីខ្ពស់ពីប្រឡាយទឹក មិនងាយលិច", "#2e7d32"),
            ("ផ្ទៃរលោងស្ងួត", "ផ្លូវកៅស៊ូ វាលខ្សាច់ ដីភ្ជួររាបស្មើ", "ពិនិត្យជាមួយរូបភាពមុន ឬអុបទិក", "#ef6c00")]
    for i, (a, b, c, col) in enumerate(rows):
        y = 90 + i * 84; f.rect(40, y, 920, 70, "#fafafa", col, 1.5, 10); f.text(64, y + 30, a, 17, col, weight="bold"); f.text(64, y + 55, b, 13, "#607d8b"); f.text(520, y + 42, c, 15, INK)
    entry(7, f.save("a07-masks"), "រកទឹកបានហើយ ត្រូវសួរថា «ពិតជាទឹកជំនន់ទេ?»",
          ["ទឹកអចិន្ត្រៃយ៍ត្រូវដកចេញ ដើម្បីកុំឲ្យទន្លេ និងទន្លេសាបរាប់ជាទឹកជំនន់។", "ស្រមោលរ៉ាដានៅជម្រាលភ្នំ ងងឹតដូចទឹក៖ mask តាម slope ឬ HAND។",
           "ផ្ទៃរលោងស្ងួត (ផ្លូវ ដីភ្ជួររាប) ក៏ងងឹតដែរ៖ ការប្រៀបធៀបមុន–ក្រោយជួយដោះស្រាយ។"], .8)
    # 7 exposure: flooded area by land cover (computed on simulated flood × real land cover)
    km2 = [(det & (C == k)).sum() * 900 / 1e6 for k in range(5)]
    f = Fig(1000, 420).title("ពីផែនទីទឹកជំនន់ ទៅជាផលប៉ះពាល់", "ផ្ទៃទឹកជំនន់ដែលរកឃើញ តាមគម្របដីមុនទឹកជំនន់ · " + SIM_SAR)
    bars(f, 60, 100, 470, 250, CLS_KH, km2, CLS_COL, fmt=lambda v: KHF(v, 1) + " គម²", lw=140)
    code(f, 640, 100, 330, ["// flooded area by land cover", "var a = ee.Image.pixelArea()", "  .divide(1e6).updateMask(flood)", "  .addBands(worldcover)", "  .reduceRegion({reducer:", "   ee.Reducer.sum().group(1),", "   geometry: aoi, scale: 10,", "   maxPixels: 1e10});"], 13)
    entry(7, f.save("a07-exposure"), "ស្រែប៉ុន្មានហិកតាលិចទឹក?",
          ["ឆ្លងផែនទីទឹកជំនន់ ជាមួយគម្របដី (ESA WorldCover ឬផែនទីមេរៀនទី៦) ដោយ reducer ជាក្រុម (មេរៀនទី៤)។", "ដំណាំ/ស្មៅ និងដីទទេជិតទន្លេ រងផលប៉ះពាល់ច្រើនជាងគេ។",
           "ឆ្លងជាមួយប្រជាជន (WorldPop) ដើម្បីប៉ាន់ស្មានចំនួនមនុស្សដែលរងផលប៉ះពាល់។"], .9)

# ---------------- Lesson 8 ----------------
CLIM = [8, 10, 35, 80, 150, 155, 160, 165, 230, 255, 130, 40]   # approximate Phnom Penh monthly normals (mm)
def rain_series(seed=21, years=range(1995, 2025)):
    rng = np.random.default_rng(seed); out = {}
    enso = {1997: .7, 2004: .85, 2015: .6, 2019: .7, 2023: .8}
    for y in years:
        k = enso.get(y, 1.0); out[y] = [max(0, c * k * rng.gamma(6, 1 / 6)) for c in CLIM]
    return out

def L08():
    ILL = "ស៊េរីក្លែងធ្វើ (សម្រាប់បង្រៀន)"
    # 1 drought types cascade
    f = Fig(1000, 430).title("គ្រោះរាំងស្ងួតបួនប្រភេទ", "ពីភ្លៀងខ្វះ ទៅផលប៉ះពាល់លើមនុស្ស")
    items = [("ឧតុនិយម", "ភ្លៀងតិចជាងធម្មតា", "CHIRPS · SPI", "#90caf9"), ("កសិកម្ម", "សំណើមដី និងដំណាំខ្វះទឹក", "VCI · TCI · VHI", "#ffcc80"),
             ("ជលសាស្ត្រ", "ទឹកទន្លេ បឹង អាងស្តុកថយ", "JRC · Sentinel-1", "#ef9a9a"), ("សង្គមសេដ្ឋកិច្ច", "ទិន្នផល ចំណូល ស្បៀង", "ស្ថិតិ · ការស្ទង់", "#ce93d8")]
    for i, (a, b, c, col) in enumerate(items):
        x = 30 + i * 240; box(f, x, 110, 215, 150, a, b, col, 19, INK); f.text(x + 107, 300, c, 14, "#607d8b", "middle")
        if i < 3: f.line(x + 217, 185, x + 236, 185, "#607d8b", 2.5, arrow=True)
    f.line(60, 360, 940, 360, "#607d8b", 2, arrow=True); f.text(500, 390, "ពេលវេលាចាប់ពីភ្លៀងខ្វះ៖ សប្ដាហ៍ → ខែ → រដូវ → ឆ្នាំ", 14, INK, "middle")
    entry(8, f.save("a08-types"), "គ្រោះរាំងស្ងួតរីកដាលជាដំណាក់កាល",
          ["ភ្លៀងខ្វះ (ឧតុនិយម) កើតមុន ហើយប្រហែលជាមិនប៉ះពាល់ដំណាំទេ ប្រសិនបើខ្លី។", "រុក្ខជាតិឆ្លើយតបយឺតជាងភ្លៀង ប៉ុន្មានសប្ដាហ៍៖ VCI និង VHI វាស់ដំណាក់កាលកសិកម្ម។",
           "សន្ទស្សន៍នីមួយៗ វាស់ដំណាក់កាលខុសគ្នា ដូច្នេះប្រើរួមគ្នា។"], .06)
    # 2 climatology
    RS = rain_series(); yrs = sorted(RS); arr = np.array([RS[y] for y in yrs])
    f = Fig(1000, 440).title("ទឹកភ្លៀងធម្មតា (climatology)", "ទឹកភ្លៀងប្រចាំខែ ភ្នំពេញ · មធ្យម និងចន្លោះ p10–p90 · " + ILL)
    X, Y = chart(f, 80, 90, 600, 280, [(list(range(12)), list(arr.mean(0)), "#1565c0", "មធ្យម ៣០ ឆ្នាំ", 3), (list(range(12)), RS[2019], "#e53935", "២០១៩", 2.5)], (0, 11), (0, 450), "", "ទឹកភ្លៀង (mm)", yt=[0, 100, 200, 300, 400], lx=700, ly=120)
    p10, p90 = np.percentile(arr, 10, 0), np.percentile(arr, 90, 0)
    f.path("M" + " L".join(f"{X(i):.1f} {Y(v):.1f}" for i, v in enumerate(p90)) + " L" + " L".join(f"{X(i):.1f} {Y(v):.1f}" for i, v in reversed(list(enumerate(p10)))) + "Z", "#1565c0", "none", 0, .15)
    for i, m in enumerate(MON): f.text(X(i), 395, m, 12, "#546e7a", "middle")
    f.text(700, 190, "ផ្ទៃពណ៌ខៀវស្រាល = ៨០% នៃឆ្នាំ", 13, "#607d8b")
    entry(8, f.save("a08-climatology"), "«ធម្មតា» គឺជាចន្លោះ មិនមែនលេខមួយទេ",
          ["Climatology = ស្ថិតិនៃខែដូចគ្នាក្នុងរយៈពេលវែង (ជាទូទៅ ៣០ ឆ្នាំ)។", "ខែមួយប្រៀបធៀបតែនឹងខែដដែលនៃឆ្នាំផ្សេងៗប៉ុណ្ណោះ៖ កក្កដា ២០១៩ ធៀបនឹងកក្កដាទាំងអស់។",
           "តម្លៃមធ្យមប្រចាំខែ ផ្អែកលើកម្រិតប្រហាក់ប្រហែលនៃភ្នំពេញ ស៊េរីឆ្នាំជាស៊េរីក្លែងធ្វើ។"], .25)
    # 3 anomalies: percent of normal and z-score for 2019 (from the series)
    mu, sd = arr.mean(0), arr.std(0); pct = np.array(RS[2019]) / mu * 100; z = (np.array(RS[2019]) - mu) / sd
    f = Fig(1000, 440).title("ភាពមិនប្រក្រតី (anomaly) ឆ្នាំ ២០១៩", "% នៃធម្មតា និង z-score · " + ILL)
    for i in range(12):
        x = 80 + i * 72; v = z[i]; h = abs(v) * 50; col = "#c62828" if v < -1 else "#ef9a9a" if v < 0 else "#64b5f6"
        f.rect(x, 250 - (h if v > 0 else 0), 50, h, col); f.text(x + 25, 250 + (h + 18 if v < 0 else -h - 8), KHF(v, 1), 12, INK, "middle"); f.text(x + 25, 400, MON[i], 12, "#546e7a", "middle"); f.text(x + 25, 425, kh(round(pct[i])) + "%", 11, "#607d8b", "middle")
    f.line(70, 250, 950, 250, INK, 1); f.line(70, 300, 950, 300, "#c62828", 1, "5 4"); f.text(955, 304, "−១", 12, "#c62828")
    f.text(80, 100, "z = (តម្លៃ − មធ្យម) / គម្លាតស្តង់ដារ", 15, INK, weight="bold")
    entry(8, f.save("a08-anomaly"), "ខ្វះប៉ុន្មាន ធៀបនឹងធម្មតា?",
          ["% នៃធម្មតាងាយយល់ ប៉ុន្តែខែប្រាំង (ភ្លៀង ១០ mm) ធ្វើឲ្យភាគរយប្រែប្រួលខ្លាំងគ្មានន័យ។", "z-score គិតពីភាពប្រែប្រួលធម្មតា៖ −១ ដល់ −២ = ស្ងួតជាងធម្មតាច្បាស់។",
           "SPI ពិតប្រើការបម្លែង gamma មុនគណនា z ព្រោះទឹកភ្លៀងមិនចែកចាយតាមរាង normal។"], .45)
    # 4 SPI accumulation windows
    series = np.array([v for y in yrs for v in RS[y]])
    def spi(k):
        acc = np.convolve(series, np.ones(k), "valid"); acc = np.concatenate([np.full(k - 1, np.nan), acc]); out = np.full_like(acc, np.nan)
        for m in range(12):
            idx = np.arange(m, len(acc), 12); v = acc[idx]; ok = ~np.isnan(v); out[idx[ok]] = (v[ok] - v[ok].mean()) / v[ok].std()
        return out
    s1, s3, s6 = spi(1), spi(3), spi(6); t0 = (2018 - 1995) * 12; t1 = (2021 - 1995) * 12; xs = list(range(t1 - t0))
    f = Fig(1000, 450).title("រយៈពេលបូក៖ SPI-១ SPI-៣ SPI-៦", "២០១៨–២០២០ · SPI សាមញ្ញ (z-score នៃទឹកភ្លៀងបូក) · " + ILL)
    X, Y = chart(f, 80, 90, 700, 290, [(xs, list(s1[t0:t1]), "#b0bec5", "SPI-១", 1.5), (xs, list(s3[t0:t1]), "#1e88e5", "SPI-៣", 2.5), (xs, list(s6[t0:t1]), "#c62828", "SPI-៦", 3)], (0, 35), (-3, 3), "", "SPI", yt=[-3, -2, -1, 0, 1, 2, 3], lx=800, ly=120)
    for k, y in enumerate((2018, 2019, 2020)): f.text(X(k * 12 + 6), 404, kh(y), 13, "#546e7a", "middle")
    f.line(X(0), Y(-1), X(35), Y(-1), "#ef6c00", 1, "5 4")
    entry(8, f.save("a08-spi"), "រយៈពេលខ្លី ឬវែង ឆ្លើយសំណួរខុសគ្នា",
          ["SPI-១ លោតឡើងចុះរាល់ខែ៖ ល្អសម្រាប់ដឹងភ្លាមៗ តែមានសំឡេងរំខានច្រើន។", "SPI-៣ ទាក់ទងនឹងសំណើមដី និងដំណាំ។ SPI-៦ ដល់ ១២ ទាក់ទងនឹងទន្លេ និងអាងស្តុកទឹក។",
           "SPI < −១ = ស្ងួតមធ្យម · < −១,៥ = ស្ងួតខ្លាំង · < −២ = ស្ងួតខ្លាំងបំផុត។"], .55)
    # 5 VCI concept
    rng = np.random.default_rng(3); doy = np.arange(1, 366, 16)
    base = .35 + .35 * np.exp(-((doy - 290) / 55) ** 2); hist = np.array([base + rng.normal(0, .05, doy.size) for _ in range(20)])
    mn, mxx = hist.min(0), hist.max(0); cur = mn + (mxx - mn) * (.6 - .5 * np.exp(-((doy - 230) / 45) ** 2)); vci = (cur - mn) / (mxx - mn) * 100
    f = Fig(1000, 460).title("សន្ទស្សន៍ស្ថានភាពរុក្ខជាតិ (VCI)", "NDVI ១៦ ថ្ងៃ · ២០ ឆ្នាំ និងឆ្នាំស្ងួត · " + ILL)
    X, Y = chart(f, 80, 90, 560, 290, [(list(doy), list(cur), "#c62828", "ឆ្នាំនេះ", 3)], (1, 365), (.1, .9), "", "NDVI", yt=[.2, .4, .6, .8], legend=False)
    f.path("M" + " L".join(f"{X(a):.1f} {Y(b):.1f}" for a, b in zip(doy, mxx)) + " L" + " L".join(f"{X(a):.1f} {Y(b):.1f}" for a, b in reversed(list(zip(doy, mn)))) + "Z", "#43a047", "none", 0, .2)
    for i, m in enumerate(MON): f.text(X(MSTART[i] + 14), 400, m, 12, "#546e7a", "middle")
    k = int(np.argmin(vci)); f.circle(X(doy[k]), Y(cur[k]), 7, "#c62828", "#fff", 2)
    f.rect(680, 100, 290, 250, "#fafafa", "#cfd8dc", 1, 10)
    f.text(700, 135, "VCI = (NDVI − NDVImin)", 15, INK, weight="bold"); f.text(760, 162, "/ (NDVImax − NDVImin) × ១០០", 14, INK)
    f.text(700, 205, f"ទាបបំផុត៖ VCI ≈ {kh(round(vci[k]))}", 16, "#c62828", weight="bold"); f.text(700, 240, "< ៤០ = រងគ្រោះរាំងស្ងួត", 14, INK); f.text(700, 268, "< ២០ = ធ្ងន់ធ្ងរ", 14, INK)
    f.text(700, 310, "ផ្ទៃបៃតង = min–max ២០ ឆ្នាំ", 13, "#607d8b")
    entry(8, f.save("a08-vci"), "ធៀបនឹងខ្លួនឯង មិនមែននឹងកន្លែងផ្សេង",
          ["VCI ដាក់ NDVI បច្ចុប្បន្នក្នុងចន្លោះ min–max នៃក្រឡាដដែល ក្នុងពេលដដែលនៃឆ្នាំ។", "ដូច្នេះព្រៃ (NDVI ខ្ពស់) និងស្រែ (NDVI ទាប) អាចប្រៀបធៀបគ្នាបាន៖ ០ = អាក្រក់បំផុតដែលធ្លាប់មាន។",
           "ត្រូវការប្រវត្តិយូរ (MODIS ២០០០–បច្ចុប្បន្ន) ដើម្បីឲ្យ min និង max មានន័យ។"], .7)
    # 6 VHI matrix
    f = Fig(1000, 440).title("VHI = α·VCI + (១ − α)·TCI", "រួមបញ្ចូលភាពបៃតង (NDVI) និងកំដៅ (LST) · α = ០,៥ ជាទូទៅ")
    for i in range(5):
        for j in range(5):
            v = .5 * (i * 25) + .5 * (j * 25); col = ["#b71c1c", "#e53935", "#fb8c00", "#fdd835", "#43a047"][min(4, int(v // 20))]
            f.rect(300 + j * 70, 90 + (4 - i) * 60, 68, 58, col); f.text(334 + j * 70, 126 + (4 - i) * 60, kh(round(v)), 14, "#fff" if v < 50 else INK, "middle", "bold")
    for k in range(5): f.text(290, 126 + (4 - k) * 60, kh(k * 25), 12, INK, "end"); f.text(334 + k * 70, 410, kh(k * 25), 12, INK, "middle")
    f.text(200, 250, "VCI", 16, IND, "middle", "bold"); f.text(475, 434, "TCI", 16, AMB, "middle", "bold")
    f.rect(700, 100, 270, 260, "#fafafa", "#cfd8dc", 1, 10)
    f.text(720, 135, "TCI = (LSTmax − LST)", 14, INK, weight="bold"); f.text(760, 160, "/ (LSTmax − LSTmin) × ១០០", 13, INK)
    f.text(720, 210, "VHI < ៤០ = រាំងស្ងួត", 15, INK); f.text(720, 245, "LST៖ MODIS MOD11A2", 13, "#607d8b"); f.text(720, 270, "NDVI៖ MODIS MOD13Q1", 13, "#607d8b")
    entry(8, f.save("a08-vhi"), "បៃតងតិច + ក្ដៅខ្លាំង = រាំងស្ងួត",
          ["TCI ខ្ពស់ពេល LST ទាប (ត្រជាក់) ព្រោះរុក្ខជាតិដែលមានទឹក ត្រជាក់ខ្លួនដោយការបញ្ចេញចំហាយ។", "VHI ទាបទាល់តែ VCI ឬ TCI ទាប៖ ក្រឡាក្រហមនៅជ្រុងខាងក្រោមឆ្វេង។",
           "ពេលពពកច្រើន LST បាត់ច្រើន៖ VHI រដូវវស្សាត្រូវបកស្រាយដោយប្រុងប្រយ័ត្ន។"], .8)
    # 7 lag rainfall -> NDVI
    m = np.arange(24); rain = np.tile(CLIM, 2).astype(float); rain[18:22] *= .4
    ndvi = np.array([.22 + .5 * min(1, np.mean(rain[max(0, i - 3):max(1, i - 1)]) / 200) for i in range(24)])
    f = Fig(1000, 440).title("រុក្ខជាតិឆ្លើយតបយឺតជាងភ្លៀង", "ភ្លៀងខ្វះ ៤ ខែ (កក្កដា–តុលា ឆ្នាំទី២) · NDVI ពីទឹកភ្លៀង ២ ខែមុន · " + ILL)
    x0, y0, w, h = 80, 90, 816, 280; bw = w / 24
    f.rect(x0, y0, w, h, "#fff", "#cfd8dc", .8)
    for i, v in enumerate(rain): f.rect(x0 + i * bw + 4, y0 + h - v / 300 * h, bw - 8, v / 300 * h, "#ef9a9a" if 18 <= i < 22 else "#90caf9")
    f.path("M" + " L".join(f"{x0 + (i + .5) * bw:.1f} {y0 + h - v * h:.1f}" for i, v in enumerate(ndvi)), "none", "#2e7d32", 3)
    for i, v in enumerate(ndvi): f.circle(x0 + (i + .5) * bw, y0 + h - v * h, 3.5, "#2e7d32")
    k = 18 + int(np.argmin(ndvi[18:24])); f.circle(x0 + (k + .5) * bw, y0 + h - ndvi[k] * h, 8, "none", "#c62828", 2.5)
    for i in range(24): f.text(x0 + (i + .5) * bw, y0 + h + 16, MON[i % 12], 10, "#546e7a", "middle")
    f.text(x0, 410, "ឆ្នាំទី១", 13, "#546e7a"); f.text(x0 + w / 2, 410, "ឆ្នាំទី២", 13, "#546e7a"); f.text(890, 112, "━ NDVI (០–១)", 13, "#2e7d32", "end", "bold"); f.text(890, 134, "■ ទឹកភ្លៀង (០–៣០០ mm)", 13, "#1565c0", "end")
    entry(8, f.save("a08-lag"), "ពិនិត្យភ្លៀងមុន រុក្ខជាតិក្រោយ",
          [f"ភ្លៀងខ្វះចាប់ផ្ដើមខែកក្កដា ប៉ុន្តែ NDVI ធ្លាក់ទាបបំផុតនៅខែ{MON[k % 12]} (រង្វង់ក្រហម)។", "ទឹកក្នុងដី និងប្រព័ន្ធធារាសាស្ត្រ ពន្យារពេលផលប៉ះពាល់៖ រយៈពេលយឺតខុសគ្នាតាមតំបន់។",
           "នេះជាហេតុផលដែលប្រព័ន្ធព្រមានប្រើ CHIRPS សម្រាប់ព្រមានមុន និង VCI សម្រាប់បញ្ជាក់។"], .9)

# ---------------- Lesson 9 ----------------
def synth_dem(n=160, seed=9):
    rng = np.random.default_rng(seed); yy, xx = np.mgrid[0:n, 0:n] / n
    z = 20 + 380 * np.clip(1 - xx * 1.4, 0, 1) ** 1.6 + 120 * np.exp(-((xx - .3) ** 2 + (yy - .25) ** 2) / .02)
    for s, a in ((24, 60), (10, 25), (4, 8)): z += a * ndi.gaussian_filter(rng.normal(size=(n, n)), n / s) * s / 3
    z -= 40 * np.exp(-((yy - .55 - .1 * np.sin(xx * 6)) ** 2) / .004) / (1 + np.exp(-(xx - .35) * 40))   # a valley
    z = ndi.gaussian_filter(z, 1.2)
    return z - z.min() + 5
def slope_aspect(z, res=30.0):
    gy, gx = np.gradient(z, res); sl = np.degrees(np.arctan(np.hypot(gx, gy))); asp = (np.degrees(np.arctan2(-gx, gy)) + 360) % 360
    return sl, asp
def hillshade(z, az=315, alt=45, res=30.0):
    gy, gx = np.gradient(z, res); sl = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, gy)
    a, e = np.radians(360 - az + 90), np.radians(alt)
    return np.clip(np.sin(e) * np.cos(sl) + np.cos(e) * np.sin(sl) * np.cos(a - asp), 0, 1)
D8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
def d8(z):
    n = z.shape[0]; zp = np.pad(z, 1, constant_values=np.inf); best = np.full(z.shape, -1); bd = np.zeros(z.shape)
    for k, (dy, dx) in enumerate(D8):
        drop = (z - zp[1 + dy:1 + dy + n, 1 + dx:1 + dx + z.shape[1]]) / np.hypot(dy, dx)
        m = drop > bd; best[m] = k; bd[m] = drop[m]
    return best
def flowacc(z, fd):
    n, m = z.shape; acc = np.ones(z.shape); order = np.argsort(-z, axis=None)
    for idx in order:
        r, c = divmod(int(idx), m); k = fd[r, c]
        if k < 0: continue
        rr, cc = r + D8[k][0], c + D8[k][1]
        if 0 <= rr < n and 0 <= cc < m: acc[rr, cc] += acc[r, c]
    return acc
def fill_sinks(z, it=200):
    """Simple priority-flood fill so D8 drains to the edge."""
    import heapq
    n, m = z.shape; f = z.copy(); done = np.zeros(z.shape, bool); h = []
    for r in range(n):
        for c in range(m):
            if r in (0, n - 1) or c in (0, m - 1): heapq.heappush(h, (f[r, c], r, c)); done[r, c] = True
    while h:
        v, r, c = heapq.heappop(h)
        for dy, dx in D8:
            rr, cc = r + dy, c + dx
            if 0 <= rr < n and 0 <= cc < m and not done[rr, cc]:
                done[rr, cc] = True; f[rr, cc] = max(f[rr, cc], v + 1e-3); heapq.heappush(h, (f[rr, cc], rr, cc))
    return f

TER = ["#1a9850", "#91cf60", "#d9ef8b", "#fee08b", "#fc8d59", "#a6611a", "#f5f5f5"]
def L09():
    SYN = "DEM ក្លែងធ្វើ ១៦០ × ១៦០ ក្រឡា ៣០ ម (សម្រាប់បង្រៀន)"
    z = synth_dem(); zf = fill_sinks(z); fd = d8(zf); acc = flowacc(zf, fd); sl, asp = slope_aspect(z); hs = hillshade(z)
    lo, hi = np.percentile(hs, [2, 98]); hs = np.clip((hs - lo) / (hi - lo), 0, 1)
    # 1 DEM sources
    f = Fig(1000, 460).title("DEM ក្នុង Earth Engine", "ជ្រើសតាមសំណួរ")
    rows = [("SRTM", "USGS/SRTMGL1_003", "៣០ ម", "២០០០ · DSM · ពេញនិយមបំផុត"), ("NASADEM", "NASA/NASADEM_HGT/001", "៣០ ម", "SRTM ដែលបានកែលម្អ"),
            ("Copernicus GLO-30", "COPERNICUS/DEM/GLO30", "៣០ ម", "២០១១–១៥ · DSM · ជាទូទៅត្រឹមត្រូវជាង"), ("ALOS AW3D30", "JAXA/ALOS/AW3D30/V3_2", "៣០ ម", "DSM · ប្រើក្នុងមេរៀនទី៦"),
            ("MERIT Hydro", "MERIT/Hydro/v1_0_1", "៩០ ម", "ជលសាស្ត្រ៖ ទិស ស្រុតទឹក HAND"), ("HydroSHEDS", "WWF/HydroSHEDS/03CONDEM ...", "៩០ ម", "DEM ដែលបានកែសម្រាប់លំហូរទឹក")]
    f.text(40, 100, "ឈ្មោះ", 14, "#607d8b", weight="bold"); f.text(250, 100, "ID", 14, "#607d8b", weight="bold"); f.text(600, 100, "ក្រឡា", 14, "#607d8b", weight="bold"); f.text(690, 100, "ចំណាំ", 14, "#607d8b", weight="bold")
    for i, (a, b, c, d) in enumerate(rows):
        y = 118 + i * 50; f.rect(30, y, 940, 42, "#f1f8e9" if i % 2 == 0 else "#fff"); f.text(40, y + 27, a, 15, INK, weight="bold"); f.text(250, y + 27, b, 13, INK, extra='font-family="monospace"'); f.text(600, y + 27, c, 14); f.text(690, y + 27, d, 13)
    entry(9, f.save("a09-sources"), "DEM ភាគច្រើនជា DSM",
          ["SRTM Copernicus និង ALOS វាស់ផ្ទៃខាងលើ (ដំបូល ពំនូកព្រៃ) មិនមែនដីទេ៖ ព្រៃខ្ពស់ធ្វើឲ្យកម្ពស់លើស។", "សម្រាប់ជលសាស្ត្រ ប្រើ MERIT Hydro ឬ HydroSHEDS ដែលបានកែលម្អរួច។",
           "វាលទំនាបកម្ពុជាមានជម្រាលតិចណាស់៖ កំហុស DEM ពីរបីម៉ែត្រ មានឥទ្ធិពលធំលើលំហូរទឹក។"], .08)
    # 2 DEM + slope + aspect + hillshade
    f = Fig(1000, 440).title("ee.Terrain.products()៖ ផលិតផលបួន", SYN)
    for k, (im, lab) in enumerate([(ramp(z, TER, z.min(), z.max()), "elevation"), (ramp(sl, ["#ffffcc", "#fd8d3c", "#bd0026"], 0, 25), "slope (°)"),
                                   (ramp(asp, ["#e41a1c", "#ffff33", "#4daf4a", "#377eb8", "#e41a1c"], 0, 360), "aspect (°)"), (Image.fromarray((hs * 255).astype(np.uint8)), "hillshade")]):
        f.img(im, 20 + k * 245, 90, 225, 225); f.text(132 + k * 245, 340, lab, 15, INK, "middle", "bold", extra='font-family="monospace"')
    f.text(500, 395, "var t = ee.Terrain.products(dem);   // elevation slope aspect hillshade", 14, INK, "middle", extra='font-family="monospace"')
    entry(9, f.save("a09-products"), "ជម្រាល ទិស និងស្រមោល ពី DEM មួយ",
          ["slope៖ មុំជាដឺក្រេ (០ = រាបស្មើ)។ aspect៖ ទិសដែលជម្រាលបែរទៅ (០ = ជើង ៩០ = កើត)។", "hillshade៖ ស្រមោលក្លែងធ្វើពីពន្លឺព្រះអាទិត្យ សម្រាប់មើលរូបរាងដី (សៀវភៅទី១)។",
           "គណនានៅ projection ដែលមានម៉ែត្រ៖ mosaic ត្រូវ setDefaultProjection (មេរៀនទី៦)។"], .25)
    # 3 D8 grid
    g = np.array([[78, 72, 69, 71, 58], [74, 67, 56, 49, 46], [69, 53, 44, 37, 38], [64, 58, 55, 22, 31], [68, 61, 47, 21, 16]], float)
    fdg = d8(g); accg = flowacc(g, fdg)
    f = Fig(1000, 440).title("ទិសលំហូរ D8 និងស្រុតទឹក", "ក្រឡានីមួយៗបង្ហូរទៅអ្នកជិតខាងដែលចុះទាបខ្លាំងបំផុត")
    for t, (x0, vals, lab) in enumerate([(40, g, "កម្ពស់ (ម)"), (360, None, "ទិស D8"), (680, accg, "ស្រុតទឹក (ក្រឡា)")]):
        f.text(x0 + 140, 95, lab, 16, IND, "middle", "bold")
        for r in range(5):
            for c in range(5):
                x, y = x0 + c * 56, 110 + r * 56
                col = "#e8f5e9" if vals is None else ramp(np.array([[vals[r, c]]]), ["#f7fbff", "#6baed6", "#08306b"] if t == 2 else TER, vals.min(), vals.max()).getpixel((0, 0))
                col = col if isinstance(col, str) else "#%02x%02x%02x" % col
                f.rect(x, y, 54, 54, col, "#fff")
                if vals is not None: f.text(x + 27, y + 33, kh(int(vals[r, c])), 15, "#fff" if (t == 2 and vals[r, c] > 6) else INK, "middle", "bold")
                else:
                    k = fdg[r, c]
                    if k >= 0: dy, dx = D8[k]; f.line(x + 27 - dx * 12, y + 27 - dy * 12, x + 27 + dx * 16, y + 27 + dy * 16, "#1565c0", 2.5, arrow=True)
                    else: f.circle(x + 27, y + 27, 6, "#1565c0")
    f.text(500, 420, "ក្រឡាស្រុតទឹកខ្ពស់ = ប្រឡាយ ឬទន្លេ", 15, "#607d8b", "middle")
    entry(9, f.save("a09-d8"), "ទឹកហូរទៅទីទាប",
          ["D8៖ ក្រឡានីមួយៗបង្ហូរទៅក្រឡាជិតខាងមួយក្នុងចំណោម ៨ ដែលជម្រាលចុះខ្លាំងបំផុត។", "ស្រុតទឹក (flow accumulation) = ចំនួនក្រឡាដែលហូរកាត់ក្រឡានីមួយៗ។",
           "ទីជ្រៅក្នុង DEM (sink) បញ្ឈប់លំហូរ៖ ត្រូវបំពេញ (fill) មុន ឬប្រើ HydroSHEDS/MERIT ដែលកែរួច។"], .45)
    # 4 flow accumulation + streams on synthetic DEM
    f = Fig(1000, 450).title("ស្រុតទឹក និងបណ្ដាញប្រឡាយ", SYN)
    f.img(Image.fromarray((hs * 200 + 40).astype(np.uint8)), 30, 85, 330, 330)
    la = np.log10(acc); f.img(ramp(la, ["#f7fbff", "#6baed6", "#08306b"], 0, la.max()), 380, 85, 330, 330)
    stream = acc > 400; img = np.dstack([(hs * 200 + 40).astype(np.uint8)] * 3); img[stream] = (21, 101, 192)
    f.img(Image.fromarray(img), 730, 85, 240, 240, fmt="PNG")
    f.text(195, 440, "hillshade", 14, INK, "middle"); f.text(545, 440, "log₁₀(ស្រុតទឹក)", 14, INK, "middle"); f.text(850, 350, "ប្រឡាយ = ស្រុតទឹក > ៤០០ ក្រឡា", 13, INK, "middle"); f.text(850, 372, f"(≈ {KHF(400 * 900 / 1e6, 2)} គម²)", 13, "#607d8b", "middle")
    entry(9, f.save("a09-flowacc"), "បណ្ដាញទន្លេកើតចេញពី DEM",
          ["ស្រុតទឹកមានលំដាប់ទំហំខុសគ្នាខ្លាំង (១ ដល់រាប់ម៉ឺន) ដូច្នេះបង្ហាញជា log។", "កម្រិតស្រុតទឹក (ឧ. > ៤០០ ក្រឡា) កំណត់ថាក្រឡាណាជាប្រឡាយ៖ កម្រិតតូច = ប្រឡាយច្រើន។",
           "ក្នុង Earth Engine ប្រើ WWF/HydroSHEDS/15ACC ឬ MERIT/Hydro upa ដែលគណនារួច។"], .6)
    # 5 watershed delineation for an outlet (computed)
    n = z.shape[0]; rows_ = np.argwhere(acc > 2000); r0, c0 = rows_[np.argmax(acc[acc > 2000])] if len(rows_) else (n - 1, n // 2)
    ws = np.zeros(z.shape, bool); ws[r0, c0] = True; changed = True
    while changed:
        changed = False
        for k, (dy, dx) in enumerate(D8):
            src = np.roll(np.roll(ws, -dy, 0), -dx, 1) & (fd == k) & ~ws
            if src.any(): ws |= src; changed = True
    img = np.dstack([(hs * 200 + 40).astype(np.uint8)] * 3); img[ws] = (0.55 * img[ws] + 0.45 * np.array([255, 152, 0])).astype(np.uint8); img[stream] = (21, 101, 192)
    f = Fig(1000, 450).title("អាងរងទឹកនៃចំណុចចេញមួយ", SYN)
    f.img(Image.fromarray(img), 30, 85, 340, 340, fmt="PNG"); s = 340 / n; f.circle(30 + c0 * s, 85 + r0 * s, 7, "#c62828", "#fff", 2)
    f.text(400, 120, f"ផ្ទៃអាង៖ {KHF(ws.sum() * 900 / 1e6, 1)} គម²", 18, INK, weight="bold"); f.text(400, 155, f"({khn(int(ws.sum()))} ក្រឡា · ចំណុចចេញ ● ក្រហម)", 14, "#607d8b")
    code(f, 400, 190, 570, ["// sub-basins from HydroBASINS (levels 1–12)", "var basins = ee.FeatureCollection(", "  'WWF/HydroSHEDS/v1/Basins/hybas_7');", "var myBasin = basins.filterBounds(", "  ee.Geometry.Point([103.9, 12.3]));", "Map.addLayer(myBasin, {color: 'orange'}, 'basin');"], 14)
    entry(9, f.save("a09-watershed"), "តាមដានលំហូរច្រាសទិស",
          ["អាងរងទឹក = គ្រប់ក្រឡាដែលលំហូររបស់វាឆ្លងកាត់ចំណុចចេញ។", "ក្នុង QGIS/GRASS/WhiteboxTools យើងកំណត់ចំណុចចេញ ហើយគណនាអាង។ ក្នុង Earth Engine ភាគច្រើនប្រើ HydroBASINS ដែលគណនារួច។",
           "អាងរងជាអង្គភាពល្អសម្រាប់ស្ថិតិ (មេរៀនទី៤)៖ ទឹកភ្លៀងមធ្យម ផ្ទៃព្រៃ ផ្ទៃទឹកជំនន់។"], .75)
    # 6 HydroBASINS nesting
    f = Fig(1000, 440).title("HydroBASINS៖ អាងរងជាកម្រិត", "Pfafstetter · កម្រិតកាន់តែខ្ពស់ អាងកាន់តែតូច")
    for k, (lvl, cnt, col) in enumerate([(4, "មេគង្គទាំងមូល", "#c5e1a5"), (5, "មេគង្គក្រោម", "#9ccc65"), (6, "ទន្លេសាប", "#7cb342"), (7, "ស្ទឹងមួយៗ", "#558b2f"), (8, "អាងរងតូចៗ", "#33691e")]):
        w = 880 - k * 150; f.rect(60 + k * 75, 90 + k * 50, w, 280 - k * 50, col, "#fff", 2, 12)
        f.text(80 + k * 75, 118 + k * 50, f"hybas_{lvl} · {cnt}", 15, "#fff" if k > 1 else INK, weight="bold")
    f.text(500, 420, "ID៖ WWF/HydroSHEDS/v1/Basins/hybas_1 … hybas_12", 14, INK, "middle", extra='font-family="monospace"')
    entry(9, f.save("a09-hybas"), "ជ្រើសកម្រិតតាមមាត្រដ្ឋានសំណួរ",
          ["កម្រិត ៤–៥ សម្រាប់អាងទន្លេធំ (មេគង្គ)។ កម្រិត ៦–៨ សម្រាប់ទន្លេសាប និងស្ទឹងក្នុងខេត្ត។", "អាងនីមួយៗមាន HYBAS_ID និង NEXT_DOWN សម្រាប់តាមដានលំហូរពីអាងមួយទៅអាងមួយ។",
           "ព្រំអាងពី DEM ៩០ ម អាចខុសនៅវាលទំនាបរាបស្មើ ជាពិសេសជុំវិញទន្លេសាប។"], .85)
    # 7 HAND concept + synthetic profile
    xs = np.linspace(0, 1, 200); ground = 12 + 30 * xs ** 1.5 + 3 * np.sin(xs * 25) * xs; ch = [(0.08, 11.5), (0.55, 24)]
    f = Fig(1000, 440).title("HAND៖ កម្ពស់ពីលើប្រឡាយទឹកជិតបំផុត", "ផ្នែកកាត់ក្លែងធ្វើ · MERIT/Hydro/v1_0_1 band 'hnd'")
    X, Y = chart(f, 80, 90, 820, 270, [(list(xs), list(ground), "#6d4c41", "ផ្ទៃដី", 3)], (0, 1), (0, 50), "ចម្ងាយ", "កម្ពស់ (ម)", yt=[0, 10, 20, 30, 40, 50], legend=False)
    for cx, cz in ch: f.circle(X(cx), Y(cz), 8, "#1e88e5", "#fff", 2); f.text(X(cx), Y(cz) + 26, "ប្រឡាយ", 12, "#1e88e5", "middle", "bold")
    for px in (.3, .8):
        gz = float(np.interp(px, xs, ground)); near = min(ch, key=lambda c: abs(c[0] - px)); f.line(X(px), Y(gz), X(px), Y(near[1]), "#ef6c00", 2.5, arrow=True)
        f.line(X(px) - 30, Y(near[1]), X(px) + 30, Y(near[1]), "#1e88e5", 1, "4 3"); f.text(X(px) + 8, (Y(gz) + Y(near[1])) / 2, f"HAND ≈ {kh(round(gz - near[1]))} ម", 14, "#ef6c00", weight="bold")
    f.text(80, 425, "HAND < ៥ ម = ងាយលិចទឹក · HAND > ១៥ ម = កម្ររងទឹកជំនន់ទន្លេ", 15, INK)
    entry(9, f.save("a09-hand"), "មិនមែនកម្ពស់ពីនីវ៉ូសមុទ្រទេ",
          ["ទីតាំងខ្ពស់ ៤០ ម ពីនីវ៉ូសមុទ្រ អាចលិចទឹក ប្រសិនបើវាខ្ពស់ត្រឹម ២ ម ពីទន្លេជិតបំផុត។", "HAND ធ្វើឲ្យកម្ពស់ប្រៀបធៀបបានពេញអាងទន្លេ៖ ល្អសម្រាប់ផែនទីហានិភ័យ និង mask ទឹកជំនន់ (មេរៀនទី៧)។",
           "MERIT Hydro មាន HAND រួចជាស្រេច (band hnd) នៅ ៩០ ម។"], .95)
