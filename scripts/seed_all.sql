-- Master seed script
-- Run all seed scripts in order

-- 1. Seed divisions first (no dependencies)
\i scripts/seed_divisions.sql

-- 2. Seed schools (depends on divisions)
\i scripts/seed_schools.sql

-- Show results
SELECT 'Divisions:' as table_name;
SELECT * FROM division;

SELECT 'Schools:' as table_name;
SELECT * FROM school;