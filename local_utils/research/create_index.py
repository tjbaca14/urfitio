import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np

def get_template(file_path: str):
    with open(file_path, 'r') as f:
        file = f.read()
    return file

def fetch_coaches(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        query = "SELECT * FROM app.coaches_detail;"
        cursor.execute(query)
        return cursor.fetchall()
    
def main():

    index = {}

    db_config = {
    'database' : os.environ.get('DATABASE'),
    'user' : os.environ.get('USER'),
    'password' : os.environ.get('PASSWORD'),
    'host' : os.environ.get('HOST'),
    'port' : os.environ.get('PORT')
    } 
    conn = psycopg2.connect(**db_config)
    coaches_detail = fetch_coaches(conn)
    coaches_detail_template = get_template("/Users/tuckerbaca/dev/urfitu/recruitio/prompt/coach_template.txt")

    for coach in coaches_detail:
        index[coach["school"]] = coaches_detail_template.format(**coach)
    
    sorted_index = {key: index[key] for key in sorted(index)}

    with open("index.json", "w") as f:
        json.dump(sorted_index, f, indent=4)






        

if __name__ == '__main__':
    main()