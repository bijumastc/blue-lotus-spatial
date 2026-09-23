# Blue Lotus – Spatial Computational Analysis

Reproducible Python pipelines supporting a spatial and postcolonial reading of Meena Alexander’s poem “Blue Lotus” (*Raw Silk*, 2004).

This repository accompanies a qualitative interpretation that draws on the spatial theories of Henri Lefebvre and Edward Soja, together with Homi Bhabha’s concepts of hybridity and the Third Space, and Avtar Brah’s work on diaspora space and the homing desire. The computational layer produces publication-ready figures and maps intended for a scholarly article.

---

## Folder structure

```
blue_lotus_spatial/

├── scripts/
│   ├── 01_extract_places.py     # Place extraction
│   ├── 02_geocode_places.py     # Geocoding with Nominatim
│   ├── 03_create_map.py         # Interactive Folium map
│   ├── 04_spatial_lexicon.py    # Section-wise spatial & thematic lexicon + chart
│   └── 05_thirdspace_network.py # Network visualisation of Thirdspace relations
├── output/                      # All results are written here
├── requirements.txt
├── run_all.py
└── README.md
```

---

## Quick start

1. Clone or download this repository.
2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the full pipeline:

```bash
python run_all.py
```

Or run the scripts individually in order:

```bash
python scripts/01_extract_places.py
python scripts/02_geocode_places.py
python scripts/03_create_map.py
python scripts/04_spatial_lexicon.py
python scripts/05_thirdspace_network.py
```

---

## Outputs

All results are saved in the `output/` folder:

- `places_extracted.csv`
- `places_geocoded.csv`
- `blue_lotus_map.html` (interactive map)
- `lexicon_by_section.csv` + `.png`
- `thirdspace_network.png`

---

## Notes

- Internet access is required only for the geocoding step (script 02).
- The interactive map uses a free basemap and does not require an API key.
- Figures are saved at 300 dpi for publication use.

---

## Data note

The poem “Blue Lotus” appears in Meena Alexander, *Raw Silk* (TriQuarterly Books / Northwestern University Press, 2004).  
Please obtain the text from a legitimate source (library, purchased copy, or publisher).  

This repository contains only derived data and analysis outputs (extracted places, geocoded locations, lexicon counts, map, and network graph).

## Licence

- **Code** (all scripts in `scripts/`, plus `run_all.py`): MIT Licence — see `LICENSE`.
- **Data and figures** (everything in `data/` and `output/`): Creative Commons
  Attribution 4.0 International (CC-BY 4.0) — see `LICENSE-data`.
- **The poem "Blue Lotus" is not included in this repository.** It remains
  © the Estate of Meena Alexander. To reproduce the analysis, supply your own
  copy from *Raw Silk* (TriQuarterly Books / Northwestern UP, 2004) and place
  it at the path noted in the pipeline configuration.

## Acknowledgements

The structure and development of this computational pipeline were assisted by Grok (xAI). The theoretical interpretation, research design, and final scholarly framing remain the responsibility of the author.
