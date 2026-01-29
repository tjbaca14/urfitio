-- Master seed script
-- Run all seed scripts in order
-- Generated from data/index.json

-- 1. Seed divisions first (no dependencies)
-- \i scripts/seed_divisions.sql

-- 2. Seed schools (depends on divisions)
\i scripts/seed_schools.sql

-- Show results
SELECT 'Divisions:' as table_name;
SELECT * FROM app.division;

SELECT 'Schools:' as table_name;
SELECT COUNT(*) as total_schools FROM app.school;
SELECT division_id, COUNT(*) as schools_per_division
FROM public.school
GROUP BY division_id
ORDER BY division_id;
