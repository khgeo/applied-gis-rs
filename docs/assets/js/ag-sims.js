/* ============================================================
   Lesson simulators · Book 4 Applied GIS and RS (khgeo/applied-gis-rs)
   Registered into window.EXTRA_SIMS; rendered by lesson-sims.js.
   gee-scale · gee-map · gee-filter · gee-composite
   ============================================================ */
(function () {
  "use strict";
  const KM = "០១២៣៤៥៦៧៨៩", kh = (n) => String(n).replace(/[0-9]/g, (d) => KM[d]);
  const khn = (n, d = 0) => kh(Number(n).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/,/g, " ").replace(".", ","));
  const AG_DATA = new URL("../data/", (document.currentScript && document.currentScript.src) || location.href);
  window.EXTRA_SIMS = window.EXTRA_SIMS || {};
  const shell = (el, title, controls) => {
    el.innerHTML = `<div class="sim-title">${title}</div><div class="sim-controls">${controls}</div><div class="sim-body"><div class="sim-canvas-wrap"><canvas></canvas></div></div><div class="sim-out" role="status"></div>`;
    return { q: (s) => el.querySelector(s), out: el.querySelector(".sim-out"), cv: el.querySelector("canvas") };
  };
  const stage = (cv, W, H, draw) => { const ctx = cv.getContext("2d");
    const fit = () => { const w = cv.parentElement.clientWidth || W, s = w / W, d = window.devicePixelRatio || 1; cv.style.width = w + "px"; cv.style.height = H * s + "px"; cv.width = w * d; cv.height = H * s * d; ctx.setTransform(s * d, 0, 0, s * d, 0, 0); draw(ctx); };
    let t; window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(() => cv.isConnected && fit(), 100); }); return fit; };
  const font = () => getComputedStyle(document.body).fontFamily || "Battambang, sans-serif";
  const seg = (el, cls) => el.querySelectorAll(`.${cls} button`).forEach((b) => b.addEventListener("click", () => { el.querySelectorAll(`.${cls} button`).forEach((x) => x.classList.remove("on")); b.classList.add("on"); b.dispatchEvent(new Event("seg", { bubbles: true })); }));

  /* ---------- 1. download vs cloud ---------- */
  window.EXTRA_SIMS["gee-scale"] = (el) => {
    const { q, out, cv } = shell(el, "ទាញយក ឬគណនាលើពពក?",
      `<label>តំបន់ <select class="gs-a"><option value="1">ខេត្តមួយ (~៧ ០០០ គម²)</option><option value="3">ខេត្តបី</option><option value="26" selected>កម្ពុជាទាំងមូល (១៨១ ០០០ គម²)</option></select></label>
       <label>ឆ្នាំ <b class="gs-yv"></b> <input type="range" class="gs-y" min="1" max="10" value="5"></label>
       <label>អ៊ីនធឺណិត <select class="gs-n"><option value="5">៥ Mbps</option><option value="20" selected>២០ Mbps</option><option value="100">១០០ Mbps</option></select></label>`);
    const W = 640, H = 300;
    const draw = (ctx) => {
      const tiles = +q(".gs-a").value * 1.15 + .2, yrs = +q(".gs-y").value, mbps = +q(".gs-n").value; q(".gs-yv").textContent = kh(yrs);
      const scenes = Math.round(tiles * 73 * yrs), gb = scenes * .8, hours = gb * 8000 / mbps / 3600, cloudMin = Math.max(1, Math.round(scenes / 900));
      ctx.fillStyle = "#fafafa"; ctx.fillRect(0, 0, W, H); ctx.font = `15px ${font()}`;
      const bar = (y, v, max, c, t, lab) => { ctx.fillStyle = "#eceff1"; ctx.fillRect(170, y, 440, 34); ctx.fillStyle = c; ctx.fillRect(170, y, Math.max(4, 440 * Math.min(1, Math.log10(v + 1) / Math.log10(max + 1))), 34);
        ctx.fillStyle = "#263238"; ctx.textAlign = "right"; ctx.fillText(t, 160, y + 23); ctx.textAlign = "left"; ctx.fillStyle = "#fff"; ctx.font = `bold 14px ${font()}`; ctx.fillText(lab, 180, y + 23); ctx.font = `15px ${font()}`; };
      bar(40, scenes, 20000, "#43a047", "រូបភាព Sentinel-2", `${khn(scenes)} ផ្ទាំង`);
      bar(100, gb, 16000, "#fb8c00", "ទំហំទិន្នន័យ", gb > 1000 ? `${khn(gb / 1000, 1)} TB` : `${khn(gb)} GB`);
      bar(160, hours, 20000, "#e53935", "ពេលទាញយក", hours > 48 ? `${khn(hours / 24)} ថ្ងៃ` : `${khn(hours, 1)} ម៉ោង`);
      bar(220, cloudMin, 20000, "#1e88e5", "Earth Engine", `~${kh(cloudMin)} នាទី (គណនានៅម៉ាស៊ីនមេ)`);
      out.innerHTML = `ទាញយកមកកុំព្យូទ័រ ត្រូវការថាសទំនេរ ${gb > 1000 ? khn(gb / 1000, 1) + " TB" : khn(gb) + " GB"} និងពេល ${hours > 48 ? khn(hours / 24) + " ថ្ងៃ" : khn(hours, 1) + " ម៉ោង"} មុនចាប់ផ្ដើមវិភាគ។ Earth Engine នាំកូដទៅកន្លែងទិន្នន័យ ហើយបញ្ជូនមកវិញតែលទ្ធផល (ផែនទី ឬតារាង)។<br><span class="sim-hint">ប៉ាន់ស្មាន៖ ~៧៣ រូបភាព/tile/ឆ្នាំ · ~០,៨ GB/រូបភាព L2A · ពេល Earth Engine ជាលំដាប់ទំហំប៉ុណ្ណោះ</span>`;
    };
    const fit = stage(cv, W, H, draw); el.querySelectorAll("select,input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 2. map() over a collection ---------- */
  window.EXTRA_SIMS["gee-map"] = (el) => {
    const { q, out, cv } = shell(el, "map() ៖ អនុវត្តមុខងារលើគ្រប់រូបភាព",
      `<span class="sim-seg gm-f"><button type="button" data-f="ndvi" class="on">addNDVI</button><button type="button" data-f="clip">clip(province)</button><button type="button" data-f="mask">maskClouds</button><button type="button" data-f="scale">× 0.0001</button></span>
       <button type="button" class="gm-run">▶ ដំណើរការ</button>`);
    const W = 640, H = 330, N = 8; let step = N;
    const dates = ["០៥ មករា", "១០ មករា", "១៥ មករា", "២០ មករា", "២៥ មករា", "៣០ មករា", "០៤ កុម្ភៈ", "០៩ កុម្ភៈ"];
    const clouds = [0.1, 0.6, 0.05, 0.3, 0.8, 0.15, 0.0, 0.4];
    const code = { ndvi: "col.map(function(img){\n  return img.addBands(\n    img.normalizedDifference(['B8','B4']).rename('NDVI'));\n})",
      clip: "col.map(function(img){\n  return img.clip(province);\n})", mask: "col.map(function(img){\n  var scl = img.select('SCL');\n  return img.updateMask(scl.neq(9));\n})", scale: "col.map(function(img){\n  return img.multiply(0.0001);\n})" };
    const tile = (ctx, x, y, i, f, done) => {
      const s = 62; ctx.fillStyle = "#8d6e63"; ctx.fillRect(x, y, s, s);
      for (let a = 0; a < 6; a++) for (let b = 0; b < 6; b++) { const v = (Math.sin(a * 1.7 + b + i) + 1) / 2; ctx.fillStyle = done && f === "ndvi" ? `rgb(${40 + 60 * (1 - v)},${120 + 100 * v},60)` : `rgb(${120 + 60 * v},${110 + 40 * v},${90 + 20 * v})`; ctx.fillRect(x + a * s / 6, y + b * s / 6, s / 6 + .5, s / 6 + .5); }
      if (!(done && f === "mask")) { ctx.fillStyle = "rgba(255,255,255,.92)"; ctx.beginPath(); ctx.arc(x + s * .6, y + s * .4, s * clouds[i] * .55, 0, 7); ctx.fill(); }
      else { ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(x + s * .6, y + s * .4, s * clouds[i] * .55, 0, 7); ctx.fill(); ctx.strokeStyle = "#e53935"; ctx.setLineDash([3, 3]); ctx.stroke(); ctx.setLineDash([]); }
      if (done && f === "clip") { ctx.fillStyle = "#fafafa"; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + s, y); ctx.lineTo(x + s, y + s * .3); ctx.lineTo(x + s * .7, y + s * .15); ctx.lineTo(x + s * .3, y + s * .4); ctx.lineTo(x, y + s * .2); ctx.fill(); ctx.fillStyle = "#fafafa"; ctx.fillRect(x, y + s * .8, s, s * .2); }
      ctx.strokeStyle = done ? "#43a047" : "#90a4ae"; ctx.lineWidth = done ? 3 : 1; ctx.strokeRect(x, y, s, s); ctx.lineWidth = 1;
    };
    const draw = (ctx) => {
      const f = q(".gm-f .on").dataset.f; ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); ctx.font = `12px ${font()}`;
      ctx.fillStyle = "#263238"; ctx.fillText("ImageCollection (៨ រូបភាព)", 10, 18);
      for (let i = 0; i < N; i++) { const x = 10 + i * 78; tile(ctx, x, 28, i, f, false); ctx.fillStyle = "#607d8b"; ctx.fillText(dates[i], x, 106); }
      for (let i = 0; i < N; i++) { const x = 10 + i * 78; ctx.strokeStyle = i < step ? "#43a047" : "#cfd8dc"; ctx.beginPath(); ctx.moveTo(x + 31, 112); ctx.lineTo(x + 31, 148); ctx.stroke();
        if (i < step) tile(ctx, x, 152, i, f, true); else { ctx.strokeStyle = "#cfd8dc"; ctx.setLineDash([4, 3]); ctx.strokeRect(x, 152, 62, 62); ctx.setLineDash([]); } }
      ctx.fillStyle = "#263238"; ctx.fillText("លទ្ធផល៖ ImageCollection ថ្មី (ចំនួនដូចគ្នា)", 10, 234);
      ctx.fillStyle = "#263238"; ctx.fillRect(10, 244, 620, 80); ctx.fillStyle = "#80cbc4"; ctx.font = "13px monospace";
      code[f].split("\n").forEach((l, k) => ctx.fillText(l, 20, 262 + k * 16));
    };
    const fit = stage(cv, W, H, draw);
    el.addEventListener("seg", () => { step = N; fit(); out.textContent = ""; }); seg(el, "gm-f");
    q(".gm-run").onclick = () => { step = 0; const t = setInterval(() => { step++; fit(); if (step >= N) { clearInterval(t);
      out.innerHTML = "មុខងារត្រូវបានអនុវត្តលើរូបភាពនីមួយៗ <b>ដាច់ដោយឡែក</b> ហើយស្របគ្នានៅលើម៉ាស៊ីនមេរាប់រយ។ map() មិនប្ដូរលំដាប់ ឬចំនួនរូបភាពទេ។<br><span class=\"sim-hint\">មុខងារក្នុង map() ត្រូវ return រូបភាពជានិច្ច ហើយមិនអាចប្រើ print() ឬ getInfo() ខាងក្នុងបានទេ</span>"; } }, 250); };
    fit();
  };

  /* ---------- 3. filter a collection ---------- */
  window.EXTRA_SIMS["gee-filter"] = (el) => {
    const { q, out, cv } = shell(el, "ត្រង ImageCollection",
      `<label>ខែចាប់ផ្ដើម <select class="gf-a">${["មករា", "កុម្ភៈ", "មីនា", "មេសា", "ឧសភា", "មិថុនា", "កក្កដា", "សីហា", "កញ្ញា", "តុលា", "វិច្ឆិកា", "ធ្នូ"].map((m, i) => `<option value="${i}" ${i === 0 ? "selected" : ""}>${m}</option>`).join("")}</select></label>
       <label>ចំនួនខែ <b class="gf-nv"></b> <input type="range" class="gf-n" min="1" max="12" value="4"></label>
       <label>ពពក &lt; <b class="gf-cv"></b>% <input type="range" class="gf-c" min="5" max="100" step="5" value="20"></label>`);
    const W = 640, H = 250; let seed = 3; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const cloudy = [.25, .2, .3, .45, .7, .85, .9, .9, .85, .7, .45, .3];
    const imgs = []; for (let d = 0; d < 365; d += 5) { const m = Math.min(11, Math.floor(d / 30.4)); imgs.push({ d, m, c: Math.max(0, Math.min(100, (cloudy[m] + (rnd() - .5) * .5) * 100)) }); }
    const draw = (ctx) => {
      const a = +q(".gf-a").value, n = +q(".gf-n").value, cmax = +q(".gf-c").value; q(".gf-nv").textContent = kh(n); q(".gf-cv").textContent = kh(cmax);
      const inMonth = (m) => ((m - a + 12) % 12) < n;
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); ctx.font = `12px ${font()}`;
      for (let m = 0; m < 12; m++) { const x = 20 + m * 50; ctx.fillStyle = inMonth(m) ? "#e8f5e9" : "#fafafa"; ctx.fillRect(x, 20, 50, 170); ctx.fillStyle = "#607d8b"; ctx.fillText(kh(m + 1), x + 20, 208); }
      ctx.strokeStyle = "#e53935"; ctx.setLineDash([5, 4]); const yc = 190 - cmax * 1.7; ctx.beginPath(); ctx.moveTo(20, yc); ctx.lineTo(620, yc); ctx.stroke(); ctx.setLineDash([]);
      let kept = 0, fdate = 0;
      imgs.forEach((im) => { const x = 20 + im.d / 365 * 600, y = 190 - im.c * 1.7, okD = inMonth(im.m), ok = okD && im.c < cmax; if (okD) fdate++; if (ok) kept++;
        ctx.beginPath(); ctx.arc(x, y, ok ? 5 : 3, 0, 7); ctx.fillStyle = ok ? "#2e7d32" : okD ? "#ef9a9a" : "#cfd8dc"; ctx.fill(); });
      ctx.fillStyle = "#263238"; ctx.fillText("ខែ", 610, 230); ctx.save(); ctx.translate(10, 110); ctx.rotate(-Math.PI / 2); ctx.fillText("% ពពក", 0, 0); ctx.restore();
      out.innerHTML = `រូបភាពសរុប ${kh(imgs.length)} → filterDate៖ ${kh(fdate)} → filter(ពពក &lt; ${kh(cmax)}%)៖ <b>${kh(kept)}</b><br><code>.filterDate(...) .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', ${cmax}))</code><br><span class="sim-hint">រដូវប្រាំង (វិច្ឆិកា–មេសា) ទុករូបភាពច្រើនជាងរដូវវស្សា · តម្លៃពពកជាគំរូបង្រៀន</span>`;
    };
    const fit = stage(cv, W, H, draw); el.querySelectorAll("select,input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 4. composite reducers on a real scene with simulated clouds ---------- */
  let SC = null; const loadScene = async () => SC || (SC = await (await fetch(new URL("s2_scene_small.json", AG_DATA))).json());
  window.EXTRA_SIMS["gee-composite"] = async (el) => {
    const { q, out, cv } = shell(el, "Composite ពីរូបភាពមានពពក",
      `<span class="sim-seg gc-r"><button type="button" data-r="first">first()</button><button type="button" data-r="median" class="on">median()</button><button type="button" data-r="min">min()</button><button type="button" data-r="max">max()</button><button type="button" data-r="green">qualityMosaic(NDVI)</button></span>
       <label><input type="checkbox" class="gc-m"> លុបពពកមុន (mask)</label>
       <label>ចំនួនរូបភាព <b class="gc-nv"></b> <input type="range" class="gc-n" min="1" max="10" value="6"></label>`);
    const S = await loadScene(), n = S.n, W = 640, H = 330;
    let seed = 11; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const T = 10, cloud = [], shadow = [], bright = [];
    for (let t = 0; t < T; t++) { const cm = new Float32Array(n * n), sm = new Float32Array(n * n); const k = 1 + Math.floor(rnd() * 3);
      for (let c = 0; c < k; c++) { const cx = rnd() * n, cy = rnd() * n, r = 5 + rnd() * 9;
        for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { const d = Math.hypot(x - cx, y - cy); if (d < r) cm[y * n + x] = Math.max(cm[y * n + x], 1 - d / r * .4); const ds = Math.hypot(x - cx - 6, y - cy - 7); if (ds < r * .8 && d >= r) sm[y * n + x] = 1; } }
      cloud.push(cm); shadow.push(sm); bright.push(.92 + rnd() * .16); }
    const px = (t, b, i) => { const v = S[b][i] / S.scale * bright[t]; if (cloud[t][i] > 0) return .15 + .55 * cloud[t][i] + v * .2; if (shadow[t][i]) return v * .35; return v; };
    const clicked = { x: 40, y: 50 };
    const draw = (ctx) => {
      const r = q(".gc-r .on").dataset.r, mask = q(".gc-m").checked, N = +q(".gc-n").value; q(".gc-nv").textContent = kh(N);
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
      const img = ctx.createImageData(n, n), bands = ["red", "green", "blue"]; let cloudyLeft = 0;
      for (let i = 0; i < n * n; i++) {
        const valid = []; for (let t = 0; t < N; t++) if (!mask || (cloud[t][i] === 0 && !shadow[t][i])) valid.push(t);
        let pick = null, vals = [0, 0, 0];
        if (!valid.length) { img.data[i * 4 + 3] = 0; continue; }
        if (r === "first") pick = valid[0];
        else if (r === "green") { let best = -2; valid.forEach((t) => { const nd = (px(t, "nir", i) - px(t, "red", i)) / (px(t, "nir", i) + px(t, "red", i) + 1e-6); if (nd > best) { best = nd; pick = t; } }); }
        if (pick !== null) vals = bands.map((b) => px(pick, b, i));
        else vals = bands.map((b) => { const a = valid.map((t) => px(t, b, i)).sort((p, q2) => p - q2); return r === "min" ? a[0] : r === "max" ? a[a.length - 1] : a.length % 2 ? a[(a.length - 1) / 2] : (a[a.length / 2 - 1] + a[a.length / 2]) / 2; });
        if (pick !== null ? cloud[pick][i] > 0 : false) cloudyLeft++;
        vals.forEach((v, k) => (img.data[i * 4 + k] = Math.min(255, Math.max(0, v / .18 * 255))));
        img.data[i * 4 + 3] = 255;
      }
      const off = document.createElement("canvas"); off.width = n; off.height = n; off.getContext("2d").putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = false; ctx.fillStyle = "#eceff1"; ctx.fillRect(10, 10, 300, 300); ctx.drawImage(off, 10, 10, 300, 300);
      ctx.strokeStyle = "#ffeb3b"; ctx.lineWidth = 2; ctx.strokeRect(10 + clicked.x * 300 / n - 4, 10 + clicked.y * 300 / n - 4, 8, 8); ctx.lineWidth = 1;
      // time series of the clicked pixel (red band brightness)
      const i = clicked.y * n + clicked.x; ctx.font = `12px ${font()}`; ctx.fillStyle = "#263238"; ctx.fillText("ក្រឡាដែលបានជ្រើស៖ ពន្លឺក្រហមតាមកាលបរិច្ឆេទ", 330, 24);
      ctx.strokeStyle = "#cfd8dc"; ctx.strokeRect(330, 34, 300, 150);
      for (let t = 0; t < N; t++) { const v = px(t, "red", i), x = 350 + t * 26, y = 174 - Math.min(1, v / .5) * 130, isC = cloud[t][i] > 0, isS = shadow[t][i];
        ctx.beginPath(); ctx.arc(x, y, 5, 0, 7); ctx.fillStyle = isC ? "#90a4ae" : isS ? "#37474f" : "#e64a19"; ctx.fill(); }
      ctx.fillStyle = "#607d8b"; ctx.fillText("● ស្អាត   ● ពពក   ● ស្រមោល", 340, 200); ctx.fillStyle = "#e64a19"; ctx.fillText("●", 340, 200); ctx.fillStyle = "#90a4ae"; ctx.fillText("●", 400, 200); ctx.fillStyle = "#37474f"; ctx.fillText("●", 452, 200);
      const msg = { first: "first() យករូបភាពដំបូង ដូច្នេះពពកនៅតែមាន", median: "median() យកតម្លៃកណ្ដាល៖ ពពក (ភ្លឺ) និងស្រមោល (ងងឹត) ត្រូវបានជៀសវាង បើវាមិនលើសពាក់កណ្ដាលនៃរូបភាព",
        min: "min() ជ្រើសតម្លៃងងឹតបំផុត៖ ស្រមោល និងទឹកលេចធ្លោ", max: "max() ជ្រើសតម្លៃភ្លឺបំផុត៖ ពពកគ្របដណ្ដប់", green: "qualityMosaic(NDVI) យករូបភាពដែលរុក្ខជាតិបៃតងបំផុតក្នុងក្រឡានីមួយៗ" }[r];
      out.innerHTML = `${msg}${mask ? " · ពពក និងស្រមោលត្រូវបាន mask មុន" : ""}<br><span class="sim-hint">ចុចលើរូបភាព ដើម្បីជ្រើសក្រឡា · មូលដ្ឋាន៖ ${S.src} · ពពក និងស្រមោលក្លែងធ្វើ</span>`;
    };
    const fit = stage(cv, W, H, draw);
    cv.addEventListener("click", (e) => { const b = cv.getBoundingClientRect(), x = (e.clientX - b.left) / b.width * W, y = (e.clientY - b.top) / b.height * H; if (x > 10 && x < 310 && y > 10 && y < 310) { clicked.x = Math.floor((x - 10) / 300 * n); clicked.y = Math.floor((y - 10) / 300 * n); fit(); } });
    el.addEventListener("seg", fit); seg(el, "gc-r"); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit)); fit();
  };
})();
