# Quick Reference: Network GeoJSON Files

## File Overview

| File | Location | Content | Lines (BO network) |
|------|----------|---------|-------------------|
| **network_full.geojson** ✨ | `results/` | All network lines | 9 lines |
| network_comparison.geojson | `results/` | Model vs Reference ratios | Varies |
| network_model.geojson | `resources/network_statistics/` | Cross-border only | 0 (empty) |

## Properties in network_full.geojson

```json
{
  "name": "0",              // Line identifier
  "bus0": "BO0 0",          // From bus
  "bus1": "BO0 3",          // To bus
  "s_nom": 2903.53,         // Nominal capacity (MW)
  "s_nom_opt": 2903.53,     // Optimized capacity (MW)
  "length": 246.53,         // Line length (km)
  "r": 4.33,                // Resistance (Ohm)
  "x": 35.47,               // Reactance (Ohm)
  "type": "Al/St 240/40 4-bundle 380.0"  // Line technology
}
```

## Commands

```bash
# Generate all network GeoJSON files
snakemake -j1 build_network_geojson

# Copy to results folder
snakemake -j1 make_comparison

# Run complete workflow
snakemake -j1 visualize_data
```

## Visualization

### Python (Quick View)
```python
import geopandas as gpd
gdf = gpd.read_file('results/network_full.geojson')
print(gdf[['name', 'bus0', 'bus1', 's_nom', 'length']])
```

### Online
- Upload to [geojson.io](http://geojson.io)
- Upload to [mapshaper.org](https://mapshaper.org)

## Bolivia Network Summary
- **9 transmission lines**
- **30 buses**
- **File size: 3.6 KB**
- **Total capacity: ~11,175 MW**
- **Total length: ~2,267 km**
