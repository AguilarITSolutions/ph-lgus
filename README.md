# Philippines LGUs (Local Government Units)

Geographic and administrative data for all Local Government Units in the Philippines, sourced from the Philippine Statistics Authority (PSA) Philippine Standard Geographic Code (PSGC). Includes GeoJSON files for mapping, conversion scripts, and database schema for hierarchical LGU relationships.

## Contents

### GeoJSON Files

- **regions.geojson** — 17 regions with geographic boundaries
- **provinces.geojson** — 82 provinces with geographic boundaries
- **cities.geojson** — Independent cities with geographic boundaries
- **municipalities.geojson** — Municipalities with geographic boundaries
- **barangays.geojson** — Barangays (smallest administrative divisions) with geographic boundaries

### Data Files

- **region_province.json** — Hierarchical mapping of regions to provinces
- **schema.sql** — PostgreSQL schema for storing LGU hierarchical data

### Python Scripts

- **build_region_province_json.py** — Converts PSGC data to region-province JSON
- **build_ph_lgus_csv.py** — Generates comprehensive LGU CSV from PSGC source
- **build_cmb_csv.py** — Generates city/municipality/barangay CSV

## Administrative Hierarchy

```txt
Region
  └── Province
      └── City / Component City / Municipality
          └── Barangay
```

## Database Schema

The `ph_lgus` PostgreSQL table stores hierarchical LGU data with:

- PSGC ID and code for unique identification
- Type (region, province, city, component_city, municipality, barangay)
- Parent-child relationships via `parent_id` foreign key
- Indexed by parent, type, and name for efficient queries
