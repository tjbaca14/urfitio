-- Seed schools with recruiting context
INSERT INTO school (id, division_id, name, context, created_date)
VALUES
    (
        'arizona-state',
        'd1',
        'Arizona State',
        'Arizona State Sun Devils Football - Head Coach: Kenny Dillingham. Located in Tempe, Arizona. Conference: Big 12. Strong emphasis on speed and athleticism in recruiting. Active in California, Arizona, and Texas markets. Values character and academic performance. Stadium: Mountain America Stadium. Contact: (480) 965-3379',
        NOW()
    ),
    (
        'usc',
        'd1',
        'USC',
        'USC Trojans Football - Head Coach: Lincoln Riley. Located in Los Angeles, California. Conference: Big Ten. Elite program with strong NFL pipeline. High-powered offensive system. Emphasis on Los Angeles and California recruits. Looking for playmakers and leaders. Stadium: United Airlines Field at LA Memorial Coliseum. Contact: (213) 740-8480',
        NOW()
    )
ON CONFLICT (id) DO NOTHING;