# មេរៀនទី៤៖ Reducer ស្ថិតិតាមតំបន់ និងការនាំចេញ

!!! info "ព័ត៌មានមេរៀន"
    **រយៈពេលបង្រៀនដែលស្នើ៖ ៣ ម៉ោង** · មេរៀនទី ៤ ក្នុងចំណោម ១៥

[:material-presentation-play: ស្លាយបង្រៀនមេរៀននេះ](../slides/lesson-04.html){ .md-button target="_blank" }

ក្នុងមេរៀនទី៣ យើងបានបង្កើតរូបភាពស្អាតមួយសម្រាប់ខេត្តទាំងមូល។ ប៉ុន្តែអ្នកសម្រេចចិត្តកម្រសួររករូបភាពណាស់។ ពួកគេសួររក **លេខ**៖ «ស្រុកណាមានរុក្ខជាតិតិចជាងគេ?» «ផ្ទៃទឹកក្នុងខេត្តមានប៉ុន្មានគីឡូម៉ែត្រការ៉េ?» «NDVI មធ្យមឆ្នាំនេះ ទាបជាងឆ្នាំមុនទេ?»

មេរៀននេះបង្រៀនរបៀបបម្លែងរូបភាពរាប់លានក្រឡា ទៅជាតារាងស្ថិតិតាមតំបន់ ដោយប្រើ **reducer** របស់ Earth Engine ហើយនាំចេញតារាង ឬរូបភាពនោះទៅ Google Drive សម្រាប់ Excel និង QGIS។

---

## ៤.១. គោលបំណងសិក្សា

បន្ទាប់ពីបញ្ចប់មេរៀន និស្សិតអាច៖

1. ពន្យល់ថា reducer ជាអ្វី ហើយបែងចែកការបង្រួមតាមពេលវេលា តាមលំហ និងតាមក្រឡាជិតខាង។
2. គណនាស្ថិតិក្នុងតំបន់មួយដោយ reduceRegion() ហើយអានលទ្ធផល Dictionary។
3. ពន្យល់ពីឥទ្ធិពលនៃប៉ារ៉ាម៉ែត្រ scale maxPixels និង tileScale លើលទ្ធផល និងកំហុស។
4. គណនាស្ថិតិសម្រាប់តំបន់ច្រើនក្នុងពេលតែមួយដោយ reduceRegions() និងបន្សំ reducer។
5. គណនាផ្ទៃដោយ ee.Image.pixelArea() និង reducer ជាក្រុម ហើយនាំចេញលទ្ធផលជា CSV និង GeoTIFF។

### ចំណេះដឹងមុនត្រូវមាន

- [មេរៀនទី៣](lesson-03.md)៖ composite និងការលុបពពក។
- សៀវភៅទី២៖ ស្ថិតិតាមតំបន់ (zonal statistics) និងការភ្ជាប់តារាងក្នុង QGIS។

---

## ៤.២. ស្ថានភាពបើកមេរៀន៖ របាយការណ៍ប្រចាំខេត្ត

ក្រសួងមួយស្នើឲ្យក្រុមរបស់អ្នកផ្ដល់ **NDVI មធ្យមរដូវប្រាំង** សម្រាប់ខេត្តទាំង ២៥ និងស្រុកទាំងអស់ក្នុងខេត្តកំពង់ឆ្នាំង ដើម្បីកំណត់តំបន់ដែលរុក្ខជាតិខ្សោយ។ ពួកគេក៏ចង់ដឹងពីផ្ទៃទឹករដូវប្រាំងក្នុងខេត្តផង។ ក្នុង QGIS ការងារនេះត្រូវទាញយករូបភាពរាប់សិបផ្ទាំង កាត់តាមស្រុកនីមួយៗ ហើយរត់ Zonal Statistics ម្ដងមួយស្រទាប់។

សំណួរដែលមេរៀននេះឆ្លើយ៖

- តើត្រូវបម្លែងរូបភាពមួយ ទៅជាលេខមួយសម្រាប់តំបន់មួយយ៉ាងដូចម្ដេច?
- តើធ្វើការគណនាដដែលសម្រាប់តំបន់រាប់រយក្នុងពេលតែមួយបានទេ?
- តើត្រូវជ្រើស scale យ៉ាងណា ហើយហេតុអ្វីចម្លើយប្ដូរនៅពេល scale ប្ដូរ?
- តើត្រូវយកលទ្ធផលចេញពី Earth Engine ទៅ Excel ឬ QGIS យ៉ាងដូចម្ដេច?

---

## ៤.៣. ទ្រឹស្ដីស្នូល

### ៤.៣.១. Reducer ជាអ្វី

<figure markdown>
--8<-- "assets/svg/agv/a04-directions.svg"
<figcaption>រូបទី៤.១៖ Reducer មួយ ប្រើបានបួនបែប។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - មេរៀនទី៣៖ បង្រួមតាមពេលវេលា (median) ដើម្បីបានរូបភាពមួយ។
    - មេរៀននេះ៖ បង្រួមតាមលំហ ដើម្បីបានលេខ ឬតារាង (reduceRegion · reduceRegions)។
    - ee.Reducer ដដែល (mean · sum · count · percentile) ប្រើបានក្នុងទិសដៅទាំងបួន។


**Reducer** គឺជាមុខងារដែលយកតម្លៃច្រើន ហើយត្រឡប់តម្លៃតិចជាង (ភាគច្រើនតម្លៃមួយ)៖ មធ្យម ផលបូក ចំនួន អប្បបរមា អតិបរមា ភាគរយ (percentile) ឬអ៊ីស្តូក្រាម។ ក្នុង Earth Engine reducer ជាវត្ថុ `ee.Reducer` ដាច់ដោយឡែក ដែលអាចប្រើជាមួយមុខងារបង្រួមផ្សេងៗ៖

| មុខងារ | បង្រួមតាម | លទ្ធផល |
|---|---|---|
| `collection.reduce()` · `median()` | ពេលវេលា (មេរៀនទី៣) | ee.Image មួយ |
| `image.reduceRegion()` | លំហ ក្នុងតំបន់មួយ | ee.Dictionary |
| `image.reduceRegions()` | លំហ ក្នុងតំបន់ច្រើន | ee.FeatureCollection |
| `image.reduceNeighborhood()` | ក្រឡាជិតខាង (kernel) | ee.Image |
| `list.reduce()` · `fc.reduceColumns()` | បញ្ជី ឬជួរឈរនៃតារាង | ee.Dictionary |

ការយល់ឃើញនេះសំខាន់៖ `ee.Reducer.mean()` ដដែលអាចផ្ដល់រូបភាពមធ្យមតាមពេលវេលា ឬលេខមធ្យមក្នុងស្រុកមួយ អាស្រ័យលើមុខងារដែលយើងហៅ។ ដូច្នេះត្រូវសួរខ្លួនឯងជានិច្ចថា៖ «ខ្ញុំកំពុងបង្រួមតាមវិមាត្រណា?»

### ៤.៣.២. reduceRegion()៖ ពីក្រឡារាប់ពាន់ ទៅជាលេខមួយ

<figure markdown>
--8<-- "assets/svg/agv/a04-region.svg"
<figcaption>រូបទី៤.២៖ ពីក្រឡារាប់ពាន់ ទៅជាលេខមួយ។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - តំបន់នេះមាន ៨ ០០០ ក្រឡា Landsat ៣០ ម៖ reduceRegion ត្រឡប់ Dictionary មួយ។
    - reducer ផ្សេងគ្នា ផ្ដល់ចម្លើយខុសគ្នា៖ mean និង median មិនដូចគ្នាទេ ពេលទិន្នន័យលំអៀង។
    - តួលេខគណនាពីរូបភាព Landsat 8 ពិតលើភ្នំពេញ (TOA · មិនបានកែបរិយាកាស)។


`reduceRegion()` គណនាស្ថិតិនៃក្រឡាទាំងអស់ក្នុងធរណីមាត្រមួយ ហើយត្រឡប់ **Dictionary** ដែលមានគន្លឹះមួយក្នុងមួយក្រុមរលក៖

```javascript
var aoi = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));
var ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI');

var stats = ndvi.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: aoi.geometry(),
  scale: 10,            // ទំហំក្រឡាដែលប្រើក្នុងការគណនា (ម៉ែត្រ)
  maxPixels: 1e10       // ចំនួនក្រឡាអតិបរមាដែលអនុញ្ញាត
});
print('NDVI មធ្យម', stats);                 // {NDVI: 0.52}
print('តម្លៃតែលេខ', stats.get('NDVI'));    // 0.52
```

ចំណុចត្រូវចាំ៖

- លទ្ធផលជា **ee.Dictionary** មិនមែនលេខ JavaScript ទេ។ ប្រើ `.get('NDVI')` ដើម្បីយកតម្លៃ ហើយរុំវាក្នុង `ee.Number()` ប្រសិនបើត្រូវគណនាបន្ត។
- ក្រឡាដែលត្រូវបាន mask (ពពក ឬក្រៅតំបន់ clip) **មិនត្រូវបានរាប់ទេ**។ ដូច្នេះ `count()` ប្រាប់ពីចំនួនក្រឡាដែលពិតជាបានប្រើ។
- ក្រឡានៅគែមធរណីមាត្រ ត្រូវបានរាប់ដោយទម្ងន់ តាមផ្នែកដែលស្ថិតក្នុងធរណីមាត្រ (reducer ភាគច្រើន ដូចជា mean និង sum)។

### ៤.៣.៣. scale ប្ដូរចម្លើយ

<figure markdown>
--8<-- "assets/svg/agv/a04-scale.svg"
<figcaption>រូបទី៤.៣៖ scale គឺជាការសម្រេចចិត្ត មិនមែនលម្អិតតូចទេ។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - mean ស្ទើរមិនប្ដូរ (០,១១ → ០,១១) ប៉ុន្តែ max និង stdDev ធ្លាក់ ហើយផ្ទៃទឹកថយពី ១៩% ទៅ ១១%។
    - scale ធំលាយក្រឡាតូចៗចូលគ្នា៖ វត្ថុតូច និងគែមតំបន់បាត់ ហើយចំនួនក្រឡាថយពីរាប់ពាន់ទៅតិចជាងដប់។
    - scale កំណត់ទំហំក្រឡាដែល Earth Engine ប្រើក្នុងការគណនា៖ សរសេរវាជានិច្ច ហើយរាយការណ៍វាជាមួយលទ្ធផល។


Earth Engine មិនធ្វើការលើក្រឡាដើមនៃរូបភាពដោយស្វ័យប្រវត្តិទេ។ វាធ្វើការនៅ **scale ដែលអ្នកប្រាប់**។ ប្រសិនបើ scale ធំជាងក្រឡាដើម វាប្រើស្រទាប់ពីរ៉ាមីត (pyramid) ដែលក្រឡាតូចៗត្រូវបានបូកមធ្យមរួចហើយ។ លទ្ធផល៖

- **mean** ស្ទើរមិនប្ដូរ ព្រោះមធ្យមនៃមធ្យមនៅតែជាមធ្យម។
- **max min stdDev** និង **ភាគរយនៃក្រឡាលើសកម្រិត** ប្ដូរច្រើន ព្រោះក្រឡាធំលាយវត្ថុតូចៗ និងគែមចូលគ្នា។
- **count** ថយខ្លាំង៖ scale ធំ ៣ ដង មានក្រឡាតិចជាង ៩ ដង។

ប្រសិនបើអ្នកមិនដាក់ `scale` ទេ Earth Engine ប្រើ scale លំនាំដើមនៃរូបភាព ដែលសម្រាប់ composite ជាញឹកញាប់ **១ ដឺក្រេ (~១១១ គម)**៖ លទ្ធផលស្ទើរតែគ្មានន័យ។ ដូច្នេះ **ត្រូវដាក់ scale ជានិច្ច**៖ ១០ ម សម្រាប់ Sentinel-2 ៣០ ម សម្រាប់ Landsat ហើយធំជាងនេះ (១០០–៥០០ ម) តែពេលតំបន់ធំខ្លាំង ហើយអ្នកដឹងថាកំពុងបាត់បង់ព័ត៌មានលម្អិត។

!!! example "ពិសោធន៍៖ reducer និង scale លើរូបភាពពិត"
    គូររង្វង់ ឬប្រអប់លើរូបភាព NDVI Sentinel-2 ពិត ជ្រើស reducer និង scale ហើយមើលថាលេខ និងចំនួនក្រឡាប្ដូរយ៉ាងដូចម្ដេច។ ប្រៀបធៀប mean ជាមួយ max ពេល scale កើនឡើង។

<div class="sim" data-sim="gee-zonal"></div>

### ៤.៣.៤. maxPixels bestEffort និង tileScale

នៅពេលតំបន់ធំ និង scale តូច ចំនួនក្រឡាអាចលើសដែនកំណត់ ហើយ Earth Engine បង្ហាញកំហុស៖

| សារកំហុស | មូលហេតុ | ដំណោះស្រាយ |
|---|---|---|
| `Too many pixels in the region` | ក្រឡាលើស maxPixels (លំនាំដើម ១០ លាន) | ដាក់ `maxPixels: 1e10` |
| `User memory limit exceeded` | ក្រឡាមួយ tile ត្រូវការអង្គចងចាំច្រើន | ដាក់ `tileScale: 4` (ឬ ៨ ១៦) |
| `Computation timed out` | ការគណនាយូរជាង ៥ នាទីក្នុង Code Editor | ប្រើ Export ជំនួស print |

`bestEffort: true` ក៏ដោះស្រាយកំហុសក្រឡាច្រើនដែរ ប៉ុន្តែវាធ្វើដោយ **បង្កើន scale ដោយស្ងាត់ៗ**។ អ្នកប្រហែលជាគិតថាបានគណនានៅ ១០ ម តែការពិតវាគណនានៅ ២៥០ ម។ ដូច្នេះចូលចិត្ត `maxPixels` និង `tileScale` ជាង `bestEffort`។ `tileScale` បំបែកការគណនាជាផ្ទាំងតូចៗ៖ យឺតជាងបន្តិច ប៉ុន្តែប្រើអង្គចងចាំតិច។

### ៤.៣.៥. បន្សំ reducer៖ ស្ថិតិច្រើនក្នុងការហៅតែមួយ

<figure markdown>
--8<-- "assets/svg/agv/a04-combine.svg"
<figcaption>រូបទី៤.៤៖ មធ្យមតែមួយ លាក់ការបែងចែក។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - អ៊ីស្តូក្រាមមានពីរក្រុម៖ ទឹក (NDVI អវិជ្ជមាន ពណ៌ខៀវ) និងដី/រុក្ខជាតិ (NDVI វិជ្ជមាន)។ មធ្យមធ្លាក់នៅចន្លោះ ដែលគ្មានក្រឡាច្រើន។
    - combine() គណនា mean stdDev និង percentile ក្នុងការឆ្លងកាត់ទិន្នន័យតែម្ដង។
    - ឈ្មោះគន្លឹះក្នុងលទ្ធផល ប្ដូរទៅជា NDVI_mean NDVI_p50 … ត្រូវប្រើឈ្មោះនេះពេល get()។


មធ្យមតែមួយលាក់ការបែងចែករបស់ទិន្នន័យ។ តំបន់ដែលមានទឹកពាក់កណ្ដាល និងរុក្ខជាតិពាក់កណ្ដាល អាចមាន NDVI មធ្យមប្រហែល ០,១ ដែលមិនតំណាងក្រឡាណាមួយទាល់តែសោះ។ `combine()` ភ្ជាប់ reducer ជាច្រើន ដើម្បីគណនាក្នុងការឆ្លងកាត់ទិន្នន័យតែម្ដង៖

```javascript
var reducer = ee.Reducer.mean()
  .combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true})
  .combine({reducer2: ee.Reducer.percentile([10, 50, 90]), sharedInputs: true})
  .combine({reducer2: ee.Reducer.count(), sharedInputs: true});
var stats = ndvi.reduceRegion({reducer: reducer, geometry: aoi.geometry(), scale: 10, maxPixels: 1e10});
print(stats);   // NDVI_mean NDVI_stdDev NDVI_p10 NDVI_p50 NDVI_p90 NDVI_count
```

`sharedInputs: true` មានន័យថា reducer ទាំងអស់ប្រើក្រុមរលកដដែល។ ឈ្មោះគន្លឹះក្នុងលទ្ធផលក្លាយជា **ក្រុមរលក_reducer** (ឧ. `NDVI_mean`)។ ពេលមានក្រុមរលកតែមួយ ហើយប្រើ reducer តែមួយ ឈ្មោះគន្លឹះគឺឈ្មោះក្រុមរលក (`NDVI`)។ ភាពខុសគ្នានេះជាមូលហេតុញឹកញាប់នៃ `get()` ដែលត្រឡប់ `null`។

### ៤.៣.៦. reduceRegions()៖ តំបន់ច្រើន ក្នុងពេលតែមួយ

<figure markdown>
--8<-- "assets/svg/agv/a04-regions.svg"
<figcaption>រូបទី៤.៥៖ តារាងស្ថិតិ ក្លាយជាផែនទី។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - reduceRegions បន្ថែមលក្ខណៈ (ឧ. mean) ទៅលើ Feature នីមួយៗ ក្នុង FeatureCollection ដើម។
    - លទ្ធផលជាតារាង៖ នាំចេញជា CSV ឬ SHP ហើយធ្វើផែនទី choropleth ក្នុង QGIS (សៀវភៅទី១)។
    - តម្លៃក្នុងរូបនេះជាគំរូ៖ លំហាត់ទី៤ គណនាតម្លៃពិតសម្រាប់ខេត្តទាំង ២៥។


`reduceRegions()` ទទួល **FeatureCollection** (ឧ. ស្រុកទាំងអស់) ហើយត្រឡប់ FeatureCollection ដដែល ដែល Feature នីមួយៗមានលក្ខណៈថ្មីពី reducer៖

```javascript
var districts = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));

var table = ndvi.reduceRegions({
  collection: districts,
  reducer: ee.Reducer.mean(),
  scale: 10,
  tileScale: 4
});
print(table.limit(5));   // ADM2_NAME, ..., mean
```

ចំណុចខុសពី reduceRegion៖ reduceRegions **មិនមាន maxPixels ទេ** ហើយឈ្មោះលក្ខណៈលទ្ធផលគឺឈ្មោះ reducer (`mean`) មិនមែន `NDVI_mean` ទេ។ ប្រសិនបើរូបភាពមានក្រុមរលកច្រើន ឈ្មោះក្លាយជា `B4_mean` ។ល។ ពេល Feature ធ្វើការជាមួយតំបន់ធំ ឬ scale តូច reduceRegions ស្ទើរតែតែងតែត្រូវ Export ជាជាង print។

លទ្ធផលគឺជាតារាងដែលមានធរណីមាត្រ៖ ដូច្នេះវាអាចបង្ហាញជាផែនទី choropleth ក្នុង Earth Engine ឬនាំចេញទៅ QGIS ដើម្បីធ្វើប្លង់ផែនទីតាមគោលការណ៍ក្នុងសៀវភៅទី១។

### ៤.៣.៧. គណនាផ្ទៃដោយ pixelArea()

<figure markdown>
--8<-- "assets/svg/agv/a04-area.svg"
<figcaption>រូបទី៤.៦៖ ផ្ទៃពិត មិនមែនចំនួនក្រឡា។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - pixelArea() ផ្ដល់ផ្ទៃ (ម²) របស់ក្រឡានីមួយៗ តាមទីតាំងពិត មិនមែនលេខថេរទេ។
    - group() បំបែកផលបូកតាមថ្នាក់៖ ផ្ទៃដីមួយថ្នាក់ៗ ក្នុងការគណនាតែមួយ។
    - រូបភាពគំរូ ៣០០ × ៣០០ ក្រឡា ៣០ ម = ៨១ គម²។ ផ្ទៃនេះជាលទ្ធផលគណនាពិតពីផែនទីគំរូ។


ការគណនាផ្ទៃដោយ «ចំនួនក្រឡា × ១០០ ម²» ងាយខុស ព្រោះក្រឡាក្នុង EPSG:4326 មិនមានទំហំស្មើគ្នា ហើយ scale ដែលប្រើប្រហែលជាមិនមែន ១០ ម។ `ee.Image.pixelArea()` បង្កើតរូបភាពដែលក្រឡានីមួយៗមានតម្លៃស្មើនឹង **ផ្ទៃពិតរបស់វា (ម²)** នៅ scale ដែលប្រើ។ វិធី៖ គុណ pixelArea ជាមួយ mask (០/១) រួច sum៖

```javascript
var water = composite.normalizedDifference(['B3', 'B11']).gt(0);   // MNDWI > 0
var waterKm2 = water.multiply(ee.Image.pixelArea()).divide(1e6)
  .reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 10, maxPixels: 1e10});
print('ផ្ទៃទឹក (គម²)', waterKm2);
```

សម្រាប់ផែនទីចាត់ថ្នាក់ (មេរៀនទី៦) **reducer ជាក្រុម** គណនាផ្ទៃនៃគ្រប់ថ្នាក់ក្នុងការហៅតែមួយ៖

```javascript
var areas = ee.Image.pixelArea().divide(1e6).addBands(classified)
  .reduceRegion({
    reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'class'}),
    geometry: aoi.geometry(), scale: 10, maxPixels: 1e10
  });
print(areas.get('groups'));   // [{class: 0, sum: 12.4}, {class: 1, sum: 30.1}, ...]
```

`groupField: 1` មានន័យថា ក្រុមរលកទី ២ (លិបិក្រម ១) គឺជាលេខថ្នាក់ ហើយក្រុមរលកទី ១ គឺជាតម្លៃដែលត្រូវបូក។ ត្រូវរក្សាលំដាប់នេះ។

### ៤.៣.៨. print() ឬ Export?

<figure markdown>
--8<-- "assets/svg/agv/a04-export.svg"
<figcaption>រូបទី៤.៧៖ ពេលណាត្រូវនាំចេញ។</figcaption>
</figure>

!!! note "អានរូបនេះ"
    - print() និង Chart ដំណើរការក្នុងកម្មវិធីរុករក ហើយមានកំណត់ពេល (ប្រហែល ៥ នាទី)។
    - Export រត់ជា Task នៅម៉ាស៊ីនមេ អាចចំណាយពេលរាប់ម៉ោង ហើយមិនពឹងលើកម្មវិធីរុករកទេ។
    - លទ្ធផលស្ថិតិជាតារាង៖ ប្រើ Export.table ជាមួយ selectors ដើម្បីរក្សាតែជួរឈរដែលត្រូវការ។


`print()` និង `ui.Chart` ល្អសម្រាប់ពិនិត្យលទ្ធផលតូចៗភ្លាមៗ។ ប៉ុន្តែការគណនាក្នុង Code Editor មានកំណត់ពេល និងអង្គចងចាំ។ **Export** បញ្ជូនការងារទៅជា Task ដែលរត់នៅម៉ាស៊ីនមេ អាចចំណាយពេលរាប់ម៉ោង ហើយរក្សាលទ្ធផលទៅ Google Drive ឬ Asset៖

```javascript
Export.table.toDrive({
  collection: table,
  description: 'KCH_district_NDVI_2024',
  folder: 'applied_gis',
  fileFormat: 'CSV',
  selectors: ['ADM2_CODE', 'ADM2_NAME', 'mean']   // ជួរឈរដែលត្រូវការប៉ុណ្ណោះ
});
```

`selectors` សំខាន់ណាស់៖ បើគ្មានវា CSV រួមទាំងជួរឈរ `.geo` (ធរណីមាត្រជា GeoJSON) ដែលធ្វើឲ្យឯកសារធំ ហើយពិបាកបើកក្នុង Excel។ ប្រសិនបើត្រូវការផែនទីក្នុង QGIS សូមប្រើ `fileFormat: 'SHP'` ឬ `'GeoJSON'` ជំនួសវិញ ឬរក្សា ADM2_CODE ដើម្បីភ្ជាប់ (join) ជាមួយស្រទាប់ព្រំដែនដែលអ្នកមានរួច។

!!! tip "ដាក់ឈ្មោះ description ឲ្យច្បាស់"
    description ក្លាយជាឈ្មោះឯកសារ។ ប្រើទម្រង់ `តំបន់_អ្វី_ឆ្នាំ` (ឧ. `KCH_NDVI_dry_2024`) ហើយកុំប្រើដកឃ្លា ឬអក្សរខ្មែរ ព្រោះ Earth Engine មិនទទួលយកទេ។

---

## ៤.៤. ឧទាហរណ៍ដែលបានដោះស្រាយ៖ NDVI រដូវប្រាំងតាមស្រុកក្នុងខេត្តកំពង់ឆ្នាំង

### ជំហានទី១៖ រៀបចំ composite និង NDVI

```javascript
var prov = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));
var districts = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kampong Chhnang'));
function maskS2(img) {
  var scl = img.select('SCL');
  var ok = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return img.updateMask(ok).divide(10000).copyProperties(img, ['system:time_start']);
}
var comp = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(prov).filterDate('2023-11-01', '2024-05-01')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
  .map(maskS2).median().clip(prov);
var ndvi = comp.normalizedDifference(['B8', 'B4']).rename('NDVI');
```

### ជំហានទី២៖ ពិនិត្យលើខេត្តទាំងមូលមុន

```javascript
print('ខេត្ត', ndvi.reduceRegion({reducer: ee.Reducer.mean(), geometry: prov.geometry(), scale: 10, maxPixels: 1e10}));
```

ការពិនិត្យលើតំបន់មួយមុន ជួយរកកំហុស (ឈ្មោះក្រុមរលកខុស scale ភ្លេច) មុនពេលរត់លើស្រុកទាំងអស់។

### ជំហានទី៣៖ ស្ថិតិតាមស្រុក

```javascript
var reducer = ee.Reducer.mean().combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true});
var byDistrict = ndvi.reduceRegions({collection: districts, reducer: reducer, scale: 10, tileScale: 4});
print(byDistrict.select(['ADM2_NAME', 'mean', 'stdDev']));
Map.addLayer(byDistrict.reduceToImage(['mean'], ee.Reducer.first()),
             {min: 0.2, max: 0.6, palette: ['#ffffcc', '#78c679', '#006837']}, 'NDVI មធ្យមតាមស្រុក');
```

### ជំហានទី៤៖ នាំចេញ

```javascript
Export.table.toDrive({collection: byDistrict, description: 'KCH_district_NDVI_dry_2024',
  folder: 'applied_gis', fileFormat: 'CSV', selectors: ['ADM2_CODE', 'ADM2_NAME', 'mean', 'stdDev']});
```

### ជំហានទី៥៖ បកស្រាយ

បើកតារាងក្នុង Excel ហើយតម្រៀបតាម `mean`។ ស្រុកដែលមានវាលស្រែ និងតំបន់លិចទឹកជិតទន្លេសាបច្រើន ទំនងជាមាន NDVI រដូវប្រាំងទាប ព្រោះស្រែត្រូវបានច្រូតរួច ឬនៅតែមានទឹក។ ស្រុកដែលមានព្រៃ និងភ្នំច្រើន ទំនងជាមាន NDVI ខ្ពស់។ `stdDev` ខ្ពស់ប្រាប់ថាស្រុកនោះមានគម្របដីចម្រុះ ដូច្នេះមធ្យមរបស់វាតំណាងមិនល្អ។

> «NDVI មធ្យមរដូវប្រាំង ២០២៣–២០២៤ (Sentinel-2 · median · scale ១០ ម) ត្រូវបានគណនាសម្រាប់ស្រុកនីមួយៗ។ ស្រុកដែលមាន NDVI ទាប ត្រូវពិនិត្យបន្តជាមួយស៊េរីពេលវេលា (មេរៀនទី៥) មុនសន្និដ្ឋានថារុក្ខជាតិខ្សោយ។»

!!! warning "អ្វីដែលយើងមិនអាចសន្និដ្ឋាន"
    NDVI ទាបក្នុងរដូវប្រាំង មិនមានន័យថាដំណាំខ្សោយទេ៖ វាអាចជាស្រែដែលច្រូតរួច ដីទំនេរ ឬទឹក។ មធ្យមតាមស្រុកក៏លាក់ភាពខុសគ្នាក្នុងស្រុក និងពឹងលើព្រំដែន GAUL ដែលប្រហែលជាមិនត្រូវនឹងព្រំដែនរដ្ឋបាលផ្លូវការថ្មីបំផុតទេ។

---

## ៤.៥. សកម្មភាពអនុវត្ត

- **លំហាត់ទី៤**៖ គណនា NDVI មធ្យមតាមខេត្តទាំង ២៥ និងតាមស្រុកក្នុងខេត្តរបស់អ្នក គណនាផ្ទៃទឹក ហើយនាំចេញ CSV ទៅធ្វើផែនទីក្នុង QGIS។ មើល [លំហាត់ទី៤](../workbook/lab-04.md)។
- **ក្នុងថ្នាក់**៖ ក្រុមនីមួយៗគណនា NDVI មធ្យមនៃខេត្តដូចគ្នានៅ scale ខុសគ្នា (១០ ៣០ ១០០ ៥០០ ម) ហើយប្រៀបធៀប mean max និង count លើក្ដារខៀន។

---

## ៤.៦. ការយល់ច្រឡំដែលត្រូវប្រុងប្រយ័ត្ន

**១. «reduceRegion ធ្វើការលើក្រឡាដើមនៃរូបភាពជានិច្ច»**
វាធ្វើការនៅ scale ដែលអ្នកប្រាប់។ បើគ្មាន scale វាអាចប្រើក្រឡាធំ ១ ដឺក្រេ ហើយលទ្ធផលគ្មានន័យ។

**២. «bestEffort ធ្វើឲ្យការគណនាដំណើរការ ដូច្នេះវាល្អ»**
bestEffort បង្កើន scale ដោយស្ងាត់ៗ។ ប្រើ maxPixels និង tileScale ជំនួសវិញ ហើយកត់ត្រា scale ពិតប្រាកដ។

**៣. «ផ្ទៃ = ចំនួនក្រឡា × ១០០ ម²»**
ទំហំក្រឡាអាស្រ័យលើ scale និង CRS ហើយក្រឡាគែមត្រូវបានរាប់ដោយទម្ងន់។ ប្រើ ee.Image.pixelArea()។

**៤. «ក្រឡាដែលបាន mask ត្រូវបានរាប់ជាសូន្យ»**
វាមិនត្រូវបានរាប់ទាល់តែសោះ។ ប្រសិនបើ ៨០% នៃខេត្តមានពពក មធ្យមតំណាងតែ ២០% ដែលនៅសល់ប៉ុណ្ណោះ៖ ពិនិត្យ count ជាមួយ។

**៥. «ប្រសិនបើ print ដំណើរការ មិនចាំបាច់ Export ទេ»**
print ល្អសម្រាប់ពិនិត្យ។ ដើម្បីរក្សាលទ្ធផលឲ្យអ្នកដទៃប្រើ និងធ្វើឡើងវិញបាន ត្រូវ Export ទៅ Drive ឬ Asset។

---

## ៤.៧. សេចក្ដីសង្ខេបមេរៀន

Reducer បង្រួមតម្លៃច្រើនទៅជាតម្លៃតិច។ reduceRegion() ផ្ដល់ Dictionary សម្រាប់តំបន់មួយ ហើយ reduceRegions() បន្ថែមស្ថិតិទៅ Feature នីមួយៗនៃ FeatureCollection ដែលក្លាយជាតារាងសម្រាប់ Excel និងផែនទីសម្រាប់ QGIS។ combine() គណនាស្ថិតិច្រើនក្នុងការហៅតែមួយ ហើយ pixelArea() ជាមួយ reducer ជាក្រុម ផ្ដល់ផ្ទៃពិតតាមថ្នាក់។

scale ជាការសម្រេចចិត្តវិទ្យាសាស្ត្រ៖ វាប៉ះពាល់ដល់ max stdDev ផ្ទៃ និងចំនួនក្រឡា។ ត្រូវដាក់ scale ជានិច្ច ដោះស្រាយកំហុសដោយ maxPixels និង tileScale ហើយប្រើ Export សម្រាប់លទ្ធផលធំ ឬលទ្ធផលដែលត្រូវរក្សាទុក។

!!! abstract "គំនិតស្នូលនៃមេរៀន"
    រូបភាពឆ្លើយសំណួរ «នៅទីណា?» ហើយ reducer ឆ្លើយសំណួរ «ប៉ុន្មាន?»។ ចម្លើយនោះត្រឹមត្រូវ លុះត្រាតែអ្នកដឹង និងរាយការណ៍ scale តំបន់ និងក្រឡាដែលបានប្រើ។

---

## ៤.៨. ពាក្យគន្លឹះខ្មែរ–អង់គ្លេស

| ពាក្យខ្មែរ | ពាក្យអង់គ្លេស | អត្ថន័យខ្លី |
|---|---|---|
| មុខងារបង្រួម | Reducer | បម្លែងតម្លៃច្រើនទៅជាតម្លៃតិច |
| ស្ថិតិតាមតំបន់ | Zonal statistics | ស្ថិតិនៃក្រឡាក្នុងតំបន់នីមួយៗ |
| វចនានុក្រម | Dictionary | គូគន្លឹះ–តម្លៃ (ឧ. {NDVI: 0.52}) |
| មាត្រដ្ឋានគណនា | Scale | ទំហំក្រឡា (ម) ដែលប្រើក្នុងការគណនា |
| ពីរ៉ាមីតរូបភាព | Image pyramid | កម្រិតក្រឡាធំៗដែលគណនារួច |
| ផ្ទៃក្រឡា | Pixel area | ផ្ទៃពិត (ម²) នៃក្រឡានីមួយៗ |
| reducer ជាក្រុម | Grouped reducer | គណនាស្ថិតិតាមថ្នាក់នីមួយៗ |
| ការនាំចេញ | Export (Task) | រក្សាលទ្ធផលទៅ Drive ឬ Asset |

---

## ៤.៩. សំណួររំលឹក និងវាយតម្លៃ

### ក. សំណួរយល់ដឹង

1. រាយមុខងារបង្រួមបួន ហើយប្រាប់ថាមុខងារនីមួយៗបង្រួមតាមវិមាត្រណា និងត្រឡប់វត្ថុប្រភេទណា។
2. ហេតុអ្វី mean ស្ទើរមិនប្ដូរ ប៉ុន្តែ max ប្ដូរច្រើន នៅពេល scale កើនឡើង?
3. ភាពខុសគ្នារវាង maxPixels tileScale និង bestEffort?
4. ហេតុអ្វីមធ្យមតែមួយអាចបំភាន់? ស្ថិតិអ្វីខ្លះគួរភ្ជាប់ជាមួយ?
5. ពន្យល់ពីមូលហេតុដែល CSV ដែលនាំចេញមានជួរឈរ `.geo` និងរបៀបដកវាចេញ។

### ខ. សំណួរអនុវត្តគោលគំនិត

6. សរសេរកូដគណនា NDVI p10 p50 p90 នៃខេត្តមួយក្នុងការហៅ reduceRegion តែមួយ ហើយប្រាប់ឈ្មោះគន្លឹះនៃលទ្ធផល។
7. `stats.get('NDVI_mean')` ត្រឡប់ null។ រាយមូលហេតុពីរដែលអាចកើតឡើង។
8. សរសេរកូដគណនាផ្ទៃព្រៃ (NDVI > ០,៦) ជាគីឡូម៉ែត្រការ៉េក្នុងខេត្តមួយ។
9. ខេត្តមួយមានពពក ៧០% ក្នុង composite រដូវវស្សា។ តើអ្នកនឹងរាយការណ៍ NDVI មធ្យមនោះដូចម្ដេច?
10. ប្រៀបធៀបការគណនា zonal statistics ក្នុង QGIS និង Earth Engine៖ ពេលណាគួរប្រើមួយណា?

### គ. កិច្ចការខ្លី

គណនាផ្ទៃទឹក (MNDWI > ០) នៃខេត្តរបស់អ្នកក្នុងខែមីនា និងខែតុលា ឆ្នាំតែមួយ។ សរសេរកថាខណ្ឌមួយពន្យល់ភាពខុសគ្នា ហើយរាយការណ៍ scale និងចំនួនក្រឡាស្អាតដែលបានប្រើ។

---

## កំណត់សម្គាល់សម្រាប់គ្រូបង្រៀន

### ក. ការបែងចែកពេលវេលា ១៨០ នាទី

| សកម្មភាព | ពេលវេលា |
|---|---:|
| ស្ថានភាពបើកមេរៀន៖ របាយការណ៍ប្រចាំខេត្ត | ១៥ នាទី |
| Reducer ជាអ្វី · ទិសដៅបួន | ១៥ នាទី |
| reduceRegion និង Dictionary | ២៥ នាទី |
| scale · ពិសោធន៍ · maxPixels tileScale | ៣៥ នាទី |
| បន្សំ reducer និង reduceRegions | ៣០ នាទី |
| pixelArea និង reducer ជាក្រុម | ២០ នាទី |
| Export · ឧទាហរណ៍កំពង់ឆ្នាំង | ២៥ នាទី |
| សង្ខេប និងណែនាំលំហាត់ | ១៥ នាទី |
| **សរុប** | **១៨០ នាទី / ៣ ម៉ោង** |

### ខ. ការភ្ជាប់ទៅមេរៀនបន្ទាប់

មេរៀននេះគណនាស្ថិតិលើ composite មួយ ពោលគឺលេខមួយសម្រាប់រយៈពេលមួយ។ ប៉ុន្តែស្រែ ព្រៃ និងទឹកប្ដូររាល់ខែ ហើយការប្ដូរនោះហើយដែលប្រាប់ពីដំណាំ គ្រោះរាំងស្ងួត ឬការបាត់បង់ព្រៃ។

> តើត្រូវតាមដានតម្លៃមួយតាមពេលវេលា ហើយបម្លែងក្រាបដែលមានពពកច្រើន ទៅជាព័ត៌មានអំពីរដូវដំណាំយ៉ាងដូចម្ដេច?

សំណួរនេះនាំទៅ **មេរៀនទី៥៖ ស៊េរីពេលវេលា និងរដូវកាលរុក្ខជាតិ**។

⬅️ [មេរៀនទី៣](lesson-03.md) · ➡️ [មេរៀនទី៥](lesson-05.md)
