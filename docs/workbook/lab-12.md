# លំហាត់ទី១២៖ LST ភ្នំពេញ

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១២៖ ទីក្រុង ការពង្រីក និងសីតុណ្ហភាពផ្ទៃដី](../lessons/lesson-12.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១២៥ នាទី

## ស្ថានភាព

អ្នកនឹងរៀបចំ «ផែនទីកំដៅ» សម្រាប់ភ្នំពេញ៖ LST រដូវក្ដៅ UHI ទំនាក់ទំនង LST–NDVI តារាងខណ្ឌជាមួយប្រជាជន និងការពង្រីកទីក្រុងពីទិន្នន័យពីរប្រភព។

## គោលបំណង

- គណនា LST ជា °C ពី Landsat 8/9 C2 L2 ជាមួយការលុបពពក។
- គណនា UHI ដោយនិយមន័យជនបទពីរ។
- វាស់ទំនាក់ទំនង LST–NDVI ដោយ linearFit។
- ធ្វើតារាងខណ្ឌ (LST NDVI ប្រជាជន) ហើយប្រៀបធៀបការពង្រីកពី Dynamic World និង GHSL។

<figure markdown>
--8<-- "assets/svg/agv/lab12-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី១២ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- `LANDSAT/LC08/C02/T1_L2` · `LANDSAT/LC09/C02/T1_L2` · `ESA/WorldCover/v200` · `GOOGLE/DYNAMICWORLD/V1` · `JRC/GHSL/P2023A/GHS_BUILT_S` · `WorldPop/GP/100m/pop` · `FAO/GAUL/2015/level2`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-urban"></div>

រកកម្រិត ΔNDVI ដែលបង្ហាញសំណង់ថ្មីច្បាស់ ដោយមិនរាប់ព្រៃ ឬដំណាំដែលប្ដូរតាមរដូវ។

## សកម្មភាពទី១៖ LST រដូវក្ដៅ · ២៥ នាទី

```javascript
var aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Phnom Penh'));
function prepL(img) {
  var qa = img.select('QA_PIXEL');
  var clear = qa.bitwiseAnd(1 << 1).eq(0).and(qa.bitwiseAnd(1 << 3).eq(0)).and(qa.bitwiseAnd(1 << 4).eq(0));
  var lst = img.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15).rename('LST');
  var ndvi = img.select(['SR_B5', 'SR_B4']).multiply(0.0000275).add(-0.2).normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI');
  return lst.addBands(ndvi).updateMask(clear).copyProperties(img, ['system:time_start']);
}
var land = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').merge(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2'))
  .filterBounds(aoi).filterDate('2021-01-01', '2025-01-01').filter(ee.Filter.calendarRange(3, 5, 'month')).map(prepL);
var med = land.median().clip(aoi);
print('រូបភាព', land.size());
Map.centerObject(aoi, 11);
Map.addLayer(med.select('LST'), {min: 28, max: 45, palette: ['#313695', '#74add1', '#ffffbf', '#f46d43', '#a50026']}, 'LST (°C)');
Map.addLayer(land.select('LST').count().clip(aoi), {min: 0, max: 20, palette: ['red', 'white', 'green']}, 'ចំនួនការសង្កេតស្អាត', false);
```

## សកម្មភាពទី២៖ UHI និងនិយមន័យជនបទ · ២៥ នាទី

```javascript
var wc = ee.ImageCollection('ESA/WorldCover/v200').first();
var region = aoi.geometry().buffer(15000);
var lstR = land.select('LST').median();
function meanIn(mask, geom) {
  return ee.Number(lstR.updateMask(mask).reduceRegion({reducer: ee.Reducer.mean(), geometry: geom, scale: 30, maxPixels: 1e10, tileScale: 4}).get('LST'));
}
var tUrban = meanIn(wc.eq(50), aoi.geometry());
var ring = region.difference(aoi.geometry());
print('UHI (ជនបទ = ដំណាំ)', tUrban.subtract(meanIn(wc.eq(40), ring)));
print('UHI (ជនបទ = ព្រៃ + ស្មៅ)', tUrban.subtract(meanIn(wc.eq(10).or(wc.eq(30)), ring)));
```

ហេតុអ្វីតម្លៃទាំងពីរខុសគ្នា? តើមួយណាសមជាងសម្រាប់ការពិភាក្សាគោលនយោបាយ?

## សកម្មភាពទី៣៖ LST–NDVI · ២០ នាទី

```javascript
var fit = med.select(['NDVI', 'LST']).updateMask(wc.neq(80)).reduceRegion({reducer: ee.Reducer.linearFit(),
  geometry: aoi.geometry(), scale: 30, maxPixels: 1e10, tileScale: 4});
print('ជម្រាល', fit.get('scale'), 'offset', fit.get('offset'));
var sample = med.select(['NDVI', 'LST']).updateMask(wc.neq(80)).sample({region: aoi.geometry(), scale: 30, numPixels: 1000, seed: 3});
print(ui.Chart.feature.byFeature(sample, 'NDVI', 'LST').setChartType('ScatterChart')
  .setOptions({pointSize: 2, hAxis: {title: 'NDVI'}, vAxis: {title: 'LST (°C)'}}));
```

`wc.neq(80)` ដកទឹកអចិន្ត្រៃយ៍ចេញ ព្រោះវាមាន NDVI ទាប និង LST ទាប ហើយធ្វើឲ្យជម្រាលខុស។

## សកម្មភាពទី៤៖ តារាងខណ្ឌ · ២៥ នាទី

```javascript
var khan = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.eq('ADM1_NAME', 'Phnom Penh'));
var pop = ee.ImageCollection('WorldPop/GP/100m/pop').filter(ee.Filter.eq('country', 'KHM')).filter(ee.Filter.eq('year', 2020)).first();
var t = med.reduceRegions({collection: khan, reducer: ee.Reducer.mean(), scale: 30, tileScale: 4})
  .map(function(f) {
    var p = pop.reduceRegion({reducer: ee.Reducer.sum(), geometry: f.geometry(), scale: 100, maxPixels: 1e9}).values().get(0);
    var hot = med.select('LST').gt(40).multiply(100).reduceRegion({reducer: ee.Reducer.mean(), geometry: f.geometry(), scale: 30, maxPixels: 1e9}).get('LST');
    return f.set({pop: p, pct_hot: hot});
  });
print(t.select(['ADM2_NAME', 'LST', 'NDVI', 'pop', 'pct_hot']).sort('LST', false));
Export.table.toDrive({collection: t, description: 'pp_khan_heat', folder: 'applied_gis', fileFormat: 'CSV',
  selectors: ['ADM2_CODE', 'ADM2_NAME', 'LST', 'NDVI', 'pop', 'pct_hot']});
Export.image.toDrive({image: med.select('LST').toFloat(), description: 'pp_lst_hot_season', folder: 'applied_gis',
  region: aoi.geometry(), scale: 30, crs: 'EPSG:32648', maxPixels: 1e10});
```

## សកម្មភាពទី៥៖ ការពង្រីកពីពីរប្រភព · ២០ នាទី

```javascript
var km2 = ee.Image.pixelArea().divide(1e6);
function dwBuilt(y) {
  return ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1').filterBounds(aoi).filterDate(y + '-01-01', (y + 1) + '-01-01')
    .select('built').mean().gt(0.5);
}
function sumKm2(mask) { return km2.updateMask(mask).reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 10, maxPixels: 1e10, tileScale: 4}).get('area'); }
print('Dynamic World ២០១៧', sumKm2(dwBuilt(2017)), '២០២៤', sumKm2(dwBuilt(2024)));
var g15 = ee.Image('JRC/GHSL/P2023A/GHS_BUILT_S/2015').select('built_surface');
var g20 = ee.Image('JRC/GHSL/P2023A/GHS_BUILT_S/2020').select('built_surface');
print('GHSL ២០១៥ (គម²)', g15.divide(1e6).reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 100}),
      '២០២០', g20.divide(1e6).reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 100}));
```

GHSL built_surface ជា ម² សំណង់ក្នុងក្រឡានីមួយៗ ដូច្នេះការបូក ÷ ១ ០០០ ០០០ ផ្ដល់ គម² ដោយផ្ទាល់។ Dynamic World ប្រើកម្រិតប្រូបាប៊ីលីតេ ដូច្នេះលេខរបស់វាមិនស្មើ GHSL ទេ។ ប្រៀបធៀបអត្រាកើនឡើង មិនមែនតម្លៃដាច់ខាតទេ។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a12-lst-ndvi.svg"
<figcaption>លទ្ធផលគំរូ ១៖ រុក្ខជាតិធ្វើឲ្យត្រជាក់។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - តំបន់សាងសង់ (ក្រហម) និងដីទទេក្ដៅបំផុត ទឹក (ខៀវ) ត្រជាក់បំផុត។
    - ក្នុងចំណោមដី LST ថយនៅពេល NDVI កើន៖ ការបញ្ចេញចំហាយពីស្លឹកធ្វើឲ្យផ្ទៃត្រជាក់។
    - LST ក្នុងរូបនេះត្រូវបានក្លែងធ្វើពីគម្របដីពិត ដើម្បីបង្ហាញទំនាក់ទំនង៖ លំហាត់ទី១២ ប្រើ ST_B10 ពិត។

<figure markdown>
--8<-- "assets/svg/agv/a12-uhi.svg"
<figcaption>លទ្ធផលគំរូ ២៖ ទីក្រុងក្ដៅជាងជនបទជុំវិញ។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - UHI = LST មធ្យមក្នុងទីក្រុង − LST មធ្យមក្នុងជនបទជុំវិញ។
    - ទន្លេ បឹង និងឧទ្យាន បង្កើត «កោះត្រជាក់» ក្នុងទីក្រុង។
    - តម្លៃ UHI អាស្រ័យលើរបៀបកំណត់ «ជនបទ»៖ ស្រែស្ងួតក្នុងរដូវប្រាំងក៏ក្ដៅដែរ។ ផ្នែកកាត់នេះជាការក្លែងធ្វើ។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| LST ≈ ៤០០០០ ឬ −២៧៣ | ភ្លេចមាត្រដ្ឋាន ST_B10 | × 0.00341802 + 149 − 273.15 |
| ចំណុចត្រជាក់ខុសប្រក្រតី | ពពកមិនបាន mask | QA_PIXEL bits 1 3 4 |
| ជម្រាល LST–NDVI វិជ្ជមាន | ទឹកនៅក្នុងសំណាក | updateMask(wc.neq(80)) |
| pop = null | ឈ្មោះក្រុមរលក WorldPop | values().get(0) |
| GHSL image not found | ឈ្មោះយុគខុស | ប្រើ ១៩៧៥ … ២០៣០ រៀងរាល់ ៥ ឆ្នាំ |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- ផែនទី LST និងផែនទីចំនួនការសង្កេតស្អាត (រូបអេក្រង់)។
- តម្លៃ UHI ពីរ និងការពន្យល់ភាពខុសគ្នា។
- ជម្រាល LST–NDVI និងក្រាប scatter។
- CSV តារាងខណ្ឌ និងផែនទីអាទិភាពពី QGIS (LST × ប្រជាជន)។
- តារាងការពង្រីកពី Dynamic World និង GHSL ជាមួយកថាខណ្ឌពន្យល់។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="0.00341802|០,០០៣៤១៨០២|0,00341802" markdown>
**១.** ST_B10 ត្រូវគុណនឹងប៉ុន្មាន មុនបូក ១៤៩,០?
</div>

<div class="self-check" data-answer="3|៣" markdown>
**២.** ក្នុង QA_PIXEL តើ bit ណាជាពពក (cloud)?
</div>

<div class="self-check" data-answer="linearFit|ee.Reducer.linearFit|ee.Reducer.linearFit()" markdown>
**៣.** Reducer ណាផ្ដល់ជម្រាល និង offset នៃ LST ធៀបនឹង NDVI?
</div>

<div class="self-check" data-answer="built" markdown>
**៤.** ក្រុមរលកណានៃ Dynamic World ជាប្រូបាប៊ីលីតេសំណង់?
</div>
