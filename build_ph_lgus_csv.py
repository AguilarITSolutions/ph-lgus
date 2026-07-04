#!/usr/bin/env python3
"""Flatten regions/provinces/cities/municipalities/barangays geojson into one
ph_lgus.csv for `COPY ph_lgus(...) FROM 'ph_lgus.csv' CSV HEADER`.

ponytail: cities.geojson is missing all HUC/ICC cities (Manila, Cebu City,
Davao City, etc.) and NCR has no province-level rows at all (its "districts"
never appear as their own entity, only as an ADM2 label on children). Both
gaps are patched here by falling back to the region as parent instead of a
nonexistent province, and by reconstructing missing cities from the
ancestry every barangay already carries.
"""
import csv
import json

rows = {}  # psgc_id -> [psgc_id, psgc_code, psgc_name, psgc_type, parent_psgc_id]


def load(path):
    with open(path) as fh:
        return json.load(fh)["features"]


def add(psgc_id, psgc_code, psgc_name, psgc_type, parent):
    rows[psgc_id] = [psgc_id, psgc_code, psgc_name, psgc_type, parent]


for feat in load("regions.geojson"):
    p = feat["properties"]
    add(p["psgc_id"], p["psgc_code"], p["psgc_name"], p["psgc_type"], None)

for feat in load("provinces.geojson"):
    p = feat["properties"]
    add(p["psgc_id"], p["psgc_code"], p["psgc_name"], p["psgc_type"], p["ADM1_PCODE"])

province_ids = {r[0] for r in rows.values() if r[3] == "province"}


def city_or_muni_parent(p):
    # NCR "districts" aren't real province rows -> attach straight to region.
    return p["ADM2_PCODE"] if p["ADM2_PCODE"] in province_ids else p["ADM1_PCODE"]


for fname in ("cities.geojson", "municipalities.geojson"):
    for feat in load(fname):
        p = feat["properties"]
        add(p["psgc_id"], p["psgc_code"], p["psgc_name"], p["psgc_type"], city_or_muni_parent(p))

for feat in load("barangays.geojson"):
    p = feat["properties"]
    city_id = p["ADM3_PCODE"]
    if city_id not in rows:
        # HUC/ICC missing from cities.geojson/municipalities.geojson.
        add(
            city_id,
            city_id.replace("PH", "") + "000",  # 7-digit city code + city-level zeros
            p["ADM3_EN"],
            "city",  # HUC/ICC not distinguished in source data
            city_or_muni_parent(p),
        )
    add(p["psgc_id"], p["psgc_code"], p["psgc_name"], p["psgc_type"], city_id)

with open("ph_lgus.csv", "w", newline="") as out:
    w = csv.writer(out)
    w.writerow(["psgc_id", "psgc_code", "psgc_name", "psgc_type", "parent_psgc_id"])
    for row in rows.values():
        w.writerow(row)

print(f"wrote {len(rows)} rows to ph_lgus.csv")
