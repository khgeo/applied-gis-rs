# លំហាត់ទី១៤៖ កម្មវិធីតាមដានទឹក

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១៤៖ កម្មវិធី Earth Engine និងផែនទីវេប](../lessons/lesson-14.md)
    **ការអនុវត្តដោយខ្លួនឯង** · Earth Engine Code Editor · ប្រហែល ១៣៥ នាទី

## ស្ថានភាព

អ្នកនឹងសាងសង់ និងបោះពុម្ពកម្មវិធី Earth Engine ពេញលេញមួយ សម្រាប់តាមដានផ្ទៃទឹកក្នុងខេត្តរបស់អ្នក៖ ជ្រើសឆ្នាំ និងខែ ក្រាបផ្ទៃទឹក ការចុចលើផែនទី legend ផែនទីមុន–ក្រោយ និងផែនទីទឹក Sentinel-1 សម្រាប់ឆ្នាំថ្មី។

## គោលបំណង

- រៀបចំ ui.root ជាមួយផ្ទាំងបញ្ជា និងផែនទី។
- សរសេរ callback សម្រាប់ Select Slider និង Map.onClick ដោយប្រើ layers().set() និង evaluate()។
- បន្ថែមក្រាប legend ប្រភព និង SplitPanel។
- បោះពុម្ពកម្មវិធី ហើយសាកល្បងលើទូរស័ព្ទ។

<figure markdown>
--8<-- "assets/svg/agv/lab14-workflow.svg"
<figcaption>លំដាប់ការងារនៃលំហាត់ទី១៤ និងពេលវេលាប្រហាក់ប្រហែល។</figcaption>
</figure>


## ឯកសារដែលប្រើ

- `JRC/GSW1_4/MonthlyHistory` · `JRC/GSW1_4/GlobalSurfaceWater` · `COPERNICUS/S1_GRD` · `FAO/GAUL/2015/level1`។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="gee-app"></div>

ចុចលើផែនទី និងប្ដូរឆ្នាំ ហើយមើលកំណត់ហេតុ៖ callback ណារត់ពេលណា? ហេតុអ្វីមាន «កំពុងគណនា…» មុនចម្លើយ?

## សកម្មភាពទី១៖ ផ្ទាំង និងផែនទី · ២០ នាទី

```javascript
var AOI_NAME = 'Kampong Chhnang';                                    // ខេត្តរបស់អ្នក
var aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', AOI_NAME));
ui.root.clear();
var map = ui.Map(); map.setOptions('HYBRID'); map.centerObject(aoi, 9);
map.layers().set(2, ui.Map.Layer(ee.Image().paint(aoi, 0, 2), {palette: ['yellow']}, 'ព្រំខេត្ត'));
var panel = ui.Panel({style: {width: '360px', padding: '8px'}});
panel.add(ui.Label('តាមដានផ្ទៃទឹក · ' + AOI_NAME, {fontSize: '20px', fontWeight: 'bold'}));
panel.add(ui.Label('ជ្រើសឆ្នាំ និងខែ។ ចុចលើផែនទីដើម្បីមើលភាពញឹកញាប់នៃទឹក។', {fontSize: '13px'}));
var years = []; for (var y = 1990; y <= 2021; y++) years.push(String(y));
var yearSel = ui.Select({items: years, value: '2020'});
var monthSl = ui.Slider({min: 1, max: 12, step: 1, value: 10, style: {stretch: 'horizontal'}});
var info = ui.Label('ចុចលើផែនទី…', {color: 'grey'});
var chartBox = ui.Panel();
panel.add(ui.Label('ឆ្នាំ')).add(yearSel).add(ui.Label('ខែ')).add(monthSl).add(info).add(chartBox);
ui.root.add(panel); ui.root.add(map);
```

`map.layers().set(2, …)` ដាក់ព្រំខេត្តជាស្រទាប់ទី ២ ដូច្នេះស្រទាប់ទឹក (០) និងចំណុច (១) មិនគ្របវា។ loop JavaScript នៅទីនេះត្រឹមត្រូវ ព្រោះវាបង្កើតបញ្ជីអក្សរធម្មតាសម្រាប់ ui.Select។

## សកម្មភាពទី២៖ ស្រទាប់ និង callback · ២៥ នាទី

```javascript
var gswM = ee.ImageCollection('JRC/GSW1_4/MonthlyHistory');
function waterOf(y, m) {
  return ee.Image(gswM.filter(ee.Filter.eq('year', y)).filter(ee.Filter.eq('month', m)).first()).eq(2).selfMask().clip(aoi);
}
function refresh() {
  var y = parseInt(yearSel.getValue(), 10), m = monthSl.getValue();
  map.layers().set(0, ui.Map.Layer(waterOf(y, m), {palette: ['#1565c0']}, 'ទឹក ' + y + '-' + m));
}
yearSel.onChange(function(v) { refresh(); yearChart(parseInt(v, 10)); });
monthSl.onChange(refresh);
```

## សកម្មភាពទី៣៖ ក្រាប និងការចុច · ៣០ នាទី

```javascript
function yearChart(y) {
  chartBox.widgets().reset([ui.Label('កំពុងគណនាក្រាប…', {color: 'grey'})]);
  var fc = ee.FeatureCollection(ee.List.sequence(1, 12).map(function(m) {
    var img = ee.Image(gswM.filter(ee.Filter.eq('year', y)).filter(ee.Filter.eq('month', m)).first());
    var km2 = ee.Image.pixelArea().divide(1e6).updateMask(img.eq(2))
      .reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi.geometry(), scale: 300, maxPixels: 1e9}).get('area');
    return ee.Feature(null, {month: m, km2: km2});
  }));
  chartBox.widgets().reset([ui.Chart.feature.byFeature(fc, 'month', 'km2')
    .setOptions({title: 'ផ្ទៃទឹក ' + y + ' (គម²)', legend: {position: 'none'}, hAxis: {title: 'ខែ'}})]);
}
var occ = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence');
map.onClick(function(c) {
  info.setValue('កំពុងគណនា…');
  var pt = ee.Geometry.Point([c.lon, c.lat]);
  map.layers().set(1, ui.Map.Layer(pt, {color: 'red'}, 'ចំណុច'));
  occ.reduceRegion({reducer: ee.Reducer.first(), geometry: pt, scale: 30}).get('occurrence').evaluate(function(v) {
    info.setValue(v === null ? 'មិនដែលមានទឹក (១៩៨៤–២០២១)' : 'មានទឹក ' + v + '% នៃពេលវេលា (១៩៨៤–២០២១)');
  });
});
refresh(); yearChart(2020);
```

ក្រាបប្រើ scale ៣០០ ម ដើម្បីលឿន។ សាកល្បង scale ៣០ ម ហើយកត់ត្រាពេលវេលា។

## សកម្មភាពទី៤៖ Legend ប្រភព និង SplitPanel · ៣០ នាទី

```javascript
function legendRow(color, text) {
  return ui.Panel([ui.Label('', {backgroundColor: color, padding: '8px', margin: '4px 6px'}), ui.Label(text, {margin: '4px'})],
                  ui.Panel.Layout.flow('horizontal'));
}
panel.add(legendRow('#1565c0', 'ទឹកក្នុងខែដែលជ្រើស')).add(legendRow('yellow', 'ព្រំខេត្ត'));
panel.add(ui.Label('ប្រភព៖ EC JRC/Google Global Surface Water v1.4 (១៩៨៤–២០២១) · FAO GAUL ២០១៥', {fontSize: '11px', color: 'grey'}));
var compareBtn = ui.Button('ប្រៀបធៀប មេសា ↔ តុលា', function() {
  var y = parseInt(yearSel.getValue(), 10);
  var left = ui.Map(), right = ui.Map(); ui.Map.Linker([left, right]);
  left.addLayer(waterOf(y, 4), {palette: ['#1565c0']}, 'មេសា'); right.addLayer(waterOf(y, 10), {palette: ['#1565c0']}, 'តុលា');
  left.centerObject(aoi, 9);
  var back = ui.Button('← ត្រឡប់', function() { ui.root.clear(); ui.root.add(panel); ui.root.add(map); });
  left.add(back);
  ui.root.clear(); ui.root.add(ui.SplitPanel({firstPanel: left, secondPanel: right, wipe: true}));
});
panel.add(compareBtn);
```

## សកម្មភាពទី៥៖ Sentinel-1 ឆ្នាំថ្មី និងការបោះពុម្ព · ២០ នាទី

JRC បញ្ចប់ត្រឹមឆ្នាំ ២០២១។ បន្ថែមប៊ូតុងមួយ «ទឹក S1 ខែនេះ ២០២៤» ដែលប្រើកម្រិត −១៦ dB លើ Sentinel-1 VV (មេរៀនទី៧) សម្រាប់ខែដែលជ្រើស៖

```javascript
panel.add(ui.Button('ទឹក Sentinel-1 (២០២៤, ខែដែលជ្រើស)', function() {
  var m = monthSl.getValue(), d = ee.Date.fromYMD(2024, m, 1);
  var vv = ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(aoi).filterDate(d, d.advance(1, 'month'))
    .filter(ee.Filter.eq('instrumentMode', 'IW')).filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .select('VV').median().focalMedian(30, 'circle', 'meters');
  map.layers().set(0, ui.Map.Layer(vv.lt(-16).selfMask().clip(aoi), {palette: ['#00bcd4']}, 'ទឹក S1 ២០២៤-' + m));
}));
```

បន្ទាប់មក៖ **Apps → New App** → ជ្រើស Cloud Project → Publish។ បើក URL លើទូរស័ព្ទ ហើយសាកល្បង។ ឲ្យមិត្តម្នាក់ប្រើដោយគ្មានការពន្យល់ ហើយកត់ត្រាបញ្ហាបី។

## លទ្ធផលដែលរំពឹងទុក

ប្រៀបធៀបលទ្ធផលរបស់អ្នកជាមួយរូបខាងក្រោម។ លេខ និងពណ៌មិនចាំបាច់ដូចបេះបិទទេ ប៉ុន្តែលំនាំគួរតែស្រដៀងគ្នា។

<figure markdown>
--8<-- "assets/svg/agv/a14-anatomy.svg"
<figcaption>លទ្ធផលគំរូ ១៖ ផ្ទាំងបញ្ជា + ផែនទី។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - កម្មវិធីភាគច្រើនមានផ្ទាំងបញ្ជា (widgets) នៅម្ខាង និងផែនទីធំនៅម្ខាងទៀត។
    - Widgets ទាំងអស់ជាវត្ថុ ui.* ដែលដាក់ក្នុង ui.Panel។
    - អ្នកប្រើមិនឃើញកូដទេ៖ ពួកគេឃើញតែផ្ទាំង ផែនទី និងក្រាប។

<figure markdown>
--8<-- "assets/svg/agv/a14-chart.svg"
<figcaption>លទ្ធផលគំរូ ២៖ ពីកូដ ទៅឧបករណ៍ដែលអ្នកដទៃប្រើបាន។</figcaption>
</figure>

!!! tip "អ្វីដែលត្រូវពិនិត្យ"
    - កម្មវិធីតាមដានទឹក ទាញផ្ទៃទឹកប្រចាំខែ ហើយបង្ហាញក្រាប និងផែនទីនៃខែដែលអ្នកប្រើចុច។
    - ក្រាបត្រូវគណនាលើម៉ាស៊ីនមេ៖ ក្រាបដែលមានច្រើនខែ ច្រើនឆ្នាំ អាចយឺត ដូច្នេះគណនាទុកមុនជា Asset បាន។
    - តម្លៃក្នុងក្រាបនេះជាគំរូ ដើម្បីបង្ហាញទម្រង់។

## កំហុសទូទៅ និងដំណោះស្រាយ

| បញ្ហាដែលឃើញ | មូលហេតុទូទៅ | ដំណោះស្រាយ |
|---|---|---|
| កម្មវិធីកក | getInfo() ក្នុង callback | evaluate(function(v) {...}) |
| ស្រទាប់ជាន់គ្នាច្រើន | addLayer ក្នុង callback | map.layers().set(0, ...) |
| Select ផ្ដល់ '2020' ជាអក្សរ | items ជាអក្សរ | parseInt(value, 10) |
| ក្រាបយឺត | scale តូចពេក | scale: 300 · Asset គណនារួច |
| Publish មិនបាន | គ្មាន Cloud Project ចុះឈ្មោះ | ចុះឈ្មោះ Project (ឧបសម្ព័ន្ធ ក) |


## លទ្ធផលត្រូវប្រគល់

- តំណស្គ្រីប និង URL កម្មវិធីដែលបានបោះពុម្ព។
- រូបអេក្រង់កម្មវិធីលើកុំព្យូទ័រ និងទូរស័ព្ទ។
- បញ្ជីបញ្ហាបីពីការសាកល្បងដោយមិត្ត និងការកែដែលបានធ្វើ។
- កថាខណ្ឌមួយ៖ ដែនកំណត់ដែលអ្នកសរសេរក្នុងកម្មវិធី ហើយហេតុអ្វី។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

<div class="self-check" data-answer="evaluate|evaluate()" markdown>
**១.** មុខងារណាស្នើលទ្ធផលពីម៉ាស៊ីនមេ ដោយមិនធ្វើឲ្យកម្មវិធីកក?
</div>

<div class="self-check" data-answer="layers().set|layers().set()|set" markdown>
**២.** មុខងារណាជំនួសស្រទាប់ផែនទីក្នុង callback?
</div>

<div class="self-check" data-answer="2021|២០២១" markdown>
**៣.** JRC Monthly History v1.4 គ្របដល់ឆ្នាំណា?
</div>

<div class="self-check" data-answer="ui.Map.Linker|Linker" markdown>
**៤.** វត្ថុណាធ្វើឲ្យផែនទីពីររំកិល និង zoom ជាមួយគ្នា?
</div>
