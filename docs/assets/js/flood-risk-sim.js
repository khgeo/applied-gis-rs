/* ============================================================
   Book 4 · Lesson 13 · Flood risk = hazard × exposure × vulnerability
   Class grids decoded from the author's Flood Mapper v2.3 sample report (Battambang).
   Usage: <div class="sim" data-sim="ag-flood-risk"></div>
   ============================================================ */
(function () {
  "use strict";
  const KM = "០១២៣៤៥៦៧៨៩", kh = (n) => String(n).replace(/[0-9]/g, (d) => KM[d]);
  const khn = (n, d = 0) => kh(Number(n).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/,/g, " ").replace(".", ","));
  const DATA = new URL("../data/btb_risk.json", (document.currentScript && document.currentScript.src) || location.href);
  const PAL = ["#1b974f", "#a6d969", "#fde089", "#f56e42", "#a40125"], NAMES = ["ទាបខ្លាំង", "ទាប", "មធ្យម", "ខ្ពស់", "ខ្ពស់ខ្លាំង"];
  const font = () => getComputedStyle(document.body).fontFamily || "Battambang, sans-serif";
  window.EXTRA_SIMS = window.EXTRA_SIMS || {};
  window.EXTRA_SIMS["ag-flood-risk"] = async (el) => {
    const D = await (await fetch(DATA)).json(), w = D.w, h = D.h, N = w * h;
    const dec = (s) => { const a = new Int8Array(N); for (let i = 0; i < N; i++) a[i] = s.charCodeAt(i) === 46 ? -1 : s.charCodeAt(i) - 48; return a; };
    const L = { H: dec(D.H), E: dec(D.E), V: dec(D.V) }, idx = []; for (let i = 0; i < N; i++) if (L.H[i] >= 0 && L.E[i] >= 0 && L.V[i] >= 0) idx.push(i);
    el.innerHTML = `<div class="sim-title">ហានិភ័យទឹកជំនន់ ខេត្តបាត់ដំបង៖ គ្រោះ × ការប៉ះពាល់ × ភាពងាយរងគ្រោះ</div>
      <div class="sim-controls">
        <label>គ្រោះ (H) <input class="fr-wh" type="range" min="0" max="100" value="54"> <b class="fr-whv"></b></label>
        <label>ការប៉ះពាល់ (E) <input class="fr-we" type="range" min="0" max="100" value="30"> <b class="fr-wev"></b></label>
        <label>ភាពងាយរងគ្រោះ (V) <input class="fr-wv" type="range" min="0" max="100" value="16"> <b class="fr-wvv"></b></label>
      </div><div class="sim-controls">
        <span class="sim-seg fr-c"><button type="button" data-v="mul" class="on">គុណមានទម្ងន់ Hʷ·Eʷ·Vʷ</button><button type="button" data-v="prod">គុណសុទ្ធ H×E×V</button><button type="button" data-v="wlc">បូក (WLC)</button></span>
        <span class="sim-seg fr-k"><button type="button" data-v="fixed" class="on">កម្រិតថេរ ០,២ ០,៤ …</button><button type="button" data-v="quant">Quantile (ក្រឡាស្មើគ្នា)</button></span>
        <button type="button" class="sim-btn fr-r">AHP ដើម</button>
      </div>
      <div class="sim-body"><div class="sim-canvas-wrap"><canvas></canvas></div></div><div class="sim-out" role="status"></div>`;
    const q = (s) => el.querySelector(s), cv = q("canvas"), ctx = cv.getContext("2d");
    let comb = "mul", klass = "fixed";
    const segs = (cls, set) => el.querySelectorAll(`.${cls} button`).forEach((b) => (b.onclick = () => { el.querySelectorAll(`.${cls} button`).forEach((x) => x.classList.toggle("on", x === b)); set(b.dataset.v); draw(); }));
    segs("fr-c", (v) => (comb = v)); segs("fr-k", (v) => (klass = v));
    const W = 720, H = 446, off = document.createElement("canvas"); off.width = w; off.height = h; const octx = off.getContext("2d");
    const paint = (vals, x, y, sw, title) => { const img = octx.createImageData(w, h);
      for (let i = 0; i < N; i++) { const c = vals[i], o = i * 4; if (c < 0) { img.data[o + 3] = 0; continue; } const p = parseInt(PAL[c].slice(1), 16); img.data[o] = p >> 16; img.data[o + 1] = (p >> 8) & 255; img.data[o + 2] = p & 255; img.data[o + 3] = 255; }
      octx.putImageData(img, 0, 0); ctx.imageSmoothingEnabled = false; const sh = (sw * h) / w; ctx.drawImage(off, x, y, sw, sh);
      ctx.fillStyle = "#212121"; ctx.font = `bold 12px ${font()}`; ctx.textAlign = "center"; ctx.fillText(title, x + sw / 2, y - 6); };
    const draw = () => {
      const s = cv.parentElement.clientWidth || W, k = s / W, dpr = window.devicePixelRatio || 1;
      cv.style.width = s + "px"; cv.style.height = H * k + "px"; cv.width = s * dpr; cv.height = H * k * dpr; ctx.setTransform(k * dpr, 0, 0, k * dpr, 0, 0);
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
      let wh = +q(".fr-wh").value, we = +q(".fr-we").value, wv = +q(".fr-wv").value; const t = wh + we + wv || 1; wh /= t; we /= t; wv /= t;
      q(".fr-whv").textContent = khn(wh, 2); q(".fr-wev").textContent = khn(we, 2); q(".fr-wvv").textContent = khn(wv, 2);
      const x = (c) => (c + 0.5) / 5;                                   // class centre 0,1 … 0,9
      const r = new Float32Array(N).fill(-1), vals = [];
      idx.forEach((i) => { const a = x(L.H[i]), b = x(L.E[i]), c = x(L.V[i]);
        const v = comb === "mul" ? Math.pow(a, wh) * Math.pow(b, we) * Math.pow(c, wv) : comb === "prod" ? a * b * c : wh * a + we * b + wv * c; r[i] = v; vals.push(v); });
      let br;
      if (klass === "fixed") br = [0.2, 0.4, 0.6, 0.8];
      else { const s2 = vals.slice().sort((p, q2) => p - q2); br = [0.2, 0.4, 0.6, 0.8].map((f) => s2[Math.floor(f * (s2.length - 1))]); }
      const cls = new Int8Array(N).fill(-1), cnt = [0, 0, 0, 0, 0];
      idx.forEach((i) => { const c = br.filter((b) => r[i] > b).length; cls[i] = c; cnt[c]++; });
      const sw = 170; paint(L.H, 10, 24, sw, "គ្រោះ H"); paint(L.E, 190, 24, sw, "ការប៉ះពាល់ E"); paint(L.V, 370, 24, sw, "ភាពងាយរងគ្រោះ V"); paint(cls, 550, 24, sw, "ហានិភ័យ R");
      // share bars
      const by = 205; ctx.textAlign = "left"; ctx.font = `12px ${font()}`; ctx.fillStyle = "#212121"; ctx.fillText(`ចំណែកផ្ទៃខេត្តតាមថ្នាក់ហានិភ័យ · កម្រិត ${br.map((b) => khn(b, 2)).join(" · ")}`, 10, by);
      cnt.forEach((c, j) => { const f = c / idx.length, y = by + 14 + j * 26;
        ctx.fillStyle = PAL[j]; ctx.fillRect(110, y, f * 520, 18); ctx.fillStyle = "#212121"; ctx.fillText(NAMES[j], 10, y + 13); ctx.fillText(khn(f * 100, 1) + "%", 116 + f * 520, y + 13); });
      // histogram of the continuous risk
      const hy = 360, bins = new Array(20).fill(0); vals.forEach((v) => bins[Math.min(19, Math.floor(v * 20))]++); const mx = Math.max(...bins);
      bins.forEach((b, j) => { ctx.fillStyle = PAL[Math.min(4, br.filter((t2) => (j + 0.5) / 20 > t2).length)]; const bh = (b / mx) * 56; ctx.fillRect(110 + j * 26, hy + 60 - bh, 24, bh); });
      ctx.fillStyle = "#212121"; ctx.fillText("តម្លៃ R បន្ត", 10, hy + 40); ctx.fillText("០", 106, hy + 74); ctx.fillText("១", 626, hy + 74);
      const vhShare = (cnt[3] + cnt[4]) / idx.length * 100;
      q(".sim-out").innerHTML = `${{ mul: "<b>គុណមានទម្ងន់</b>៖ កត្តាទាបមួយទាញ R ចុះ ហើយមិនអាចប៉ះប៉ូវដោយកត្តាខ្ពស់បានទេ។ V ស្ទើរតែ «ទាបខ្លាំង» គ្រប់កន្លែង ដូច្នេះ R ទាបទាំងខេត្ត។", prod: "<b>គុណសុទ្ធ</b>៖ គ្មានទម្ងន់ ហើយតម្លៃរួញខ្លាំង (០,៥ × ០,៥ × ០,៥ = ០,១២៥) ដូច្នេះកម្រិតថេរដាក់ស្ទើរទាំងអស់ក្នុងថ្នាក់ទាប។", wlc: "<b>បូក (WLC)</b>៖ កត្តាខ្ពស់មួយ អាចប៉ះប៉ូវកត្តាទាបមួយទៀតបាន។" }[comb]} ` +
        `${klass === "fixed" ? "កម្រិតថេរប្រាប់កម្រិតហានិភ័យដាច់ខាត៖ ប្រៀបធៀបខេត្ត ឬឆ្នាំបាន។" : "Quantile ដាក់ក្រឡា ២០% ក្នុងថ្នាក់នីមួយៗជានិច្ច៖ «ខ្ពស់ខ្លាំង» តែងមាន ២០% ទោះគ្រោះពិតតិចក៏ដោយ ដូច្នេះប្រៀបធៀបខេត្តមិនបានទេ។"}` +
        `<br>ផ្ទៃ «ខ្ពស់» និង «ខ្ពស់ខ្លាំង»៖ <b>${khn(vhShare, 1)}%</b>។ ទិន្នន័យដូចគ្នា តែការរួមបញ្ចូល និងវិធីចាត់ថ្នាក់ខុសគ្នា ផ្ដល់ផែនទីខុសគ្នាទាំងស្រុង៖ ត្រូវសរសេរវិធីទាំងពីរលើផែនទី។` +
        `<br><span class="sim-hint">ថ្នាក់ H E V បកស្រាយពីផែនទីក្នុងរបាយការណ៍គំរូ Flood Mapper v2.3 (ក្រឡាប្រហែល ១ គម) ហើយប្រើតម្លៃកណ្ដាលថ្នាក់ ០,១ … ០,៩។ ទម្ងន់ AHP ដើម ០,៥៤ · ០,៣០ · ០,១៦ (CR ០,០៣១)។</span>`;
    };
    el.querySelectorAll("input").forEach((i) => i.addEventListener("input", draw));
    q(".fr-r").onclick = () => { q(".fr-wh").value = 54; q(".fr-we").value = 30; q(".fr-wv").value = 16; draw(); };
    draw(); window.addEventListener("resize", () => el.isConnected && draw());
  };
})();
