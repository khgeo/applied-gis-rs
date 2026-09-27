# លំហាត់ទី៦៖ ផែនទីគម្របដីខេត្តមួយ

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៦៖ ការចាត់ថ្នាក់គម្របដីដោយ Random Forest](../lessons/lesson-06.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១៤០ នាទី

## ស្ថានភាព

អ្នកនឹងធ្វើផែនទីគម្របដីឆ្នាំ ២០២៤ សម្រាប់ខេត្តរបស់អ្នក ជាមួយថ្នាក់ប្រាំ៖ តំបន់សាងសង់ (០) ដីទទេ (១) ទឹក (២) រុក្ខជាតិ (៣) និងស្រែ (៤)។ អ្នកនឹងគូរចំណុចគំរូដោយខ្លួនឯង វាយតម្លៃភាពត្រឹមត្រូវ កែលម្អដោយលក្ខណៈបន្ថែម គណនាផ្ទៃ ហើយនាំចេញផែនទីទៅ QGIS។

## គោលបំណង

- រៀបចំរូបភាពលក្ខណៈពីរកម្រិត៖ ក្រុមរលកតែប៉ុណ្ណោះ និងក្រុមរលក + សន្ទស្សន៍ + DEM + រដូវវស្សា។
- គូរ និងរក្សាចំណុចគំរូ យ៉ាងហោចណាស់ ៥០ ក្នុងមួយថ្នាក់។
- បណ្ដុះបណ្ដាល Random Forest ហើយវាយតម្លៃដោយចំណុច ៣០% ដែលបំបែកមុន sampleRegions។
- គណនាផ្ទៃតាមថ្នាក់ ហើយនាំចេញ GeoTIFF និងតារាងភាពត្រឹមត្រូវ។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `COPERNICUS/S2_SR_HARMONIZED` · `JAXA/ALOS/AW3D30/V3_2` · `FAO/GAUL/2015/level1`។
- ជម្រើស (សម្រាប់ហាត់មុន)៖ `users/yamsarath168/rupp_wfp_applied_gisrs4drm/kep_gcps` (ចំណុចខេត្តកែប)។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-rf"></div>

បណ្ដុះបណ្ដាលជាមួយ ២០ ចំណុច/ថ្នាក់ បន្ទាប់មក ១០០ ចំណុច/ថ្នាក់។ តើ OA ប្ដូរប៉ុន្មាន? ថ្នាក់ណាច្រឡំច្រើនជាងគេ?

## សកម្មភាពទី១៖ Composite និងលក្ខណៈ · ២០ នាទី

```javascript
var aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));
Map.centerObject(aoi, 9);
function maskS2(img) {
  var scl = img.select('SCL');
  var ok = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return img.updateMask(ok).divide(10000);
}
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50)).map(maskS2)
  .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']);
var dry = s2.filterDate('2023-11-01', '2024-05-01').median();
var wet = s2.filterDate('2024-07-01', '2024-11-01').median();
function addIndices(img) {
  return img.addBands([
    img.normalizedDifference(['B8', 'B4']).rename('NDVI'),
    img.normalizedDifference(['B11', 'B8']).rename('NDBI'),
    img.normalizedDifference(['B3', 'B11']).rename('MNDWI'),
    img.expression('((S + R) - (N + B)) / ((S + R) + (N + B))',
      {S: img.select('B11'), R: img.select('B4'), N: img.select('B8'), B: img.select('B2')}).rename('BSI')]);
}
var alos = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2').select('DSM');
var dem = alos.mosaic().setDefaultProjection(alos.first().projection());
var basic = dry.clip(aoi);                                              // លក្ខណៈ ៦
var full = addIndices(dry)
  .addBands(wet.normalizedDifference(['B8', 'B4']).rename('NDVI_wet'))
  .addBands(dem.rename('elev')).addBands(ee.Terrain.slope(dem).rename('slope'))
  .clip(aoi);                                                            // លក្ខណៈ ១៣
Map.addLayer(dry.clip(aoi), {bands: ['B4', 'B3', 'B2'], min: 0, max: 0.3}, 'រដូវប្រាំង');
Map.addLayer(dry.clip(aoi), {bands: ['B11', 'B8', 'B4'], min: 0, max: 0.4}, 'ពណ៌មិនពិត', false);
print(full.bandNames());
```

## សកម្មភាពទី២៖ គូរចំណុចគំរូ · ៣៥ នាទី

1. ក្នុង **Geometry Imports** ចុច **+ new layer** ប្រាំដង ហើយដាក់ឈ្មោះ `urban` `bare` `water` `vegetation` `paddy`។
2. សម្រាប់ស្រទាប់នីមួយៗ ចុចរូបកង់ ⚙ → **Import as: FeatureCollection** → **+ Add property** `landcover` = ០ ១ ២ ៣ ៤ រៀងគ្នា។
3. ដាក់យ៉ាងហោចណាស់ **៥០ ចំណុចក្នុងមួយថ្នាក់** រាយពេញខេត្ត។ ប្រើរូបភាពពណ៌មិនពិត និង composite រដូវវស្សា ដើម្បីបែងចែកស្រែ (បៃតងក្នុងវស្សា ទំនេរក្នុងប្រាំង) ពីរុក្ខជាតិដទៃ។
4. រក្សាចំណុចជា Asset ដើម្បីកុំឲ្យបាត់៖

```javascript
var gcps = urban.merge(bare).merge(water).merge(vegetation).merge(paddy);
print('ចំណុចតាមថ្នាក់', gcps.aggregate_histogram('landcover'));
Export.table.toAsset({collection: gcps, description: 'my_gcps_2024', assetId: 'my_gcps_2024'});
```

## សកម្មភាពទី៣៖ បណ្ដុះបណ្ដាល និងវាយតម្លៃ · ៣០ នាទី

```javascript
var gcp = gcps.randomColumn('random', 42);
var trainGcp = gcp.filter(ee.Filter.lt('random', 0.7));
var validGcp = gcp.filter(ee.Filter.gte('random', 0.7));
var PAL = ['red', '926829', '1488ff', 'green', 'fffcbf'];
function run(features, name) {
  var training = features.sampleRegions({collection: trainGcp, properties: ['landcover'], scale: 10, tileScale: 16});
  var clf = ee.Classifier.smileRandomForest({numberOfTrees: 100, seed: 42})
    .train({features: training, classProperty: 'landcover', inputProperties: features.bandNames()});
  var classified = features.classify(clf);
  var cm = classified.sampleRegions({collection: validGcp, properties: ['landcover'], scale: 10, tileScale: 16})
    .errorMatrix('landcover', 'classification');
  print(name, 'OA', cm.accuracy(), 'Kappa', cm.kappa(), 'PA', cm.producersAccuracy(), 'UA', cm.consumersAccuracy());
  Map.addLayer(classified, {min: 0, max: 4, palette: PAL}, name);
  return {classified: classified, cm: cm, clf: clf};
}
var r6 = run(basic, 'លក្ខណៈ ៦');
var r13 = run(full, 'លក្ខណៈ ១៣');
print('ភាពសំខាន់', r13.clf.explain().get('importance'));
```

ធ្វើតារាងប្រៀបធៀប OA Kappa និង PA/UA នៃថ្នាក់នីមួយៗ សម្រាប់ម៉ូដែលទាំងពីរ។ លក្ខណៈណាសំខាន់បំផុត?

## សកម្មភាពទី៤៖ កែលម្អ · ២៥ នាទី

មើលតារាងកំហុសនៃម៉ូដែល ១៣ លក្ខណៈ ហើយរកគូថ្នាក់ដែលច្រឡំច្រើនបំផុត។ បន្ថែមចំណុច ១៥–២០ នៅតំបន់ដែលច្រឡំ ពិនិត្យ និងលុបចំណុចដែលដាក់ខុស រួចរត់ម្ដងទៀត។ កត់ត្រា OA មុន និងក្រោយ។

!!! warning "កុំកែតាមចំណុចផ្ទៀងផ្ទាត់"
    ប្រសិនបើអ្នកកែចំណុចដោយមើលតែកំហុសលើចំណុចផ្ទៀងផ្ទាត់ ម្ដងហើយម្ដងទៀត OA នឹងឡើង ប៉ុន្តែវាលែងជាការវាយតម្លៃឯករាជ្យទៀតហើយ។ កែតាមការមើលផែនទី ហើយរក្សា seed នៃ randomColumn ដដែល។

## សកម្មភាពទី៥៖ ផ្ទៃ និងការនាំចេញ · ២០ នាទី

```javascript
var areas = ee.Image.pixelArea().divide(1e6).addBands(r13.classified).reduceRegion({
  reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'landcover'}),
  geometry: aoi.geometry(), scale: 10, maxPixels: 1e10, tileScale: 4});
print('ផ្ទៃ (គម²)', areas.get('groups'));
Export.image.toDrive({image: r13.classified.toByte(), description: 'LULC_2024_myprov', folder: 'applied_gis',
  region: aoi.geometry(), scale: 10, crs: 'EPSG:32648', maxPixels: 1e10});
Export.table.toDrive({collection: ee.FeatureCollection([ee.Feature(null, {
  matrix: r13.cm.array(), oa: r13.cm.accuracy(), kappa: r13.cm.kappa()})]),
  description: 'LULC_2024_accuracy', folder: 'applied_gis', fileFormat: 'CSV'});
```

ក្នុង QGIS បើក GeoTIFF ដាក់ពណ៌ **Paletted/Unique values** តាមថ្នាក់ ហើយបង្កើតប្លង់ផែនទីដែលមានកំណត់ចំណាំ OA និងប្រភពទិន្នន័យ។

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប និង Asset ចំណុចគំរូ (ចែករំលែកជាមួយគ្រូ)។
- តារាងប្រៀបធៀបម៉ូដែល ៦ និង ១៣ លក្ខណៈ (OA Kappa PA UA)។
- តារាងផ្ទៃតាមថ្នាក់ (គម² និង %)។
- ផែនទីគម្របដីពី QGIS ជាមួយ OA ក្នុងកំណត់ចំណាំ។
- កថាខណ្ឌមួយ៖ ថ្នាក់ណាទុកចិត្តបានតិចបំផុត ហើយហេតុអ្វី។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="sampleRegions|sampleRegions()" markdown>
**១.** មុខងារណាទាញតម្លៃក្រឡានៅចំណុចគំរូ ទៅជាតារាងបណ្ដុះបណ្ដាល?
</div>

<div class="self-check" data-answer="consumersAccuracy|consumersAccuracy()" markdown>
**២.** ក្នុង Earth Engine មុខងារណាផ្ដល់ User's Accuracy?
</div>

<div class="self-check" data-answer="0.7|០,៧|0,7" markdown>
**៣.** ប្រសិនបើ trainGcp ប្រើ lt(0.7) តើ validGcp ត្រូវប្រើ gte(?)
</div>

<div class="self-check" data-answer="toByte|toByte()" markdown>
**៤.** មុខងារណាធ្វើឲ្យ GeoTIFF ផែនទីថ្នាក់មានទំហំតូច (មួយបៃ/ក្រឡា)?
</div>
