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
EXPECT = {1: ["a01-first-script", "a01-scene-count"], 2: ["a02-map-loop", "a02-errors"], 3: ["a03-reducers", "a03-qa"]}
ERR = {
 1: [("ផែនទីទទេ ក្រោយចុច Run", "គ្មានរូបភាពត្រូវនឹងតម្រង", "print(col.size()) · ពង្រីកកាលបរិច្ឆេទ"), ("រូបភាពស ឬខ្មៅទាំងស្រុង", "min/max ខុស", "L2A៖ min 0 · max 3000"), ("GAUL រកខេត្តមិនឃើញ", "អក្ខរាវិរុទ្ធខុសពី GAUL", "print aggregate_array('ADM1_NAME')"), ("Not signed up / project error", "មិនទាន់ភ្ជាប់គម្រោង Cloud", "ធ្វើតាមឧបសម្ព័ន្ធ ក")],
 2: [("normalizedDifference: band not found", "ឈ្មោះក្រុមរលកខុសតាមឧបករណ៍", "Sentinel-2៖ B8 B4 · Landsat C2៖ SR_B5 SR_B4"), ("if មិនដំណើរការលើ ee.Number", "ប្រៀបធៀបលើ client", "n.gt(50) · ee.Algorithms.If"), ("map() ត្រឡប់ collection ទទេ", "ភ្លេច return", "ត្រូវ return img ជានិច្ច"), ("require() error", "ផ្លូវស្គ្រីបខុស ឬគ្មាន exports", "exports.addNDVI = addNDVI")],
 3: [("Composite នៅមានស្នាមពពក", "SCL ខកពពកស្ដើង", "ប្រើ Cloud Score+ (cs_cdf ≥ ០,៦)"), ("ចន្លោះគ្មានទិន្នន័យ (ខ្មៅ)", "រដូវវស្សា ឬតម្រងតឹងពេក", "ពង្រីករយៈពេល · CLOUDY < ៤០–៦០%"), ("Export បរាជ័យ maxPixels", "តំបន់ធំ × ក្រឡា ១០ ម", "maxPixels: 1e10 · ឬ scale 20"), ("ពណ៌ខុសក្នុង QGIS", "ប្រភេទទិន្នន័យ ឬ stretch", "toFloat() · stretch ២–៩៨%")]}
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
