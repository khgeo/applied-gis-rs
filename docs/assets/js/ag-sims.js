/* ============================================================
   Lesson simulators · Book 4 Applied GIS and RS (khgeo/applied-gis-rs)
   Registered into window.EXTRA_SIMS; rendered by lesson-sims.js.
   gee-scale · gee-map · gee-filter · gee-composite
   gee-zonal · gee-harmonic · gee-rf (Chapter 2)
   gee-flood · gee-drought · gee-terrain (Chapter 3)
   gee-forest · gee-rice · gee-urban (Chapter 4)
   gee-mcda · gee-app · gee-ethics (Chapter 5)
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

  /* ---------- 8. SAR water threshold (Lesson 7) ---------- */
  window.EXTRA_SIMS["gee-flood"] = async (el) => {
    const { q, out, cv } = shell(el, "កម្រិតទឹកលើរូបភាព SAR (VV)",
      `<label>កម្រិត <b class="gf-tv"></b> <input type="range" class="gf-t" min="-25" max="-5" step="0.5" value="-12"></label>
       <label>តម្រង <select class="gf-k"><option value="1">គ្មាន</option><option value="3">៣ × ៣</option><option value="5" selected>៥ × ៥</option><option value="7">៧ × ៧</option></select></label>
       <button type="button" class="gf-o">Otsu</button>
       <span class="sim-seg gf-v"><button type="button" data-v="img" class="on">រូបភាព</button><button type="button" data-v="map">ផែនទីទឹក</button><button type="button" data-v="err">កំហុស</button></span>`);
    const D = await loadL8(), n = D.n, N = n * n, W = 640, H = 330, MEAN = [-21, -7.5, -12, -5, -14];
    let sd = 99; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647);
    const raw = new Float32Array(N), truth = new Uint8Array(N);
    for (let i = 0; i < N; i++) { const c = D.cls[i]; truth[i] = c === 0 ? 1 : 0; let g = 0; for (let k = 0; k < 4; k++) g -= Math.log(rnd() + 1e-9); raw[i] = MEAN[c] + 10 * Math.log10(g / 4); }
    const cache = {};
    const filt = (k) => { if (cache[k]) return cache[k]; if (k === 1) return (cache[1] = raw); const o = new Float32Array(N), r = (k - 1) / 2, buf = [];
      for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { buf.length = 0;
        for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) { const yy = Math.min(n - 1, Math.max(0, y + dy)), xx = Math.min(n - 1, Math.max(0, x + dx)); buf.push(raw[yy * n + xx]); }
        buf.sort((a, b) => a - b); o[y * n + x] = buf[buf.length >> 1]; }
      return (cache[k] = o); };
    const hist = (a) => { const h = new Array(60).fill(0); for (let i = 0; i < N; i++) { const b = Math.floor((a[i] + 30) / 30 * 60); if (b >= 0 && b < 60) h[b]++; } return h; };
    const otsu = (a) => { const h = hist(a), tot = h.reduce((x, y) => x + y, 0); let sum = 0; h.forEach((c, i) => sum += c * i); let wB = 0, sB = 0, best = 0, bi = 0;
      for (let i = 0; i < 60; i++) { wB += h[i]; if (!wB || wB === tot) continue; sB += i * h[i]; const mB = sB / wB, mF = (sum - sB) / (tot - wB), v = wB * (tot - wB) * (mB - mF) ** 2; if (v > best) { best = v; bi = i; } }
      return -30 + (bi + 1) * .5; };
    const draw = (ctx) => {
      const k = +q(".gf-k").value, t = +q(".gf-t").value, v = q(".gf-v .on").dataset.v, a = filt(k); q(".gf-tv").textContent = khn(t, 1) + " dB";
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const img = ctx.createImageData(n, n); let tp = 0, fp = 0, fn = 0, wat = 0;
      for (let i = 0; i < N; i++) { const w = a[i] < t, tr = truth[i]; if (w) wat++; if (w && tr) tp++; else if (w) fp++; else if (tr) fn++;
        let c; if (v === "img") { const g = Math.max(0, Math.min(255, (a[i] + 25) / 25 * 255)); c = [g, g, g]; }
        else if (v === "map") c = w ? [30, 136, 229] : [235, 235, 235]; else c = w && tr ? [30, 136, 229] : w ? [229, 57, 53] : tr ? [255, 152, 0] : [245, 245, 245];
        img.data.set([c[0], c[1], c[2], 255], i * 4); }
      const tmp = document.createElement("canvas"); tmp.width = n; tmp.height = n; tmp.getContext("2d").putImageData(img, 0, 0); ctx.imageSmoothingEnabled = false; ctx.drawImage(tmp, 10, 15, 300, 300);
      const h = hist(a), mx = Math.max(...h), x0 = 340, y0 = 30, w = 280, hh = 200;
      h.forEach((c, i) => { const val = -30 + i * .5; ctx.fillStyle = val < t ? "#64b5f6" : "#bcaaa4"; ctx.fillRect(x0 + i * w / 60, y0 + hh - hh * c / mx, w / 60 - 1, hh * c / mx); });
      const xt = x0 + (t + 30) / 30 * w; ctx.strokeStyle = "#c62828"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(xt, y0 - 5); ctx.lineTo(xt, y0 + hh); ctx.stroke();
      ctx.font = `12px ${font()}`; ctx.fillStyle = "#607d8b"; ctx.textAlign = "center"; [-30, -20, -10, 0].forEach((d) => ctx.fillText(kh(d), x0 + (d + 30) / 30 * w, y0 + hh + 16)); ctx.fillText("VV (dB)", x0 + w / 2, y0 + hh + 32);
      const acc = (N - fp - fn) / N, prec = tp / Math.max(1, tp + fp), rec = tp / Math.max(1, tp + fn);
      ctx.textAlign = "left"; ctx.fillStyle = "#263238"; ctx.font = `bold 15px ${font()}`; ctx.fillText(`ភាពត្រឹមត្រូវ ${khn(acc * 100, 1)}%`, x0, 285);
      ctx.font = `13px ${font()}`; ctx.fillText(`ទឹកដែលរកឃើញ ${kh(Math.round(rec * 100))}% · ទឹកក្លែងក្លាយ ${kh(Math.round((1 - prec) * 100))}%`, x0, 308);
      if (v === "err") { ctx.fillStyle = "#e53935"; ctx.fillText("■ ទឹកក្លែងក្លាយ", 10, 328); ctx.fillStyle = "#ff9800"; ctx.fillText("■ ទឹកដែលខក", 120, 328); }
      out.innerHTML = (k === 1 ? "គ្មានតម្រង៖ speckle ធ្វើឲ្យកំពូលពីរត្រួតគ្នា ហើយក្រឡាដីជាច្រើនធ្លាក់ក្រោមកម្រិត។ " : `តម្រង median ${kh(k)} × ${kh(k)} ធ្វើឲ្យកំពូលទឹក (ខៀវ) និងដី (ត្នោត) ច្បាស់។ `) +
        `<br><span class="sim-hint">SAR ក្លែងធ្វើ៖ តម្លៃ VV ធម្មតាតាមគម្របដីពិតនៃ Landsat 8 ភ្នំពេញ + speckle (៤ look) · ការពិត = ថ្នាក់ទឹកក្នុងផែនទីយោង</span>`;
    };
    const fit = stage(cv, W, H, draw);
    q(".gf-o").addEventListener("click", () => { q(".gf-t").value = otsu(filt(+q(".gf-k").value)); fit(); });
    el.addEventListener("seg", fit); seg(el, "gf-v"); el.querySelectorAll("input,select").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 9. SPI accumulation windows (Lesson 8) ---------- */
  window.EXTRA_SIMS["gee-drought"] = (el) => {
    const Y0 = 1995, Y1 = 2024, CLIM = [8, 10, 35, 80, 150, 155, 160, 165, 230, 255, 130, 40], ENSO = { 1997: .7, 2004: .85, 2015: .6, 2019: .7, 2023: .8 };
    const opts = []; for (let y = Y1; y >= 2000; y--) opts.push(`<option value="${y}"${y === 2019 ? " selected" : ""}>${kh(y)}${ENSO[y] ? " · El Niño" : ""}</option>`);
    const { q, out, cv } = shell(el, "SPI តាមរយៈពេលបូក",
      `<label>ឆ្នាំ <select class="gd-y">${opts.join("")}</select></label>
       <span class="sim-seg gd-k"><button type="button" data-k="1">SPI-១</button><button type="button" data-k="3" class="on">SPI-៣</button><button type="button" data-k="6">SPI-៦</button></span>`);
    let sd = 21; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647);
    const gam = (k) => { let s = 0; for (let i = 0; i < k; i++) s -= Math.log(rnd() + 1e-9); return s / k; };
    const series = []; for (let y = Y0; y <= Y1; y++) for (let m = 0; m < 12; m++) series.push(Math.max(0, CLIM[m] * (ENSO[y] || 1) * gam(6)));
    const W = 640, H = 330, MON = ["មក", "កម", "មន", "មស", "ឧស", "មថ", "កក", "សហ", "កញ", "តល", "វច", "ធន"];
    const draw = (ctx) => {
      const Y = +q(".gd-y").value, k = +q(".gd-k .on").dataset.k;
      const acc = series.map((_, i) => i >= k - 1 ? series.slice(i - k + 1, i + 1).reduce((a, b) => a + b, 0) : null);
      const spi = []; for (let m = 0; m < 12; m++) { const vals = []; for (let y = Y0; y <= Y1; y++) { const v = acc[(y - Y0) * 12 + m]; if (v != null) vals.push(v); }
        const mu = vals.reduce((a, b) => a + b, 0) / vals.length, s = Math.sqrt(vals.reduce((a, b) => a + (b - mu) ** 2, 0) / vals.length); const v = acc[(Y - Y0) * 12 + m]; spi.push(v == null ? 0 : (v - mu) / s); }
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const x0 = 60, y0 = 30, w = 560, h = 220, Yp = (v) => y0 + h / 2 - v / 3 * (h / 2);
      [-2, -1, 0, 1, 2].forEach((v) => { ctx.strokeStyle = v === 0 ? "#263238" : v === -1 ? "#ef6c00" : "#eceff1"; ctx.setLineDash(v === -1 ? [5, 4] : []); ctx.beginPath(); ctx.moveTo(x0, Yp(v)); ctx.lineTo(x0 + w, Yp(v)); ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = "#607d8b"; ctx.font = `12px ${font()}`; ctx.textAlign = "right"; ctx.fillText(khn(v, 0), x0 - 6, Yp(v) + 4); });
      spi.forEach((v, m) => { const bx = x0 + m * w / 12 + 6, bw = w / 12 - 12; ctx.fillStyle = v < -2 ? "#7f0000" : v < -1.5 ? "#c62828" : v < -1 ? "#ef6c00" : v < 1 ? "#b0bec5" : "#1e88e5";
        ctx.fillRect(bx, Math.min(Yp(0), Yp(v)), bw, Math.abs(Yp(v) - Yp(0))); ctx.fillStyle = "#263238"; ctx.textAlign = "center"; ctx.fillText(MON[m], bx + bw / 2, y0 + h + 16);
        ctx.fillText(khn(v, 1), bx + bw / 2, v < 0 ? Yp(v) + 14 : Yp(v) - 4); });
      const rain = series.slice((Y - Y0) * 12, (Y - Y0) * 12 + 12), tot = rain.reduce((a, b) => a + b, 0), norm = CLIM.reduce((a, b) => a + b, 0);
      ctx.textAlign = "left"; ctx.font = `13px ${font()}`; ctx.fillStyle = "#263238"; ctx.fillText(`ទឹកភ្លៀងឆ្នាំ ${kh(Y)}៖ ${khn(tot)} mm (${kh(Math.round(tot / norm * 100))}% នៃមធ្យមប្រចាំខែ)`, x0, y0 + h + 44);
      const dry = spi.filter((v) => v < -1).length, wetMon = [4, 5, 6, 7, 8, 9].filter((m) => spi[m] < -1).length;
      out.innerHTML = `SPI-${kh(k)}៖ ${kh(dry)} ខែក្រោម −១ (${kh(wetMon)} ក្នុងរដូវវស្សា ឧសភា–តុលា)។ ` + (k === 1 ? "SPI-១ លោតឡើងចុះរាល់ខែ៖ ខែស្ងួតមួយអាចមិនប៉ះពាល់ដំណាំទេ។" : k === 3 ? "SPI-៣ ទាក់ទងនឹងសំណើមដី និងដំណាំ៖ ខែស្ងួតជាប់ៗគ្នាបង្ហាញខ្លាំង។" : "SPI-៦ រលោង និងយឺត៖ ទាក់ទងនឹងទន្លេ និងអាងស្តុកទឹក។") +
        `<br><span class="sim-hint">ទឹកភ្លៀងក្លែងធ្វើ ${kh(Y0)}–${kh(Y1)} ពីមធ្យមប្រចាំខែប្រហាក់ប្រហែលនៃភ្នំពេញ · ឆ្នាំ El Niño ត្រូវបានកាត់បន្ថយ · SPI សាមញ្ញ (z-score គ្មានការបម្លែង gamma)</span>`;
    };
    const fit = stage(cv, W, H, draw); el.addEventListener("seg", fit); seg(el, "gd-k"); q(".gd-y").addEventListener("change", fit); fit();
  };

  /* ---------- 10. terrain products and watersheds (Lesson 9) ---------- */
  window.EXTRA_SIMS["gee-terrain"] = async (el) => {
    const { q, out, cv } = shell(el, "ទីសណ្ឋាន និងអាងរងទឹក",
      `<span class="sim-seg gt-p"><button type="button" data-p="elev">កម្ពស់</button><button type="button" data-p="slope">ជម្រាល</button><button type="button" data-p="aspect">ទិស</button><button type="button" data-p="hs" class="on">ស្រមោល</button></span>
       <label>ទិសពន្លឺ <b class="gt-av"></b> <input type="range" class="gt-a" min="0" max="360" step="15" value="315"></label>
       <label>ប្រឡាយ > <b class="gt-sv"></b> <input type="range" class="gt-s" min="1" max="3.5" step="0.25" value="2.5"></label>`);
    const j = await (await fetch(new URL("dem_synthetic.json", AG_DATA))).json(), n = j.n, N = n * n, res = j.res;
    const dec16 = (b64) => { const bs = atob(b64), a = new Float32Array(N); for (let i = 0; i < N; i++) a[i] = (bs.charCodeAt(2 * i) | (bs.charCodeAt(2 * i + 1) << 8)) * j.scale; return a; };
    const z = dec16(j.z), zr = dec16(j.zr);
    const zmin = Math.min(...zr), zmax = Math.max(...zr), DY = [-1, -1, -1, 0, 0, 1, 1, 1], DX = [-1, 0, 1, -1, 1, -1, 0, 1];
    const fd = new Int8Array(N).fill(-1);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { let best = 0, bk = -1; const i = y * n + x;
      for (let k = 0; k < 8; k++) { const yy = y + DY[k], xx = x + DX[k]; if (yy < 0 || yy >= n || xx < 0 || xx >= n) continue; const d = (z[i] - z[yy * n + xx]) / Math.hypot(DY[k], DX[k]); if (d > best) { best = d; bk = k; } }
      fd[i] = bk; }
    const acc = new Float32Array(N).fill(1), order = Array.from({ length: N }, (_, i) => i).sort((a, b) => z[b] - z[a]);
    for (const i of order) { const k = fd[i]; if (k < 0) continue; const y = Math.floor(i / n) + DY[k], x = (i % n) + DX[k]; if (y >= 0 && y < n && x >= 0 && x < n) acc[y * n + x] += acc[i]; }
    const up = Array.from({ length: N }, () => []); for (let i = 0; i < N; i++) { const k = fd[i]; if (k < 0) continue; const y = Math.floor(i / n) + DY[k], x = (i % n) + DX[k]; if (y >= 0 && y < n && x >= 0 && x < n) up[y * n + x].push(i); }
    const sl = new Float32Array(N), as = new Float32Array(N);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { const g = (yy, xx) => zr[Math.min(n - 1, Math.max(0, yy)) * n + Math.min(n - 1, Math.max(0, xx))];
      const gx = (g(y, x + 1) - g(y, x - 1)) / (2 * res), gy = (g(y + 1, x) - g(y - 1, x)) / (2 * res); sl[y * n + x] = Math.atan(Math.hypot(gx, gy)); as[y * n + x] = Math.atan2(-gx, gy); }
    let ws = null, outlet = null;
    const ramp = (t, P) => { t = Math.max(0, Math.min(1, t)) * (P.length - 1); const i = Math.min(P.length - 2, Math.floor(t)), u = t - i; return P[i].map((c, k) => c + (P[i + 1][k] - c) * u); };
    const TER = [[26, 152, 80], [145, 207, 96], [217, 239, 139], [254, 224, 139], [252, 141, 89], [166, 97, 26], [245, 245, 245]];
    const W = 640, H = 330;
    const draw = (ctx) => {
      const p = q(".gt-p .on").dataset.p, az = +q(".gt-a").value, thr = 10 ** +q(".gt-s").value; q(".gt-av").textContent = kh(az) + "°"; q(".gt-sv").textContent = khn(thr * res * res / 1e6, 1) + " គម²";
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const img = ctx.createImageData(n, n), A = (360 - az + 90) * Math.PI / 180, E = 45 * Math.PI / 180;
      for (let i = 0; i < N; i++) { let c;
        if (p === "elev") c = ramp((zr[i] - zmin) / (zmax - zmin), TER);
        else if (p === "slope") c = ramp(sl[i] * 180 / Math.PI / 25, [[255, 255, 204], [253, 141, 60], [189, 0, 38]]);
        else if (p === "aspect") { const d = ((as[i] * 180 / Math.PI) + 360) % 360 / 360; c = ramp(d, [[228, 26, 28], [255, 255, 51], [77, 175, 74], [55, 126, 184], [228, 26, 28]]); }
        else { const v = Math.sin(E) * Math.cos(sl[i]) + Math.cos(E) * Math.sin(sl[i]) * Math.cos(A - as[i]); const g = Math.max(0, Math.min(1, (v - .55) / .45)) * 215 + 40; c = [g, g, g]; }
        if (ws && ws[i]) c = c.map((v, k) => v * .55 + [255, 152, 0][k] * .45);
        if (acc[i] > thr) c = [21, 101, 192];
        img.data.set([c[0], c[1], c[2], 255], i * 4); }
      const tmp = document.createElement("canvas"); tmp.width = n; tmp.height = n; tmp.getContext("2d").putImageData(img, 0, 0); ctx.imageSmoothingEnabled = false; ctx.drawImage(tmp, 10, 10, 310, 310);
      if (outlet != null) { ctx.beginPath(); ctx.arc(10 + (outlet % n + .5) * 310 / n, 10 + (Math.floor(outlet / n) + .5) * 310 / n, 6, 0, 7); ctx.fillStyle = "#c62828"; ctx.fill(); ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke(); }
      ctx.textAlign = "left"; ctx.fillStyle = "#263238"; ctx.font = `bold 15px ${font()}`; ctx.fillText("ព័ត៌មាន", 345, 34); ctx.font = `13px ${font()}`;
      const lines = [["កម្ពស់", `${khn(zmin)}–${khn(zmax)} ម`], ["ក្រឡា", `${kh(n)} × ${kh(n)} · ${kh(res)} ម`], ["ក្រឡាប្រឡាយ", khn([...acc].filter((v) => v > thr).length)]];
      if (ws) { const cnt = ws.reduce((a, b) => a + b, 0); lines.push(["ផ្ទៃអាងរង", `${khn(cnt * res * res / 1e6, 2)} គម²`], ["ស្រុតទឹកនៅចំណុចចេញ", khn(acc[outlet])]); }
      lines.forEach(([a, b], k) => { ctx.fillStyle = "#607d8b"; ctx.fillText(a, 345, 64 + k * 44); ctx.fillStyle = "#263238"; ctx.font = `bold 15px ${font()}`; ctx.fillText(b, 345, 84 + k * 44); ctx.font = `13px ${font()}`; });
      out.innerHTML = (ws ? "អាងរង (ពណ៌ទឹកក្រូច) = គ្រប់ក្រឡាដែលទឹកហូរចេញតាមចំណុចក្រហម។ ចុចកន្លែងខាងក្រោមនៃប្រឡាយដដែល ដើម្បីមើលអាងរីកធំ។" : "ចុចលើប្រឡាយ (ខៀវ) ដើម្បីកំណត់អាងរងទឹកនៃចំណុចនោះ។") +
        `<br><span class="sim-hint">DEM ក្លែងធ្វើ (មិនមែនទីកន្លែងពិត) · ទិសលំហូរ D8 និងស្រុតទឹកគណនាក្នុងកម្មវិធីរុករក</span>`;
    };
    const fit = stage(cv, W, H, draw);
    cv.addEventListener("click", (e) => { const b = cv.getBoundingClientRect(), px = (e.clientX - b.left) / b.width * W, py = (e.clientY - b.top) / b.height * H;
      const x = Math.floor((px - 10) / 310 * n), y = Math.floor((py - 10) / 310 * n); if (x < 0 || y < 0 || x >= n || y >= n) return;
      let bi = y * n + x; for (let dy = -3; dy <= 3; dy++) for (let dx = -3; dx <= 3; dx++) { const yy = y + dy, xx = x + dx; if (yy >= 0 && yy < n && xx >= 0 && xx < n && acc[yy * n + xx] > acc[bi]) bi = yy * n + xx; }
      outlet = bi; ws = new Uint8Array(N); const st = [bi]; ws[bi] = 1; while (st.length) { const i = st.pop(); for (const u of up[i]) if (!ws[u]) { ws[u] = 1; st.push(u); } } fit(); });
    el.addEventListener("seg", fit); seg(el, "gt-p"); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 11. forest loss and protected areas (Lesson 10) ---------- */
  window.EXTRA_SIMS["gee-forest"] = async (el) => {
    const yopt = (sel) => Array.from({ length: 23 }, (_, i) => 2001 + i).map((y) => `<option value="${y}"${y === sel ? " selected" : ""}>${kh(y)}</option>`).join("");
    const { q, out, cv } = shell(el, "ការបាត់បង់ព្រៃ និងតំបន់ការពារ",
      `<label>កម្រិតគម្រប <b class="gfo-tv"></b> <input type="range" class="gfo-t" min="10" max="70" step="5" value="30"></label>
       <label>ពី <select class="gfo-a">${yopt(2001)}</select></label><label>ដល់ <select class="gfo-b">${yopt(2023)}</select></label>`);
    const D = await loadL8(), n = D.n, N = n * n, W = 640, H = 330;
    let sd = 12; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647);
    const raw = new Float32Array(N); for (let i = 0; i < N; i++) raw[i] = rnd();
    const tc = new Float32Array(N), ly = new Uint8Array(N), BASE = [5, 85, 25, 5, 5];
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { let s_ = 0, c = 0; for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) { const yy = y + dy, xx = x + dx; if (yy >= 0 && yy < n && xx >= 0 && xx < n) { s_ += raw[yy * n + xx]; c++; } }
      tc[y * n + x] = Math.max(0, Math.min(100, BASE[D.cls[y * n + x]] + (s_ / c - .5) * 90)); }
    for (let by = 0; by < n; by += 3) for (let bx = 0; bx < n; bx += 3) {
      const d = Math.min(Math.abs(bx - 110), by < 170 ? Math.abs(by - 150) + (bx > 170 ? bx - 170 : 0) : 999, by > 150 ? Math.abs(bx - 40) : 999);
      if (rnd() < Math.exp(-d / 18) * .45) { let yr = Math.round(12 + 4.5 * Math.sqrt(-2 * Math.log(rnd() + 1e-9)) * Math.cos(2 * Math.PI * rnd())); yr = Math.max(1, Math.min(23, yr));
        for (let dy = 0; dy < 3; dy++) for (let dx = 0; dx < 3; dx++) { const i = (by + dy) * n + bx + dx; if (by + dy < n && bx + dx < n && tc[i] > 25) ly[i] = yr; } } }
    const PA = [175, 290, 185, 295], zone = new Uint8Array(N);   // 1 in · 2 buffer · 0 out
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { const inPA = y >= PA[0] && y < PA[1] && x >= PA[2] && x < PA[3];
      const dy = Math.max(PA[0] - y, 0, y - PA[1] + 1), dx = Math.max(PA[2] - x, 0, x - PA[3] + 1); zone[y * n + x] = inPA ? 1 : Math.hypot(dx, dy) <= 30 ? 2 : 0; }
    const draw = (ctx) => {
      const t = +q(".gfo-t").value; let a = +q(".gfo-a").value, b = +q(".gfo-b").value; if (b < a) [a, b] = [b, a]; q(".gfo-tv").textContent = kh(t) + "%";
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const img = ctx.createImageData(n, n);
      const byY = new Array(23).fill(0), f = [0, 0, 0], l = [0, 0, 0];
      for (let i = 0; i < N; i++) { const isF = tc[i] >= t, lost = isF && ly[i] >= a - 2000 && ly[i] <= b - 2000 && ly[i] > 0; let c = [240, 240, 240];
        if (isF) { c = [116, 196, 118]; f[zone[i]]++; }
        if (isF && ly[i] > 0) byY[ly[i] - 1]++;
        if (lost) { const u = (ly[i] - 1) / 22; c = [255, Math.round(237 - u * 200), Math.round(160 - u * 160)]; l[zone[i]]++; }
        img.data.set([c[0], c[1], c[2], 255], i * 4); }
      const tmp = document.createElement("canvas"); tmp.width = n; tmp.height = n; tmp.getContext("2d").putImageData(img, 0, 0); ctx.imageSmoothingEnabled = false; ctx.drawImage(tmp, 10, 10, 300, 300);
      const s_ = 300 / n; ctx.strokeStyle = "#1565c0"; ctx.lineWidth = 2.5; ctx.strokeRect(10 + PA[2] * s_, 10 + PA[0] * s_, (PA[3] - PA[2]) * s_, (PA[1] - PA[0]) * s_);
      ctx.setLineDash([4, 3]); ctx.strokeStyle = "#607d8b"; ctx.lineWidth = 1.2; ctx.strokeRect(10 + (PA[2] - 30) * s_, 10 + (PA[0] - 30) * s_, (PA[3] - PA[2] + 60) * s_, (PA[1] - PA[0] + 60) * s_); ctx.setLineDash([]);
      const x0 = 340, y0 = 30, w = 280, hh = 120, mx = Math.max(1, ...byY); ctx.font = `12px ${font()}`; ctx.fillStyle = "#263238"; ctx.textAlign = "left"; ctx.fillText("ការបាត់បង់តាមឆ្នាំ (ក្នុងព្រៃ ២០០០)", x0, y0 - 8);
      byY.forEach((v, i) => { const on = 2001 + i >= a && 2001 + i <= b; ctx.fillStyle = on ? "#c62828" : "#e0e0e0"; ctx.fillRect(x0 + i * w / 23, y0 + hh - hh * v / mx, w / 23 - 2, hh * v / mx); });
      ctx.fillStyle = "#607d8b"; ctx.fillText("២០០១", x0, y0 + hh + 14); ctx.textAlign = "right"; ctx.fillText("២០២៣", x0 + w, y0 + hh + 14);
      const rate = (k) => f[k] ? l[k] / f[k] * 100 : 0, R = [["ក្នុងតំបន់ការពារ", rate(1), "#1565c0"], ["ទ្រនាប់", rate(2), "#78909c"], ["ក្រៅ", rate(0), "#c62828"]], rm = Math.max(1, ...R.map((r) => r[1]));
      ctx.textAlign = "left"; ctx.fillStyle = "#263238"; ctx.fillText(`% នៃព្រៃ ២០០០ ដែលបាត់បង់ ${kh(a)}–${kh(b)}`, x0, 196);
      R.forEach(([lab, v, col], k) => { const y = 210 + k * 32; ctx.fillStyle = "#263238"; ctx.fillText(lab, x0, y + 14); ctx.fillStyle = col; ctx.fillRect(x0 + 100, y, 120 * v / rm, 20); ctx.fillStyle = "#263238"; ctx.fillText(khn(v, 1) + "%", x0 + 106 + 120 * v / rm, y + 14); });
      const fa = (f[0] + f[1] + f[2]) * 900 / 1e6;
      out.innerHTML = `ព្រៃ ២០០០ (≥ ${kh(t)}%)៖ ${khn(fa, 1)} គម² · បាត់បង់ ${kh(a)}–${kh(b)}៖ ${khn((l[0] + l[1] + l[2]) * 900 / 1e6, 2)} គម²។ ` +
        (rate(1) < rate(0) ? "អត្រាក្នុងតំបន់ការពារទាបជាងក្រៅ ប៉ុន្តែតំបន់នេះនៅឆ្ងាយពីផ្លូវ៖ ការប្រៀបធៀបនេះមិនបញ្ជាក់ប្រសិទ្ធភាពទេ។" : "") +
        `<br><span class="sim-hint">ស្រទាប់ក្លែងធ្វើតាមទម្រង់ Hansen GFC លើគម្របដីពិតនៃ Landsat 8 ភ្នំពេញ · ការបាត់បង់ប្រមូលផ្ដុំជិតផ្លូវក្លែងធ្វើ · ប្រអប់ខៀវ = តំបន់ការពារ · ដាច់ៗ = ទ្រនាប់</span>`;
    };
    const fit = stage(cv, W, H, draw); el.querySelectorAll("input,select").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 12. rice rules from VH (Lesson 11) ---------- */
  window.EXTRA_SIMS["gee-rice"] = (el) => {
    const { q, out, cv } = shell(el, "ក្បួនស្រែពី Sentinel-1 VH",
      `<label>VH អប្បបរមា < <b class="gr2-mv"></b> <input type="range" class="gr2-m" min="-26" max="-14" step="0.5" value="-19"></label>
       <label>ការកើនឡើង > <b class="gr2-rv"></b> <input type="range" class="gr2-r" min="0" max="10" step="0.5" value="5"></label>
       <label>ភាពខុសគ្នា <b class="gr2-sv"></b> <input type="range" class="gr2-s" min="0.5" max="2" step="0.25" value="1"></label>`);
    const W = 640, H = 330, T = Array.from({ length: 365 }, (_, i) => i + 1);
    const K = [["wet", "ស្រែ", "#2e7d32"], ["crop", "ដំណាំដទៃ", "#ff9800"], ["forest", "ព្រៃ", "#1b5e20"], ["urban", "ទីក្រុង", "#e53935"], ["water", "ទឹក", "#1e88e5"]];
    const curve = (k, t) => k === "wet" ? -16.5 - 7 * Math.exp(-(((t - 205) / 14) ** 2)) + 3.5 * Math.exp(-(((t - 265) / 30) ** 2)) / (1 + Math.exp(-(t - 200) / 4)) - 1.5 / (1 + Math.exp(-(t - 320) / 5))
      : k === "crop" ? -17 + 2 * Math.exp(-(((t - 250) / 45) ** 2)) : k === "forest" ? -13 + .4 * Math.sin(t / 50) : k === "urban" ? -9 + .3 * Math.sin(t / 40) : -25 + .8 * Math.sin(t / 30);
    const gen = (spread) => { let sd = 5; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647); const g = () => Math.sqrt(-2 * Math.log(rnd() + 1e-9)) * Math.cos(2 * Math.PI * rnd()); const pts = [];
      K.forEach(([k], ki) => { for (let p = 0; p < 50; p++) { const amp = Math.max(.2, 1 + (rnd() - .5) * .9 * spread), off = g() * 1.8 * spread; const base = T.map((t) => curve(k, t)), m = base.reduce((a, b) => a + b, 0) / 365;
        const s = base.map((v) => m + (v - m) * amp + off + g() * 1.5 * spread), sm = s.map((_, i) => { let a = 0, c = 0; for (let j = i - 6; j <= i + 5; j++) if (j >= 0 && j < 365) { a += s[j]; c++; } return a / c; });
        let mn = 99; for (let i = 150; i < 260; i++) mn = Math.min(mn, sm[i]); let mx = -99; for (let i = 180; i < 330; i++) mx = Math.max(mx, sm[i]); pts.push({ ki, mn, rise: mx - mn }); } });
      return pts; };
    let cacheS = null, cacheP = null;
    const draw = (ctx) => {
      const tm = +q(".gr2-m").value, tr = +q(".gr2-r").value, sp = +q(".gr2-s").value; q(".gr2-mv").textContent = khn(tm, 1) + " dB"; q(".gr2-rv").textContent = khn(tr, 1) + " dB"; q(".gr2-sv").textContent = "×" + khn(sp, 2);
      if (cacheS !== sp) { cacheP = gen(sp); cacheS = sp; }
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const x0 = 60, y0 = 20, w = 380, h = 270, X = (v) => x0 + (v + 30) / 22 * w, Y = (v) => y0 + h - Math.max(0, Math.min(14, v)) / 14 * h;
      ctx.fillStyle = "rgba(46,125,50,.08)"; ctx.fillRect(x0, y0, X(tm) - x0, Y(tr) - y0); ctx.strokeStyle = "#cfd8dc"; ctx.strokeRect(x0, y0, w, h);
      ctx.strokeStyle = "#2e7d32"; ctx.setLineDash([6, 4]); ctx.beginPath(); ctx.moveTo(X(tm), y0); ctx.lineTo(X(tm), y0 + h); ctx.moveTo(x0, Y(tr)); ctx.lineTo(x0 + w, Y(tr)); ctx.stroke(); ctx.setLineDash([]);
      let tp = 0, fp = 0, fn = 0, tn = 0;
      cacheP.forEach((p) => { const isR = p.mn < tm && p.rise > tr, truth = p.ki === 0; if (isR && truth) tp++; else if (isR) fp++; else if (truth) fn++; else tn++;
        ctx.beginPath(); ctx.arc(X(Math.max(-30, Math.min(-8.5, p.mn))), Y(p.rise), 3.5, 0, 7); ctx.fillStyle = K[p.ki][2]; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
        if (isR !== truth) { ctx.strokeStyle = "#000"; ctx.lineWidth = 1.2; ctx.stroke(); } });
      ctx.font = `12px ${font()}`; ctx.fillStyle = "#607d8b"; ctx.textAlign = "center"; [-30, -25, -20, -15, -10].forEach((v) => ctx.fillText(kh(v), X(v), y0 + h + 14)); ctx.fillText("VH អប្បបរមា (dB)", x0 + w / 2, y0 + h + 30);
      ctx.textAlign = "right"; [0, 4, 8, 12].forEach((v) => ctx.fillText(kh(v), x0 - 6, Y(v) + 4));
      ctx.textAlign = "left"; K.forEach(([, lab, col], k) => { ctx.fillStyle = col; ctx.beginPath(); ctx.arc(470, 40 + k * 24, 5, 0, 7); ctx.fill(); ctx.fillStyle = "#263238"; ctx.fillText(lab, 482, 44 + k * 24); });
      const oa = (tp + tn) / (tp + tn + fp + fn), pa = tp / Math.max(1, tp + fn), ua = tp / Math.max(1, tp + fp);
      ctx.font = `bold 15px ${font()}`; ctx.fillText(`OA ${kh(Math.round(oa * 100))}%`, 470, 190); ctx.font = `13px ${font()}`;
      ctx.fillText(`PA ស្រែ ${kh(Math.round(pa * 100))}%`, 470, 214); ctx.fillText(`UA ស្រែ ${kh(Math.round(ua * 100))}%`, 470, 236); ctx.fillStyle = "#607d8b"; ctx.fillText("គូសខ្មៅ = ចាត់ខុស", 470, 262);
      out.innerHTML = (oa >= .97 ? "កម្រិតទាំងពីរបំបែកស្រែបានល្អ។ សាកបង្កើន «ភាពខុសគ្នា»។ " : fp > fn ? "ក្រឡាមិនមែនស្រែច្រើនត្រូវបានរាប់ជាស្រែ (UA ទាប)៖ តឹងកម្រិត។ " : fn > fp ? "ស្រែច្រើនត្រូវបានខក (PA ទាប)៖ បន្ធូរកម្រិត។ " : "កម្រិតសមតុល្យ។ ") +
        (sp > 1.4 ? "ពេលភាពខុសគ្នាក្នុងថ្នាក់ធំ គ្មានកម្រិតណាដែលល្អឥតខ្ចោះទេ៖ នេះជាពេលដែល Random Forest ជួយបាន។" : "") +
        `<br><span class="sim-hint">ក្រឡាក្លែងធ្វើ ២៥០ (៥០ ក្នុងមួយថ្នាក់) តាមលំនាំ VH នៃស្រែអាស៊ីអាគ្នេយ៍ · មធ្យមរំកិល ១២ ថ្ងៃ</span>`;
    };
    const fit = stage(cv, W, H, draw); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 13. urban change, Sihanoukville 2015-2021 (Lesson 12) ---------- */
  window.EXTRA_SIMS["gee-urban"] = async (el) => {
    const { q, out, cv } = shell(el, "ការពង្រីកក្រុងព្រះសីហនុ ២០១៥–២០២១",
      `<label>ប្រៀបធៀប <input type="range" class="gu-x" min="0" max="100" value="50"></label>
       <label>ΔNDVI < <b class="gu-dv"></b> <input type="range" class="gu-d" min="-0.6" max="-0.05" step="0.05" value="-0.2"></label>
       <label>ΔNDBI > <b class="gu-bv"></b> <input type="range" class="gu-b" min="0" max="0.3" step="0.025" value="0.05"></label>
       <label><input type="checkbox" class="gu-m" checked> បង្ហាញសំណង់ថ្មី</label>`);
    const j = await (await fetch(new URL("shv_change.json", AG_DATA))).json(), bin = (s_) => Uint8Array.from(atob(s_), (c) => c.charCodeAt(0));
    const w = j.w, h = j.h, N = w * h, r15 = bin(j.y2015), r21 = bin(j.y2021), n15 = bin(j.ndvi2015), n21 = bin(j.ndvi2021);
    const band = (r, k, i) => r[k * N + i], ndbi = (r, i) => (band(r, 4, i) - band(r, 3, i)) / (band(r, 4, i) + band(r, 3, i) + 1e-9);
    const W = 640, H = 330, S = Math.min(300 / h, 420 / w), dw = w * S, dh = h * S;
    const draw = (ctx) => {
      const sx = +q(".gu-x").value / 100, td = +q(".gu-d").value, tb = +q(".gu-b").value, show = q(".gu-m").checked; q(".gu-dv").textContent = khn(td, 2); q(".gu-bv").textContent = khn(tb, 3);
      ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const img = ctx.createImageData(w, h); let cnt = 0;
      for (let i = 0; i < N; i++) { const x = i % w, r = x < sx * w ? r15 : r21;
        const d = n21[i] / 127.5 - n15[i] / 127.5, nb = ndbi(r21, i) - ndbi(r15, i), isNew = d < td && n21[i] / 127.5 - 1 < .3 && nb > tb; if (isNew) cnt++;
        let c = [band(r, 2, i), band(r, 1, i), band(r, 0, i)]; if (show && isNew && r === r21) c = [229, 57, 53];
        img.data.set([c[0], c[1], c[2], 255], i * 4); }
      const tmp = document.createElement("canvas"); tmp.width = w; tmp.height = h; tmp.getContext("2d").putImageData(img, 0, 0); ctx.imageSmoothingEnabled = false; ctx.drawImage(tmp, 10, 10, dw, dh);
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(10 + sx * dw, 10); ctx.lineTo(10 + sx * dw, 10 + dh); ctx.stroke();
      ctx.font = `bold 13px ${font()}`; ctx.fillStyle = "#fff"; ctx.textAlign = "left"; ctx.fillText("២០១៥", 16, 28); ctx.textAlign = "right"; ctx.fillText("២០២១", 4 + dw, 28);
      ctx.textAlign = "left"; ctx.fillStyle = "#263238"; ctx.font = `bold 15px ${font()}`; ctx.fillText("សំណង់/ដីទទេថ្មី", 450, 50);
      ctx.font = `bold 22px ${font()}`; ctx.fillStyle = "#c62828"; ctx.fillText(`${khn(cnt * 900 / 1e6, 2)} គម²`, 450, 84);
      ctx.font = `13px ${font()}`; ctx.fillStyle = "#263238"; ctx.fillText(`${khn(cnt / N * 100, 1)}% នៃ ${khn(N * 900 / 1e6, 1)} គម²`, 450, 108);
      ctx.fillStyle = "#607d8b"; ["ΔNDVI < កម្រិត", "NDVI ២០២១ < ០,៣", "ΔNDBI > កម្រិត"].forEach((t_, k) => ctx.fillText("• " + t_, 450, 150 + k * 22));
      out.innerHTML = `អូសរបារ «ប្រៀបធៀប» ដើម្បីមើលរូបភាពពីរឆ្នាំ។ ក្រហម = ក្រឡាដែលបំពេញលក្ខខណ្ឌទាំងបី (បង្ហាញតែលើផ្នែក ២០២១)។ ` + (td > -.15 ? "កម្រិត ΔNDVI តូចពេក៖ ដំណាំ និងរុក្ខជាតិប្ដូរតាមរដូវ ត្រូវបានរាប់។" : "") +
        `<br><span class="sim-hint">Sentinel-2 ពិត · ក្រុងព្រះសីហនុ ២០១៥ និង ២០២១ · ក្រឡា ៣០ ម · ពណ៌ពង្រីកពន្លឺសម្រាប់មើល · NDVI ពិតពី GeoTIFF ដើម · NDBI ប្រហាក់ប្រហែលពីក្រុមរលកដែលបានពង្រីកពន្លឺ</span>`;
    };
    const fit = stage(cv, W, H, draw); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit)); fit();
  };

  /* ---------- 14. weighted overlay (Lesson 13) ---------- */
  window.EXTRA_SIMS["gee-mcda"] = async (el) => {
    const NAMES = ["ជម្រាល", "ចម្ងាយពីដំណាំ", "ដីឥដ្ឋ", "ទឹកភ្លៀង"], AHP = [47, 16, 28, 9];
    const { q, out, cv } = shell(el, "ទម្ងន់ និងភាពសមស្រប (WLC)",
      NAMES.map((nm, i) => `<label>${nm} <b class="gm-v${i}"></b> <input type="range" class="gm-w${i}" min="0" max="100" value="${AHP[i]}"></label>`).join("") +
      `<button type="button" class="gm-ahp">AHP</button><button type="button" class="gm-eq">ស្មើគ្នា</button>`);
    const j = await (await fetch(new URL("dem_synthetic.json", AG_DATA))).json(), n = j.n, N = n * n;
    const bs = atob(j.zr), z = new Float32Array(N); for (let i = 0; i < N; i++) z[i] = (bs.charCodeAt(2 * i) | (bs.charCodeAt(2 * i + 1) << 8)) * j.scale;
    const sl = new Float32Array(N); for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { const g = (yy, xx) => z[Math.min(n - 1, Math.max(0, yy)) * n + Math.min(n - 1, Math.max(0, xx))];
      sl[y * n + x] = Math.atan(Math.hypot((g(y, x + 1) - g(y, x - 1)) / 60, (g(y + 1, x) - g(y - 1, x)) / 60)) * 180 / Math.PI; }
    const zs = Array.from(z).sort((a, b) => a - b), z55 = zs[Math.floor(N * .55)], z85 = zs[Math.floor(N * .85)];
    const crop = new Uint8Array(N); for (let i = 0; i < N; i++) crop[i] = sl[i] < 3 && z[i] < z55 ? 1 : 0;
    const dist = new Float32Array(N).fill(1e9);                                     // two-pass chamfer distance (m)
    for (let i = 0; i < N; i++) if (crop[i]) dist[i] = 0;
    for (let pass = 0; pass < 2; pass++) for (let k = 0; k < N; k++) { const i = pass ? N - 1 - k : k, y = Math.floor(i / n), x = i % n, s_ = pass ? 1 : -1;
      for (const [dy, dx, c] of [[0, s_, 30], [s_, 0, 30], [s_, s_, 42], [s_, -s_, 42]]) { const yy = y + dy, xx = x + dx; if (yy >= 0 && yy < n && xx >= 0 && xx < n) dist[i] = Math.min(dist[i], dist[yy * n + xx] + c); } }
    let sd = 31; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647); const noise = (sc) => { const g = new Float32Array(N); const m = Math.ceil(n / sc) + 2, c = Array.from({ length: m * m }, rnd);
      for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) { const fy = y / sc, fx = x / sc, y0 = Math.floor(fy), x0 = Math.floor(fx), u = fy - y0, v = fx - x0, at = (a, b) => c[a * m + b];
        g[y * n + x] = (at(y0, x0) * (1 - v) + at(y0, x0 + 1) * v) * (1 - u) + (at(y0 + 1, x0) * (1 - v) + at(y0 + 1, x0 + 1) * v) * u; } return g; };
    const nc = noise(20), clay = new Float32Array(N), rain = new Float32Array(N);
    for (let i = 0; i < N; i++) { const y = Math.floor(i / n) / n; clay[i] = 10 + 45 * nc[i]; rain[i] = 1300 + 500 * y + 60 * (nc[(i * 7) % N] - .5); }
    const cl = (v) => Math.max(0, Math.min(1, v)); const F = [new Float32Array(N), new Float32Array(N), new Float32Array(N), new Float32Array(N)], cons = new Uint8Array(N);
    for (let i = 0; i < N; i++) { F[0][i] = 1 - cl((sl[i] - 1) / 5); F[1][i] = 1 - cl(dist[i] / 1500); F[2][i] = cl((clay[i] - 15) / 30); F[3][i] = cl((rain[i] - 1300) / 600); cons[i] = sl[i] > 8 || z[i] > z85 ? 1 : 0; }
    const top = (w) => { const s_ = w.reduce((a, b) => a + b, 0) || 1, S = new Float32Array(N); for (let i = 0; i < N; i++) S[i] = cons[i] ? -1 : (w[0] * F[0][i] + w[1] * F[1][i] + w[2] * F[2][i] + w[3] * F[3][i]) / s_;
      const v = Array.from(S).filter((x) => x >= 0).sort((a, b) => a - b); return { S, p90: v[Math.floor(v.length * .9)] }; };
    const ref = top(AHP), W = 640, H = 330;
    const draw = (ctx) => {
      const w = NAMES.map((_, i) => +q(".gm-w" + i).value), s_ = w.reduce((a, b) => a + b, 0) || 1; NAMES.forEach((_, i) => q(".gm-v" + i).textContent = kh(Math.round(w[i] / s_ * 100)) + "%");
      const { S, p90 } = top(w); ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); const img = ctx.createImageData(n, n); let both = 0, cnt = 0, rc = 0;
      const P = [[215, 25, 28], [253, 174, 97], [255, 255, 191], [166, 217, 106], [26, 150, 65]];
      for (let i = 0; i < N; i++) { let c; if (S[i] < 0) c = [200, 200, 200]; else { const t = cl((S[i] - .2) / .7) * 4, k = Math.min(3, Math.floor(t)), u = t - k; c = P[k].map((a, m) => a + (P[k + 1][m] - a) * u); }
        const isTop = S[i] >= p90, isRef = ref.S[i] >= ref.p90; if (isTop) { cnt++; c = [106, 27, 154]; } if (isRef) rc++; if (isTop && isRef) both++;
        img.data.set([c[0], c[1], c[2], 255], i * 4); }
      const tmp = document.createElement("canvas"); tmp.width = n; tmp.height = n; tmp.getContext("2d").putImageData(img, 0, 0); ctx.imageSmoothingEnabled = false; ctx.drawImage(tmp, 10, 10, 310, 310);
      ctx.textAlign = "left"; ctx.font = `bold 15px ${font()}`; ctx.fillStyle = "#263238"; ctx.fillText("ទម្ងន់", 345, 34); ctx.font = `13px ${font()}`;
      NAMES.forEach((nm, i) => { const y = 50 + i * 30; ctx.fillStyle = "#263238"; ctx.fillText(nm, 345, y + 14); ctx.fillStyle = ["#1565c0", "#43a047", "#8d6e63", "#0288d1"][i]; ctx.fillRect(460, y, 150 * w[i] / s_, 18); });
      const ov = both / Math.max(1, rc) * 100; ctx.fillStyle = "#263238"; ctx.font = `bold 15px ${font()}`; ctx.fillText(`ត្រួត top ១០% AHP៖ ${kh(Math.round(ov))}%`, 345, 200);
      ctx.font = `13px ${font()}`; ctx.fillStyle = "#6a1b9a"; ctx.fillText("■ ល្អបំផុត ១០%", 345, 228); ctx.fillStyle = "#9e9e9e"; ctx.fillText("■ ឧបសគ្គ (ជម្រាល > ៨° · ទីខ្ពស់)", 345, 250);
      out.innerHTML = (ov > 85 ? "ទីតាំងល្អបំផុតស្ទើរមិនប្ដូរ៖ លទ្ធផលរឹងមាំចំពោះទម្ងន់ទាំងនេះ។" : ov > 60 ? "ទីតាំងល្អបំផុតប្ដូរមួយផ្នែក៖ ពិនិត្យថាតំបន់ណានៅល្អក្នុងគ្រប់សេណារីយ៉ូ។" : "ទីតាំងល្អបំផុតប្ដូរច្រើន៖ ការសម្រេចពឹងខ្លាំងលើទម្ងន់ ដូច្នេះត្រូវពិភាក្សាទម្ងន់ជាមួយអ្នកជំនាញ។") +
        `<br><span class="sim-hint">ស្រទាប់ក្លែងធ្វើលើ DEM គំរូ · ទម្ងន់ AHP ពីម៉ាទ្រីសក្នុងមេរៀន (CR ≈ ០,០១) · ស្វាយ = ក្រឡាល្អបំផុត ១០% ក្រោមទម្ងន់បច្ចុប្បន្ន</span>`;
    };
    const fit = stage(cv, W, H, draw); el.querySelectorAll("input").forEach((i) => i.addEventListener("input", fit));
    const setW = (a) => { a.forEach((v, i) => q(".gm-w" + i).value = v); fit(); };
    q(".gm-ahp").addEventListener("click", () => setW(AHP)); q(".gm-eq").addEventListener("click", () => setW([25, 25, 25, 25])); fit();
  };

  /* ---------- 15. app events demo (Lesson 14) ---------- */
  window.EXTRA_SIMS["gee-app"] = (el) => {
    const yrs = []; for (let y = 2016; y <= 2021; y++) yrs.push(`<option${y === 2020 ? " selected" : ""}>${y}</option>`);
    const { q, out, cv } = shell(el, "កម្មវិធីតាមដានទឹក (គំរូ)",
      `<label>yearSel <select class="ga-y">${yrs.join("")}</select></label>
       <label>monthSl <b class="ga-mv"></b> <input type="range" class="ga-m" min="1" max="12" value="10"></label>
       <label><input type="checkbox" class="ga-g"> ប្រើ getInfo() (មិនណែនាំ)</label>`);
    const W = 640, H = 330, MON = ["មក", "កម", "មន", "មស", "ឧស", "មថ", "កក", "សហ", "កញ", "តល", "វច", "ធន"];
    const area = (y, m) => 2700 + (7200 + (y % 3) * 500) * Math.pow((1 + Math.cos(2 * Math.PI * (m - 9.5) / 12)) / 2, 1.5);
    const log = []; let info = "ចុចលើផែនទី…", busy = false, pt = null;
    const addLog = (t) => { log.unshift(t); log.length = Math.min(log.length, 7); };
    const draw = (ctx) => {
      const y = +q(".ga-y").value, m = +q(".ga-m").value; q(".ga-mv").textContent = kh(m); ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = "#e8f5e9"; ctx.fillRect(10, 10, 300, 200); const a = area(y, m), r = Math.sqrt(a) * 1.05;
      ctx.fillStyle = "#1565c0"; ctx.beginPath(); ctx.ellipse(160, 110, r * 1.3, r * .6, -.5, 0, 7); ctx.fill();
      ctx.fillStyle = "#0d47a1"; ctx.beginPath(); ctx.ellipse(160, 110, 45, 20, -.5, 0, 7); ctx.fill();
      if (pt) { ctx.fillStyle = "#c62828"; ctx.beginPath(); ctx.arc(pt[0], pt[1], 5, 0, 7); ctx.fill(); }
      ctx.font = `12px ${font()}`; ctx.fillStyle = "#263238"; ctx.textAlign = "left"; ctx.fillText(`ផែនទី · ទឹក ${kh(y)}-${kh(m)}`, 16, 26);
      const x0 = 330, y0 = 20, w = 290, h = 110, vals = Array.from({ length: 12 }, (_, k) => area(y, k + 1));
      ctx.fillText(`ផ្ទៃទឹក ${kh(y)} (គម²)`, x0, y0 + 6);
      vals.forEach((v, k) => { ctx.fillStyle = k + 1 === m ? "#ef6c00" : "#90caf9"; const hh = v / 11000 * h; ctx.fillRect(x0 + k * w / 12, y0 + 12 + h - hh, w / 12 - 3, hh); ctx.fillStyle = "#607d8b"; ctx.fillText(MON[k], x0 + k * w / 12, y0 + h + 26); });
      ctx.fillStyle = busy ? "#ef6c00" : "#263238"; ctx.font = `bold 13px ${font()}`; ctx.fillText("info៖ " + info, 10, 232);
      ctx.fillStyle = "#263238"; ctx.font = `bold 12px ${font()}`; ctx.fillText("កំណត់ហេតុ callback", 330, 186); ctx.font = `11px monospace`;
      log.forEach((t, k) => { ctx.fillStyle = k === 0 ? "#1565c0" : "#78909c"; ctx.fillText(t, 330, 206 + k * 17); });
      out.innerHTML = `ផ្ទៃទឹកខែនេះ ≈ ${khn(Math.round(a))} គម² (តម្លៃគំរូ)។ ` + (q(".ga-g").checked ? "ជាមួយ getInfo() ការរំកិល និងការចុចរង់ចាំ ១ វិនាទី ហើយកម្មវិធីទាំងមូលកក។" : "evaluate() បង្ហាញ «កំពុងគណនា…» ហើយកម្មវិធីនៅតែឆ្លើយតប។") +
        `<br><span class="sim-hint">កម្មវិធីក្លែងធ្វើ ដែលធ្វើតាមរចនាសម្ព័ន្ធក្នុងមេរៀន · ផ្ទៃទឹក និងភាពញឹកញាប់ជាតម្លៃគំរូ</span>`;
    };
    const fit = stage(cv, W, H, draw);
    const block = (ms) => { const t = Date.now(); while (Date.now() - t < ms) {} };
    q(".ga-y").addEventListener("change", (e) => { addLog(`yearSel.onChange('${e.target.value}') → refresh() · yearChart()`); if (q(".ga-g").checked) block(1000); fit(); });
    q(".ga-m").addEventListener("input", (e) => { addLog(`monthSl.onChange(${e.target.value}) → layers().set(0)`); if (q(".ga-g").checked) block(1000); fit(); });
    cv.addEventListener("click", (e) => { const b = cv.getBoundingClientRect(), x = (e.clientX - b.left) / b.width * W, y = (e.clientY - b.top) / b.height * H; if (x > 310 || y > 210) return;
      pt = [x, y]; const d = Math.hypot((x - 160) / 1.4, (y - 110) / .7), v = Math.max(0, Math.min(100, Math.round(100 - d * 1.2)));
      addLog(`map.onClick({lon, lat}) → layers().set(1)`);
      if (q(".ga-g").checked) { block(1000); info = v ? `មានទឹក ${kh(v)}% នៃពេលវេលា` : "មិនដែលមានទឹក"; addLog("getInfo() ← " + v); fit(); return; }
      info = "កំពុងគណនា…"; busy = true; addLog("evaluate(callback) … ស្នើរួច"); fit();
      setTimeout(() => { busy = false; info = v ? `មានទឹក ${kh(v)}% នៃពេលវេលា` : "មិនដែលមានទឹក"; addLog("callback(v = " + v + ") → info.setValue()"); fit(); }, 700); });
    addLog("refresh() · yearChart(2020)  (ពេលចាប់ផ្ដើម)"); fit();
  };

  /* ---------- 16. data-ethics scenarios (Lesson 15) ---------- */
  window.EXTRA_SIMS["gee-ethics"] = (el) => {
    const SC = [
      { t: "អ្នកធ្វើផែនទីការបាត់បង់ព្រៃជុំវិញភូមិមួយ ហើយក្រឡាបាត់បង់ខ្លះនៅជាប់ដីផ្ទះគ្រួសារ។ អ្នកនឹងចែករំលែកយ៉ាងណា?",
        o: [["បង្ហោះផែនទីលម្អិតលើបណ្ដាញសង្គម ដាក់ចំណងជើង «កាប់ព្រៃខុសច្បាប់»", 0, "ទិន្នន័យមិនប្រាប់ថាស្របច្បាប់ ឬអត់ទេ ហើយក្រឡាខ្លះអាចជាចម្ការ។ ការចោទប្រកាន់អាចធ្វើឲ្យគ្រួសាររងគ្រោះ។"],
            ["ពិនិត្យគំរូ ពិភាក្សាជាមួយមន្ត្រី និងសហគមន៍ ហើយរាយការណ៍ជាស្ថិតិតាមឃុំ", 2, "ល្អ៖ ផ្ទៀងផ្ទាត់ ការចូលរួម និងកម្រិតសរុប កាត់បន្ថយគ្រោះថ្នាក់ ដោយនៅតែផ្ដល់ព័ត៌មាន។"],
            ["មិនចែករំលែកអ្វីទាំងអស់", 1, "ការពារគ្រោះថ្នាក់ ប៉ុន្តែព័ត៌មានដែលមានប្រយោជន៍ក៏បាត់ដែរ។ ជាញឹកញាប់មានវិធីចែករំលែកដោយសុវត្ថិភាព។"]] },
      { t: "អ្នកប្រើ Open Buildings ដើម្បីរាប់ផ្ទះក្នុងតំបន់លិចទឹក សម្រាប់ផែនការជំនួយ។ តំបន់ភ្នំមួយស្ទើរតែគ្មានអគារក្នុងទិន្នន័យ។",
        o: [["យកលទ្ធផលដដែល៖ ទិន្នន័យបង្ហាញថាគ្មានមនុស្សនៅទីនោះ", 0, "ទិន្នន័យសកលអាចខកផ្ទះដំបូលស្លឹក ឬក្រោមដើមឈើ។ សហគមន៍នោះអាចត្រូវបានមើលរំលង។"],
            ["ពិនិត្យរូបភាព និងទិន្នន័យជំរឿន ហើយរាយការណ៍ថាទិន្នន័យអាចខកតំបន់នោះ", 2, "ល្អ៖ ពិនិត្យថាអ្នកណាមិនមាននៅក្នុងទិន្នន័យ គឺជាផ្នែកនៃយុត្តិធម៌។"],
            ["ដកតំបន់នោះចេញពីការវិភាគ", 1, "ភាពស្មោះត្រង់អំពីការខ្វះទិន្នន័យល្អ ប៉ុន្តែការដកចេញ អាចមានន័យថាគ្មានជំនួយ។"]] },
      { t: "ក្រុមអភិរក្សសុំឲ្យអ្នកបោះពុម្ពកម្មវិធីវេប ដែលបង្ហាញទីតាំងសំបុកបក្សីកម្រ ពី GPS ដែលពួកគេប្រមូល។",
        o: [["បោះពុម្ពទីតាំងពិតប្រាកដ ដើម្បីតម្លាភាព", 0, "ទីតាំងពិតអាចជួយអ្នកបរបាញ់។ តម្លាភាពមិនមានន័យថាបង្ហាញគ្រប់យ៉ាងទេ។"],
            ["បង្ហាញជាក្រឡា ១០ គម ឬកម្រិតស្រុក ហើយរក្សាទីតាំងពិតជាឯកជន", 2, "ល្អ៖ ការបន្ថយភាពលម្អិត (generalization) ការពារធនធាន ដោយនៅតែបង្ហាញលំនាំ។"],
            ["បង្ហាញទីតាំងពិត តែដាក់ពាក្យសម្ងាត់", 1, "កាត់បន្ថយហានិភ័យ ប៉ុន្តែពាក្យសម្ងាត់អាចលេចធ្លាយ។ ពិចារណាថាតើអ្នកណាពិតជាត្រូវការទីតាំងពិត។"]] },
      { t: "អ្នកប្រើផែនទីគម្របដី Dynamic World និង Sentinel-2 ក្នុងរបាយការណ៍ដែលអ្នកលក់ឲ្យក្រុមហ៊ុនឯកជន។",
        o: [["ទិន្នន័យឥតគិតថ្លៃ ដូច្នេះមិនចាំបាច់ដកស្រង់ទេ", 0, "ទិន្នន័យទាំងនេះទាមទារការដកស្រង់ ហើយការប្រើ Earth Engine សម្រាប់ពាណិជ្ជកម្មត្រូវការអាជ្ញាបណ្ណពាណិជ្ជកម្ម។"],
            ["ដកស្រង់ទិន្នន័យ និងពិនិត្យលក្ខខណ្ឌពាណិជ្ជកម្មរបស់ Earth Engine និងទិន្នន័យនីមួយៗ", 2, "ល្អ៖ អាជ្ញាបណ្ណ CC BY ទាមទារការដកស្រង់ ហើយ Earth Engine មានលក្ខខណ្ឌផ្សេងសម្រាប់ពាណិជ្ជកម្ម។"],
            ["ប្ដូរពណ៌ផែនទី ដើម្បីកុំឲ្យគេស្គាល់ប្រភព", 0, "នេះជាការលាក់ប្រភព៖ មិនស្មោះត្រង់ និងអាចបំពានអាជ្ញាបណ្ណ។"]] },
      { t: "ផែនទីភាពសមស្របរបស់អ្នក បង្ហាញថាដីរបស់សហគមន៍មួយ «សមស្របបំផុត» សម្រាប់កសិដ្ឋានសូឡា។ វិនិយោគិនមួយសុំទិន្នន័យ។",
        o: [["ផ្ដល់ផែនទីភ្លាមៗ៖ វាជាលទ្ធផលវិទ្យាសាស្ត្រ", 0, "ផែនទីមិនដឹងពីកម្មសិទ្ធិដី ឬតម្រូវការសហគមន៍ទេ ហើយអាចត្រូវប្រើដើម្បីដណ្ដើមដី។"],
            ["ពន្យល់ដែនកំណត់ ហើយណែនាំឲ្យពិគ្រោះសហគមន៍ និងអាជ្ញាធរ មុនការសម្រេច", 2, "ល្អ៖ ផែនទីភាពសមស្របជាឧបករណ៍ពិភាក្សា មិនមែនការសម្រេចទេ។"],
            ["កែទម្ងន់ ដើម្បីកុំឲ្យដីសហគមន៍លេចជាសមស្រប", 0, "ការកែលទ្ធផលតាមចិត្ត បំពានតម្លាភាព។ ដាក់ដីសហគមន៍ជាឧបសគ្គដោយបើកចំហ ប្រសិនបើនោះជាការសម្រេចរបស់អ្នកពាក់ព័ន្ធ។"]] }];
    const { q, out, cv } = shell(el, "សេណារីយ៉ូក្រមសីលធម៌", `<span class="sim-seg ge-s">${SC.map((_, i) => `<button type="button" data-s="${i}"${i ? "" : ' class="on"'}>${kh(i + 1)}</button>`).join("")}</span>`);
    const W = 640, H = 330, ans = new Array(SC.length).fill(null); let boxes = [];
    const wrap = (ctx, t, x, y, w, lh) => { const words = t.split(/(?<=[ ៖។,])/); let line = "", yy = y; for (const wd of words) { if (ctx.measureText(line + wd).width > w && line) { ctx.fillText(line, x, yy); line = wd; yy += lh; } else line += wd; } ctx.fillText(line, x, yy); return yy; };
    const draw = (ctx) => {
      const s_ = +q(".ge-s .on").dataset.s, S = SC[s_]; ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H); ctx.textAlign = "left"; ctx.fillStyle = "#263238"; ctx.font = `bold 14px ${font()}`;
      let y = wrap(ctx, S.t, 16, 28, 600, 22) + 16; boxes = []; ctx.font = `13px ${font()}`;
      S.o.forEach(([t], k) => { const h = 50, sel = ans[s_] === k, sc = S.o[k][1]; ctx.fillStyle = sel ? (sc === 2 ? "#e8f5e9" : sc === 1 ? "#fff8e1" : "#ffebee") : "#fafafa"; ctx.strokeStyle = sel ? "#607d8b" : "#cfd8dc";
        ctx.fillRect(16, y, 608, h); ctx.strokeRect(16, y, 608, h); ctx.fillStyle = "#263238"; wrap(ctx, `${["ក", "ខ", "គ"][k]}. ${t}`, 26, y + 20, 588, 18); boxes.push([y, y + h, k]); y += h + 8; });
      const done = ans.filter((a) => a !== null).length, score = ans.reduce((a, v, i) => a + (v === null ? 0 : SC[i].o[v][1]), 0);
      if (ans[s_] !== null) { const [, sc, fb] = S.o[ans[s_]]; out.innerHTML = `<b>${sc === 2 ? "ល្អ" : sc === 1 ? "អាចទទួលយកបាន" : "មានហានិភ័យ"}</b>៖ ${fb}`; }
      else out.innerHTML = "ចុចលើចម្លើយដែលអ្នកគិតថាសមបំផុត។";
      out.innerHTML += `<br><span class="sim-hint">បានឆ្លើយ ${kh(done)}/${kh(SC.length)} · ពិន្ទុ ${kh(score)}/${kh(SC.length * 2)} · មិនមានចម្លើយតែមួយដែលត្រូវរាល់ពេលទេ៖ ពិភាក្សាជាមួយក្រុម</span>`;
    };
    const fit = stage(cv, W, H, draw);
    cv.addEventListener("click", (e) => { const b = cv.getBoundingClientRect(), y = (e.clientY - b.top) / b.height * H; const hit = boxes.find(([a, c]) => y >= a && y <= c); if (hit) { ans[+q(".ge-s .on").dataset.s] = hit[2]; fit(); } });
    el.addEventListener("seg", fit); seg(el, "ge-s"); fit();
  };
})();
