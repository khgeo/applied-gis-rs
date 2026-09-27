# លំហាត់ទី៥៖ ក្រាប NDVI និង harmonic

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៥៖ ស៊េរីពេលវេលា និងរដូវកាលរុក្ខជាតិ](../lessons/lesson-05.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · ប្រហែល ១១០ នាទី

## ស្ថានភាព

អ្នកនឹងសិក្សាប្រតិទិនដំណាំនៃខេត្តរបស់អ្នក៖ ទាញក្រាប NDVI និង LSWI នៃស្រែ ព្រៃ និងទីក្រុង បង្កើត composite ប្រចាំខែ សមម៉ូដែល harmonic ហើយធ្វើផែនទីទំហំរដូវកាល និងខែកំពូល NDVI។

## គោលបំណង

- ទាញក្រាប NDVI នៃចំណុចច្រើនដោយ seriesByRegion។
- ប្រៀបធៀបស៊េរីឆៅ និង composite ប្រចាំខែ ហើយដោះស្រាយខែគ្មានទិន្នន័យ។
- សមម៉ូដែល harmonic លំដាប់ ១ និង ២ ហើយគណនាទំហំ។
- ធ្វើផែនទីខែកំពូល NDVI ដោយ qualityMosaic។

<figure markdown>
--8<-- "assets/svg/agv/lab05-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី៥ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- `COPERNICUS/S2_SR_HARMONIZED` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-harmonic"></div>

ជ្រើស «ស្រែពីរដង» ហើយរកលំដាប់ harmonic ទាបបំផុតដែលចាប់កំពូលទាំងពីរ។

## សកម្មភាពទី១៖ ចំណុចគំរូបី · ១៥ នាទី

ក្នុង Code Editor ប្រើ **Geometry Tools → Add a marker** ដាក់ចំណុចបី៖ ស្រែ ព្រៃ និងទីក្រុង ក្នុងខេត្តរបស់អ្នក (ប្រើផែនទី Satellite ជាមូលដ្ឋាន)។ បន្ទាប់មកបង្កើត FeatureCollection៖

```javascript
var sites = ee.FeatureCollection([
  ee.Feature(paddy,  {label: 'ស្រែ'}),
  ee.Feature(forest, {label: 'ព្រៃ'}),
  ee.Feature(town,   {label: 'ទីក្រុង'})
]);
function prep(img) {
  var scl = img.select('SCL');
  var ok = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  var ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI');
  var lswi = img.normalizedDifference(['B8', 'B11']).rename('LSWI');
  return ndvi.addBands(lswi).updateMask(ok).copyProperties(img, ['system:time_start']);
}
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(sites).filterDate('2023-01-01', '2025-01-01').map(prep);
print('រូបភាព', s2.size());
```

## សកម្មភាពទី២៖ ក្រាបឆៅ · ២០ នាទី

```javascript
print(ui.Chart.image.seriesByRegion({imageCollection: s2, regions: sites, reducer: ee.Reducer.mean(),
  band: 'NDVI', scale: 10, seriesProperty: 'label'})
  .setOptions({title: 'NDVI ឆៅ', lineWidth: 0, pointSize: 3, vAxis: {viewWindow: {min: -0.2, max: 1}}}));
print(ui.Chart.image.series(s2.select(['NDVI', 'LSWI']), paddy, ee.Reducer.mean(), 10)
  .setOptions({title: 'ស្រែ៖ NDVI និង LSWI'}));
```

លើក្រាបស្រែ សម្គាល់៖ ពេលបញ្ចូលទឹក (LSWI ឡើង) ពេលកំពូល NDVI និងពេលច្រូត។ រាប់ចំណុចដែលធ្លាក់ចុះដោយសារពពកក្នុងរដូវវស្សា។

## សកម្មភាពទី៣៖ Composite ប្រចាំខែ · ២០ នាទី

```javascript
var months = ee.List.sequence(0, 23);
var monthly = ee.ImageCollection.fromImages(months.map(function(m) {
  var start = ee.Date('2023-01-01').advance(m, 'month');
  var sub = s2.filterDate(start, start.advance(1, 'month'));
  var empty = ee.Image.constant([0, 0]).rename(['NDVI', 'LSWI']).updateMask(0);
  return ee.Image(ee.Algorithms.If(sub.size().gt(0), sub.median(), empty))
    .set('system:time_start', start.millis()).set('month', start.get('month')).set('n', sub.size());
}));
print(ui.Chart.image.seriesByRegion({imageCollection: monthly, regions: sites, reducer: ee.Reducer.mean(),
  band: 'NDVI', scale: 10, seriesProperty: 'label'}).setOptions({title: 'NDVI ប្រចាំខែ', pointSize: 4}));
print('រូបភាពក្នុងខែនីមួយៗ', monthly.aggregate_array('n'));
```

ខែណាខ្លះគ្មានរូបភាព ឬមានតិចជាង ៣? ប្រៀបធៀបក្រាបនេះជាមួយក្រាបឆៅ។

## សកម្មភាពទី៤៖ Harmonic · ២៥ នាទី

```javascript
function harmonic(order) {
  var names = ['const', 't'];
  for (var k = 1; k <= order; k++) names.push('cos' + k, 'sin' + k);   // loop JS ធម្មតា (order ជាលេខ JS)
  var col = s2.select('NDVI').map(function(img) {
    var t = img.date().difference(ee.Date('2023-01-01'), 'year');
    var bands = [ee.Image(1), ee.Image(t)];
    for (var k = 1; k <= order; k++) {
      var w = t.multiply(2 * Math.PI * k);
      bands.push(ee.Image(w.cos()), ee.Image(w.sin()));
    }
    return ee.Image.cat(bands).rename(names).float().addBands(img).updateMask(img.mask());
  });
  var coef = col.reduce(ee.Reducer.linearRegression({numX: names.length, numY: 1}))
    .select('coefficients').arrayProject([0]).arrayFlatten([names]);
  var fitted = col.map(function(img) {
    return img.select(names).multiply(coef).reduce('sum').rename('fitted')
      .addBands(img.select('NDVI')).copyProperties(img, ['system:time_start']);
  });
  return {coef: coef, fitted: fitted};
}
var h1 = harmonic(1), h2 = harmonic(2);
print(ui.Chart.image.series(h2.fitted, paddy, ee.Reducer.mean(), 10)
  .setOptions({title: 'ស្រែ៖ NDVI និង harmonic លំដាប់ ២', series: {0: {lineWidth: 0, pointSize: 3}, 1: {lineWidth: 2}}}));
var amp1 = h2.coef.select('cos1').hypot(h2.coef.select('sin1'));
var amp2 = h2.coef.select('cos2').hypot(h2.coef.select('sin2'));
var prov = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Takeo'));  // ខេត្តរបស់អ្នក
Map.addLayer(amp1.clip(prov), {min: 0, max: 0.3, palette: ['white', 'green']}, 'ទំហំ harmonic ១');
Map.addLayer(amp2.clip(prov), {min: 0, max: 0.2, palette: ['white', 'purple']}, 'ទំហំ harmonic ២');
```

ប្រសិនបើគណនាលើខេត្តទាំងមូល យឺតពេក សូមបន្ថែម `.filterBounds(prov)` ទៅ s2 (ជំនួស sites) ហើយពង្រីកផែនទីចូលតំបន់តូចជាងមុន។ តំបន់ណាខ្លះមានទំហំ harmonic ទី២ ខ្ពស់?

## សកម្មភាពទី៥៖ ខែកំពូល NDVI · ២០ នាទី

```javascript
var y2024 = monthly.filterDate('2024-01-01', '2025-01-01').map(function(img) {
  return img.addBands(ee.Image.constant(ee.Number(img.get('month'))).rename('peakMonth').toFloat());
});
var peak = y2024.qualityMosaic('NDVI');
Map.addLayer(peak.select('peakMonth').clip(prov).updateMask(peak.select('NDVI').gt(0.4)),
  {min: 1, max: 12, palette: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#fee090', '#fdae61', '#f46d43', '#d73027']}, 'ខែកំពូល NDVI ២០២៤');
```

`updateMask(NDVI > ០,៤)` លាក់តំបន់ដែលគ្មានរុក្ខជាតិច្បាស់ (ទឹក ទីក្រុង)។ ពិពណ៌នាលំនាំលំហនៃខែកំពូល។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a05-monthly.svg"
<figcaption>លទ្ធផលគំរូ ១៖ ១២ តម្លៃ ជំនួសរាប់សិប។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - ee.List.sequence(1, 12).map() បង្កើត composite មួយក្នុងមួយខែ ហើយកំណត់ system:time_start។
    - median ក្នុងខែ ដកតម្លៃពពកដែលរត់ចួលភាគច្រើន។
    - ខែខ្លះក្នុងរដូវវស្សាអាចគ្មានការសង្កេតស្អាតទាល់តែសោះ (១ ខែក្នុងឧទាហរណ៍នេះ)៖ ត្រូវការ Sentinel-1 ឬ harmonic។

<figure markdown>
--8<-- "assets/svg/agv/a05-harmonic.svg"
<figcaption>លទ្ធផលគំរូ ២៖ ខ្សែកោងរលោង ពីការសង្កេតមិនទៀងទាត់។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - លំដាប់ ១ (cos និង sin មួយគូ) មានកំពូលតែមួយ/ឆ្នាំ៖ វាខកកំពូលទាំងពីរនៃស្រែពីរដង។ លំដាប់ ២ ចាប់បានទាំងពីរ។
    - ខ្សែសមបំពេញចន្លោះពពក ហើយផ្ដល់តម្លៃនៅថ្ងៃណាក៏បាន។
    - ទំហំ (amplitude) និងដំណាក់ (phase) ក្លាយជាក្រុមរលកថ្មី សម្រាប់ផែនទី និងការចាត់ថ្នាក់។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| Chart: No features contain non-null values | ចំណុចលើក្រឡាដែលបាន mask ឬខុសតំបន់ | ពិនិត្យកូអរដោនេ · s2.size() |
| Image.select: band 'NDVI' not found | ខែគ្មានរូបភាព៖ median() គ្មានក្រុមរលក | ee.Algorithms.If ជាមួយរូបភាពទទេ |
| ក្រាបគ្មានអ័ក្សពេលវេលា | បាត់ system:time_start | copyProperties · set('system:time_start') |
| Computation timed out (ក្រាប) | តំបន់ធំ ឬរយៈពេលវែងពេក | ប្រើចំណុច ឬ Export.table |
| Harmonic ឡើងចុះខុសប្រក្រតី | លំដាប់ខ្ពស់ពេក · ទិន្នន័យតិច | ប្រើលំដាប់ ១–២ · ពិនិត្យ count |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- ក្រាបបី៖ NDVI ឆៅ · NDVI ប្រចាំខែ · ស្រែជាមួយខ្សែ harmonic។
- រូបអេក្រង់ផែនទីទំហំ harmonic ទី២ និងខែកំពូល NDVI។
- កថាខណ្ឌមួយពិពណ៌នាប្រតិទិនស្រែ (SOS POS EOS ប្រហាក់ប្រហែល) ហើយប្រៀបធៀបជាមួយប្រតិទិនដែលអ្នកស្គាល់។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="system:time_start" markdown>
**១.** លក្ខណៈណាដែល ui.Chart.image.series ប្រើសម្រាប់អ័ក្សពេលវេលា?
</div>

<div class="self-check" data-answer="B8 B11|B8,B11|B8 និង B11|B8, B11" markdown>
**២.** LSWI Sentinel-2 ប្រើក្រុមរលកពីរណា? (សរសេរ ឧ. B8 B11)
</div>

<div class="self-check" data-answer="linearRegression|ee.Reducer.linearRegression" markdown>
**៣.** Reducer ណាសម្រាប់សមម៉ូដែល harmonic ដែលមានអថេរឯករាជ្យច្រើន?
</div>

<div class="self-check" data-answer="2|២" markdown>
**៤.** លំដាប់ harmonic ទាបបំផុតដែលអាចមានកំពូលពីរក្នុងមួយឆ្នាំ?
</div>
