# លំហាត់ទី១១៖ ស្រែពី Sentinel-1

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១១៖ កសិកម្ម និងការធ្វើផែនទីស្រែ](../lessons/lesson-11.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១៤០ នាទី

## ស្ថានភាព

អ្នកនឹងធ្វើផែនទីស្រូវវស្សាឆ្នាំ ២០២៤ សម្រាប់ខេត្តរបស់អ្នក ពី Sentinel-1 VH ដោយវិធីពីរ (ក្បួនកម្រិត និង Random Forest) ផ្ទៀងផ្ទាត់ដោយចំណុចដែលអ្នកប្រមូលពីរូបភាព ហើយគណនាផ្ទៃតាមស្រុក។

## គោលបំណង

- ទាញ និងបកស្រាយស៊េរី VH នៃស្រែ និងគម្របដីផ្សេង។
- បង្កើតស៊េរី ១២ ថ្ងៃ លក្ខណៈ vhMin និង rise ហើយកំណត់កម្រិតពីទិន្នន័យ។
- បណ្ដុះបណ្ដាល Random Forest លើ VH ប្រចាំខែ ហើយប្រៀបធៀបជាមួយក្បួន។
- គណនាផ្ទៃស្រូវតាមស្រុក ហើយនាំចេញ។

<figure markdown>
--8<-- "assets/svg/agv/lab11-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី១១ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- `COPERNICUS/S1_GRD` · `JRC/GSW1_4/GlobalSurfaceWater` · `USGS/SRTMGL1_003` · `ESA/WorldCover/v200` · `FAO/GAUL/2015/level1` · `level2`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-rice"></div>

រកកម្រិតដែលផ្ដល់ភាពត្រឹមត្រូវខ្ពស់បំផុត។ ប្ដូរ «ភាពខុសគ្នា» (ភាពប្រែប្រួលក្នុងថ្នាក់) ហើយមើលថាកម្រិតល្អបំផុតប្ដូរឬទេ។

## សកម្មភាពទី១៖ ចំណុចគំរូ · ៣០ នាទី

ដោយប្រើ Geometry Tools និងផែនទី Satellite បង្កើតស្រទាប់ពីរ៖ `ricePts` (ស្រែ · property `rice` = ១) និង `otherPts` (ភូមិ ព្រៃ ដំណាំដទៃ ទឹក · `rice` = ០) យ៉ាងហោចណាស់ ៦០ ចំណុចក្នុងមួយស្រទាប់ រាយពេញខេត្ត។ ពិនិត្យស្រែដោយក្រាប VH (សកម្មភាពទី២) ប្រសិនបើមិនប្រាកដ។

```javascript
var points = ricePts.merge(otherPts).randomColumn('r', 11);
var cal = points.filter(ee.Filter.lt('r', 0.5));     // សម្រាប់កែកម្រិត និងបណ្ដុះបណ្ដាល
var val = points.filter(ee.Filter.gte('r', 0.5));    // សម្រាប់ផ្ទៀងផ្ទាត់ប៉ុណ្ណោះ
Export.table.toAsset({collection: points, description: 'rice_points_2024', assetId: 'rice_points_2024'});
```

## សកម្មភាពទី២៖ ស៊េរី VH · ២០ នាទី

```javascript
var aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Takeo'));   // ខេត្តរបស់អ្នក
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(aoi)
  .filter(ee.Filter.eq('instrumentMode', 'IW')).filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
  .filterDate('2024-04-01', '2025-01-15').select('VH');
var start = ee.Date('2024-04-01');
var series = ee.ImageCollection.fromImages(ee.List.sequence(0, 23).map(function(k) {
  var d = start.advance(ee.Number(k).multiply(12), 'day'), sub = s1.filterDate(d, d.advance(12, 'day'));
  var empty = ee.Image.constant(0).rename('VH').updateMask(0);
  return ee.Image(ee.Algorithms.If(sub.size().gt(0), sub.median().focalMedian(30, 'circle', 'meters'), empty))
    .set('system:time_start', d.millis());
}));
print(ui.Chart.image.seriesByRegion({imageCollection: series, regions: cal.limit(6), reducer: ee.Reducer.mean(),
  band: 'VH', scale: 10, seriesProperty: 'rice'}).setOptions({title: 'VH ១២ ថ្ងៃ (១ = ស្រែ)'}));
```

ពីក្រាប កំណត់រយៈពេលស្ទូង (VH ទាបបំផុត) និងរយៈពេលលូតលាស់ សម្រាប់ខេត្តរបស់អ្នក។

## សកម្មភាពទី៣៖ ក្បួនកម្រិត · ២៥ នាទី

```javascript
var vhMin = series.filterDate('2024-06-01', '2024-09-15').min().rename('vhMin');   // កែតាមក្រាប
var rise = series.filterDate('2024-07-15', '2024-11-15').max().subtract(vhMin).rename('rise');
var feats = vhMin.addBands(rise);
var calVals = feats.sampleRegions({collection: cal, properties: ['rice'], scale: 10});
print(ui.Chart.feature.groups(calVals, 'vhMin', 'rise', 'rice').setChartType('ScatterChart')
  .setOptions({title: 'vhMin និង rise តាមចំណុច', hAxis: {title: 'vhMin (dB)'}, vAxis: {title: 'rise (dB)'}}));
var T_MIN = -19, T_RISE = 5;                                // កែតាម scatter
var jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('seasonality').unmask(0);
var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var wc = ee.ImageCollection('ESA/WorldCover/v200').first();
var ruleRice = vhMin.lt(T_MIN).and(rise.gt(T_RISE)).updateMask(jrc.lt(10)).updateMask(slope.lt(5)).updateMask(wc.neq(50))
  .unmask(0).clip(aoi).rename('classification');
Map.centerObject(aoi, 10);
Map.addLayer(ruleRice.selfMask(), {palette: ['#2e7d32']}, 'ស្រែ (ក្បួន)');
```

## សកម្មភាពទី៤៖ Random Forest និងការប្រៀបធៀប · ៣០ នាទី

```javascript
var names = ['VH_05', 'VH_06', 'VH_07', 'VH_08', 'VH_09', 'VH_10', 'VH_11'];
var monthly = ee.ImageCollection.fromImages(ee.List.sequence(5, 11).map(function(m) {
  var d = ee.Date.fromYMD(2024, m, 1); return s1.filterDate(d, d.advance(1, 'month')).median();
})).toBands().rename(names).addBands(feats).clip(aoi);
var clf = ee.Classifier.smileRandomForest({numberOfTrees: 100, seed: 1}).train({
  features: monthly.sampleRegions({collection: cal, properties: ['rice'], scale: 10}),
  classProperty: 'rice', inputProperties: monthly.bandNames()});
var rfRice = monthly.classify(clf).updateMask(jrc.lt(10)).updateMask(slope.lt(5)).unmask(0).clip(aoi).rename('classification');
Map.addLayer(rfRice.selfMask(), {palette: ['#1565c0']}, 'ស្រែ (RF)', false);
function acc(img, name) {
  var cm = img.sampleRegions({collection: val, properties: ['rice'], scale: 10}).errorMatrix('rice', 'classification');
  print(name, 'OA', cm.accuracy(), 'PA', cm.producersAccuracy(), 'UA', cm.consumersAccuracy());
}
acc(ruleRice, 'ក្បួន'); acc(rfRice, 'RF');
```

## សកម្មភាពទី៥៖ ផ្ទៃតាមស្រុក · ២៥ នាទី

```javascript
var districts = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.eq('ADM1_NAME', 'Takeo'));
var haImg = ee.Image.pixelArea().divide(1e4);
var areas = haImg.updateMask(ruleRice.eq(1)).rename('rule_ha').addBands(haImg.updateMask(rfRice.eq(1)).rename('rf_ha'))
  .reduceRegions({collection: districts, reducer: ee.Reducer.sum(), scale: 10, tileScale: 16});
Export.table.toDrive({collection: areas, description: 'rice_area_2024', folder: 'applied_gis', fileFormat: 'CSV',
  selectors: ['ADM2_CODE', 'ADM2_NAME', 'rule_ha', 'rf_ha']});
Export.image.toDrive({image: ruleRice.toByte(), description: 'rice_rule_2024', folder: 'applied_gis',
  region: aoi.geometry(), scale: 10, crs: 'EPSG:32648', maxPixels: 1e10});
```

ប្រសិនបើអ្នកមានស្ថិតិផ្ទៃស្រូវតាមស្រុក (ពីមន្ទីរកសិកម្ម) សូមបន្ថែមជួរឈរមួយក្នុង Excel ហើយគូរក្រាប scatter ផែនទី ធៀបនឹងស្ថិតិ។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a11-rules.svg"
<figcaption>លទ្ធផលគំរូ ១៖ លក្ខខណ្ឌពីរ បែងចែកស្រែបាន។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - ទឹកអចិន្ត្រៃយ៍មាន min ទាប ប៉ុន្តែមិនឡើងវិញ៖ លក្ខខណ្ឌទីពីរកាត់វាចេញ។
    - ដំណាំដទៃ និងព្រៃមិនធ្លាក់ដល់ −១៩ dB៖ លក្ខខណ្ឌទីមួយកាត់វាចេញ។
    - កម្រិតក្នុងរូបនេះជាឧទាហរណ៍៖ ត្រូវកែតាមតំបន់ ដោយប្រើចំណុចស្រែដែលដឹង។

<figure markdown>
--8<-- "assets/svg/agv/a11-vh.svg"
<figcaption>លទ្ធផលគំរូ ២៖ ទាបពេលស្ទូង ខ្ពស់ពេលស្រូវធំ។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - ពេលស្ទូង វាលស្រែមានទឹក៖ VH ធ្លាក់ទាបដូចទឹក (−២២ ដល់ −២៥ dB)។
    - ពេលស្រូវលូតលាស់ ដើមស្រូវបង្កើនការចាំងត្រឡប់៖ VH ឡើង ៥–៩ dB។
    - ទឹកអចិន្ត្រៃយ៍ទាបជានិច្ច ព្រៃ និងទីក្រុងខ្ពស់ជានិច្ច៖ មិនមានទម្រង់ «ចុះ រួចឡើង» ទេ។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| ក្រាប VH លោតខ្លាំង | speckle · ចំណុចតែមួយក្រឡា | focalMedian · buffer(50) |
| min() បរាជ័យ band not found | ចន្លោះ ១២ ថ្ងៃគ្មានរូបភាព | ee.Algorithms.If ជាមួយរូបភាពទទេ |
| បឹងរាប់ជាស្រែ | rise តូចពេក ឬគ្មាន mask ទឹក | បង្កើន T_RISE · JRC seasonality |
| toBands ឈ្មោះចម្លែក (0_VH …) | ឈ្មោះលំនាំដើមនៃ toBands | rename(names) |
| OA ខ្ពស់ពេក | ចំណុចផ្ទៀងផ្ទាត់ប្រើកែកម្រិតផង | បំបែក cal / val មុន |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប និង Asset ចំណុច។
- ក្រាប VH និង scatter vhMin–rise ជាមួយកម្រិតដែលអ្នកជ្រើស និងហេតុផល។
- តារាងភាពត្រឹមត្រូវ ក្បួន ធៀបនឹង RF (OA PA UA)។
- CSV ផ្ទៃតាមស្រុក និងផែនទីស្រែពី QGIS។
- កថាខណ្ឌមួយ៖ វិធីណាល្អជាងសម្រាប់ខេត្តរបស់អ្នក ហើយហេតុអ្វី។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="VH" markdown>
**១.** ប៉ូលការីសាស្យុងណាដែលបង្ហាញការលូតលាស់ស្រូវបានច្បាស់ជាង?
</div>

<div class="self-check" data-answer="min|min()" markdown>
**២.** Reducer ណាលើស៊េរីក្នុងរយៈពេលស្ទូង ដែលចាប់សញ្ញាលិចទឹក?
</div>

<div class="self-check" data-answer="toBands|toBands()" markdown>
**៣.** មុខងារណាបម្លែង ImageCollection ប្រចាំខែ ទៅជារូបភាពមួយដែលមានក្រុមរលកច្រើន?
</div>

<div class="self-check" data-answer="50|៥០" markdown>
**៤.** ក្នុង ESA WorldCover តើតម្លៃណាជាតំបន់សំណង់ (built-up)?
</div>
