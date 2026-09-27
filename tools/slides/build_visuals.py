"""Generate Book 4 figures (docs/assets/svg/agv) and tools/slides/visuals.json.

    python tools/slides/build_visuals.py            # every group whose data is available
    python tools/slides/build_visuals.py L04 L05     # only these groups

Groups: L01 L02 L03 (need the real imagery in $RS_REALDATA), L04–L09 (bundled or synthetic data),
LABS (workflow diagrams from src/lab-XX.md). Entries of groups that are not rebuilt are
kept from the existing visuals.json, so a partial rebuild never loses figures.
Lesson 6 figures also need scikit-learn (pip install scikit-learn).
"""
import json, os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import vis_core
GROUPS = {"L01": ("vis_ag1", 1), "L02": ("vis_ag1", 2), "L03": ("vis_ag1", 3),
          "L04": ("vis_ag2", 4), "L05": ("vis_ag2", 5), "L06": ("vis_ag2", 6), "L07": ("vis_ag3", 7), "L08": ("vis_ag3", 8), "L09": ("vis_ag3", 9), "LABS": ("vis_ag_labs", None)}
MAN = os.path.join(HERE, "visuals.json")
old = json.load(open(MAN, encoding="utf-8")) if os.path.exists(MAN) else []
want = sys.argv[1:] or list(GROUPS)
done = []
for g in want:
    mod, _ = GROUPS[g]
    try:
        getattr(importlib.import_module(mod), g)(); done.append(g)
    except Exception as e:
        print(f"skip {g}: {type(e).__name__}: {e}")
rebuilt_lessons = {GROUPS[g][1] for g in done if GROUPS[g][1]}
keep = [v for v in old if not (v.get("lesson") in rebuilt_lessons and "file" in v) and not ("LABS" in done and "lab" in v)]
new = keep + vis_core.MANIFEST
new.sort(key=lambda v: (v.get("lesson") or 99, v.get("lab") or 0))
json.dump(new, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rebuilt", " ".join(done) or "nothing", "·", len(new), "figures in visuals.json")
