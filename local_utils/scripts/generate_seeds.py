#!/usr/bin/env python3
"""
Generate SQL seed files from index.json data.
Reads data/index.json and creates seed_divisions.sql and seed_schools.sql
"""

import json
import os
from pathlib import Path
import uuid


def generate_id(name: str) -> str:
    """Generate a URL-friendly ID from school name."""
    return name.lower().replace(' ', '-').replace("'", '').replace('.', '')


def escape_sql_string(s: str) -> str:
    """Escape single quotes for SQL."""
    return s.replace("'", "''")


def load_index_data(index_path: Path) -> dict:
    """Load the index.json file."""
    with open(index_path, 'r') as f:
        return json.load(f)


def generate_divisions_sql(data: dict, schema: str = 'public') -> str:
    """Generate seed_divisions.sql content."""
    sql = f"""-- Seed divisions
-- Generated from data/index.json

INSERT INTO {schema}.division (id, division_type)
VALUES
"""

    divisions = []
    division_map = {
        'D1': 'Division I',
        'D2': 'Division II',
        'D3': 'Division III',
        'JUCO': 'Junior College'
    }

    for div_key in data.keys():
        if div_key in division_map:
            div_id = div_key.lower()
            div_name = division_map[div_key]
            divisions.append(f"    ('{div_id}', '{div_name}')")

    sql += ',\n'.join(divisions)
    sql += '\nON CONFLICT (id) DO NOTHING;\n'

    return sql


def generate_schools_sql(data: dict, schema: str = 'public') -> str:
    """Generate seed_schools.sql content."""
    sql = f"""-- Seed schools with context from index.json
-- Generated from data/index.json

INSERT INTO {schema}.school (id, division_id, name, context, created_date)
VALUES
"""

    schools = []

    for division_key, schools_dict in data.items():
        division_id = division_key.lower()

        for school_name, context in schools_dict.items():
            school_id = generate_id(school_name)
            escaped_name = escape_sql_string(school_name)
            escaped_context = escape_sql_string(context)

            school_entry = f"""    (
        '{school_id}',
        '{division_id}',
        '{escaped_name}',
        '{escaped_context}',
        NOW()
    )"""
            schools.append(school_entry)

    sql += ',\n'.join(schools)
    sql += '\nON CONFLICT (id) DO NOTHING;\n'

    return sql


def generate_seed_all_sql(schema: str = 'public') -> str:
    """Generate master seed_all.sql script."""
    return f"""-- Master seed script
-- Run all seed scripts in order
-- Generated from data/index.json

-- 1. Seed divisions first (no dependencies)
\\i scripts/seed_divisions.sql

-- 2. Seed schools (depends on divisions)
\\i scripts/seed_schools.sql

-- Show results
SELECT 'Divisions:' as table_name;
SELECT * FROM {schema}.division;

SELECT 'Schools:' as table_name;
SELECT COUNT(*) as total_schools FROM {schema}.school;
SELECT division_id, COUNT(*) as schools_per_division
FROM {schema}.school
GROUP BY division_id
ORDER BY division_id;
"""


def main():
    # Get schema from environment variable
    schema = os.getenv('DB_SCHEMA', 'public')

    # Paths
    project_root = Path(__file__).parent.parent
    data_path = project_root / 'data' / 'index.json'
    scripts_dir = project_root / 'scripts'

    print(f"Reading data from: {data_path}")
    print(f"Using schema: {schema}")

    # Load data
    data = load_index_data(data_path)

    # Count schools
    total_schools = sum(len(schools) for schools in data.values())
    print(f"Found {len(data)} divisions with {total_schools} schools")

    # Generate SQL files
    print("\nGenerating seed files...")

    divisions_sql = generate_divisions_sql(data, schema)
    with open(scripts_dir / 'seed_divisions.sql', 'w') as f:
        f.write(divisions_sql)
    print(f"  ✓ seed_divisions.sql ({len(data)} divisions)")

    schools_sql = generate_schools_sql(data, schema)
    with open(scripts_dir / 'seed_schools.sql', 'w') as f:
        f.write(schools_sql)
    print(f"  ✓ seed_schools.sql ({total_schools} schools)")

    seed_all_sql = generate_seed_all_sql(schema)
    with open(scripts_dir / 'seed_all.sql', 'w') as f:
        f.write(seed_all_sql)
    print(f"  ✓ seed_all.sql (master script)")

    print("\n✅ Seed files generated successfully!")
    print("\nTo apply seeds:")
    print(f"  docker exec -it baseball psql -U bb_admin -d baseball -f /path/to/scripts/seed_all.sql")


if __name__ == '__main__':
    main()