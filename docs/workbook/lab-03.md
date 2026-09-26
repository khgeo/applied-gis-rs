# លំហាត់ទី៣៖ Composite ឥតពពកនៃកម្ពុជា

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៣៖ Image Collection ការត្រង ការលុបពពក និង Composite](../lessons/lesson-03.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · ប្រហែល ១១០ នាទី

## ស្ថានភាព

អ្នកនឹងបង្កើតរូបភាពមូលដ្ឋានឥតពពកសម្រាប់ខេត្តរបស់អ្នក ក្នុងរដូវប្រាំង និងរដូវវស្សា ប្រៀបធៀបការលុបពពកពីរវិធី និង reducer ពីរ រួចនាំចេញលទ្ធផលទៅ Google Drive ដើម្បីប្រើក្នុង QGIS។

## គោលបំណង

- ត្រង collection ជាជំហាន ហើយពិនិត្យចំនួននៅជំហាននីមួយៗ។
- លុបពពកដោយ SCL និងដោយ Cloud Score+។
- បង្កើត composite median និង qualityMosaic ហើយស្រទាប់ចំនួនការសង្កេតស្អាត។
- នាំចេញ composite ជា GeoTIFF ដែលមានក្រឡា ១០ ម និង CRS UTM 48N។

<figure markdown>
--8<-- "assets/svg/agv/lab03-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី៣ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- `COPERNICUS/S2_SR_HARMONIZED` · `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១៥ នាទី

<div class="sim" data-sim="gee-filter"></div>

<div class="sim" data-sim="gee-composite"></div>

## សកម្មភាពទី១៖ ត្រងជាជំហាន · ១៥ នាទី

```javascript
var prov = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));
var all = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED');
var a = all.filterBounds(prov);
var b = a.filterDate('2023-11-01', '2024-05-01');
var c = b.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40));
print('bounds', a.size(), 'date', b.size(), 'cloud<40', c.size());
```

## សកម្មភាពទី២៖ លុបពពកពីរវិធី · ២៥ នាទី

```javascript
function maskSCL(img) {
  var scl = img.select('SCL');
  var ok = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return img.updateMask(ok).divide(10000).copyProperties(img, ['system:time_start']);
}
var csp = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
function maskCSP(img) {
  return img.updateMask(img.select('cs_cdf').gte(0.6)).divide(10000)
            .copyProperties(img, ['system:time_start']);
}
var sclC = c.map(maskSCL).median().clip(prov);
var cspC = c.linkCollection(csp, ['cs_cdf']).map(maskCSP).median().clip(prov);
var vis = {bands: ['B4', 'B3', 'B2'], min: 0, max: 0.3};
Map.centerObject(prov, 9);
Map.addLayer(sclC, vis, 'SCL median');
Map.addLayer(cspC, vis, 'Cloud Score+ median');
```

ប្រៀបធៀបតំបន់ភ្នំ និងគែមទន្លេ៖ វិធីណាទុកពពកស្ដើង ឬស្រមោលតិចជាង?

## សកម្មភាពទី៣៖ median ធៀបនឹង qualityMosaic · ២០ នាទី

```javascript
var green = c.linkCollection(csp, ['cs_cdf']).map(maskCSP).map(function(img) {
  return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'));
}).qualityMosaic('NDVI').clip(prov);
Map.addLayer(green, {bands: ['B8', 'B4', 'B3'], min: 0, max: 0.4}, 'greenest pixel');
var n = c.linkCollection(csp, ['cs_cdf']).map(maskCSP).select('B4').count().clip(prov);
Map.addLayer(n, {min: 0, max: 30, palette: ['red', 'yellow', 'green']}, 'ចំនួនការសង្កេតស្អាត');
```

## សកម្មភាពទី៤៖ រដូវវស្សា · ២០ នាទី

ធ្វើសកម្មភាពទី២ ម្ដងទៀតសម្រាប់ `2024-06-01` ដល់ `2024-10-31`។ ប្រៀបធៀបស្រទាប់ចំនួនការសង្កេតស្អាតនៃរដូវទាំងពីរ ហើយកត់ត្រាតំបន់ដែលគ្មានទិន្នន័យ។

## សកម្មភាពទី៥៖ នាំចេញ · ១៥ នាទី

```javascript
Export.image.toDrive({
  image: cspC.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']).toFloat(),
  description: 'KCH_S2_dry_2024',
  folder: 'applied_gis',
  region: prov.geometry(),
  scale: 10,
  crs: 'EPSG:32648',
  maxPixels: 1e10
});
```

ចុច **Run** ក្នុងផ្ទាំង **Tasks**។ នៅពេលបញ្ចប់ ទាញយក GeoTIFF ពី Google Drive ហើយបើកក្នុង QGIS។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a03-reducers.svg"
<figcaption>លទ្ធផលគំរូ ១៖ ជ្រើស reducer សម្រាប់ composite។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - first() យករូបភាពមួយ ដូច្នេះពពករបស់វានៅដដែល។
    - max() ជ្រើសពពក ព្រោះពពកភ្លឺជាងដី។
    - median() + mask ផ្ដល់លទ្ធផលស្អាតបំផុតសម្រាប់តំបន់ត្រូពិច។

<figure markdown>
--8<-- "assets/svg/agv/a03-qa.svg"
<figcaption>លទ្ធផលគំរូ ២៖ ក្រុមរលកគុណភាពប្រាប់ពពក។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - Sentinel-2 L2A មានក្រុមរលក SCL ដែលចាត់ថ្នាក់ក្រឡានីមួយៗ។
    - Landsat Collection 2 ប្រើប៊ីតក្នុង QA_PIXEL៖ ត្រូវប្រើ bitwiseAnd()។
    - updateMask() ធ្វើឲ្យក្រឡាពពកក្លាយជា «គ្មានទិន្នន័យ» មុនធ្វើ composite។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| Composite នៅមានស្នាមពពក | SCL ខកពពកស្ដើង | ប្រើ Cloud Score+ (cs_cdf ≥ ០,៦) |
| ចន្លោះគ្មានទិន្នន័យ (ខ្មៅ) | រដូវវស្សា ឬតម្រងតឹងពេក | ពង្រីករយៈពេល · CLOUDY < ៤០–៦០% |
| Export បរាជ័យ maxPixels | តំបន់ធំ × ក្រឡា ១០ ម | maxPixels: 1e10 · ឬ scale 20 |
| ពណ៌ខុសក្នុង QGIS | ប្រភេទទិន្នន័យ ឬ stretch | toFloat() · stretch ២–៩៨% |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- រូបអេក្រង់ composite រដូវប្រាំង និងរដូវវស្សា ព្រមស្រទាប់ចំនួនការសង្កេតស្អាត។
- ឯកសារ GeoTIFF ដែលបាននាំចេញ (បើកក្នុង QGIS)។
- តារាងចំនួនរូបភាពនៅជំហានត្រងនីមួយៗ និងកថាខណ្ឌប្រៀបធៀបវិធីលុបពពកទាំងពីរ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="9|៩" markdown>
**១.** តម្លៃ SCL សម្រាប់ «ពពកប្រូបាប៊ីលីតេខ្ពស់»?
</div>

<div class="self-check" data-answer="median|median()" markdown>
**២.** Reducer លំនាំដើមសម្រាប់រូបភាពមូលដ្ឋានពណ៌ពិត?
</div>

<div class="self-check" data-answer="count|count()" markdown>
**៣.** Reducer ណាបង្ហាញចំនួនការសង្កេតស្អាតក្នុងក្រឡានីមួយៗ?
</div>

<div class="self-check" data-answer="EPSG:32648|32648" markdown>
**៤.** CRS UTM 48N (WGS 84) សម្រាប់កម្ពុជា?
</div>
