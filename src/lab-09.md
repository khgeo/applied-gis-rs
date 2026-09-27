# លំហាត់ទី៩៖ អាងរងពី DEM

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៩៖ ទីសណ្ឋាន ជម្រាល និងអាងទន្លេ](../lessons/lesson-09.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១២៥ នាទី

## ស្ថានភាព

អ្នកនឹងពិពណ៌នាទីសណ្ឋាន និងជលសាស្ត្រនៃខេត្តរបស់អ្នក៖ ប្រៀបធៀប DEM ពីរ ធ្វើផែនទីប្រឡាយពីស្រុតទឹក ជ្រើសអាងរងដែលពាក់ព័ន្ធ ហើយបង្កើតតារាងលក្ខណៈអាងរង (ផ្ទៃ កម្ពស់ ជម្រាល HAND ទឹកភ្លៀង) សម្រាប់ QGIS។

## គោលបំណង

- គណនាជម្រាល ទិស និងស្រមោលភ្នំ ហើយប្រៀបធៀប SRTM និង Copernicus GLO-30។
- ធ្វើផែនទីប្រឡាយពី MERIT Hydro ដោយកម្រិតស្រុតទឹកបី ហើយប្រៀបធៀបជាមួយ HydroRIVERS។
- ជ្រើសអាងរង HydroBASINS ដែលប៉ះខេត្តរបស់អ្នក។
- គណនាស្ថិតិតាមអាងរង ហើយនាំចេញជា Shapefile។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `USGS/SRTMGL1_003` · `COPERNICUS/DEM/GLO30` · `MERIT/Hydro/v1_0_1` · `WWF/HydroSHEDS/v1/Basins/hybas_8` · `WWF/HydroSHEDS/v1/FreeFlowingRivers` · `UCSB-CHG/CHIRPS/DAILY`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-terrain"></div>

ចុចលើប្រឡាយបីកន្លែង ពីខាងលើទៅខាងក្រោម។ តើផ្ទៃអាងរងប្ដូរយ៉ាងដូចម្ដេច ហើយហេតុអ្វី?

## សកម្មភាពទី១៖ ផលិតផលទីសណ្ឋាន · ២០ នាទី

```javascript
var prov = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Pursat'));   // ខេត្តរបស់អ្នក
var srtm = ee.Image('USGS/SRTMGL1_003').select('elevation');
var t = ee.Terrain.products(srtm).clip(prov);
Map.centerObject(prov, 9);
Map.addLayer(t.select('hillshade'), {min: 0, max: 255}, 'hillshade');
Map.addLayer(t.select('elevation'), {min: 0, max: 800, palette: ['#1a9850', '#fee08b', '#a6611a', 'white']}, 'កម្ពស់', true, 0.6);
Map.addLayer(t.select('slope'), {min: 0, max: 30, palette: ['#ffffcc', '#fd8d3c', '#bd0026']}, 'ជម្រាល', false);
var steep = t.select('slope').gt(15);
print('% ផ្ទៃជម្រាល > ១៥°', steep.multiply(100).reduceRegion({reducer: ee.Reducer.mean(), geometry: prov.geometry(),
  scale: 30, maxPixels: 1e10, tileScale: 4}));
```

## សកម្មភាពទី២៖ SRTM ធៀបនឹង GLO-30 · ២០ នាទី

```javascript
var glo = ee.ImageCollection('COPERNICUS/DEM/GLO30').select('DEM').filterBounds(prov)
  .mosaic().setDefaultProjection('EPSG:4326', null, 30).rename('elevation');
var d = glo.subtract(srtm).clip(prov);
Map.addLayer(d, {min: -10, max: 10, palette: ['#b2182b', '#f7f7f7', '#2166ac']}, 'GLO-30 − SRTM (ម)');
var wc = ee.ImageCollection('ESA/WorldCover/v200').first();
[10, 40].forEach(function(c) {                                        // ១០ ព្រៃ · ៤០ ដំណាំ
  print('ភាពខុសគ្នាមធ្យម ថ្នាក់ ' + c, d.updateMask(wc.eq(c)).reduceRegion({reducer: ee.Reducer.mean()
    .combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true}), geometry: prov.geometry(), scale: 30, maxPixels: 1e10, tileScale: 4}));
});
```

តើភាពខុសគ្នាធំជាងនៅព្រៃ ឬនៅដីដំណាំ? ពន្យល់ដោយប្រើគោលគំនិត DSM (SRTM ឆ្នាំ ២០០០ · GLO-30 ឆ្នាំ ២០១១–២០១៥ · ព្រៃអាចត្រូវបានកាប់ចន្លោះឆ្នាំទាំងនោះ)។

## សកម្មភាពទី៣៖ ប្រឡាយពីស្រុតទឹក · ២៥ នាទី

```javascript
var merit = ee.Image('MERIT/Hydro/v1_0_1');
var upa = merit.select('upa').clip(prov);
[10, 100, 1000].forEach(function(k) {
  Map.addLayer(upa.gt(k).selfMask(), {palette: ['#1565c0']}, 'upa > ' + k + ' គម²', k === 100);
});
var rivers = ee.FeatureCollection('WWF/HydroSHEDS/v1/FreeFlowingRivers').filterBounds(prov);
Map.addLayer(rivers, {color: 'ff9800'}, 'HydroRIVERS', false);
```

ប្រៀបធៀបប្រឡាយនីមួយៗជាមួយផែនទី Satellite។ កម្រិតណាដែលស៊ីនឹងស្ទឹងដែលមើលឃើញជាងគេ?

## សកម្មភាពទី៤៖ តារាងអាងរង · ៣០ នាទី

```javascript
var subs = ee.FeatureCollection('WWF/HydroSHEDS/v1/Basins/hybas_8').filterBounds(prov);
Map.addLayer(ee.Image().paint(subs, 0, 2), {palette: ['orange']}, 'អាងរងកម្រិត ៨');
var rain = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterDate('2014-01-01', '2024-01-01').sum().divide(10).rename('rain_mm');
var stack = ee.Terrain.products(srtm).select(['elevation', 'slope'])
  .addBands(merit.select('hnd').lt(5).multiply(100).rename('pct_low'))
  .addBands(rain);
var table = stack.reduceRegions({collection: subs, reducer: ee.Reducer.mean(), scale: 90, tileScale: 4})
  .map(function(f) { return f.set('area_km2', f.geometry().area(100).divide(1e6)); });
print(table.select(['HYBAS_ID', 'NEXT_DOWN', 'area_km2', 'elevation', 'slope', 'pct_low', 'rain_mm']));
Export.table.toDrive({collection: table, description: 'subbasins_myprov', folder: 'applied_gis', fileFormat: 'SHP'});
Export.image.toDrive({image: srtm.clip(prov).toInt16(), description: 'srtm_myprov', folder: 'applied_gis',
  region: prov.geometry(), scale: 30, crs: 'EPSG:32648', maxPixels: 1e10});
```

DEM ដែលនាំចេញ អាចប្រើក្នុង QGIS ជាមួយ GRASS `r.watershed` ដើម្បីកំណត់អាងរងពីចំណុចចេញផ្ទាល់ខ្លួន (ជម្រើស)។

## សកម្មភាពទី៥៖ ផែនទី និងការបកស្រាយ · ២០ នាទី

ក្នុង QGIS បើក Shapefile អាងរង ហើយធ្វើផែនទីពីរ៖ `slope` និង `pct_low`។ ដាក់ hillshade (ពី DEM ដែលនាំចេញ) នៅខាងក្រោម។ កំណត់អាងរងពីរ៖ មួយដែលទឹកហូរលឿនបំផុត និងមួយដែលងាយលិចបំផុត ហើយពន្យល់ដោយប្រើលក្ខណៈក្នុងតារាង។

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- % ផ្ទៃជម្រាល > ១៥° និងតារាងភាពខុសគ្នា GLO-30 − SRTM តាមព្រៃ និងដីដំណាំ។
- រូបអេក្រង់ប្រឡាយបីកម្រិត ជាមួយការជ្រើសកម្រិតដែលសមបំផុត។
- Shapefile អាងរង និងផែនទីពីរពី QGIS។
- កថាខណ្ឌមួយពិពណ៌នាអាងរងពីរដែលអ្នកជ្រើស។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="setDefaultProjection|setDefaultProjection()" markdown>
**១.** មុខងារណាត្រូវហៅលើ mosaic មុនគណនាជម្រាល?
</div>

<div class="self-check" data-answer="upa" markdown>
**២.** ក្រុមរលកណានៃ MERIT Hydro ផ្ដល់ផ្ទៃស្រុតទឹក (គម²)?
</div>

<div class="self-check" data-answer="hnd|HAND" markdown>
**៣.** ក្រុមរលកណានៃ MERIT Hydro ផ្ដល់ HAND?
</div>

<div class="self-check" data-answer="NEXT_DOWN" markdown>
**៤.** លក្ខណៈណានៃ HydroBASINS ប្រាប់ពីអាងដែលអាងនេះហូរចូល?
</div>
