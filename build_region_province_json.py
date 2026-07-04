#!/usr/bin/env python3
"""Static region+province dataset for client-side bundling/caching, nested
region -> provinces. 17 regions + 82 provinces, essentially immutable
(PSGC updates ~yearly)."""
import json


def load(path):
    with open(path) as fh:
        return json.load(fh)["features"]


regions = {}

for feat in load("regions.geojson"):
    p = feat["properties"]
    regions[p["psgc_id"]] = {
        "psgc_id": p["psgc_id"],
        "psgc_code": p["psgc_code"],
        "psgc_name": p["psgc_name"],
        "psgc_type": p["psgc_type"],
        "provinces": [],
    }

for feat in load("provinces.geojson"):
    p = feat["properties"]
    regions[p["ADM1_PCODE"]]["provinces"].append({
        "psgc_id": p["psgc_id"],
        "psgc_code": p["psgc_code"],
        "psgc_name": p["psgc_name"],
        "psgc_type": p["psgc_type"],
    })

with open("region_province.json", "w") as out:
    json.dump(list(regions.values()), out, indent=2, ensure_ascii=False)

print(f"wrote {len(regions)} regions to region_province.json")
