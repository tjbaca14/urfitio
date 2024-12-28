import pathlib
import json
from typing import List
import uuid
from typing import Dict
from app.models.school import School

async def create_cache() -> Dict[str, str]:
    cache_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    cache_path = f"{cache_dir}/data/index.json"
    with open(cache_path, "r") as f:
        cache = json.load(f)
    return cache


async def get_school_names(cache: Dict[str, str]) -> List[School]:
    school_names = cache.keys()
    schools = [School(id=str(uuid.uuid4()), name=school) for school in school_names]
    return schools