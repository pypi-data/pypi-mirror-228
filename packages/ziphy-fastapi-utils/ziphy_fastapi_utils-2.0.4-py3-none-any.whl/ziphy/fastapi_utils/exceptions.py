from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Self, TypeAlias

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from ziphy.fastapi_utils import jsonify


# :)
def cls_name_to_snake(obj: type[Any] | Any) -> str:
    name = obj.__name__ if isinstance(obj, type) else type(obj).__name__
    parts, upper = [], False
    for i in range(len(name)):
        if name[i].isupper():
            if not upper and i > 0:
                parts.append("_")
            parts.append(name[i].lower())
            upper = True
        else:
            if upper and len(parts) > 2 and parts[-2] != "_":
                parts.append("_" + parts.pop())
            parts.append(name[i])
            upper = False
    return "".join(parts)


@dataclass
class ExceptionHandler:
    status_code: int
    error_name: str | None = None
    detail: Any = None

    def __call__(self, _request: Request, exception: Exception) -> JSONResponse:
        error_name = self.error_name or cls_name_to_snake(exception)

        content = {"error": error_name}
        if self.detail is not False:
            content["detail"] = jsonify(self.detail) if self.detail else str(exception)

        return JSONResponse(content=content, status_code=self.status_code)


class HTTPError(Exception):
    status_code: int = 400
    error_name: str | None = None
    detail: Any | None = None

    def __init__(
        self,
        status_code: int | None = None,
        error_name: str | None = None,
        detail: Any = None,
    ) -> None:
        self.status_code = status_code or self.status_code
        self.error_name = error_name or self.error_name
        self.detail = detail or self.detail

    @classmethod
    def fastapi_handler(cls, request: Request, exception: Self) -> JSONResponse:
        handler = ExceptionHandler(
            exception.status_code, exception.error_name, exception.detail
        )
        return handler(request, exception)


def pydantic_validation_exception_handler(
    _request: Request, exception: RequestValidationError
) -> JSONResponse:
    errors = jsonable_encoder(exception.errors())
    return JSONResponse(
        content={"error": "validation_error", "detail": errors},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


ExceptionHandlersAlias: TypeAlias = dict[
    int | type[Exception], Callable[[Request, Any], Any]
]
