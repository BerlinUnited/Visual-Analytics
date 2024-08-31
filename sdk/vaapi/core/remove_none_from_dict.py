from typing import Any, Dict, Mapping, Optional


def remove_none_from_dict(original: Mapping[str, Optional[Any]]) -> Dict[str, Any]:
    new: Dict[str, Any] = {}
    for key, value in original.items():
        if value is not None:
            new[key] = value
    return new