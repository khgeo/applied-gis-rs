from vis_core import *
from rs_chart import chart, bars
import numpy as np
from PIL import Image
import rs_data as R

def box(f, x, y, w, h, t, sub="", c=IND, fs=17):
    f.rect(x, y, w, h, c, rx=12); f.text(x + w / 2, y + h / 2 + (-4 if sub else 6), t, fs, "#fff", "middle", "bold")
    if sub: f.text(x + w / 2, y + h / 2 + 20, sub, 13, "#fff", "middle")
def code(f, x, y, w, lines, fs=15):
    f.rect(x, y, w, 24 + len(lines) * 22, "#263238", rx=8)
    for i, l in enumerate(lines): f.text(x + 16, y + 28 + i * 22, l, fs, "#80cbc4" if not l.strip().startswith("//") else "#a5d6a7", extra='font-family="monospace" xml:space="preserve"')

def L01():
    # 1 archive growth (illustrative)
    f = Fig(1000, 440).title("ទំហំបណ្ណសាររូបភាពផ្កាយរណបកើនលឿន", "ប្រហាក់ប្រហែល · Landsat + Sentinel (PB)")
    yrs = [2000, 2005, 2010, 2015, 2018, 2020, 2022, 2024]; pb = [.4, .8, 1.5, 4, 10, 18, 27, 40]
    bars(f, 60, 90, 880, 260, [kh(y) for y in yrs], pb, ["#a5d6a7"] * 4 + ["#43a047"] * 4, fmt=lambda v: kh(v) + " PB", horizontal=False)
    entry(1, f.save("a01-archive"), "ទិន្នន័យច្រើនពេកសម្រាប់កុំព្យូទ័រមួយ",
          ["តាំងពី Sentinel-2 (២០១៥) បណ្ណសារកើនឡើងលឿនជាងមុនច្រើន។", "១ PB = ១ លាន GB៖ មិនអាចទាញយកមកកុំព្យូទ័រផ្ទាល់ខ្លួនបានទេ។", "តួលេខជាលំដាប់ទំហំប្រហាក់ប្រហែល សម្រាប់បង្រៀន។"], .1)
    # 2 traditional vs cloud workflow
    f = Fig(1000, 440).title("លំហូរការងារបុរាណ ធៀបនឹងលើពពក")
    f.text(40, 105, "បុរាណ (QGIS)", 18, "#c62828", weight="bold")
    for i, (t, s) in enumerate([("ស្វែងរក", ""), ("ទាញយក", "GB–TB"), ("រក្សាទុក", "ថាសរឹង"), ("ដំណើរការ", "កុំព្យូទ័រមួយ"), ("លទ្ធផល", "")]):
        box(f, 40 + i * 188, 120, 170, 80, t, s, ["#ef9a9a", "#e57373", "#ef5350", "#e53935", "#c62828"][i]); i < 4 and f.line(212 + i * 188, 160, 226 + i * 188, 160, "#607d8b", 2, arrow=True)
    f.text(40, 265, "លើពពក (Earth Engine)", 18, IND, weight="bold")
    for i, (t, s) in enumerate([("សរសេរកូដ", "កម្មវិធីរុករក"), ("ម៉ាស៊ីនមេ Google", "ទិន្នន័យ + គណនា"), ("លទ្ធផល", "ផែនទី · តារាង")]):
        box(f, 40 + i * 315, 280, 290, 80, t, s, ["#81c784", "#43a047", "#2e7d32"][i]); i < 2 and f.line(332 + i * 315, 320, 352 + i * 315, 320, "#607d8b", 2, arrow=True)
    entry(1, f.save("a01-workflows"), "នាំកូដទៅកន្លែងទិន្នន័យ",
          ["លំហូរបុរាណ ចំណាយពេលភាគច្រើនលើការទាញយក និងរក្សាទុក។", "Earth Engine រក្សាទិន្នន័យ និងគណនានៅកន្លែងតែមួយ។", "យើងទាញយកតែលទ្ធផលតូចៗ៖ ផែនទី តារាង ឬក្រាប។"], .2)
    # 3 GEE architecture
    f = Fig(1000, 460).title("ផ្នែកសំខាន់ៗនៃ Google Earth Engine")
    box(f, 40, 90, 280, 120, "កាតាឡុកទិន្នន័យ", "៩០+ PB · Landsat Sentinel MODIS...", "#1b5e20")
    box(f, 360, 90, 280, 120, "ម៉ាស៊ីនគណនា", "ម៉ាស៊ីនមេរាប់ពាន់ · ស្របគ្នា", "#2e7d32")
    box(f, 680, 90, 280, 120, "API", "JavaScript · Python", "#388e3c")
    box(f, 40, 290, 280, 120, "Code Editor", "សរសេរ រត់ មើលផែនទី", "#ef6c00"); box(f, 360, 290, 280, 120, "Earth Engine Apps", "ចែករំលែកជាគេហទំព័រ", "#f57c00"); box(f, 680, 290, 280, 120, "នាំចេញ", "Drive · Asset · Cloud Storage", "#fb8c00")
    for x in (180, 500, 820): f.line(x, 212, x, 286, "#90a4ae", 2, arrow=True)
    entry(1, f.save("a01-architecture"), "Earth Engine មានអ្វីខ្លះ",
          ["កាតាឡុក៖ ទិន្នន័យដែលរៀបចំរួច (រួមទាំង L2A Landsat C2 CHIRPS SRTM)។", "Code Editor៖ កន្លែងសរសេរ JavaScript ក្នុងកម្មវិធីរុករក។", "Apps និងការនាំចេញ៖ ផ្លូវចែករំលែកលទ្ធផលទៅអ្នកដទៃ។"], .35)
    # 4 Code Editor layout mockup
    f = Fig(1000, 520).title("ផ្ទៃ Code Editor")
    f.rect(40, 80, 920, 420, "#fafafa", "#b0bec5", 1.5, 8)
    f.rect(50, 90, 230, 190, "#e8f5e9", "#a5d6a7"); f.text(165, 190, "Scripts · Docs · Assets", 15, IND, "middle", "bold")
    f.rect(290, 90, 380, 190, "#263238"); f.text(480, 190, "កន្លែងសរសេរកូដ", 16, "#80cbc4", "middle", "bold")
    f.rect(680, 90, 270, 190, "#fff3e0", "#ffcc80"); f.text(815, 190, "Inspector · Console · Tasks", 15, AMB, "middle", "bold")
    try:
        f.img(R.rgb(R.shv(2021)[3], R.shv(2021)[2], R.shv(2021)[1]), 50, 290, 900, 200)
    except Exception: f.rect(50, 290, 900, 200, "#c8e6c9")
    f.text(500, 400, "ផែនទី (Map)", 22, "#fff", "middle", "bold", 'stroke="#000" stroke-width="3" paint-order="stroke"')
    entry(1, f.save("a01-code-editor"), "ស្គាល់ Code Editor",
          ["ខាងឆ្វេង៖ ស្គ្រីបរបស់អ្នក ឯកសារ API និង Assets។", "កណ្ដាល៖ សរសេរកូដ ហើយចុច Run។ ខាងស្ដាំ៖ Console (print) Inspector (ចុចលើផែនទី) និង Tasks (នាំចេញ)។", "ខាងក្រោម៖ ផែនទីសម្រាប់ Map.addLayer()។"], .5)
    # 5 scenes over Cambodia per year (computation)
    f = Fig(1000, 420).title("រូបភាព Sentinel-2 ប៉ុន្មានផ្ទាំងលើកម្ពុជា?", "ប្រហាក់ប្រហែល · ~៣០ tile × ~៧៣ ថ្ងៃ/ឆ្នាំ")
    vals = [30 * 73 * y for y in (1, 2, 5, 10)]; bars(f, 80, 100, 820, 240, ["១ ឆ្នាំ", "២ ឆ្នាំ", "៥ ឆ្នាំ", "១០ ឆ្នាំ"], vals, ["#a5d6a7", "#66bb6a", "#43a047", "#1b5e20"], fmt=lambda v: khn(v) + " ផ្ទាំង", lw=120)
    entry(1, f.save("a01-scene-count"), "ចំនួនរូបភាពនៅកម្ពុជា",
          ["មួយឆ្នាំមានរូបភាព Sentinel-2 ជាង ២ ០០០ ផ្ទាំងលើកម្ពុជា។", "Composite មួយ ឬស៊េរីពេលវេលា អាចប្រើរូបភាពរាប់ពាន់ក្នុងការគណនាតែមួយ។", "នេះជាហេតុផលចម្បងដែលវគ្គនេះប្រើ Earth Engine។"], .15)
    # 6 strengths and limits
    f = Fig(1000, 440).title("ចំណុចខ្លាំង និងដែនកំណត់នៃ Earth Engine")
    f.rect(40, 90, 440, 320, "#e8f5e9", "#81c784", 2, 12); f.text(260, 125, "✓ ចំណុចខ្លាំង", 20, "#2e7d32", "middle", "bold")
    for i, t in enumerate(["ទិន្នន័យរៀបចំរួច", "គណនាលឿនលើតំបន់ធំ", "ឥតគិតថ្លៃសម្រាប់ការសិក្សា", "កូដចែករំលែកបានតាមតំណ", "កម្មវិធីវេបងាយ"]): f.text(70, 170 + i * 44, "• " + t, 17)
    f.rect(520, 90, 440, 320, "#fff3e0", "#ffb74d", 2, 12); f.text(740, 125, "! ដែនកំណត់", 20, "#e65100", "middle", "bold")
    for i, t in enumerate(["ត្រូវការអ៊ីនធឺណិត", "កំណត់ពេល និងអង្គចងចាំ", "ក្បួនដោះស្រាយមានកំណត់", "ពឹងលើក្រុមហ៊ុនមួយ", "លក្ខខណ្ឌប្រើពាណិជ្ជកម្ម"]): f.text(550, 170 + i * 44, "• " + t, 17)
    entry(1, f.save("a01-pros-cons"), "ប្រើ Earth Engine ពេលណា",
          ["ល្អសម្រាប់តំបន់ធំ រយៈពេលវែង និងទិន្នន័យដែលមានក្នុងកាតាឡុក។", "QGIS នៅតែល្អជាងសម្រាប់ការកែសម្រួលវ៉ិចទ័រ ប្លង់ផែនទី និងទិន្នន័យក្នុងស្រុក។", "អ្នកជំនាញប្រើទាំងពីររួមគ្នា (មេរៀនទី១៣–១៤)។"], .85)
    # 7 hello world code + result
    f = Fig(1000, 420).title("ស្គ្រីបដំបូង")
    code(f, 40, 90, 560, ["// ផ្កាយរណប Sentinel-2 · ភ្នំពេញ · រដូវប្រាំង", "var img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')", "  .filterBounds(ee.Geometry.Point(104.92, 11.55))", "  .filterDate('2024-01-01', '2024-03-31')", "  .sort('CLOUDY_PIXEL_PERCENTAGE')", "  .first();", "Map.centerObject(img, 10);", "Map.addLayer(img, {bands:['B4','B3','B2'], min:0, max:3000});"], 14)
    try: f.img(R.rgb(R.toa(4)[400:1000, 400:1100], R.toa(3)[400:1000, 400:1100], R.toa(2)[400:1000, 400:1100]), 630, 90, 330, 280)
    except Exception: pass
    f.text(795, 395, "លទ្ធផល៖ ពណ៌ពិត (គំរូ)", 14, INK, "middle")
    entry(1, f.save("a01-first-script"), "ប្រាំបីបន្ទាត់ ជំនួសការទាញយក ១ GB",
          ["ImageCollection៖ បណ្ណសារទាំងមូល · filter៖ ជ្រើសតំបន់ និងកាលបរិច្ឆេទ។", "sort + first៖ យករូបភាពពពកតិចបំផុត។", "addLayer៖ Earth Engine គណនា និងបង្ហាញតែក្រឡាដែលអ្នកមើល។"], .65)

def L02():
    # client vs server
    f = Fig(1000, 440).title("ម៉ាស៊ីនភ្ញៀវ (client) និងម៉ាស៊ីនមេ (server)")
    box(f, 40, 110, 330, 230, "កម្មវិធីរុករករបស់អ្នក", "JavaScript ធម្មតា · var x = 5", "#ef6c00")
    box(f, 630, 110, 330, 230, "ម៉ាស៊ីនមេ Google", "ee.Image · ee.Number · ee.List", IND)
    f.line(375, 180, 625, 180, "#607d8b", 3, arrow=True); f.text(500, 168, "សំណើ (ពិពណ៌នាការគណនា)", 14, INK, "middle")
    f.line(625, 280, 375, 280, "#607d8b", 3, arrow=True); f.text(500, 305, "លទ្ធផល (ក្រឡាផែនទី · print)", 14, INK, "middle")
    f.text(500, 400, "វត្ថុ ee.* គ្រាន់តែជា «ការពិពណ៌នា» នៅក្នុងកម្មវិធីរុករក រហូតដល់ត្រូវការលទ្ធផល", 15, "#607d8b", "middle")
    entry(2, f.save("a02-client-server"), "ហេតុអ្វី if និង for ធម្មតាមិនដំណើរការលើ ee.Number",
          ["ee.Number(5) មិនមែនលេខ ៥ ក្នុងកម្មវិធីរុករកទេ៖ វាជាការណែនាំឲ្យម៉ាស៊ីនមេគណនា។", "ប្រើ .add() .gt() ee.Algorithms.If() ជំនួស + > និង if។", "print() និង Map.addLayer() ស្នើលទ្ធផលពីម៉ាស៊ីនមេ។"], .15)
    # object hierarchy
    f = Fig(1000, 440).title("ប្រភេទវត្ថុ Earth Engine")
    items = [("ee.Image", "រ៉ាស្ទ័រ · ក្រុមរលកច្រើន", "#2e7d32"), ("ee.ImageCollection", "បណ្ដុំរូបភាព", "#388e3c"), ("ee.Geometry", "ចំណុច បន្ទាត់ ពហុកោណ", "#ef6c00"), ("ee.Feature", "ធរណីមាត្រ + គុណលក្ខណៈ", "#f57c00"), ("ee.FeatureCollection", "ស្រទាប់វ៉ិចទ័រ", "#fb8c00"), ("ee.Reducer", "ស្ថិតិ", "#6d4c41"), ("ee.Number · ee.String · ee.List · ee.Date · ee.Dictionary", "ទិន្នន័យសាមញ្ញលើម៉ាស៊ីនមេ", "#546e7a")]
    for i, (a, b, c) in enumerate(items[:6]): box(f, 40 + (i % 3) * 315, 90 + (i // 3) * 120, 290, 100, a, b, c, 17)
    box(f, 40, 340, 920, 70, items[6][0], items[6][1], items[6][2], 15)
    entry(2, f.save("a02-objects"), "វត្ថុសំខាន់ៗ",
          ["រ៉ាស្ទ័រ៖ ee.Image (មួយ) និង ee.ImageCollection (ច្រើន)។", "វ៉ិចទ័រ៖ ee.Geometry → ee.Feature → ee.FeatureCollection (ដូចស្រទាប់ QGIS)។", "Reducer៖ បម្លែងតម្លៃច្រើនទៅជាស្ថិតិ (មេរៀនទី៤)។"], .3)
    # method chaining
    f = Fig(1000, 400).title("ការភ្ជាប់មុខងារ (method chaining)")
    steps = [("ImageCollection", "៥ លាន+"), (".filterBounds()", "~៧ ០០០"), (".filterDate()", "~២៥០"), (".filter(ពពក < ២០)", "~៨០"), (".median()", "១ រូបភាព")]
    for i, (a, b) in enumerate(steps): box(f, 30 + i * 192, 130, 175, 110, a, b, ["#a5d6a7", "#81c784", "#66bb6a", "#43a047", "#2e7d32"][i], 14); i < 4 and f.line(206 + i * 192, 185, 220 + i * 192, 185, "#607d8b", 2, arrow=True)
    f.text(500, 300, "មុខងារនីមួយៗ ត្រឡប់វត្ថុថ្មី ដែលមុខងារបន្ទាប់ប្រើបន្ត · លេខរូបភាពជាប្រហាក់ប្រហែល", 14, "#607d8b", "middle")
    entry(2, f.save("a02-chaining"), "អានកូដពីឆ្វេងទៅស្ដាំ",
          ["មុខងារនីមួយៗមិនប្ដូរវត្ថុដើមទេ៖ វាត្រឡប់វត្ថុថ្មី។", "ត្រងឲ្យបានច្រើនមុន (filterBounds filterDate) ទើបការគណនាលឿន។", "ចុងក្រោយ reducer (median) បម្លែងបណ្ដុំទៅជារូបភាពមួយ។"], .5)
    # map vs loop
    f = Fig(1000, 420).title("map() ជំនួស for loop")
    code(f, 40, 90, 440, ["// ✗ មិនដំណើរការលើម៉ាស៊ីនមេ", "for (var i = 0; i < col.size(); i++) {", "  var img = col.get(i);", "  ...", "}"], 14)
    code(f, 520, 90, 440, ["// ✓ map() ស្របគ្នា", "var withNdvi = col.map(function(img) {", "  var nd = img.normalizedDifference(['B8','B4']);", "  return img.addBands(nd.rename('NDVI'));", "});"], 14)
    f.text(260, 260, "col.size() ជា ee.Number មិនមែនលេខ JS", 14, "#c62828", "middle"); f.text(740, 260, "មុខងារត្រូវ return រូបភាព", 14, "#2e7d32", "middle")
    entry(2, f.save("a02-map-loop"), "គិតជា «អនុវត្តលើគ្រប់ធាតុ»",
          ["for loop ដំណើរការក្នុងកម្មវិធីរុករក ហើយមិនស្គាល់ទំហំពិតនៃ collection។", "map() ផ្ញើមុខងារទៅម៉ាស៊ីនមេ ដែលអនុវត្តលើធាតុនីមួយៗស្របគ្នា។", "ក្នុង map() មិនអាចប្រើ print() getInfo() ឬ Map.addLayer() បានទេ។"], .7)
    # filter-map-reduce pipeline
    f = Fig(1000, 380).title("គំរូ filter → map → reduce")
    for i, (a, b, c) in enumerate([("filter", "ជ្រើសតែអ្វីដែលត្រូវការ", "#43a047"), ("map", "គណនាលើធាតុនីមួយៗ", "#ef6c00"), ("reduce", "សង្ខេបជាលទ្ធផលមួយ", "#6d4c41")]): box(f, 60 + i * 310, 130, 260, 120, a, b, c, 22); i < 2 and f.line(322 + i * 310, 190, 366 + i * 310, 190, "#607d8b", 3, arrow=True)
    f.text(500, 320, "ស្គ្រីប Earth Engine ភាគច្រើនជាបន្សំនៃជំហានទាំងបី", 16, INK, "middle")
    entry(2, f.save("a02-fmr"), "លំនាំស្គ្រីប Earth Engine",
          ["filter៖ តំបន់ កាលបរិច្ឆេទ ពពក។", "map៖ លុបពពក គណនាសន្ទស្សន៍ កាត់តាមព្រំ។", "reduce៖ median ពេលវេលា ឬស្ថិតិតាមតំបន់។"], .85)
    # deferred execution
    f = Fig(1000, 380).title("ការគណនាពន្យារពេល (lazy evaluation)")
    lines = [("var col = ee.ImageCollection(...)", "គ្មានការគណនា"), ("var comp = col.median()", "គ្មានការគណនា"), ("var ndvi = comp.normalizedDifference(...)", "គ្មានការគណនា"), ("Map.addLayer(ndvi)", "គណនាឥឡូវ! តែក្រឡាដែលមើល")]
    for i, (a, b) in enumerate(lines):
        y = 100 + i * 60; f.rect(60, y, 560, 44, "#263238", rx=6); f.text(76, y + 28, a, 14, "#80cbc4", extra='font-family="monospace"'); f.text(660, y + 28, b, 16, "#c62828" if i == 3 else "#90a4ae", weight="bold" if i == 3 else "normal")
    entry(2, f.save("a02-lazy"), "Earth Engine គណនាតែពេលត្រូវការ",
          ["បន្ទាត់ var គ្រាន់តែបង្កើតផែនការ (graph) នៃការគណនា។", "ការគណនាពិតកើតឡើងពេល print Map.addLayer ឬ Export។", "នៅកម្រិត zoom ទាប Earth Engine គណនាលើក្រឡាធំ (pyramid) ដើម្បីលឿន។"], .4)
    # common errors
    f = Fig(1000, 440).title("កំហុសទូទៅក្នុង Code Editor")
    errs = [("Line 5: col.get is not a function", "ឈ្មោះមុខងារខុស ឬវត្ថុខុសប្រភេទ"), ("Collection query aborted after accumulating over 5000 elements", "print collection ធំពេក → ប្រើ .limit(10)"), ("User memory limit exceeded", "តំបន់ធំពេក → បង្កើន scale ឬ Export"), ("Computation timed out", "គណនាលើផែនទីយូរ → Export ជា Task"), ("Image.select: Pattern 'B8' did not match", "ឈ្មោះក្រុមរលកខុស (Landsat vs Sentinel)")]
    for i, (a, b) in enumerate(errs): y = 90 + i * 64; f.rect(40, y, 540, 50, "#ffebee", "#ef9a9a", 1, 6); f.text(56, y + 31, a, 13, "#c62828", extra='font-family="monospace"'); f.text(600, y + 31, b, 15)
    entry(2, f.save("a02-errors"), "អានសារកំហុស",
          ["សារកំហុសក្នុង Console ប្រាប់លេខបន្ទាត់ និងមូលហេតុ។", "កំហុសអង្គចងចាំ និងពេលវេលា ជាទូទៅដោះស្រាយដោយ Export ឬ scale ធំជាង។", "ឈ្មោះក្រុមរលកខុស ជាកំហុសញឹកញាប់បំផុតពេលប្ដូរពី Sentinel-2 ទៅ Landsat។"], .95)

def L03():
    s = R.shv(2021); base = [s[3], s[2], s[1]]
    rng = np.random.default_rng(4); H, W = s.shape[1:]
    yy, xx = np.mgrid[0:H, 0:W]
    stack, masks = [], []
    for t in range(6):
        cm = np.zeros((H, W))
        for k in range(3 + t % 3):
            cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(30, 90); cm = np.maximum(cm, np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) * 1.6)
        cm = np.clip(cm, 0, 1); masks.append(cm > .05)
        stack.append([b * (.95 + .1 * rng.random()) * (1 - cm) + (.45 + .1 * cm) * cm for b in base])
    toim = lambda bands: Image.fromarray(np.dstack([(np.clip(b / .2, 0, 1) * 255).astype(np.uint8) for b in bands]))
    # 1 six dates with simulated clouds
    f = Fig(1000, 470).title("រូបភាពប្រាំមួយកាលបរិច្ឆេទ (ពពកក្លែងធ្វើ)", "ក្រុងព្រះសីហនុ · Sentinel-2")
    for t in range(6): f.img(toim(stack[t]), 30 + (t % 3) * 320, 85 + (t // 3) * 185, 300, 170); f.text(180 + (t % 3) * 320, 85 + (t // 3) * 185 + 165, f"កាលបរិច្ឆេទ {kh(t+1)}", 13, "#fff", "middle", "bold", 'stroke="#000" stroke-width="3" paint-order="stroke"')
    entry(3, f.save("a03-dates"), "គ្មានរូបភាពណាមួយស្អាតទាំងស្រុង",
          ["រូបភាពនីមួយៗមានពពកនៅកន្លែងខុសៗគ្នា។", "ប៉ុន្តែក្រឡានីមួយៗ ត្រូវបានមើលឃើញស្អាតយ៉ាងហោចណាស់ម្ដង។", "Composite យកផ្នែកស្អាតពីរូបភាពផ្សេងៗ ផ្គុំជារូបភាពថ្មី។"], .5)
    # 2 composites comparison
    arr = np.array(stack)  # t, band, H, W
    med = np.median(arr, 0); mx = arr.max(0); first = arr[0]
    marr = np.where(np.array(masks)[:, None], np.nan, arr); mmed = np.nanmedian(marr, 0); mmed = np.where(np.isnan(mmed), med, mmed)
    f = Fig(1000, 440).title("Composite បួនបែប")
    for i, (a, t) in enumerate([(first, "first()"), (mx, "max()"), (med, "median()"), (mmed, "mask + median()")]): f.img(toim(list(a)), 20 + i * 245, 90, 225, 225); f.text(132 + i * 245, 345, t, 16, IND, "middle", "bold")
    f.text(500, 400, "median() ជៀសវាងពពកភាគច្រើន · mask មុនធ្វើឲ្យស្អាតជាង", 15, "#607d8b", "middle")
    entry(3, f.save("a03-reducers"), "ជ្រើស reducer សម្រាប់ composite",
          ["first() យករូបភាពមួយ ដូច្នេះពពករបស់វានៅដដែល។", "max() ជ្រើសពពក ព្រោះពពកភ្លឺជាងដី។", "median() + mask ផ្ដល់លទ្ធផលស្អាតបំផុតសម្រាប់តំបន់ត្រូពិច។"], .7)
    # 3 filter funnel
    f = Fig(1000, 420).title("ត្រងជាជំហាន", "ឧទាហរណ៍៖ Sentinel-2 L2A · ខេត្តកំពង់ឆ្នាំង · ២០២៤ (ប្រហាក់ប្រហែល)")
    steps = [("បណ្ណសារទាំងមូល", 6000000), ("filterBounds(ខេត្ត)", 1100), ("filterDate(២០២៤)", 290), ("ពពក < ២០%", 95), ("រដូវប្រាំង", 60)]
    for i, (t, v) in enumerate(steps):
        w = 880 * (math.log10(v) / math.log10(6e6)); x = 500 - w / 2; y = 90 + i * 58; f.rect(x, y, w, 46, ["#c8e6c9", "#a5d6a7", "#81c784", "#4caf50", "#2e7d32"][i], rx=8)
        f.text(500, y + 30, f"{t} · {khn(v)}", 15, INK if i < 3 else "#fff", "middle", "bold")
    entry(3, f.save("a03-funnel"), "ត្រងពីធំទៅតូច",
          ["filterBounds និង filterDate ធ្វើមុន ព្រោះវាថយចំនួនយ៉ាងលឿន។", "តម្រងពពកប្រើ metadata (CLOUDY_PIXEL_PERCENTAGE) នៃរូបភាពទាំងមូល។", "ពិនិត្យ .size() នៅជំហាននីមួយៗ ដើម្បីដឹងថានៅសល់ប៉ុន្មាន។"], .2)
    # 4 SCL / QA bits
    f = Fig(1000, 440).title("ការលុបពពកដោយ SCL (Sentinel-2) និង QA_PIXEL (Landsat)")
    scl = [("3", "ស្រមោលពពក", "#424242"), ("4", "រុក្ខជាតិ", "#43a047"), ("5", "ដីទទេ", "#bcaaa4"), ("6", "ទឹក", "#1e88e5"), ("8", "ពពកប្រូបាប៊ីលីតេមធ្យម", "#bdbdbd"), ("9", "ពពកប្រូបាប៊ីលីតេខ្ពស់", "#eeeeee"), ("10", "Cirrus", "#e1f5fe")]
    for i, (a, b, c) in enumerate(scl): y = 90 + i * 42; f.rect(40, y, 34, 32, c, "#9e9e9e"); f.text(90, y + 22, f"SCL = {kh(a)}", 14, INK, weight="bold"); f.text(190, y + 22, b, 14); f.text(420, y + 22, "✗ mask" if a in ("3", "8", "9", "10") else "✓ ទុក", 14, "#c62828" if a in ("3", "8", "9", "10") else "#2e7d32", weight="bold")
    bits = ["0 Fill", "1 Dilated", "2 Cirrus", "3 Cloud", "4 Shadow", "5 Snow", "6 Clear", "7 Water"]
    f.text(560, 100, "Landsat QA_PIXEL (ប៊ីត)", 16, IND, weight="bold")
    for i, b in enumerate(bits): x = 560 + (i % 4) * 100; y = 120 + (i // 4) * 60; f.rect(x, y, 92, 48, "#ffcdd2" if b.split()[0] in ("3", "4", "1", "2") else "#e8f5e9", "#9e9e9e", 1, 6); f.text(x + 46, y + 30, b, 13, INK, "middle")
    f.text(560, 290, "mask = bit 3 (cloud) ឬ bit 4 (shadow) = 1", 14, "#c62828")
    entry(3, f.save("a03-qa"), "ក្រុមរលកគុណភាពប្រាប់ពពក",
          ["Sentinel-2 L2A មានក្រុមរលក SCL ដែលចាត់ថ្នាក់ក្រឡានីមួយៗ។", "Landsat Collection 2 ប្រើប៊ីតក្នុង QA_PIXEL៖ ត្រូវប្រើ bitwiseAnd()។", "updateMask() ធ្វើឲ្យក្រឡាពពកក្លាយជា «គ្មានទិន្នន័យ» មុនធ្វើ composite។"], .4)
    # 5 time cube
    f = Fig(1000, 440).title("ImageCollection ជាគូបពេលវេលា")
    for t in range(6)[::-1]:
        x, y = 120 + t * 40, 110 + t * 30; f.img(toim(stack[t]).resize((240, 160)), x, y, 240, 160, extra='opacity=".95"'); f.rect(x, y, 240, 160, "none", "#fff", 2)
    f.line(470, 330, 700, 330, "#607d8b", 3, arrow=True); f.text(585, 318, "reducer តាមពេលវេលា", 14, INK, "middle")
    f.img(toim(list(mmed)).resize((240, 160)), 720, 250, 240, 160); f.text(840, 430, "រូបភាពមួយ", 14, IND, "middle", "bold")
    f.line(360, 150, 360, 300, "#ef6c00", 3, "4 3"); f.text(370, 145, "ក្រឡាមួយ = ស៊េរីតម្លៃ", 14, "#ef6c00", weight="bold")
    entry(3, f.save("a03-cube"), "Reducer ធ្វើការតាមក្រឡានីមួយៗ",
          ["នៅក្រឡានីមួយៗ មានតម្លៃមួយក្នុងរូបភាពនីមួយៗ៖ ស៊េរីពេលវេលា។", "median() យកតម្លៃកណ្ដាលនៃស៊េរីនោះ ដាច់ដោយឡែកក្នុងក្រុមរលកនីមួយៗ។", "ដូច្នេះ composite អាចលាយពណ៌ពីកាលបរិច្ឆេទខុសគ្នា ក្នុងក្រឡាជិតគ្នា។"], .6)
    # 6 median vs greenest pixel concept chart
    f = Fig(1000, 420).title("ស៊េរីក្រឡាមួយ៖ median ធៀបនឹង qualityMosaic", "តម្លៃក្រហម និង NDVI (គំរូ)")
    red = [.05, .42, .06, .07, .38, .05, .02, .06]; ndvi = [.55, .05, .6, .62, .08, .58, .1, .7]
    X, Y = chart(f, 100, 90, 620, 250, [(list(range(1, 9)), red, "#e53935", "ក្រហម", 3), (list(range(1, 9)), ndvi, "#2e7d32", "NDVI", 3)], (1, 8), (0, .8), "កាលបរិច្ឆេទ", "តម្លៃ", xt=list(range(1, 9)), yt=[0, .4, .8], lx=760, ly=120)
    f.line(X(1), Y(np.median(red)), X(8), Y(np.median(red)), "#e53935", 1.5, "5 4"); f.text(X(8) + 4, Y(np.median(red)) + 4, "median", 12, "#e53935")
    f.circle(X(8), Y(.7), 9, "none", "#2e7d32", 2.5); f.text(760, 220, "qualityMosaic ជ្រើស", 14); f.text(760, 244, "កាលបរិច្ឆេទ ៨ (NDVI ខ្ពស់បំផុត)", 14)
    entry(3, f.save("a03-quality"), "ក្បួនជ្រើសក្រឡាពីរបែប",
          ["កាលបរិច្ឆេទ ២ និង ៥ មានពពក (ក្រហមខ្ពស់ NDVI ទាប)។", "median តាមក្រុមរលក ជៀសវាងតម្លៃខ្ពស់ទាំងនោះដោយស្វ័យប្រវត្តិ។", "qualityMosaic យកកាលបរិច្ឆេទតែមួយដែលល្អបំផុតតាមលក្ខណៈវិនិច្ឆ័យ (ឧ. NDVI) ដូច្នេះក្រុមរលកស៊ីគ្នា។"], .85)
