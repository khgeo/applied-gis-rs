# លំហាត់ទី១៖ ចាប់ផ្ដើមជាមួយ Code Editor

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១៖ ការគណនាលើពពក និង Google Earth Engine](../lessons/lesson-01.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · ប្រហែល ១០០ នាទី

## ស្ថានភាព

អ្នកនឹងរៀបចំគណនី Earth Engine ស្គាល់ Code Editor ដំណើរការស្គ្រីបដំបូង ហើយរាប់រូបភាព Sentinel-2 ដែលប្រើការបានលើខេត្តរបស់អ្នកតាមខែ។

## គោលបំណង

- ចុះឈ្មោះ និងភ្ជាប់គម្រោង Google Cloud សម្រាប់ Earth Engine។
- ស្គាល់ផ្ទាំងទាំងបួននៃ Code Editor ហើយរក្សាទុកស្គ្រីប។
- បង្ហាញរូបភាព Sentinel-2 ជាពណ៌ពិត និងពណ៌សន្មត។
- រាប់រូបភាពលើខេត្តមួយ តាមឆ្នាំ និងតាមកម្រិតពពក។

<figure markdown>
--8<-- "assets/svg/agv/lab01-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី១ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- គណនី Google · កម្មវិធីរុករក Chrome ឬ Firefox។
- ទិន្នន័យពីកាតាឡុក៖ `COPERNICUS/S2_SR_HARMONIZED` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-scale"></div>

## សកម្មភាពទី១៖ ចុះឈ្មោះ និងរៀបចំ · ២០ នាទី

1. ធ្វើតាម [ឧបសម្ព័ន្ធ ក](../appendix/a-gee-setup.md) ដើម្បីចុះឈ្មោះសម្រាប់ «Noncommercial / Academic use» និងបង្កើតគម្រោង Cloud។
2. បើក [code.earthengine.google.com](https://code.earthengine.google.com/)។
3. ក្នុងផ្ទាំង **Scripts** ចុច **NEW → Repository** ដាក់ឈ្មោះ `applied-gis` ហើយបង្កើតស្គ្រីប `lab01`។

## សកម្មភាពទី២៖ ស្គ្រីបដំបូង · ២០ នាទី

បិទភ្ជាប់កូដ ចុច **Run** ហើយពិនិត្យ Console និងផែនទី៖

```javascript
var pp = ee.Geometry.Point(104.92, 11.55);
var img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(pp)
  .filterDate('2024-01-01', '2024-03-31')
  .sort('CLOUDY_PIXEL_PERCENTAGE')
  .first();
print('រូបភាព', img);
Map.centerObject(pp, 11);
Map.addLayer(img, {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000}, 'ពណ៌ពិត');
Map.addLayer(img, {bands: ['B8', 'B4', 'B3'], min: 0, max: 4000}, 'ពណ៌សន្មត', false);
```

1. ក្នុង Console ពង្រីក `img` → `properties`។ កត់ត្រា `CLOUDY_PIXEL_PERCENTAGE` និង `MGRS_TILE`។
2. ប្រើ **Inspector** ចុចលើទន្លេ និងលើព្រៃ។ កត់ត្រាតម្លៃ B4 និង B8។
3. បើកស្រទាប់ «ពណ៌សន្មត» ក្នុងប្រអប់ Layers។

## សកម្មភាពទី៣៖ ខេត្តរបស់អ្នក · ២០ នាទី

```javascript
var prov = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));   // ប្ដូរឈ្មោះខេត្ត
Map.centerObject(prov, 9);
Map.addLayer(prov.style({color: 'red', fillColor: '00000000'}), {}, 'ព្រំខេត្ត');
print('ផ្ទៃខេត្ត (គម²)', prov.geometry().area().divide(1e6));
```

!!! tip "រកឈ្មោះខេត្តដែលត្រឹមត្រូវ"
    `print(ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM0_NAME', 'Cambodia')).aggregate_array('ADM1_NAME'));` បង្ហាញឈ្មោះខេត្តទាំងអស់តាមអក្ខរាវិរុទ្ធរបស់ GAUL។

## សកម្មភាពទី៤៖ រាប់រូបភាព · ២០ នាទី

```javascript
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(prov).filterDate('2024-01-01', '2025-01-01');
print('សរុប', s2.size());
print('ពពក < ២០%', s2.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)).size());
```

បំពេញតារាង (ប្ដូរ `filterDate` សម្រាប់ខែនីមួយៗ ឬប្រើ `ee.Filter.calendarRange(m, m, 'month')`)៖

| ខែ | សរុប | ពពក < ២០% |
|---|---:|---:|
| មករា | | |
| មេសា | | |
| កក្កដា | | |
| តុលា | | |

## សកម្មភាពទី៥៖ រក្សាទុក និងចែករំលែក · ១០ នាទី

1. ចុច **Save**។
2. ចុច **Get Link** ហើយចម្លងតំណ។ តំណនេះជាផ្នែកមួយនៃលទ្ធផលត្រូវប្រគល់។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a01-first-script.svg"
<figcaption>លទ្ធផលគំរូ ១៖ ប្រាំបីបន្ទាត់ ជំនួសការទាញយក ១ GB។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - ImageCollection៖ បណ្ណសារទាំងមូល · filter៖ ជ្រើសតំបន់ និងកាលបរិច្ឆេទ។
    - sort + first៖ យករូបភាពពពកតិចបំផុត។
    - addLayer៖ Earth Engine គណនា និងបង្ហាញតែក្រឡាដែលអ្នកមើល។

<figure markdown>
--8<-- "assets/svg/agv/a01-scene-count.svg"
<figcaption>លទ្ធផលគំរូ ២៖ ចំនួនរូបភាពនៅកម្ពុជា។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - មួយឆ្នាំមានរូបភាព Sentinel-2 ជាង ២ ០០០ ផ្ទាំងលើកម្ពុជា។
    - Composite មួយ ឬស៊េរីពេលវេលា អាចប្រើរូបភាពរាប់ពាន់ក្នុងការគណនាតែមួយ។
    - នេះជាហេតុផលចម្បងដែលវគ្គនេះប្រើ Earth Engine។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| ផែនទីទទេ ក្រោយចុច Run | គ្មានរូបភាពត្រូវនឹងតម្រង | print(col.size()) · ពង្រីកកាលបរិច្ឆេទ |
| រូបភាពស ឬខ្មៅទាំងស្រុង | min/max ខុស | L2A៖ min 0 · max 3000 |
| GAUL រកខេត្តមិនឃើញ | អក្ខរាវិរុទ្ធខុសពី GAUL | print aggregate_array('ADM1_NAME') |
| Not signed up / project error | មិនទាន់ភ្ជាប់គម្រោង Cloud | ធ្វើតាមឧបសម្ព័ន្ធ ក |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប (Get Link)។
- រូបអេក្រង់ពណ៌ពិត និងពណ៌សន្មតនៃខេត្តរបស់អ្នក។
- តារាងចំនួនរូបភាពតាមខែ និងកថាខណ្ឌមួយពន្យល់ភាពខុសគ្នារវាងរដូវ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់។

<div class="self-check" data-answer="Console|console" markdown>
**១.** ផ្ទាំងណាបង្ហាញលទ្ធផលពី print()?
</div>

<div class="self-check" data-answer="B8|b8" markdown>
**២.** ក្រុមរលកណាជា NIR របស់ Sentinel-2 (១០ ម)?
</div>

<div class="self-check" data-answer="10000|១០០០០|10 000" markdown>
**៣.** តម្លៃ L2A ត្រូវចែកនឹងប៉ុន្មាន ដើម្បីបានការចាំងផ្លាត ០–១?
</div>

<div class="self-check" data-answer="Get Link|get link|link" markdown>
**៤.** ប៊ូតុងណាប្រើចែករំលែកស្គ្រីប?
</div>
