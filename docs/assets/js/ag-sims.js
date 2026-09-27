/* ============================================================
   Lesson simulators · Book 4 Applied GIS and RS (khgeo/applied-gis-rs)
   Registered into window.EXTRA_SIMS; rendered by lesson-sims.js.
   gee-scale · gee-map · gee-filter · gee-composite
   gee-zonal · gee-harmonic · gee-rf (Chapter 2)
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

  /* ---------- 5. zonal statistics and scale (Lesson 4) ---------- */
  window.EXTRA_SIMS["gee-zonal"] = async (el) => {
    const { q, out, cv } = shell(el, "reduceRegion()៖ reducer និង scale",
      `<span class="sim-seg gz-r"><button type="button" data-r="mean" class="on">mean</button><button type="button" data-r="median">median</button><button type="button" data-r="max">max</button><button type="button" data-r="min">min</button><button type="button" data-r="stdDev">stdDev</button></span>
       <label>scale <b class="gz-sv"></b> <input type="range" class="gz-s" min="0" max="4" value="0"></label>`);
    const S = await loadScene(), n = S.n, W = 640, H = 330, K = [1, 2, 4, 8, 16];
    const nd = new Float32Array(n * n); for (let i = 0; i < n * n; i++) { const r = S.red[i], ni = S.nir[i]; nd[i] = (ni - r) / (ni + r + 1e-9); }
    let box = { x0: 30, y0: 18, x1: 70, y1: 58 }, drag = null;
    const col = (v) => { const t = Math.max(0, Math.min(1, (v + .2) / 1)); const P = [[165, 0, 38], [244, 109, 67], [254, 224, 139], [217, 239, 139], [102, 189, 99], [0, 104, 55]];
      const f = t * 5, i = Math.min(4, Math.floor(f)), u = f - i; return P[i].map((c, k) => Math.round(c + (P[i + 1][k] - c) * u)); };
    const stats = (k) => {
      const m = Math.floor(n / k), vals = [];
      for (let by = 0; by < m; by++) for (let bx = 0; bx < m; bx++) {
        const cx = (bx + .5) * k, cy = (by + .5) * k; if (cx < box.x0 || cx >= box.x1 || cy < box.y0 || cy >= box.y1) continue;
        let sum = 0; for (let y = by * k; y < by * k + k; y++) for (let x = bx * k; x < bx * k + k; x++) sum += nd[y * n + x]; vals.push(sum / (k * k)); }
      if (!vals.length) return null;
      vals.sort((a, b) => a - b); const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
      return { mean, median: vals[Math.floor(vals.length / 2)], max: vals[vals.length - 1], min: vals[0], stdDev: Math.sqrt(vals.reduce((a, b) => a + (b - mean) ** 2, 0) / vals.length), count: vals.length, vals };
    };
    const f2 = (v) => khn(v, 2);
    const draw = (ctx) => {
      const ki = +q(".gz-s").value, k = K[ki], r = q(".gz-r .on").dataset.r; q(".gz-sv").textContent = `${kh(k)} × ក្រឡាដើម`;
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const s = 300 / n, m = Math.floor(n / k);
      for (let by = 0; by < m; by++) for (let bx = 0; bx < m; bx++) {
        let sum = 0; for (let y = by * k; y < by * k + k; y++) for (let x = bx * k; x < bx * k + k; x++) sum += nd[y * n + x];
        const c = col(sum / (k * k)); ctx.fillStyle = `rgb(${c})`; ctx.fillRect(10 + bx * k * s, 15 + by * k * s, k * s + .6, k * s + .6);
        const cx = (bx + .5) * k, cy = (by + .5) * k;
        if (k > 1 && cx >= box.x0 && cx < box.x1 && cy >= box.y0 && cy < box.y1) { ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.beginPath(); ctx.arc(10 + cx * s, 15 + cy * s, Math.min(3, k * s / 4), 0, 7); ctx.fill(); }
      }
      if (k > 1) { ctx.strokeStyle = "rgba(0,0,0,.18)"; ctx.lineWidth = .6; for (let i = 0; i <= m; i++) { ctx.beginPath(); ctx.moveTo(10 + i * k * s, 15); ctx.lineTo(10 + i * k * s, 15 + m * k * s); ctx.moveTo(10, 15 + i * k * s); ctx.lineTo(10 + m * k * s, 15 + i * k * s); ctx.stroke(); } }
      ctx.lineWidth = 3; ctx.strokeStyle = "#fff"; ctx.strokeRect(10 + box.x0 * s, 15 + box.y0 * s, (box.x1 - box.x0) * s, (box.y1 - box.y0) * s);
      ctx.lineWidth = 2; ctx.strokeStyle = "#ef6c00"; ctx.strokeRect(10 + box.x0 * s, 15 + box.y0 * s, (box.x1 - box.x0) * s, (box.y1 - box.y0) * s);
      const st = stats(k), s1 = stats(1); ctx.font = `14px ${font()}`; ctx.fillStyle = "#263238"; ctx.textAlign = "left";
      if (!st) { ctx.fillText("គ្មានក្រឡាណាដែលមានចំណុចកណ្ដាលក្នុងតំបន់", 330, 40); out.innerHTML = "តំបន់តូចជាងក្រឡាមួយនៅ scale នេះ៖ Earth Engine នឹងត្រឡប់ null ។ បន្ថយ scale ឬពង្រីកតំបន់។"; return; }
      ctx.font = `bold 15px ${font()}`; ctx.fillText("លទ្ធផល (NDVI)", 330, 30); ctx.font = `13px ${font()}`;
      ctx.fillStyle = "#78909c"; ctx.fillText("scale នេះ", 480, 52); ctx.fillText("ក្រឡាដើម", 570, 52);
      ["mean", "median", "max", "min", "stdDev", "count"].forEach((key, i) => { const y = 76 + i * 24;
        ctx.fillStyle = key === r ? "#ef6c00" : "#263238"; ctx.font = `${key === r ? "bold " : ""}14px ${font()}`; ctx.fillText(key, 340, y);
        ctx.fillText(key === "count" ? khn(st[key]) : f2(st[key]), 480, y); ctx.fillStyle = "#90a4ae"; ctx.fillText(key === "count" ? khn(s1[key]) : f2(s1[key]), 570, y); });
      const hx = 340, hy = 225, hw = 280, hh = 80, bins = 20, hist = new Array(bins).fill(0);
      st.vals.forEach((v) => { hist[Math.max(0, Math.min(bins - 1, Math.floor((v + .3) / 1.2 * bins)))]++; }); const mx = Math.max(...hist);
      hist.forEach((c, i) => { ctx.fillStyle = (i / bins * 1.2 - .3) < 0 ? "#64b5f6" : "#81c784"; ctx.fillRect(hx + i * hw / bins, hy + hh - hh * c / mx, hw / bins - 1, hh * c / mx); });
      const xv = hx + (st[r] + .3) / 1.2 * hw; if (r !== "stdDev") { ctx.strokeStyle = "#ef6c00"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(xv, hy - 6); ctx.lineTo(xv, hy + hh); ctx.stroke(); }
      ctx.fillStyle = "#607d8b"; ctx.font = `12px ${font()}`; ctx.fillText("-០,៣", hx - 6, hy + hh + 16); ctx.fillText("០,៩", hx + hw - 16, hy + hh + 16); ctx.fillText("អ៊ីស្តូក្រាមក្រឡានៅ scale នេះ", hx + 60, hy - 10);
      out.innerHTML = `<b>${r}</b> = ${r === "count" ? khn(st.count) : f2(st[r])} ពី ${khn(st.count)} ក្រឡា (ក្រឡាដើម៖ ${f2(s1[r])} ពី ${khn(s1.count)})។ ` +
        (k === 1 ? "ប្ដូរ scale ដើម្បីមើលថា mean ស្ទើរមិនប្ដូរ ប៉ុន្តែ max min stdDev និង count ប្ដូរ។" : `នៅ scale ${kh(k)} ដង ក្រឡានីមួយៗជាមធ្យមនៃក្រឡាដើម ${kh(k * k)}៖ តម្លៃខ្លាំងៗត្រូវបានលាយ។ ចំណុចស = ក្រឡាដែលបានរាប់ (ចំណុចកណ្ដាលក្នុងតំបន់)។`) +
        `<br><span class="sim-hint">អូសលើរូបភាពដើម្បីគូរតំបន់ថ្មី · NDVI ពី ${S.src}</span>`;
    };
    const fit = stage(cv, W, H, draw);
    const pos = (e) => { const b = cv.getBoundingClientRect(), p = e.touches ? e.touches[0] : e; return [((p.clientX - b.left) / b.width * W - 10) / (300 / n), ((p.clientY - b.top) / b.height * H - 15) / (300 / n)]; };
    const down = (e) => { const [x, y] = pos(e); if (x < 0 || y < 0 || x > n || y > n) return; drag = [x, y]; e.preventDefault(); };
    const move = (e) => { if (!drag) return; const [x, y] = pos(e); box = { x0: Math.max(0, Math.min(drag[0], x)), y0: Math.max(0, Math.min(drag[1], y)), x1: Math.min(n, Math.max(drag[0], x)), y1: Math.min(n, Math.max(drag[1], y)) }; fit(); e.preventDefault(); };
    const up = () => { drag = null; };
    cv.addEventListener("mousedown", down); cv.addEventListener("mousemove", move); window.addEventListener("mouseup", up);
    cv.addEventListener("touchstart", down, { passive: false }); cv.addEventListener("touchmove", move, { passive: false }); cv.addEventListener("touchend", up);
    el.addEventListener("seg", fit); seg(el, "gz-r"); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 6. harmonic regression (Lesson 5) ---------- */
  window.EXTRA_SIMS["gee-harmonic"] = (el) => {
    const { q, out, cv } = shell(el, "តំរែតំរង់ harmonic លើស៊េរី NDVI",
      `<span class="sim-seg gh-c"><button type="button" data-c="wet" class="on">ស្រែវស្សា</button><button type="button" data-c="double">ស្រែពីរដង</button><button type="button" data-c="dec">ព្រៃរបោះស្លឹក</button><button type="button" data-c="ever">ព្រៃស្រោងទាប</button></span>
       <label>លំដាប់ <b class="gh-ov"></b> <input type="range" class="gh-o" min="0" max="3" value="1"></label>
       <label>ពពករដូវវស្សា <b class="gh-pv"></b> <input type="range" class="gh-p" min="0" max="80" step="10" value="50"></label>
       <label><input type="checkbox" class="gh-m" checked> លុបពពក</label>`);
    const W = 640, H = 330, X0 = 50, Y0 = 20, PW = 400, PH = 250;
    const curves = { wet: (t) => .18 + .58 * Math.exp(-(((t - 280) / 38) ** 2)) * (t > 190 ? 1 : 0) + .05 * Math.exp(-(((t - 60) / 40) ** 2)),
      double: (t) => .16 + .56 * Math.exp(-(((t - 50) / 30) ** 2)) + .55 * Math.exp(-(((t - 250) / 30) ** 2)),
      dec: (t) => .55 + .22 * Math.cos(2 * Math.PI * (t - 260) / 365), ever: (t) => .8 + .03 * Math.cos(2 * Math.PI * (t - 250) / 365) };
    const solve = (A, b) => { const n = b.length, M = A.map((r, i) => [...r, b[i]]);
      for (let c = 0; c < n; c++) { let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r; [M[c], M[p]] = [M[p], M[c]]; if (Math.abs(M[c][c]) < 1e-12) return null;
        for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / M[c][c]; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; } }
      return M.map((r, i) => r[n] / r[i]); };
    const basis = (t, o) => { const v = [1]; for (let k = 1; k <= o; k++) v.push(Math.cos(2 * Math.PI * k * t / 365), Math.sin(2 * Math.PI * k * t / 365)); return v; };
    const draw = (ctx) => {
      const c = q(".gh-c .on").dataset.c, o = +q(".gh-o").value, pc = +q(".gh-p").value / 100, mask = q(".gh-m").checked; q(".gh-ov").textContent = kh(o); q(".gh-pv").textContent = kh(Math.round(pc * 100)) + "%";
      let sd = 7; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647); const gauss = () => Math.sqrt(-2 * Math.log(rnd() + 1e-9)) * Math.cos(2 * Math.PI * rnd());
      const fn = curves[c], obs = [];
      for (let t = 3; t <= 365; t += 5) { const wet = t > 135 && t < 305, cl = rnd() < (wet ? pc : pc * .25); const v = fn(t) + .025 * gauss(); obs.push({ t, y: cl ? v * (.05 + .55 * rnd()) : v, cl }); }
      const used = obs.filter((p) => !mask || !p.cl), nb = 1 + 2 * o;
      const A = Array.from({ length: nb }, () => new Array(nb).fill(0)), b = new Array(nb).fill(0);
      used.forEach((p) => { const v = basis(p.t, o); for (let i = 0; i < nb; i++) { b[i] += v[i] * p.y; for (let j = 0; j < nb; j++) A[i][j] += v[i] * v[j]; } });
      const beta = used.length > nb ? solve(A, b) : null; const pred = (t) => beta ? basis(t, o).reduce((a, v, i) => a + v * beta[i], 0) : null;
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const X = (t) => X0 + (t - 1) / 364 * PW, Y = (v) => Y0 + PH - v * PH;
      ctx.fillStyle = "rgba(144,202,249,.18)"; ctx.fillRect(X(135), Y0, X(305) - X(135), PH); ctx.strokeStyle = "#cfd8dc"; ctx.strokeRect(X0, Y0, PW, PH);
      ctx.font = `12px ${font()}`; ctx.fillStyle = "#607d8b"; ctx.textAlign = "right"; [0, .2, .4, .6, .8, 1].forEach((v) => ctx.fillText(khn(v, 1), X0 - 6, Y(v) + 4)); ctx.textAlign = "center";
      ["មក", "កម", "មន", "មស", "ឧស", "មថ", "កក", "សហ", "កញ", "តល", "វច", "ធន"].forEach((m, i) => ctx.fillText(m, X(15 + i * 30.4), Y0 + PH + 16));
      ctx.strokeStyle = "#bdbdbd"; ctx.lineWidth = 2; ctx.beginPath(); for (let t = 1; t <= 365; t += 2) { const x = X(t), y = Y(fn(t)); t === 1 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke();
      obs.forEach((p) => { ctx.beginPath(); ctx.arc(X(p.t), Y(Math.max(0, p.y)), 3.5, 0, 7); ctx.fillStyle = p.cl ? (mask ? "rgba(144,164,174,.35)" : "#90a4ae") : "#2e7d32"; ctx.fill(); });
      let rmse = null, amp = null, peak = null;
      if (beta) { ctx.strokeStyle = "#6a1b9a"; ctx.lineWidth = 3; ctx.beginPath(); let se = 0, best = -9;
        for (let t = 1; t <= 365; t++) { const v = pred(t), x = X(t), y = Y(Math.max(-.05, Math.min(1.05, v))); t === 1 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); se += (v - fn(t)) ** 2; if (v > best) { best = v; peak = t; } }
        ctx.stroke(); rmse = Math.sqrt(se / 365); amp = o >= 1 ? Math.hypot(beta[1], beta[2]) : 0; }
      ctx.textAlign = "left"; ctx.font = `bold 14px ${font()}`; ctx.fillStyle = "#263238"; ctx.fillText("លទ្ធផល", 470, 40); ctx.font = `13px ${font()}`;
      const rows = [["ចំណុចដែលប្រើ", khn(used.length)], ["RMSE ធៀបនឹងសញ្ញាពិត", rmse == null ? "–" : khn(rmse, 3)], ["ទំហំ harmonic ១", amp == null ? "–" : khn(amp, 2)], ["ថ្ងៃកំពូល (DOY)", peak == null ? "–" : kh(peak)]];
      rows.forEach(([a, v], i) => { ctx.fillStyle = "#607d8b"; ctx.fillText(a, 470, 70 + i * 44); ctx.fillStyle = "#263238"; ctx.font = `bold 16px ${font()}`; ctx.fillText(v, 470, 90 + i * 44); ctx.font = `13px ${font()}`; });
      ctx.fillStyle = "#2e7d32"; ctx.fillText("● ស្អាត", 470, 262); ctx.fillStyle = "#90a4ae"; ctx.fillText("● ពពក", 540, 262); ctx.fillStyle = "#6a1b9a"; ctx.fillText("━ ខ្សែសម", 470, 284); ctx.fillStyle = "#9e9e9e"; ctx.fillText("━ សញ្ញាពិត", 550, 284);
      const msg = o === 0 ? "លំដាប់ ០ គឺជាមធ្យមតែមួយ៖ គ្មានរដូវកាលទេ។" : c === "double" && o === 1 ? "លំដាប់ ១ មានកំពូលតែមួយ ដូច្នេះវាមិនអាចតំណាងស្រែពីរដងបានទេ។ សាកលំដាប់ ២។" :
        !mask && pc > 0 ? "ពពកដែលមិនបានលុប ទាញខ្សែសមចុះក្រោមក្នុងរដូវវស្សា៖ ធីក «លុបពពក»។" : o === 3 ? "លំដាប់ ៣ ស្ទើរមិនល្អជាងលំដាប់ ២ ទេ ហើយអាចបង្កើតរលកក្លែងក្លាយ ពេលទិន្នន័យតិច។" : "ខ្សែសមបំពេញចន្លោះពពក ហើយផ្ដល់តម្លៃនៅថ្ងៃណាក៏បាន។";
      out.innerHTML = `${msg}<br><span class="sim-hint">ស៊េរីក្លែងធ្វើតាមប្រតិទិនដំណាំនៅកម្ពុជា · ការសង្កេតរៀងរាល់ ៥ ថ្ងៃ · RMSE វាស់ភាពខុសរវាងខ្សែសម និងសញ្ញាពិត (ពណ៌ប្រផេះ)</span>`;
    };
    const fit = stage(cv, W, H, draw); el.addEventListener("seg", fit); seg(el, "gh-c"); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 7. Random Forest on a real Landsat 8 scene (Lesson 6) ---------- */
  let L8 = null;
  const loadL8 = async () => { if (L8) return L8; const j = await (await fetch(new URL("l8_pp_scene.json", AG_DATA))).json();
    const dec = (b) => { const s = atob(b), a = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; };
    const d = dec(j.data), N = j.n * j.n, B = []; for (let k = 0; k < 6; k++) { const a = new Float32Array(N); for (let i = 0; i < N; i++) a[i] = d[k * N + i] * j.scale; B.push(a); }
    return (L8 = { n: j.n, B, cls: dec(j.cls), names: j.classes }); };
  window.EXTRA_SIMS["gee-rf"] = async (el) => {
    const { q, out, cv } = shell(el, "Random Forest លើរូបភាព Landsat 8 ពិត",
      `<label>ចំណុច/ថ្នាក់ <select class="gr-n"><option>10</option><option>20</option><option selected>50</option><option>100</option><option>200</option></select></label>
       <label>ដើមឈើ <select class="gr-t"><option>1</option><option>10</option><option selected>30</option><option>60</option></select></label>
       <span class="sim-seg gr-f"><button type="button" data-f="rgb">RGB</button><button type="button" data-f="six" class="on">B2–B7</button><button type="button" data-f="idx">+ សន្ទស្សន៍</button></span>
       <span class="sim-seg gr-v"><button type="button" data-v="map" class="on">ផែនទី</button><button type="button" data-v="ref">យោង</button><button type="button" data-v="err">កំហុស</button></span>
       <button type="button" class="gr-go">▶ បណ្ដុះបណ្ដាលម្ដងទៀត</button>`);
    const D = await loadL8(), n = D.n, N = n * n, W = 640, H = 330, COL = [[30, 136, 229], [27, 94, 32], [156, 204, 101], [229, 57, 53], [215, 204, 200]];
    const KH = ["ទឹក", "ដើមឈើ", "ដំណាំ/ស្មៅ", "សាងសង់", "ដីទទេ"];
    const [b2, b3, b4, b5, b6, b7] = D.B, nd = (a, b, i) => (a[i] - b[i]) / (a[i] + b[i] + 1e-9);
    const FEAT = { rgb: [(i) => b2[i], (i) => b3[i], (i) => b4[i]], six: D.B.map((a) => (i) => a[i]) };
    FEAT.idx = [...FEAT.six, (i) => nd(b5, b4, i), (i) => nd(b3, b6, i), (i) => nd(b6, b5, i)];
    let seed = 5, pred = null, result = null; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const gini = (cnt, tot) => { let g = 1; for (const c of cnt) g -= (c / tot) ** 2; return g; };
    const grow = (X, y, idx, depth, F) => {
      const cnt = [0, 0, 0, 0, 0]; idx.forEach((i) => cnt[y[i]]++); const maj = cnt.indexOf(Math.max(...cnt));
      if (depth >= 12 || idx.length < 2 || Math.max(...cnt) === idx.length) return { leaf: maj };
      const m = Math.max(1, Math.round(Math.sqrt(F))), feats = []; while (feats.length < m) { const f = Math.floor(rnd() * F); if (!feats.includes(f)) feats.push(f); }
      let best = null;
      for (const f of feats) { const vals = idx.map((i) => X[i][f]).sort((a, b) => a - b);
        for (let qn = 1; qn < 12; qn++) { const thr = vals[Math.floor(qn / 12 * vals.length)]; const L = [0, 0, 0, 0, 0], R = [0, 0, 0, 0, 0]; let nl = 0;
          idx.forEach((i) => { if (X[i][f] < thr) { L[y[i]]++; nl++; } else R[y[i]]++; }); const nr = idx.length - nl; if (!nl || !nr) continue;
          const g = (nl * gini(L, nl) + nr * gini(R, nr)) / idx.length; if (!best || g < best.g) best = { g, f, thr }; } }
      if (!best) return { leaf: maj };
      const li = idx.filter((i) => X[i][best.f] < best.thr), ri = idx.filter((i) => X[i][best.f] >= best.thr);
      return { f: best.f, thr: best.thr, l: grow(X, y, li, depth + 1, F), r: grow(X, y, ri, depth + 1, F) };
    };
    const run = () => {
      const per = +q(".gr-n").value, T = +q(".gr-t").value, fs = FEAT[q(".gr-f .on").dataset.f], F = fs.length; seed = 5 + per;
      const pts = []; for (let c = 0; c < 5; c++) { let k = 0, guard = 0; while (k < per && guard++ < 1e6) { const i = Math.floor(rnd() * N); if (D.cls[i] === c) { pts.push(i); k++; } } }
      for (let i = pts.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [pts[i], pts[j]] = [pts[j], pts[i]]; }
      const ntr = Math.round(pts.length * .7), tr = pts.slice(0, ntr), te = pts.slice(ntr);
      const X = tr.map((i) => fs.map((g) => g(i))), y = tr.map((i) => D.cls[i]), all = X.map((_, k) => k);
      const trees = []; for (let t = 0; t < T; t++) { const bs = T === 1 ? all : all.map(() => Math.floor(rnd() * all.length)); trees.push(grow(X, y, bs, 0, T === 1 ? F * F : F)); }
      const classify = (i) => { const v = fs.map((g) => g(i)), votes = [0, 0, 0, 0, 0]; for (const tr_ of trees) { let nd_ = tr_; while (nd_.leaf === undefined) nd_ = v[nd_.f] < nd_.thr ? nd_.l : nd_.r; votes[nd_.leaf]++; } return votes.indexOf(Math.max(...votes)); };
      pred = new Uint8Array(N); for (let i = 0; i < N; i++) pred[i] = classify(i);
      const cm = Array.from({ length: 5 }, () => [0, 0, 0, 0, 0]); te.forEach((i) => cm[D.cls[i]][pred[i]]++);
      const tot = te.length, diag = cm.reduce((a, r, i) => a + r[i], 0), oa = diag / tot;
      const pe = cm.reduce((a, r, i) => a + r.reduce((x, y_) => x + y_, 0) * cm.reduce((x, rr) => x + rr[i], 0), 0) / (tot * tot);
      let agree = 0; for (let i = 0; i < N; i++) if (pred[i] === D.cls[i]) agree++;
      result = { cm, oa, kappa: (oa - pe) / (1 - pe), tr, te, all: agree / N, F, T, per }; fit();
    };
    const draw = (ctx) => {
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); if (!pred) return; const v = q(".gr-v .on").dataset.v;
      const img = ctx.createImageData(n, n);
      for (let i = 0; i < N; i++) { const c = v === "ref" ? COL[D.cls[i]] : v === "err" ? (pred[i] === D.cls[i] ? [245, 245, 245] : [211, 47, 47]) : COL[pred[i]]; img.data.set([c[0], c[1], c[2], 255], i * 4); }
      const tmp = document.createElement("canvas"); tmp.width = n; tmp.height = n; tmp.getContext("2d").putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = false; ctx.drawImage(tmp, 10, 15, 300, 300);
      const s = 300 / n; result.tr.forEach((i) => { ctx.beginPath(); ctx.arc(10 + (i % n + .5) * s, 15 + (Math.floor(i / n) + .5) * s, 2.2, 0, 7); ctx.fillStyle = "#fff"; ctx.fill(); ctx.strokeStyle = "#000"; ctx.lineWidth = .6; ctx.stroke(); });
      const x0 = 400, y0 = 44, c = 38; ctx.font = `12px ${font()}`; ctx.textAlign = "center"; ctx.fillStyle = "#263238"; ctx.fillText("ចាត់ថ្នាក់ →", x0 + 2.5 * c, 26);
      for (let i = 0; i < 5; i++) { ctx.textAlign = "right"; ctx.fillStyle = `rgb(${COL[i]})`; ctx.fillText(KH[i], x0 - 6, y0 + i * c + c / 2 + 4);
        for (let j = 0; j < 5; j++) { const val = result.cm[i][j]; ctx.fillStyle = i === j ? "#2e7d32" : val ? "#ffcdd2" : "#fafafa"; ctx.fillRect(x0 + j * c, y0 + i * c, c - 2, c - 2);
          ctx.fillStyle = i === j ? "#fff" : "#263238"; ctx.textAlign = "center"; ctx.font = `bold 13px ${font()}`; ctx.fillText(kh(val), x0 + j * c + c / 2 - 1, y0 + i * c + c / 2 + 4); ctx.font = `12px ${font()}`; } }
      for (let j = 0; j < 5; j++) { ctx.fillStyle = `rgb(${COL[j]})`; ctx.fillRect(x0 + j * c + 8, y0 + 5 * c + 2, c - 18, 6); }
      ctx.textAlign = "left"; ctx.fillStyle = "#263238"; ctx.font = `bold 17px ${font()}`; ctx.fillText(`OA ${kh(Math.round(result.oa * 100))}%  ·  Kappa ${khn(result.kappa, 2)}`, 335, y0 + 5 * c + 36);
      ctx.font = `12px ${font()}`; ctx.fillStyle = "#607d8b"; ctx.fillText(`ត្រូវគ្នានឹងយោង លើ ${khn(N)} ក្រឡា៖ ${kh(Math.round(result.all * 100))}%`, 335, y0 + 5 * c + 58);
    };
    const fit = stage(cv, W, H, draw);
    const describe = () => { if (!result) return; const cm = result.cm; let worst = 0, wv = 2;
      for (let i = 0; i < 5; i++) { const rs = cm[i].reduce((a, b) => a + b, 0); const pa = rs ? cm[i][i] / rs : 1; if (pa < wv) { wv = pa; worst = i; } }
      out.innerHTML = `ចំណុចបណ្ដុះបណ្ដាល ${khn(result.tr.length)} (ចំណុចស) · ផ្ទៀងផ្ទាត់ ${khn(result.te.length)} · លក្ខណៈ ${kh(result.F)} · ដើមឈើ ${kh(result.T)}។ ថ្នាក់ខ្សោយបំផុត៖ <b>${KH[worst]}</b> (PA ${kh(Math.round(wv * 100))}%)។` +
        `<br><span class="sim-hint">Landsat 8 OLI TOA · ភ្នំពេញ · ១១ កុម្ភៈ ២០១៩ · ផែនទីយោងបានពីកម្រិតសន្ទស្សន៍ មិនមែនការស្ទង់វាល ដូច្នេះ OA ក្នុងពិសោធន៍នេះខ្ពស់ជាងការងារពិតបន្តិច</span>`; };
    const go = () => { out.textContent = "កំពុងបណ្ដុះបណ្ដាល…"; setTimeout(() => { run(); describe(); }, 30); };
    q(".gr-go").addEventListener("click", go); el.querySelectorAll("select").forEach((s_) => s_.addEventListener("change", go));
    el.addEventListener("seg", (e) => { if (e.target.closest(".gr-f")) go(); else fit(); }); seg(el, "gr-f"); seg(el, "gr-v"); go();
  };
})();
