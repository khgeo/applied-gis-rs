# លំហាត់ទី១៣៖ សមស្របភាពទីតាំង

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១៣៖ ការវិភាគពហុលក្ខខណ្ឌជាមួយទិន្នន័យ RS](../lessons/lesson-13.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · Excel/Python · QGIS · ប្រហែល ១៤០ នាទី

## ស្ថានភាព

អ្នកនឹងធ្វើការវិភាគភាពសមស្របពេញលេញមួយ សម្រាប់ខេត្តរបស់អ្នក៖ ជ្រើសសំណួរទីតាំង កំណត់កត្តា និងឧបសគ្គ គណនាទម្ងន់ AHP ធ្វើផែនទី WLC ពិនិត្យភាពរសើប ហើយនាំចេញទីតាំងបេក្ខភាព។

## គោលបំណង

- បម្លែងសំណួរទីតាំង ទៅជាកត្តា ៤–៥ និងឧបសគ្គ ៣–៥។
- គណនាទម្ងន់ AHP និង CR ពីម៉ាទ្រីសរបស់អ្នក។
- ធ្វើផែនទីភាពសមស្រប និងការវិភាគភាពរសើបបីសេណារីយ៉ូ។
- នាំចេញទីតាំងបេក្ខភាព ២០–៤០ ជា KML/SHP។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `USGS/SRTMGL1_003` · `ESA/WorldCover/v200` · `OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02` · `UCSB-CHG/CHIRPS/DAILY` · `JRC/GSW1_4/GlobalSurfaceWater` · `MERIT/Hydro/v1_0_1` · `WCMC/WDPA/current/polygons`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-mcda"></div>

ដាក់ទម្ងន់ទាំងអស់ស្មើគ្នា បន្ទាប់មកដាក់ជម្រាល ៧០%។ តើទីតាំងល្អបំផុតផ្លាស់ទីប៉ុណ្ណា?

## សកម្មភាពទី១៖ សំណួរ និងលក្ខខណ្ឌ · ២០ នាទី

ជ្រើសសំណួរមួយ៖ (ក) ស្រះសហគមន៍ (ដូចមេរៀន) (ខ) ជម្រកសង្គ្រោះពេលទឹកជំនន់ ឬ (គ) កសិដ្ឋានសូឡា។ សរសេរតារាង៖ លក្ខខណ្ឌ · កត្តា/ឧបសគ្គ · ទិន្នន័យ · ទិស (ច្រើនល្អ/តិចល្អ) · ចំណុចបត់ · ប្រភពនៃចំណុចបត់។ ឧទាហរណ៍សម្រាប់ (ខ)៖ HAND ខ្ពស់ល្អ (> ៥ ម) · ជិតភូមិ (< ២ គម) · ជិតផ្លូវ · ជម្រាលតិច · ឧបសគ្គ៖ ទឹក ព្រៃការពារ។

## សកម្មភាពទី២៖ ស្រទាប់ និងស្តង់ដារ · ៣០ នាទី

```javascript
var aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Kampong Speu'));   // ខេត្តរបស់អ្នក
Map.centerObject(aoi, 9);
function up(img, a, b) { return img.unitScale(a, b).clamp(0, 1); }
function down(img, a, b) { return ee.Image(1).subtract(up(img, a, b)); }
var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var wc = ee.ImageCollection('ESA/WorldCover/v200').first();
function distTo(mask) {
  return mask.selfMask().unmask(0).fastDistanceTransform(256).sqrt().multiply(ee.Image.pixelArea().sqrt())
    .reproject({crs: 'EPSG:32648', scale: 30});
}
var clay = ee.Image('OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02').select('b30');
var rain = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterDate('2004-01-01', '2024-01-01').sum().divide(20);
var F = ee.Image.cat([
  down(slope, 1, 6).rename('f1'),
  down(distTo(wc.eq(40)), 0, 1500).rename('f2'),
  up(clay, 15, 45).rename('f3'),
  up(rain, 1100, 1800).rename('f4')
]).clip(aoi);
var vis = {min: 0, max: 1, palette: ['#d7191c', '#ffffbf', '#1a9641']};
['f1', 'f2', 'f3', 'f4'].forEach(function(b) { Map.addLayer(F.select(b), vis, b, false); });
```

សម្រាប់សំណួរ (ខ) ឬ (គ) ប្ដូរកត្តាតាមតារាងរបស់អ្នក (ឧ. `ee.Image('MERIT/Hydro/v1_0_1').select('hnd')` សម្រាប់ HAND)។ បើកស្រទាប់នីមួយៗ ហើយពិនិត្យថាបៃតង = ល្អ។

## សកម្មភាពទី៣៖ AHP · ២៥ នាទី

បំពេញម៉ាទ្រីស ៤ × ៤ (មាត្រដ្ឋាន Saaty ១–៩) ក្នុង Excel ឬ Python៖

```python
import numpy as np
M = np.array([[1, 3, 2, 4], [1/3, 1, 1/2, 2], [1/2, 2, 1, 3], [1/4, 1/2, 1/3, 1]])   # ប្ដូរតាមការវិនិច្ឆ័យរបស់អ្នក
w, v = np.linalg.eig(M); k = np.argmax(w.real)
weights = np.abs(v[:, k].real); weights /= weights.sum()
CR = ((w[k].real - 4) / 3) / 0.90
print(weights.round(3), round(CR, 3))
```

ប្រសិនបើ CR ≥ ០,១ ពិនិត្យការវិនិច្ឆ័យដែលផ្ទុយគ្នា ហើយកែ។ កត់ត្រាទម្ងន់ចុងក្រោយ។

## សកម្មភាពទី៤៖ WLC ឧបសគ្គ និងភាពរសើប · ៣៥ នាទី

```javascript
var W_AHP = [0.47, 0.16, 0.28, 0.09];                              // ពីសកម្មភាពទី៣
var pa = ee.FeatureCollection('WCMC/WDPA/current/polygons').filter(ee.Filter.eq('ISO3', 'KHM'));
var jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').unmask(0);
var ok = ee.Image(1).paint(pa, 0).and(wc.neq(10)).and(wc.neq(50)).and(wc.neq(80)).and(jrc.lt(20)).and(slope.lt(8));
function wlc(w) {
  var s = w[0] + w[1] + w[2] + w[3];
  return F.select('f1').multiply(w[0] / s).add(F.select('f2').multiply(w[1] / s))
    .add(F.select('f3').multiply(w[2] / s)).add(F.select('f4').multiply(w[3] / s)).updateMask(ok).rename('S');
}
function top10(img) {
  var p = ee.Number(img.reduceRegion({reducer: ee.Reducer.percentile([90]), geometry: aoi.geometry(), scale: 90, maxPixels: 1e9}).get('S'));
  return img.gte(p);
}
var sA = wlc(W_AHP), sB = wlc([1, 1, 1, 1]), sC = wlc([4, 3, 2, 1]);
var robust = top10(sA).and(top10(sB)).and(top10(sC)).selfMask();
Map.addLayer(sA, {min: 0.2, max: 0.9, palette: ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']}, 'ភាពសមស្រប (AHP)');
Map.addLayer(robust, {palette: ['#6a1b9a']}, 'ល្អបំផុតក្នុងសេណារីយ៉ូទាំងបី');
var km2 = ee.Image.pixelArea().divide(1e6);
print('ផ្ទៃ top10 AHP', km2.updateMask(top10(sA)).reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 30, maxPixels: 1e10, tileScale: 4}),
      'ផ្ទៃរឹងមាំ', km2.updateMask(robust).reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 30, maxPixels: 1e10, tileScale: 4}));
```

ការ reduceRegion នៃ percentile ផ្ដល់គន្លឹះ `S` ព្រោះរូបភាពមានក្រុមរលកតែមួយ និង reducer តែមួយ។ ប្រសិនបើ print បង្ហាញ `S_p90` សូមប្ដូរឈ្មោះគន្លឹះ។

## សកម្មភាពទី៥៖ ទីតាំងបេក្ខភាព · ២០ នាទី

```javascript
var big = robust.updateMask(robust.connectedPixelCount(100, true).gte(20));
var sites = big.reduceToVectors({geometry: aoi.geometry(), scale: 30, geometryType: 'polygon', maxPixels: 1e10, tileScale: 4})
  .map(function(f) {
    return f.set({area_ha: f.geometry().area(10).divide(1e4),
                  score: sA.reduceRegion({reducer: ee.Reducer.mean(), geometry: f.geometry(), scale: 30}).get('S')});
  }).sort('score', false).limit(40);
Map.addLayer(sites, {color: 'purple'}, 'ទីតាំងបេក្ខភាព');
Export.table.toDrive({collection: sites, description: 'suitability_candidates', folder: 'applied_gis', fileFormat: 'KML'});
Export.image.toDrive({image: sA.toFloat(), description: 'suitability_ahp', folder: 'applied_gis', region: aoi.geometry(),
  scale: 30, crs: 'EPSG:32648', maxPixels: 1e10});
```

បើក KML ក្នុង Google Earth Pro ហើយពិនិត្យទីតាំង ៥ ល្អបំផុតដោយភ្នែក៖ តើមានអ្វីដែលទិន្នន័យមិនបានឃើញ (ផ្ទះ វត្ត ផ្លូវ)?

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តារាងលក្ខខណ្ឌ (សកម្មភាពទី១) ជាមួយប្រភពចំណុចបត់។
- ម៉ាទ្រីស AHP ទម្ងន់ និង CR។
- ផែនទីភាពសមស្រប និងផែនទីទីតាំងរឹងមាំ (រូបអេក្រង់ ឬ QGIS)។
- KML ទីតាំងបេក្ខភាព និងកំណត់ត្រាពិនិត្យដោយភ្នែកនៃ ៥ ទីតាំងល្អបំផុត។
- កថាខណ្ឌមួយ៖ ដែនកំណត់ និងជំហានបន្ទាប់ (វាល សហគមន៍ កម្មសិទ្ធិ)។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="unitScale|unitScale()" markdown>
**១.** មុខងារណាបម្លែងរូបភាពទៅចន្លោះ ០–១ តាមតម្លៃ a និង b?
</div>

<div class="self-check" data-answer="0.1|០,១|0,1" markdown>
**២.** CR ក្រោមប៉ុន្មានដែលចាត់ទុកថាទទួលយកបាន?
</div>

<div class="self-check" data-answer="fastDistanceTransform|fastDistanceTransform()" markdown>
**៣.** មុខងារណាគណនាចម្ងាយពីក្រឡាមួយប្រភេទ?
</div>

<div class="self-check" data-answer="reduceToVectors|reduceToVectors()" markdown>
**៤.** មុខងារណាបម្លែងក្រុមក្រឡាទៅជាពហុកោណ?
</div>
