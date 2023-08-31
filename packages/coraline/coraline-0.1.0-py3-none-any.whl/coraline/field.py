from pydantic import Field

from coraline.types import HashType


def KeyField(*args, **kwargs):  # C901
    hash_type: HashType = kwargs.pop("hash_type", HashType.HASH)
    if "json_schema_extra" not in kwargs:
        kwargs["json_schema_extra"] = {
            "dynamodb_key": True,
            "dynamodb_hash_type": hash_type,
        }
    else:
        kwargs["json_schema_extra"].update(
            {"dynamodb_key": True, "dynamodb_hash_type": hash_type}
        )
    return Field(*args, **kwargs)
