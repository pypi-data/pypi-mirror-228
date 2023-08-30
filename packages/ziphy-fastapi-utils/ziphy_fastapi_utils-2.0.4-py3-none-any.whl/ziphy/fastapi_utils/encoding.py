from collections.abc import Callable, Sequence
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.types import IncEx


def jsonify(
    obj: Any,
    *,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    custom_encoder: dict[Any, Callable[[Any], Any]] | None = None,
    update: dict[str, Any] | None = None,
    by_alias: bool = True,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
) -> Any:
    result = jsonable_encoder(
        obj=obj,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder or {},
    )
    update = jsonable_encoder(update or {}, custom_encoder=custom_encoder or {})
    return result if isinstance(result, Sequence) else result | update
