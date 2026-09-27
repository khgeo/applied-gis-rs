# លំហាត់ទី១០៖ Hansen GFC និងតំបន់ការពារ

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១០៖ ព្រៃឈើ និងការបាត់បង់ព្រៃ](../lessons/lesson-10.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១៣០ នាទី

## ស្ថានភាព

អ្នកនឹងរៀបចំទិន្នន័យសម្រាប់របាយការណ៍ការបាត់បង់ព្រៃថ្នាក់ជាតិ៖ ព្រៃឆ្នាំ ២០០០ និងការបាត់បង់តាមខេត្ត តាមឆ្នាំ និងតាមកម្រិតពីរ ហើយវិភាគតំបន់ការពារមួយ ជាមួយតំបន់ទ្រនាប់ និងការពិនិត្យគំរូ។

## គោលបំណង

- កំណត់ព្រៃឆ្នាំ ២០០០ ដោយកម្រិត ១០% និង ៣០% ហើយប្រៀបធៀបផ្ទៃ។
- គណនាផ្ទៃ និងអត្រាបាត់បង់តាមខេត្តទាំង ២៥។
- គណនាការបាត់បង់តាមឆ្នាំក្នុងតំបន់ការពារមួយ និងតំបន់ទ្រនាប់។
- ពិនិត្យក្រឡាបាត់បង់គំរូ ២០ ដោយភ្នែក ហើយកត់ត្រាប្រភេទ។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `UMD/hansen/global_forest_change_2023_v1_11` (ឬកំណែថ្មីជាងក្នុងកាតាឡុក) · `WCMC/WDPA/current/polygons` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-forest"></div>

ប្ដូរកម្រិតពី ១០% ទៅ ៥០%។ ផ្ទៃព្រៃប្ដូរប៉ុន្មាន? អត្រាបាត់បង់ក្នុងតំបន់ការពារប្ដូរដែរទេ?

## សកម្មភាពទី១៖ ព្រៃ ២០០០ តាមកម្រិតពីរ · ២០ នាទី

```javascript
var gfc = ee.Image('UMD/hansen/global_forest_change_2023_v1_11');
var provs = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM0_NAME', 'Cambodia'));
var ha = ee.Image.pixelArea().divide(1e4);
var tc = gfc.select('treecover2000');
var img = ha.updateMask(tc.gte(10)).rename('f10').addBands(ha.updateMask(tc.gte(30)).rename('f30'))
  .addBands(ha.updateMask(gfc.select('loss').and(tc.gte(10))).rename('l10'))
  .addBands(ha.updateMask(gfc.select('loss').and(tc.gte(30))).rename('l30'));
Map.centerObject(provs, 7);
Map.addLayer(tc.clip(provs), {min: 0, max: 100, palette: ['white', 'green']}, 'treecover2000');
Map.addLayer(gfc.select('lossyear').selfMask().clip(provs), {min: 1, max: 23, palette: ['yellow', 'red']}, 'lossyear');
```

## សកម្មភាពទី២៖ តារាងខេត្ត · ២៥ នាទី

```javascript
var table = img.reduceRegions({collection: provs, reducer: ee.Reducer.sum(), scale: 30, tileScale: 16})
  .map(function(f) {
    return f.set('rate30', ee.Number(f.get('l30')).divide(f.get('f30')).multiply(100));
  });
Export.table.toDrive({collection: table, description: 'KH_forest_loss_by_province', folder: 'applied_gis',
  fileFormat: 'CSV', selectors: ['ADM1_CODE', 'ADM1_NAME', 'f10', 'f30', 'l10', 'l30', 'rate30']});
```

ការគណនានេះធំ (ប្រទេសទាំងមូល នៅ ៣០ ម)៖ ត្រូវតែ Export។ ខណៈរង់ចាំ សូមធ្វើសកម្មភាពទី៣។ ពេល CSV មកដល់ សូមតម្រៀបខេត្តតាម `l30` និងតាម `rate30`។ តើលំដាប់ខុសគ្នាទេ?

## សកម្មភាពទី៣៖ តំបន់ការពារ និងទ្រនាប់ · ៣០ នាទី

```javascript
var wdpa = ee.FeatureCollection('WCMC/WDPA/current/polygons').filter(ee.Filter.eq('ISO3', 'KHM'));
print(wdpa.aggregate_array('NAME').sort());
var pa = wdpa.filter(ee.Filter.eq('NAME', 'Prey Lang'));                // ប្ដូរតាមការជ្រើស
var buffer = pa.geometry().buffer(10000, 100).difference(pa.geometry(), 100);
Map.addLayer(pa, {color: 'blue'}, 'តំបន់ការពារ'); Map.addLayer(ee.Feature(buffer), {color: 'grey'}, 'ទ្រនាប់ ១០ គម');
var forest = tc.gte(30), loss = gfc.select('loss').and(forest);
function byYear(geom) {
  var g = ha.addBands(gfc.select('lossyear')).updateMask(loss).reduceRegion({
    reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'y'}), geometry: geom, scale: 30, maxPixels: 1e13, tileScale: 8});
  return ee.List(g.get('groups')).map(function(d) { d = ee.Dictionary(d);
    return ee.Feature(null, {year: ee.Number(d.get('y')).add(2000), ha: d.get('sum')}); });
}
var fcIn = ee.FeatureCollection(byYear(pa.geometry())).map(function(f) { return f.set('zone', 'ក្នុង'); });
var fcBuf = ee.FeatureCollection(byYear(buffer)).map(function(f) { return f.set('zone', 'ទ្រនាប់'); });
print(ui.Chart.feature.groups(fcIn.merge(fcBuf), 'year', 'ha', 'zone').setChartType('ColumnChart')
  .setOptions({title: 'ការបាត់បង់តាមឆ្នាំ (ហិកតា)'}));
```

គណនាផ្ទៃព្រៃ ២០០០ ក្នុងតំបន់ទាំងពីរ ហើយបម្លែងក្រាបជាអត្រា (% នៃព្រៃ ២០០០) ក្នុង Excel ឬ QGIS។

## សកម្មភាពទី៤៖ ពិនិត្យគំរូ · ៣០ នាទី

```javascript
var pts = loss.selfMask().rename('loss').addBands(gfc.select('lossyear'))
  .sample({region: pa.geometry(), scale: 30, numPixels: 20, seed: 7, geometries: true});
Map.addLayer(pts, {color: 'yellow'}, 'គំរូ ២០');
Export.table.toDrive({collection: pts, description: 'loss_samples', folder: 'applied_gis', fileFormat: 'KML'});
```

បើក KML ក្នុង Google Earth Pro ហើយប្រើប្រវត្តិរូបភាព (historical imagery)។ សម្រាប់ចំណុចនីមួយៗ កត់ត្រា៖ ព្រៃធម្មជាតិ → ដំណាំ · ព្រៃ → ចម្ការ · ចម្ការច្រូត · ភ្លើង · មិនច្បាស់ · កំហុស។

## សកម្មភាពទី៥៖ ផែនទី និងសេចក្ដីសន្និដ្ឋាន · ២៥ នាទី

ក្នុង QGIS ធ្វើផែនទី choropleth ពីរ៖ `l30` (ហិកតា) និង `rate30` (%)។ ប្រៀបធៀបផែនទីទាំងពីរ ហើយសរសេរកថាខណ្ឌមួយពីមូលហេតុដែលខេត្តខុសគ្នាលេចឡើងជា «អាក្រក់បំផុត»។

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- CSV តារាងខេត្ត និងផែនទីពីរពី QGIS។
- ក្រាបការបាត់បង់តាមឆ្នាំ (ក្នុង និងទ្រនាប់) ជាអត្រា។
- តារាងពិនិត្យគំរូ ២០ ចំណុច ជាមួយភាគរយតាមប្រភេទ។
- កថាខណ្ឌមួយ៖ សេចក្ដីសន្និដ្ឋាន និងដែនកំណត់ (កម្រិត ចម្ការ ការលំអៀងទីតាំង)។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="treecover2000" markdown>
**១.** ក្រុមរលកណាដែលប្រើកំណត់ព្រៃឆ្នាំ ២០០០?
</div>

<div class="self-check" data-answer="23|២៣" markdown>
**២.** ក្នុង lossyear តើតម្លៃប៉ុន្មានតំណាងឆ្នាំ ២០២៣?
</div>

<div class="self-check" data-answer="2012|២០១២" markdown>
**៣.** ក្រុមរលក gain គ្របរហូតដល់ឆ្នាំណា?
</div>

<div class="self-check" data-answer="ISO3" markdown>
**៤.** លក្ខណៈណានៃ WDPA ដែលប្រើត្រងប្រទេស (KHM)?
</div>
