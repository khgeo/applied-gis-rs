# លំហាត់ទី៨៖ CHIRPS និង VCI

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៨៖ គ្រោះរាំងស្ងួត ទឹកភ្លៀង និងសុខភាពរុក្ខជាតិ](../lessons/lesson-08.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · QGIS · ប្រហែល ១៣០ នាទី

## ស្ថានភាព

អ្នកនឹងរៀបចំ «ព្រឹត្តិបត្រគ្រោះរាំងស្ងួត» សម្រាប់ឆ្នាំមួយដែលអ្នកជ្រើស (ណែនាំ ២០១៩)៖ ទឹកភ្លៀងប្រចាំខែធៀបនឹងធម្មតា SPI-៣ សាមញ្ញ VCI និង VHI ហើយចាត់ថ្នាក់ខេត្តតាមសញ្ញាទាំងពីរ។

## គោលបំណង

- បង្កើតទឹកភ្លៀងប្រចាំខែពី CHIRPS ហើយគណនា climatology ១៩៩១–២០២០។
- គណនា % នៃធម្មតា z-score និង SPI-៣ សាមញ្ញ។
- គណនា VCI TCI និង VHI ពី MODIS។
- គណនាសន្ទស្សន៍លើដីដំណាំតាមខេត្ត ហើយចាត់ថ្នាក់។

{{WORKFLOW}}

## ឯកសារដែលប្រើ

- `UCSB-CHG/CHIRPS/DAILY` · `MODIS/061/MOD13Q1` · `MODIS/061/MOD11A2` · `ESA/WorldCover/v200` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-drought"></div>

ជ្រើសឆ្នាំ ២០១៩ និង SPI-៣។ ខែណាខ្លះធ្លាក់ក្រោម −១? ធ្វើម្ដងទៀតជាមួយ SPI-១ ហើយពន្យល់ភាពខុសគ្នា។

## សកម្មភាពទី១៖ ក្រាបទឹកភ្លៀងខេត្តរបស់អ្នក · ២០ នាទី

```javascript
var YEAR = 2019;                                                   // ប្ដូរតាមការជ្រើស
var provs = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM0_NAME', 'Cambodia'));
var myProv = provs.filter(ee.Filter.eq('ADM1_NAME', 'Kampong Speu'));   // ខេត្តរបស់អ្នក
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').select('precipitation');
function monthly(y, m) {
  var s = ee.Date.fromYMD(y, m, 1);
  return chirps.filterDate(s, s.advance(1, 'month')).sum().set({month: m, 'system:time_start': s.millis()});
}
var cur = ee.ImageCollection.fromImages(ee.List.sequence(1, 12).map(function(m) { return monthly(YEAR, m); }));
var clim = ee.ImageCollection.fromImages(ee.List.sequence(1, 12).map(function(m) {
  var refs = ee.ImageCollection.fromImages(ee.List.sequence(1991, 2020).map(function(y) { return monthly(y, m); }));
  return refs.mean().set({month: m, 'system:time_start': ee.Date.fromYMD(YEAR, m, 1).millis()});
}));
var both = cur.map(function(img) {
  var c = clim.filter(ee.Filter.eq('month', img.get('month'))).first();
  return img.rename('ឆ្នាំនេះ').addBands(ee.Image(c).rename('ធម្មតា'));
});
print(ui.Chart.image.series(both, myProv, ee.Reducer.mean(), 5000).setChartType('ColumnChart')
  .setOptions({title: 'ទឹកភ្លៀងប្រចាំខែ (mm)'}));
```

ប្រសិនបើក្រាប timeout ប្ដូរទៅ `UCSB-CHG/CHIRPS/PENTAD` (ដូចគ្នា តែលឿនជាង)។

## សកម្មភាពទី២៖ z-score និង SPI-៣ · ២៥ នាទី

```javascript
var M = 7;                                                         // ខែដែលចាប់អារម្មណ៍
var refM = ee.ImageCollection.fromImages(ee.List.sequence(1991, 2020).map(function(y) { return monthly(y, M); }));
var z = monthly(YEAR, M).subtract(refM.mean()).divide(refM.reduce(ee.Reducer.stdDev())).rename('z');
function acc3(y) { var s = ee.Date.fromYMD(y, M, 1).advance(-2, 'month'); return chirps.filterDate(s, s.advance(3, 'month')).sum(); }
var ref3 = ee.ImageCollection.fromImages(ee.List.sequence(1991, 2020).map(function(y) { return acc3(y); }));
var spi3 = acc3(YEAR).subtract(ref3.mean()).divide(ref3.reduce(ee.Reducer.stdDev())).rename('SPI3');
var kh = provs.geometry();
Map.centerObject(kh, 7);
Map.addLayer(z.clip(kh), {min: -2, max: 2, palette: ['#b2182b', '#f7f7f7', '#2166ac']}, 'z ខែ ' + M);
Map.addLayer(spi3.clip(kh), {min: -2, max: 2, palette: ['#b2182b', '#f7f7f7', '#2166ac']}, 'SPI-3');
```

## សកម្មភាពទី៣៖ VCI TCI VHI · ៣០ នាទី

```javascript
var VM = 8;                                                        // ខែរុក្ខជាតិ (យឺតពីទឹកភ្លៀង)
function inMonth(col, m) { return col.filter(ee.Filter.calendarRange(m, m, 'month')); }
var nd = ee.ImageCollection('MODIS/061/MOD13Q1').select('NDVI');
var ndH = inMonth(nd.filterDate('2001-01-01', '2024-01-01'), VM);
var vci = inMonth(nd.filterDate(YEAR + '-01-01', (YEAR + 1) + '-01-01'), VM).mean()
  .subtract(ndH.reduce(ee.Reducer.percentile([5]))).divide(
    ndH.reduce(ee.Reducer.percentile([95])).subtract(ndH.reduce(ee.Reducer.percentile([5]))))
  .multiply(100).clamp(0, 100).rename('VCI');
var lst = ee.ImageCollection('MODIS/061/MOD11A2').select('LST_Day_1km');
var lH = inMonth(lst.filterDate('2001-01-01', '2024-01-01'), VM);
var lp5 = lH.reduce(ee.Reducer.percentile([5])), lp95 = lH.reduce(ee.Reducer.percentile([95]));
var tci = lp95.subtract(inMonth(lst.filterDate(YEAR + '-01-01', (YEAR + 1) + '-01-01'), VM).mean())
  .divide(lp95.subtract(lp5)).multiply(100).clamp(0, 100).rename('TCI');
var vhi = vci.multiply(0.5).add(tci.multiply(0.5)).rename('VHI');
var pal = ['#a50026', '#f46d43', '#fee08b', '#a6d96a', '#006837'];
Map.addLayer(vci.clip(kh), {min: 0, max: 100, palette: pal}, 'VCI');
Map.addLayer(vhi.clip(kh), {min: 0, max: 100, palette: pal}, 'VHI');
```

យើងប្រើ percentile ៥ និង ៩៥ ជំនួស min និង max ដើម្បីកាត់បន្ថយឥទ្ធិពលពពក ហើយ `clamp(0, 100)` កាត់តម្លៃដែលហួសចន្លោះ។

## សកម្មភាពទី៤៖ តារាងខេត្ត · ២៥ នាទី

```javascript
var crop = ee.ImageCollection('ESA/WorldCover/v200').first().eq(40);
var stack = spi3.addBands(vhi.resample('bilinear')).updateMask(crop.reduceResolution({
  reducer: ee.Reducer.mean(), maxPixels: 1024}).reproject({crs: 'EPSG:4326', scale: 250}).gt(0.5));
var table = stack.reduceRegions({collection: provs, reducer: ee.Reducer.mean(), scale: 250, tileScale: 4})
  .map(function(f) {
    var s = ee.Number(f.get('SPI3')), v = ee.Number(f.get('VHI'));
    var cls = ee.Algorithms.If(s.lt(-1).and(v.lt(40)), 'បានបញ្ជាក់',
              ee.Algorithms.If(s.lt(-1), 'ភ្លៀងខ្វះ', ee.Algorithms.If(v.lt(40), 'ពិនិត្យ', 'ធម្មតា')));
    return f.set('class', cls);
  });
print(table.select(['ADM1_NAME', 'SPI3', 'VHI', 'class']).sort('VHI'));
Export.table.toDrive({collection: table, description: 'drought_bulletin_' + YEAR, folder: 'applied_gis',
  fileFormat: 'CSV', selectors: ['ADM1_CODE', 'ADM1_NAME', 'SPI3', 'VHI', 'class']});
```

`reduceResolution` គណនាភាគរយដំណាំក្នុងក្រឡា ២៥០ ម ហើយរក្សាតែក្រឡាដែលដំណាំលើស ៥០%។

## សកម្មភាពទី៥៖ ព្រឹត្តិបត្រក្នុង QGIS · ២០ នាទី

ភ្ជាប់ CSV ទៅស្រទាប់ខេត្ត ហើយធ្វើផែនទីពីរ (SPI-៣ និង VHI) និងផែនទីចាត់ថ្នាក់មួយ។ បង្កើតប្លង់ A4 មួយទំព័រ៖ ចំណងជើង ផែនទីបី តារាងខេត្តដែល «បានបញ្ជាក់» និងកំណត់ចំណាំប្រភព និងដែនកំណត់។

{{EXPECT}}

## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប។
- ក្រាបទឹកភ្លៀងប្រចាំខែនៃខេត្តរបស់អ្នក ធៀបនឹងធម្មតា។
- ផែនទី z-score SPI-៣ VCI និង VHI (រូបអេក្រង់)។
- CSV តារាងខេត្ត និងព្រឹត្តិបត្រ A4 ជា PDF។
- កថាខណ្ឌមួយ៖ ខេត្តណាមានសញ្ញាមិនស៊ីគ្នា (ភ្លៀងខ្វះ តែ VHI ល្អ ឬផ្ទុយមកវិញ) ហើយហេតុអ្វី។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="sum|sum()" markdown>
**១.** Reducer ណាសម្រាប់ទឹកភ្លៀងសរុបប្រចាំខែពី CHIRPS ប្រចាំថ្ងៃ?
</div>

<div class="self-check" data-answer="-1|−1|-១|−១" markdown>
**២.** SPI ក្រោមតម្លៃប៉ុន្មានដែលចាត់ទុកថាស្ងួតមធ្យម?
</div>

<div class="self-check" data-answer="40|៤០" markdown>
**៣.** VHI ក្រោមប៉ុន្មាន ជាទូទៅបង្ហាញគ្រោះរាំងស្ងួត?
</div>

<div class="self-check" data-answer="MOD11A2" markdown>
**៤.** ផលិតផល MODIS ណាផ្ដល់ LST ៨ ថ្ងៃ សម្រាប់ TCI?
</div>
