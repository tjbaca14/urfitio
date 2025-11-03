import json
import pathlib
import uuid
from typing import Dict, List


from pydantic import BaseModel


class School(BaseModel):
    id: str
    name: str

async def create_cache() -> Dict[str, Dict[str, str]]:
    cache_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    cache_path = f"{cache_dir}/data/index.json"
    with open(cache_path, "r") as f:
        cache = json.load(f)

    return cache


async def get_school_names(
    cache: Dict[str, Dict[str, str]], division: str
) -> List[School]:
    filtered_schools = cache.get(division)
    school_names = filtered_schools.keys()
    schools = [School(id=str(uuid.uuid4()), name=school) for school in school_names]
    return schools
