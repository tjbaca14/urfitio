-- Seed divisions
-- Generated from data/index.json

INSERT INTO app.division (id, division_type)
VALUES
    ('d1', 'Division I'),
    ('d2', 'Division II'),
    ('d3', 'Division III')
ON CONFLICT (id) DO NOTHING;
