import logging

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class ResponseLoggingMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def log_info(request: Request, response: Response, response_body: bytes) -> None:
        if str(response.status_code).startswith("4") and response_body:
            assert request.client
            address = f"{request.client.host}:{request.client.port}"
            logging.getLogger("uvicorn.info").info(
                f"{address} - {response_body.decode()}"
            )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:  # type: ignore[attr-defined]
            response_body += chunk

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=BackgroundTask(self.log_info, request, response, response_body),
        )
