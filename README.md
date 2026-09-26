# GIS និងការយកព័ត៌មានពីចម្ងាយអនុវត្តន៍ · Applied GIS and Remote Sensing

សៀវភៅទី៤ នៃស៊េរីសៀវភៅ GIS និងការយកព័ត៌មានពីចម្ងាយជាភាសាខ្មែរ (ឆ្នាំទី៣ ឆមាសទី២) · Google Earth Engine · ១៥ មេរៀន · ១៥ លំហាត់

- គេហទំព័រ៖ https://khgeo.github.io/applied-gis-rs/
- អ្នកនិពន្ធ៖ យាំ សារដ្ឋ (YAM Sarath) · អាជ្ញាបណ្ណ CC BY-SA 4.0

## Build

```text
pip install -r requirements.txt
python tools/slides/build_visuals.py   # figures → docs/assets/svg/agv + visuals.json (needs shapely, matplotlib, Pillow, rasterio)
python tools/build_content.py          # src/*.md → docs/lessons, docs/workbook
python tools/slides/build_slides.py    # docs/slides/lesson-XX.html
mkdocs serve
```

Write lessons and labs in `src/` (placeholders `{{FIG:name}}`, `{{WORKFLOW}}`, `{{EXPECT}}`), never in `docs/lessons` or `docs/workbook` directly.
