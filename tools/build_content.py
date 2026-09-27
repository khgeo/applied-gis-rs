"""Render src/*.md → docs/lessons and docs/workbook.
{{FIG:name}}  → numbered figure + "អានរូបនេះ" note (from tools/slides/visuals.json)
{{WORKFLOW}}  → the lab's workflow diagram
{{EXPECT}}    → expected results (figures) + common errors table
Run tools/slides/build_visuals.py first when figures change."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SRC = os.path.join(ROOT, "src"); DOCS = os.path.join(ROOT, "docs")
KM = "០១២៣៤៥៦៧៨៩"; kh = lambda n: "".join(KM[int(c)] for c in str(n))
V = json.load(open(os.path.join(ROOT, "tools", "slides", "visuals.json"), encoding="utf-8"))
BY = {os.path.basename(v["file"])[:-4]: v for v in V}
EXPECT = {1: ["a01-first-script", "a01-scene-count"], 2: ["a02-map-loop", "a02-errors"], 3: ["a03-reducers", "a03-qa"],
          4: ["a04-regions", "a04-scale"], 5: ["a05-monthly", "a05-harmonic"], 6: ["a06-confusion", "a06-map"],
          7: ["a07-otsu", "a07-change"], 8: ["a08-spi", "a08-vci"], 9: ["a09-flowacc", "a09-watershed"],
          10: ["a10-lossyear", "a10-protected"], 11: ["a11-rules", "a11-vh"], 12: ["a12-lst-ndvi", "a12-uhi"]}
ERR = {
 1: [("ផែនទីទទេ ក្រោយចុច Run", "គ្មានរូបភាពត្រូវនឹងតម្រង", "print(col.size()) · ពង្រីកកាលបរិច្ឆេទ"), ("រូបភាពស ឬខ្មៅទាំងស្រុង", "min/max ខុស", "L2A៖ min 0 · max 3000"), ("GAUL រកខេត្តមិនឃើញ", "អក្ខរាវិរុទ្ធខុសពី GAUL", "print aggregate_array('ADM1_NAME')"), ("Not signed up / project error", "មិនទាន់ភ្ជាប់គម្រោង Cloud", "ធ្វើតាមឧបសម្ព័ន្ធ ក")],
 2: [("normalizedDifference: band not found", "ឈ្មោះក្រុមរលកខុសតាមឧបករណ៍", "Sentinel-2៖ B8 B4 · Landsat C2៖ SR_B5 SR_B4"), ("if មិនដំណើរការលើ ee.Number", "ប្រៀបធៀបលើ client", "n.gt(50) · ee.Algorithms.If"), ("map() ត្រឡប់ collection ទទេ", "ភ្លេច return", "ត្រូវ return img ជានិច្ច"), ("require() error", "ផ្លូវស្គ្រីបខុស ឬគ្មាន exports", "exports.addNDVI = addNDVI")],
 3: [("Composite នៅមានស្នាមពពក", "SCL ខកពពកស្ដើង", "ប្រើ Cloud Score+ (cs_cdf ≥ ០,៦)"), ("ចន្លោះគ្មានទិន្នន័យ (ខ្មៅ)", "រដូវវស្សា ឬតម្រងតឹងពេក", "ពង្រីករយៈពេល · CLOUDY < ៤០–៦០%"), ("Export បរាជ័យ maxPixels", "តំបន់ធំ × ក្រឡា ១០ ម", "maxPixels: 1e10 · ឬ scale 20"), ("ពណ៌ខុសក្នុង QGIS", "ប្រភេទទិន្នន័យ ឬ stretch", "toFloat() · stretch ២–៩៨%")],
 4: [("Too many pixels in the region", "maxPixels លំនាំដើមតូចពេក", "maxPixels: 1e10 · tileScale: 4"), ("User memory limit exceeded", "tile ធំពេកសម្រាប់អង្គចងចាំ", "tileScale: 8 ឬ 16 · ឬ Export"), ("stats.get('NDVI') = null", "ឈ្មោះគន្លឹះប្ដូរ ក្រោយ combine", "ប្រើ 'NDVI_mean' · print(stats) មុន"), ("CSV ធំ មានជួរឈរ .geo", "គ្មាន selectors", "selectors: ['ADM1_NAME', 'mean']"), ("ជួរខ្លះក្នុង QGIS គ្មានតម្លៃក្រោយ join", "អក្ខរាវិរុទ្ធឈ្មោះខេត្តខុសគ្នា", "join តាមកូដ ឬកែឈ្មោះក្នុង CSV")],
 5: [("Chart: No features contain non-null values", "ចំណុចលើក្រឡាដែលបាន mask ឬខុសតំបន់", "ពិនិត្យកូអរដោនេ · s2.size()"), ("Image.select: band 'NDVI' not found", "ខែគ្មានរូបភាព៖ median() គ្មានក្រុមរលក", "ee.Algorithms.If ជាមួយរូបភាពទទេ"), ("ក្រាបគ្មានអ័ក្សពេលវេលា", "បាត់ system:time_start", "copyProperties · set('system:time_start')"), ("Computation timed out (ក្រាប)", "តំបន់ធំ ឬរយៈពេលវែងពេក", "ប្រើចំណុច ឬ Export.table"), ("Harmonic ឡើងចុះខុសប្រក្រតី", "លំដាប់ខ្ពស់ពេក · ទិន្នន័យតិច", "ប្រើលំដាប់ ១–២ · ពិនិត្យ count")],
 6: [("sampleRegions ត្រឡប់ជួរតិចជាងចំណុច", "ចំណុចលើក្រឡាដែលបាន mask", "ពិនិត្យ size() · ផ្លាស់ចំណុច"), ("Property 'landcover' of feature ... is missing", "ស្រទាប់ចំណុចមួយគ្មានលក្ខណៈ landcover", "⚙ Import as FeatureCollection + property"), ("Only one class", "landcover ជាអក្សរ ឬចំណុចតែមួយថ្នាក់", "landcover ជាលេខ ០–៤ · aggregate_histogram"), ("OA ខ្ពស់ពេកមិនគួរជឿ", "ចំណុចផ្ទៀងផ្ទាត់ត្រួត ឬជិតចំណុចបណ្ដុះបណ្ដាល", "lt(0.7) និង gte(0.7) · បំបែកមុន sampleRegions"), ("slope ពេញដោយតម្លៃខុស", "DEM mosaic បាត់ projection", "setDefaultProjection(alos.first().projection())")],
 7: [("កម្រិត Otsu ចេញក្រៅ −២៥ ដល់ −១០ dB", "AOI គ្មានទឹក ឬគ្មានដីគ្រប់គ្រាន់", "ជ្រើស AOI ជុំវិញគែមទឹក · ពិនិត្យអ៊ីស្តូក្រាម"), ("ឆ្នូតភ្លឺ/ងងឹតត្រង់ព្រំរូបភាព", "លាយគន្លង ឬមុំខុសគ្នា", "ត្រង orbitProperties_pass · relativeOrbitNumber_start"), ("ទឹកជំនន់រាយប៉ាយលើភ្នំ", "ស្រមោលរ៉ាដា", "mask slope < ៥ · HAND < ១៥"), ("ទន្លេរាប់ជាទឹកជំនន់", "គ្មាន mask ទឹកអចិន្ត្រៃយ៍", "JRC seasonality ≥ ១០ · unmask(0)"), ("ព្រៃលិចទឹកមិនត្រូវបានរកឃើញ", "ចាំងពីរដង (ភ្លឺ)", "កត់ត្រាជាដែនកំណត់ · ពិនិត្យ VH")],
 8: [("ទឹកភ្លៀងខែ ≈ ៥–១០ mm គ្រប់កន្លែង", "ប្រើ mean() ជំនួស sum()", "sum() សម្រាប់ទឹកភ្លៀងសរុប"), ("Computation timed out", "climatology ៣០ ឆ្នាំប្រចាំថ្ងៃ", "CHIRPS/PENTAD · ឬ Export"), ("VCI < ០ ឬ > ១០០", "min/max ពីពពក ឬតម្លៃលើស", "percentile ៥/៩៥ · clamp(0, 100)"), ("VHI មានចន្លោះធំ", "LST គ្មាននៅពេលពពក", "ប្រើរយៈពេលវែងជាង · កត់ត្រាដែនកំណត់"), ("ខេត្តខ្លះ SPI3 = null", "mask ដំណាំតឹងពេក", "ពិនិត្យ crop mask · បន្ថយកម្រិត ៥០%")],
 9: [("ជម្រាលស្ទើរសូន្យគ្រប់កន្លែង", "mosaic គ្មាន projection", "setDefaultProjection('EPSG:4326', null, 30)"), ("ប្រឡាយច្រើនពេក", "កម្រិត upa តូចពេក", "បង្កើនកម្រិត · ប្រៀបធៀប HydroRIVERS"), ("អាងរងលើសព្រំខេត្តច្រើន", "filterBounds យកអាងដែលប៉ះ", "ទទួលយក ឬ filter ដោយ centroid"), ("area_km2 ខុសពី SUB_AREA", "ធរណីមាត្រសាមញ្ញ vs ពិត", "ភាពខុសតិចតួចទទួលយកបាន · រាយការណ៍ប្រភព"), ("Export SHP បរាជ័យ", "ឈ្មោះលក្ខណៈវែង > ១០ តួ", "ប្រើឈ្មោះខ្លី ឬ GeoJSON")],
 10: [("Too many pixels · timed out", "ប្រទេសទាំងមូលនៅ ៣០ ម", "Export · maxPixels: 1e13 · tileScale: 16"), ("rate30 ធំជាង ១០០", "loss មិនត្រូវបាន mask ដោយព្រៃ ២០០០", "loss.and(treecover2000.gte(30))"), ("WDPA ត្រងមិនឃើញឈ្មោះ", "អក្ខរាវិរុទ្ធ NAME ខុស", "print(aggregate_array('NAME'))"), ("buffer យឺតខ្លាំង", "ធរណីមាត្រស្មុគស្មាញ", "buffer(10000, 100) · maxError"), ("ក្រាបតាមឆ្នាំទទេ", "groups មិនបានបម្លែងជា Feature", "ee.List(g.get('groups')).map(...)")],
 11: [("ក្រាប VH លោតខ្លាំង", "speckle · ចំណុចតែមួយក្រឡា", "focalMedian · buffer(50)"), ("min() បរាជ័យ band not found", "ចន្លោះ ១២ ថ្ងៃគ្មានរូបភាព", "ee.Algorithms.If ជាមួយរូបភាពទទេ"), ("បឹងរាប់ជាស្រែ", "rise តូចពេក ឬគ្មាន mask ទឹក", "បង្កើន T_RISE · JRC seasonality"), ("toBands ឈ្មោះចម្លែក (0_VH …)", "ឈ្មោះលំនាំដើមនៃ toBands", "rename(names)"), ("OA ខ្ពស់ពេក", "ចំណុចផ្ទៀងផ្ទាត់ប្រើកែកម្រិតផង", "បំបែក cal / val មុន")],
 12: [("LST ≈ ៤០០០០ ឬ −២៧៣", "ភ្លេចមាត្រដ្ឋាន ST_B10", "× 0.00341802 + 149 − 273.15"), ("ចំណុចត្រជាក់ខុសប្រក្រតី", "ពពកមិនបាន mask", "QA_PIXEL bits 1 3 4"), ("ជម្រាល LST–NDVI វិជ្ជមាន", "ទឹកនៅក្នុងសំណាក", "updateMask(wc.neq(80))"), ("pop = null", "ឈ្មោះក្រុមរលក WorldPop", "values().get(0)"), ("GHSL image not found", "ឈ្មោះយុគខុស", "ប្រើ ១៩៧៥ … ២០៣០ រៀងរាល់ ៥ ឆ្នាំ")]}
def figblock(name, caption=None):
    v = BY[name]; b = "\n".join(f"    - {x}" for x in v["bullets"])
    return f'<figure markdown>\n--8<-- "{v["file"]}"\n<figcaption>រូបទី០.០៖ {caption or v["title"]}។</figcaption>\n</figure>\n\n!!! note "អានរូបនេះ"\n{b}\n'
def render(kind, fn):
    s = open(os.path.join(SRC, fn), encoding="utf-8").read(); n = int(re.search(r"(\d\d)", fn).group(1))
    s = re.sub(r"\{\{FIG:([\w-]+)\}\}", lambda m: figblock(m.group(1)), s)
    if kind == "lab":
        s = s.replace("{{WORKFLOW}}", f'<figure markdown>\n--8<-- "{BY[f"lab{n:02d}-workflow"]["file"]}"\n<figcaption>លំដាប់ការងារនៃលំហាត់ទី{kh(n)} និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>\n</figure>\n')
        exp = "## លទ្ធផលដែលរំពឹងទុក\n\nប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។\n\n"
        for i, name in enumerate(EXPECT.get(n, []), 1):
            v = BY[name]; exp += f'<figure markdown>\n--8<-- "{v["file"]}"\n<figcaption>លទ្ធផលគំរូ {kh(i)}៖ {v["title"]}។</figcaption>\n</figure>\n\n!!! tip "អ្វីដែលត្រូវពិនិត្យ"\n' + "".join(f"    - {x}\n" for x in v["bullets"]) + "\n"
        exp += "## កំហុសទូទៅ និងដំណោះស្រាយ\n\n| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |\n|---|---|---|\n" + "".join(f"| {a} | {b} | {c} |\n" for a, b, c in ERR.get(n, []))
        s = s.replace("{{EXPECT}}", exp)
    k = [0]
    def num(m): k[0] += 1; return f"<figcaption>រូបទី{kh(n)}.{kh(k[0])}៖"
    if kind == "lesson": s = re.sub(r"<figcaption>រូបទី០\.០៖", num, s)
    else: s = s.replace("<figcaption>រូបទី០.០៖ ", "<figcaption>")
    out = os.path.join(DOCS, "lessons" if kind == "lesson" else "workbook", fn)
    if kind == "lesson":
        s = re.sub(r"(!!! info \"ព័ត៌មានមេរៀន\"\n    .+\n)", r"\1\n" + f'[:material-presentation-play: ស្លាយបង្រៀនមេរៀននេះ](../slides/lesson-{n:02d}.html){{ .md-button target="_blank" }}\n', s, 1)
    open(out, "w", encoding="utf-8").write(s); return k[0]
for fn in sorted(os.listdir(SRC)):
    if fn.startswith("lesson-"): print(fn, render("lesson", fn), "figures")
    elif fn.startswith("lab-"): render("lab", fn); print(fn, "ok")
