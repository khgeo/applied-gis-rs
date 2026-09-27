# លំហាត់ទី៧៖ ផែនទីទឹកជំនន់ទន្លេសាប

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៧៖ ទឹកលើផ្ទៃដី និងទឹកជំនន់ដោយ Sentinel-1](../lessons/lesson-07.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១៣៥ នាទី

## ស្ថានភាព

ទន្លេសាបពង្រីកពីប្រហែល ២ ៥០០ គម² ក្នុងរដូវប្រាំង ដល់ជាង ១០ ០០០ គម² ក្នុងរដូវទឹកឡើង។ អ្នកនឹងធ្វើផែនទីផ្ទៃទឹកនៅពេលទាបបំផុត និងខ្ពស់បំផុតនៃឆ្នាំមួយ ពី Sentinel-1 គណនាផ្ទៃលិចតាមខេត្តជុំវិញបឹង ហើយប្រៀបធៀបជាមួយ JRC Global Surface Water។

## គោលបំណង

- ត្រង Sentinel-1 តាមគន្លងតែមួយ ហើយកាត់បន្ថយ speckle។
- គណនាកម្រិត Otsu ហើយប្រៀបធៀបជាមួយកម្រិតថេរ។
- ធ្វើផែនទីទឹករដូវប្រាំង រដូវទឹកឡើង និងតំបន់លិចតាមរដូវ។
- គណនាផ្ទៃលិចតាមខេត្ត ហើយនាំចេញទៅ QGIS។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `COPERNICUS/S1_GRD` · `JRC/GSW1_4/GlobalSurfaceWater` · `MERIT/Hydro/v1_0_1` · `ESA/WorldCover/v200` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-flood"></div>

រកកម្រិតដែលផ្ដល់ភាពត្រឹមត្រូវខ្ពស់បំផុត ដោយមិនប្រើតម្រង និងប្រើតម្រង ៥ × ៥។ ប្រៀបធៀបជាមួយកម្រិត Otsu។

## សកម្មភាពទី១៖ Collection និងគន្លង · ២០ នាទី

```javascript
var lake = ee.Geometry.Rectangle([103.3, 12.2, 104.7, 13.4]);          // ទន្លេសាប និងជុំវិញ
var provs = ee.FeatureCollection('FAO/GAUL/2015/level1').filterBounds(lake)
  .filter(ee.Filter.inList('ADM1_NAME', ['Battambang', 'Pursat', 'Kampong Chhnang', 'Kampong Thom', 'Siem Reap', 'Banteay Meanchey']));
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(lake)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')).select('VV');
print('រូបភាព ២០២៤', s1.filterDate('2024-01-01', '2025-01-01').size());
print(ui.Chart.feature.histogram(s1.filterDate('2024-01-01', '2025-01-01'), 'relativeOrbitNumber_start'));
Map.centerObject(lake, 9);
```

កត់ត្រាគន្លង (relative orbit) ដែលគ្របបឹងភាគច្រើន។ ប្រសិនបើមានគន្លងពីរ ត្រូវប្រើរូបភាពពីគន្លងទាំងពីរនៅក្នុងរយៈពេលនីមួយៗ តែ median មុន mosaic។

## សកម្មភាពទី២៖ រដូវប្រាំង និងរដូវទឹកឡើង · ២៥ នាទី

```javascript
function season(start, end) {
  return s1.filterDate(start, end).median().focalMedian(30, 'circle', 'meters').clip(lake);
}
var dry = season('2024-03-15', '2024-05-01');     // ទឹកទាបបំផុត
var wet = season('2024-09-20', '2024-10-31');     // ទឹកខ្ពស់បំផុត
Map.addLayer(dry, {min: -25, max: 0}, 'VV រដូវប្រាំង');
Map.addLayer(wet, {min: -25, max: 0}, 'VV រដូវទឹកឡើង');
Map.addLayer(dry.addBands(wet).addBands(wet), {min: -25, max: -5}, 'RGB៖ ប្រាំង វស្សា វស្សា');
```

នៅទីនេះ median នៃរូបភាពច្រើនសប្ដាហ៍ទទួលយកបាន ព្រោះយើងចង់បានស្ថានភាពតាមរដូវ មិនមែនទឹកជំនន់ភ្លាមៗទេ។ តំបន់ណាខ្លះភ្លឺក្នុងរដូវវស្សា ទោះបីជាលិចទឹក? (ព្រៃលិចទឹក)

## សកម្មភាពទី៣៖ Otsu · ២៥ នាទី

ចម្លងមុខងារ `otsu()` ពីមេរៀនទី៧ ផ្នែក ៧.៣.៥ ហើយ៖

```javascript
function waterMap(img) {
  var h = img.reduceRegion({reducer: ee.Reducer.histogram(255, 0.1), geometry: lake, scale: 30,
                            maxPixels: 1e10, tileScale: 4}).get('VV');
  var t = ee.Number(otsu(h));
  print('កម្រិត Otsu', t);
  return img.lt(t).rename('water');
}
var wDry = waterMap(dry), wWet = waterMap(wet);
var w16 = wet.lt(-16);
Map.addLayer(wDry.selfMask(), {palette: ['#08306b']}, 'ទឹក ប្រាំង');
Map.addLayer(wWet.selfMask(), {palette: ['#6baed6']}, 'ទឹក វស្សា (Otsu)');
Map.addLayer(w16.selfMask(), {palette: ['#ff9800']}, 'ទឹក វស្សា (−១៦ dB)', false);
```

កត់ត្រាកម្រិត Otsu ទាំងពីរ។ វាខុសពី −១៦ dB ប៉ុន្មាន?

## សកម្មភាពទី៤៖ ផ្ទៃលិចតាមរដូវ និងតាមខេត្ត · ៣០ នាទី

```javascript
var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var hand = ee.Image('MERIT/Hydro/v1_0_1').select('hnd');
var seasonal = wWet.and(wDry.not()).updateMask(slope.lt(5)).updateMask(hand.lt(15)).selfMask();
Map.addLayer(seasonal, {palette: ['#e53935']}, 'លិចតាមរដូវ');
var area = ee.Image.pixelArea().divide(1e6);
var img = area.updateMask(wDry).rename('dry_km2')
  .addBands(area.updateMask(wWet).rename('wet_km2'))
  .addBands(area.updateMask(seasonal).rename('seasonal_km2'));
var byProv = img.reduceRegions({collection: provs, reducer: ee.Reducer.sum(), scale: 30, tileScale: 8});
print(byProv.select(['ADM1_NAME', 'dry_km2', 'wet_km2', 'seasonal_km2']));
var wc = ee.ImageCollection('ESA/WorldCover/v200').first();
print('ដីដំណាំលិចតាមរដូវ (គម²)', area.updateMask(seasonal).updateMask(wc.eq(40))
  .reduceRegion({reducer: ee.Reducer.sum(), geometry: lake, scale: 30, maxPixels: 1e10, tileScale: 8}));
```

## សកម្មភាពទី៥៖ ប្រៀបធៀបជាមួយ JRC និងនាំចេញ · ២៥ នាទី

```javascript
var gsw = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').clip(lake);
Map.addLayer(gsw, {min: 0, max: 100, palette: ['white', '#08306b']}, 'JRC occurrence (%)', false);
var agree = wWet.and(gsw.gt(20).unmask(0));
print('ទឹកវស្សា ដែល JRC ក៏ឃើញ (គម²)', area.updateMask(agree).reduceRegion({reducer: ee.Reducer.sum(),
  geometry: lake, scale: 30, maxPixels: 1e10, tileScale: 8}));
Export.table.toDrive({collection: byProv, description: 'tonlesap_water_2024', folder: 'applied_gis',
  fileFormat: 'CSV', selectors: ['ADM1_NAME', 'dry_km2', 'wet_km2', 'seasonal_km2']});
Export.image.toDrive({image: wDry.add(wWet.multiply(2)).toByte(), description: 'tonlesap_water_classes_2024',
  folder: 'applied_gis', region: lake, scale: 30, crs: 'EPSG:32648', maxPixels: 1e10});
```

រូបភាពដែលនាំចេញមានតម្លៃ ០ (ដី) ១ (ទឹកតែរដូវប្រាំង កម្រ) ២ (ទឹកតែរដូវវស្សា) ៣ (ទឹកទាំងពីររដូវ)។ ក្នុង QGIS ដាក់ពណ៌តាមតម្លៃ ហើយធ្វើប្លង់ផែនទីដែលមានតារាងផ្ទៃតាមខេត្ត។

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- កម្រិត Otsu រដូវទាំងពីរ និងផ្ទៃទឹកសរុបពីកម្រិត Otsu ធៀបនឹង −១៦ dB។
- តារាងផ្ទៃទឹកតាមខេត្ត (CSV) និងផ្ទៃដីដំណាំលិចតាមរដូវ។
- ផែនទីពី QGIS បង្ហាញទឹកអចិន្ត្រៃយ៍ និងតំបន់លិចតាមរដូវ។
- កថាខណ្ឌមួយ៖ តំបន់ណាដែល Sentinel-1 និង JRC មិនស៊ីគ្នា ហើយហេតុអ្វី (គិតពីព្រៃលិចទឹក)។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="VV" markdown>
**១.** ប៉ូលការីសាស្យុងណាដែលបំបែកទឹក និងដីបានល្អជាង ជាទូទៅ?
</div>

<div class="self-check" data-answer="orbitProperties_pass" markdown>
**២.** លក្ខណៈ metadata ណាដែលប្រើត្រង ascending/descending?
</div>

<div class="self-check" data-answer="histogram|ee.Reducer.histogram|ee.Reducer.histogram()" markdown>
**៣.** Reducer ណាដែល Otsu ត្រូវការជាធាតុចូល?
</div>

<div class="self-check" data-answer="double bounce|ចាំងពីរដង" markdown>
**៤.** យន្តការណាធ្វើឲ្យព្រៃលិចទឹកភ្លឺ ជាជាងងងឹត?
</div>
