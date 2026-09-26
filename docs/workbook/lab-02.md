# លំហាត់ទី២៖ វត្ថុ មុខងារ និង map()

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី២៖ JavaScript សម្រាប់ Earth Engine](../lessons/lesson-02.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · ប្រហែល ១០០ នាទី

## ស្ថានភាព

អ្នកនឹងសរសេរមុខងារដំបូងរបស់អ្នក អនុវត្តវាលើរូបភាពមួយឆ្នាំដោយ map() ហើយបង្កើតផែនទី NDVI អតិបរមា និងមធ្យម។ អ្នកក៏នឹងកែស្គ្រីបខុសៗផងដែរ។

## គោលបំណង

- ប្រើអថេរ អារេ និងវត្ថុ JavaScript ក្នុងកូដ Earth Engine។
- សរសេរមុខងារ addNDVI និង addNDWI។
- អនុវត្តមុខងារលើ ImageCollection ដោយ map() ហើយពិនិត្យលទ្ធផល។
- កែកំហុស client/server និងកំហុសឈ្មោះក្រុមរលក។

<figure markdown>
--8<-- "assets/svg/agv/lab02-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី២ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- ស្គ្រីបពីលំហាត់ទី១ (ព្រំខេត្ត `prov`)។
- `COPERNICUS/S2_SR_HARMONIZED`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-map"></div>

## សកម្មភាពទី១៖ JavaScript មូលដ្ឋាន · ១៥ នាទី

```javascript
var year = 2024;
var bands = ['B4', 'B3', 'B2'];
var vis = {bands: bands, min: 0, max: 3000};
print('ឆ្នាំ', year, 'ក្រុមរលក', bands, 'ការបង្ហាញ', vis);
print('ee.Number', ee.Number(year).add(1));       // server
print('JS', year + 1);                             // client
```

សួរខ្លួនឯង៖ ហេតុអ្វីបន្ទាត់ពីរចុងក្រោយបង្ហាញលទ្ធផលដូចគ្នា ប៉ុន្តែដំណើរការនៅកន្លែងខុសគ្នា?

## សកម្មភាពទី២៖ សរសេរមុខងារ · ២០ នាទី

```javascript
function addNDVI(img) {
  return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'));
}
function addNDWI(img) {
  return img.addBands(img.normalizedDifference(['B3', 'B8']).rename('NDWI'));
}
var one = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(prov).filterDate('2024-02-01', '2024-03-01').first();
print(addNDWI(addNDVI(one)).bandNames());
```

## សកម្មភាពទី៣៖ map() លើមួយឆ្នាំ · ២៥ នាទី

```javascript
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(prov).filterDate('2024-01-01', '2025-01-01')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
  .map(addNDVI);
var ndviMax  = s2.select('NDVI').max().clip(prov);
var ndviMean = s2.select('NDVI').mean().clip(prov);
var pal = ['#a50026', '#fee08b', '#1a9850'];
Map.addLayer(ndviMax,  {min: 0, max: 0.9, palette: pal}, 'NDVI អតិបរមា');
Map.addLayer(ndviMean, {min: 0, max: 0.9, palette: pal}, 'NDVI មធ្យម');
```

1. ប្រៀបធៀបស្រទាប់ទាំងពីរលើស្រែ ព្រៃ និងទឹក។
2. ហេតុអ្វី NDVI អតិបរមាលើស្រែខ្ពស់ជាងមធ្យមច្រើន ប៉ុន្តែលើព្រៃស្ទើរតែដូចគ្នា?

## សកម្មភាពទី៤៖ ស្វែងរកកំហុស · ២០ នាទី

ស្គ្រីបនីមួយៗខាងក្រោមមានកំហុស។ កែ ហើយសរសេរមូលហេតុ៖

```javascript
// ក
var n = s2.size();
if (n > 50) { print('គ្រប់គ្រាន់'); }
// ខ
var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(prov).first();
print(l8.normalizedDifference(['B8', 'B4']));
// គ
var count = 0;
s2.map(function(img) { count = count + 1; return img; });
print(count);
```

## សកម្មភាពទី៥៖ រក្សាទុកមុខងារ · ១០ នាទី

រក្សាទុកមុខងារ `addNDVI` និង `addNDWI` ក្នុងស្គ្រីបដាច់ដោយឡែក `utils` ហើយហៅវាពីស្គ្រីបផ្សេងដោយ `require('users/…/applied-gis:utils')` (ប្ដូរ `…` ជាឈ្មោះអ្នកប្រើរបស់អ្នក)។ ក្នុង `utils` ត្រូវសរសេរ `exports.addNDVI = addNDVI;`។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a02-map-loop.svg"
<figcaption>លទ្ធផលគំរូ ១៖ គិតជា «អនុវត្តលើគ្រប់ធាតុ»។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - for loop ដំណើរការក្នុងកម្មវិធីរុករក ហើយមិនស្គាល់ទំហំពិតនៃ collection។
    - map() ផ្ញើមុខងារទៅម៉ាស៊ីនមេ ដែលអនុវត្តលើធាតុនីមួយៗស្របគ្នា។
    - ក្នុង map() មិនអាចប្រើ print() getInfo() ឬ Map.addLayer() បានទេ។

<figure markdown>
--8<-- "assets/svg/agv/a02-errors.svg"
<figcaption>លទ្ធផលគំរូ ២៖ អានសារកំហុស។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - សារកំហុសក្នុង Console ប្រាប់លេខបន្ទាត់ និងមូលហេតុ។
    - កំហុសអង្គចងចាំ និងពេលវេលា ជាទូទៅដោះស្រាយដោយ Export ឬ scale ធំជាង។
    - ឈ្មោះក្រុមរលកខុស ជាកំហុសញឹកញាប់បំផុតពេលប្ដូរពី Sentinel-2 ទៅ Landsat។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| normalizedDifference: band not found | ឈ្មោះក្រុមរលកខុសតាមឧបករណ៍ | Sentinel-2៖ B8 B4 · Landsat C2៖ SR_B5 SR_B4 |
| if មិនដំណើរការលើ ee.Number | ប្រៀបធៀបលើ client | n.gt(50) · ee.Algorithms.If |
| map() ត្រឡប់ collection ទទេ | ភ្លេច return | ត្រូវ return img ជានិច្ច |
| require() error | ផ្លូវស្គ្រីបខុស ឬគ្មាន exports | exports.addNDVI = addNDVI |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- រូបអេក្រង់ NDVI អតិបរមា និងមធ្យម ព្រមការពន្យល់ ៣–៥ ប្រយោគ។
- ចម្លើយកែកំហុស ក ខ គ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="gt|n.gt(50)|.gt" markdown>
**១.** មុខងារ ee ណាជំនួសសញ្ញា «>»?
</div>

<div class="self-check" data-answer="SR_B5|B5" markdown>
**២.** ក្នុង Landsat 8 C2 L2 ក្រុមរលក NIR មានឈ្មោះអ្វី?
</div>

<div class="self-check" data-answer="return|រ៉េទើន" markdown>
**៣.** មុខងារក្នុង map() ត្រូវមានពាក្យគន្លឹះអ្វីជានិច្ច?
</div>

<div class="self-check" data-answer="size|s2.size()|.size()" markdown>
**៤.** មុខងារណារាប់ធាតុក្នុង collection?
</div>
