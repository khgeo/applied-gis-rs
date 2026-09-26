"""Generate Book 4 figures (docs/assets/svg/agv) and tools/slides/visuals.json."""
import json, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vis_core
for m, fns in [("vis_ag1", ["L01", "L02", "L03"]), ("vis_ag_labs", ["LABS"])]:
    mod = importlib.import_module(m)
    for fn in fns: getattr(mod, fn)()
json.dump(vis_core.MANIFEST, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "visuals.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(vis_core.MANIFEST), "figures")
