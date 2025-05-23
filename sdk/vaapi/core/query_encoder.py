from collections import ChainMap
from typing import Any, Dict, Optional

from .pydantic_utilities import pydantic_v1


# Flattens dicts to be of the form {"key[subkey][subkey2]": value} where value is not a dict
def traverse_query_dict(
    dict_flat: Dict[str, Any], key_prefix: Optional[str] = None
) -> Dict[str, Any]:
    result = {}
    for k, v in dict_flat.items():
        key = f"{key_prefix}[{k}]" if key_prefix is not None else k
        if isinstance(v, dict):
            result.update(traverse_query_dict(v, key))
        else:
            result[key] = v
    return result


def single_query_encoder(query_key: str, query_value: Any) -> Dict[str, Any]:
    if isinstance(query_value, pydantic_v1.BaseModel) or isinstance(query_value, dict):
        if isinstance(query_value, pydantic_v1.BaseModel):
            obj_dict = query_value.dict(by_alias=True)
        else:
            obj_dict = query_value
        return traverse_query_dict(obj_dict, query_key)

    return {query_key: query_value}


def encode_query(query: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    return (
        dict(ChainMap(*[single_query_encoder(k, v) for k, v in query.items()]))
        if query is not None
        else None
    )
