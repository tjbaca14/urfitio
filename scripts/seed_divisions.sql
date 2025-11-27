-- Seed divisions
INSERT INTO division (id, division_type)
VALUES
    ('d1', 'Division I'),
    ('d2', 'Division II')
ON CONFLICT (id) DO NOTHING;