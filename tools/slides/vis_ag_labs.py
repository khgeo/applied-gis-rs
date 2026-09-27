from vis_core import *
import re, os
SRC = os.path.join(ROOT, "src")
def LABS():
    for fn in sorted(os.listdir(SRC)):
        m = re.match(r"lab-(\d\d)\.md", fn)
        if not m: continue
        n = int(m.group(1)); s = open(os.path.join(SRC, fn), encoding="utf-8").read()
        title = re.search(r"^# (.+)$", s, re.M).group(1).split("៖", 1)[-1].strip()
        acts = re.findall(r"^## សកម្មភាពទី[០-៩]+៖ (.+?) · (.+)$", s, re.M)
        f = Fig(1000, 330).title(f"លំដាប់ការងារ លំហាត់ទី{kh(n)}", title)
        k = len(acts); w = (940 - (k - 1) * 18) / max(1, k)
        for i, (a, b) in enumerate(acts):
            x = 30 + i * (w + 18); c = ["#a5d6a7", "#81c784", "#66bb6a", "#43a047", "#2e7d32", "#1b5e20"][i % 6]
            f.rect(x, 110, w, 120, c, rx=12); f.text(x + w / 2, 164, a if len(a) < 26 else a[:24] + "…", 15, "#fff" if i > 1 else INK, "middle", "bold"); f.text(x + w / 2, 192, b, 13, "#fff" if i > 1 else INK, "middle")
            if i < k - 1: f.line(x + w + 1, 170, x + w + 16, 170, "#607d8b", 2, arrow=True)
        tot = sum(int("".join(str(KM.index(c)) for c in re.findall("[០-៩]", b)) or 0) for a, b in acts)
        f.text(500, 290, f"សរុបប្រហែល {kh(tot)} នាទី" if all("នាទី" in b for a, b in acts) else "គម្រោង ៤–៦ សប្ដាហ៍", 15, "#607d8b", "middle")
        MANIFEST.append(dict(lab=n, file=f.save(f"lab{n:02d}-workflow"), title=f"លំដាប់ការងារ លំហាត់ទី{kh(n)}", bullets=[a for a, b in acts]))
