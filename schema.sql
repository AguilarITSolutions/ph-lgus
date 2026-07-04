CREATE TABLE ph_lgus (
    id              BIGSERIAL PRIMARY KEY,
    psgc_id         TEXT NOT NULL UNIQUE,
    psgc_code       TEXT NOT NULL,
    psgc_name       TEXT NOT NULL,
    psgc_type       TEXT NOT NULL CHECK (psgc_type IN
                        ('region', 'province', 'component_city', 'municipality', 'city', 'barangay')),
    parent_id       BIGINT REFERENCES ph_lgus(id)
);

CREATE INDEX idx_ph_lgus_parent_id ON ph_lgus(parent_id);
CREATE INDEX idx_ph_lgus_type      ON ph_lgus(psgc_type);
CREATE INDEX idx_ph_lgus_name      ON ph_lgus(psgc_name);

-- staging table matches the CSV shape (parent as psgc_id, not the DB id)
CREATE TEMP TABLE ph_lgus_staging (
    psgc_id         TEXT,
    psgc_code       TEXT,
    psgc_name       TEXT,
    psgc_type       TEXT,
    parent_psgc_id  TEXT
);

\copy ph_lgus_staging FROM 'ph_lgus.csv' WITH (FORMAT csv, HEADER true)

INSERT INTO ph_lgus (psgc_id, psgc_code, psgc_name, psgc_type)
SELECT psgc_id, psgc_code, psgc_name, psgc_type FROM ph_lgus_staging;

UPDATE ph_lgus l
SET parent_id = p.id
FROM ph_lgus_staging s
JOIN ph_lgus p ON p.psgc_id = s.parent_psgc_id
WHERE l.psgc_id = s.psgc_id AND s.parent_psgc_id IS NOT NULL;
