# លំហាត់ទី៤៖ NDVI មធ្យមតាមខេត្ត

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៤៖ Reducer ស្ថិតិតាមតំបន់ និងការនាំចេញ](../lessons/lesson-04.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១៣០ នាទី

## ស្ថានភាព

អ្នកនឹងគណនា NDVI មធ្យមរដូវប្រាំងសម្រាប់ខេត្តទាំង ២៥ និងស្រុកទាំងអស់ក្នុងខេត្តរបស់អ្នក ពិនិត្យឥទ្ធិពលនៃ scale គណនាផ្ទៃទឹក ហើយនាំចេញតារាងទៅធ្វើផែនទី choropleth ក្នុង QGIS។

## គោលបំណង

- គណនាស្ថិតិក្នុងតំបន់មួយ ដោយ reduceRegion ហើយអាន Dictionary។
- ប្រៀបធៀបលទ្ធផលនៅ scale បួនផ្សេងគ្នា។
- គណនាស្ថិតិតាមខេត្ត និងតាមស្រុក ដោយ reduceRegions និង reducer បន្សំ។
- គណនាផ្ទៃទឹកដោយ pixelArea ហើយនាំចេញ CSV ដែលភ្ជាប់បានក្នុង QGIS។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `COPERNICUS/S2_SR_HARMONIZED` · `FAO/GAUL/2015/level1` · `FAO/GAUL/2015/level2`។
- ស្រទាប់ព្រំដែនខេត្តក្នុង QGIS (ពីសៀវភៅទី១ ឬទី២) សម្រាប់ភ្ជាប់តារាង។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-zonal"></div>

គូរតំបន់ដែលមានទាំងទឹក និងរុក្ខជាតិ ហើយប្ដូរ scale ពី ១០ ម ទៅ ៤០០ ម។ កត់ត្រា mean max និង count។

## សកម្មភាពទី១៖ ស្ថិតិខេត្តមួយ · ២០ នាទី

```javascript
var provinces = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM0_NAME', 'Cambodia'));
var myProv = provinces.filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));   // ប្ដូរជាខេត្តរបស់អ្នក
function maskS2(img) {
  var scl = img.select('SCL');
  var ok = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return img.updateMask(ok).divide(10000).copyProperties(img, ['system:time_start']);
}
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterDate('2023-11-01', '2024-05-01')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40)).map(maskS2);
var ndvi = s2.filterBounds(myProv).median().normalizedDifference(['B8', 'B4']).rename('NDVI');
var reducer = ee.Reducer.mean()
  .combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true})
  .combine({reducer2: ee.Reducer.percentile([10, 50, 90]), sharedInputs: true})
  .combine({reducer2: ee.Reducer.count(), sharedInputs: true});
print('ខេត្តរបស់ខ្ញុំ', ndvi.reduceRegion({reducer: reducer, geometry: myProv.geometry(), scale: 10, maxPixels: 1e10, tileScale: 4}));
Map.centerObject(myProv, 9);
Map.addLayer(ndvi.clip(myProv), {min: 0, max: 0.8, palette: ['#a50026', '#fee08b', '#006837']}, 'NDVI');
```

កត់ត្រាតម្លៃទាំងប្រាំមួយ។ ពន្យល់ថាហេតុអ្វី mean និង p50 ខុសគ្នា។

## សកម្មភាពទី២៖ ឥទ្ធិពលនៃ scale · ២០ នាទី

```javascript
[10, 30, 100, 500].forEach(function(sc) {
  print('scale ' + sc, ndvi.reduceRegion({
    reducer: ee.Reducer.mean().combine({reducer2: ee.Reducer.max(), sharedInputs: true})
      .combine({reducer2: ee.Reducer.count(), sharedInputs: true}),
    geometry: myProv.geometry(), scale: sc, maxPixels: 1e10, tileScale: 4}));
});
```

ចំណាំ៖ `forEach` ជា JavaScript ធម្មតាក្នុងកម្មវិធីរុករក ហើយលេខ scale ជាលេខ JavaScript ដូច្នេះការប្រើ loop នៅទីនេះត្រឹមត្រូវ។ ធ្វើតារាង scale · mean · max · count ហើយពន្យល់លំនាំ។

## សកម្មភាពទី៣៖ ខេត្តទាំង ២៥ · ២៥ នាទី

```javascript
var ndviKH = s2.filterBounds(provinces).median()
  .normalizedDifference(['B8', 'B4']).rename('NDVI');
var byProv = ndviKH.reduceRegions({
  collection: provinces,
  reducer: ee.Reducer.mean().combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true}),
  scale: 100,           // ថ្នាក់ជាតិ៖ ១០០ ម ដើម្បីកុំឲ្យយូរពេក
  tileScale: 4
});
Export.table.toDrive({collection: byProv, description: 'KH_province_NDVI_dry_2024',
  folder: 'applied_gis', fileFormat: 'CSV', selectors: ['ADM1_CODE', 'ADM1_NAME', 'mean', 'stdDev']});
```

ចុច **Run** ក្នុងផ្ទាំង Tasks។ ការងារនេះអាចចំណាយពេល ៥–២០ នាទី។ ខណៈរង់ចាំ សូមធ្វើសកម្មភាពទី៤។

## សកម្មភាពទី៤៖ ស្រុក និងផ្ទៃទឹក · ២៥ នាទី

```javascript
var districts = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));        // ខេត្តរបស់អ្នក
var comp = s2.filterBounds(myProv).median().clip(myProv);
var water = comp.normalizedDifference(['B3', 'B11']).gt(0).rename('water');   // MNDWI > 0
var img = ndvi.addBands(water.multiply(ee.Image.pixelArea()).divide(1e6).rename('water_km2'));
var byDist = img.reduceRegions({
  collection: districts,
  reducer: ee.Reducer.mean().forEach(['NDVI']).combine({    // NDVI៖ mean
    reducer2: ee.Reducer.sum().forEach(['water_km2']), sharedInputs: false}),
  scale: 10, tileScale: 8
});
print(byDist.select(['ADM2_NAME', 'NDVI', 'water_km2']));
Export.table.toDrive({collection: byDist, description: 'district_NDVI_water_2024', folder: 'applied_gis',
  fileFormat: 'CSV', selectors: ['ADM2_CODE', 'ADM2_NAME', 'NDVI', 'water_km2']});
```

`forEach()` អនុវត្ត reducer ទៅលើក្រុមរលកជាក់លាក់៖ mean សម្រាប់ NDVI និង sum សម្រាប់ផ្ទៃទឹក។ ឈ្មោះលក្ខណៈលទ្ធផលគឺឈ្មោះក្រុមរលក។ ប្រសិនបើ print យូរពេក សូមរំលង print ហើយ Export ផ្ទាល់។

## សកម្មភាពទី៥៖ ផែនទីក្នុង QGIS · ៣០ នាទី

1. ទាញយក CSV ពី Google Drive។
2. ក្នុង QGIS បើកស្រទាប់ព្រំដែនខេត្ត ហើយបន្ថែម CSV ជាស្រទាប់ «No geometry»។
3. **Properties → Joins** ភ្ជាប់តាមឈ្មោះខេត្ត (ពិនិត្យអក្ខរាវិរុទ្ធ GAUL ធៀបនឹងស្រទាប់របស់អ្នក ឧ. `Siem Reap` និង `Siemreap`)។
4. ធ្វើ choropleth ៥ ថ្នាក់ ពណ៌លឿង–បៃតង ហើយបង្កើតប្លង់ដែលមានចំណងជើង ប្រភព (Sentinel-2 median វិច្ឆិកា ២០២៣–មេសា ២០២៤ · scale ១០០ ម) និងកំណត់ចំណាំ។

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- តារាងស្ថិតិខេត្តរបស់អ្នក (សកម្មភាពទី១) និងតារាង scale (សកម្មភាពទី២) ជាមួយកថាខណ្ឌពន្យល់។
- ឯកសារ CSV ពីរ (ខេត្ត និងស្រុក)។
- ផែនទី choropleth NDVI តាមខេត្ត ជា PDF ឬ PNG ពី QGIS។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="Dictionary|ee.Dictionary|dictionary" markdown>
**១.** reduceRegion() ត្រឡប់វត្ថុប្រភេទណា?
</div>

<div class="self-check" data-answer="NDVI_mean" markdown>
**២.** ក្រោយ combine mean និង stdDev លើក្រុមរលក NDVI តើគន្លឹះនៃមធ្យមមានឈ្មោះអ្វី?
</div>

<div class="self-check" data-answer="pixelArea|ee.Image.pixelArea|ee.Image.pixelArea()" markdown>
**៣.** មុខងារណាផ្ដល់ផ្ទៃពិតរបស់ក្រឡានីមួយៗ?
</div>

<div class="self-check" data-answer="selectors" markdown>
**៤.** ប៉ារ៉ាម៉ែត្រណាក្នុង Export.table រក្សាតែជួរឈរដែលត្រូវការ (និងដក .geo)?
</div>
