import json
import logging
import time
from typing import Any
from urllib import response

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request


logger = logging.getLogger("uvicorn.error")

class NotificationLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        if not self._should_log_request(path = path, method = method):
            return await call_next(request)

        start_time = time.perf_counter()

        request_body = await self._read_json_body(request = request)

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_data = self._parse_json_bytes(response_body)

        self._log_notification_request(
            request=request,
            response=response,
            request_body=request_body,
            response_data=response_data,
            duration_ms=duration_ms,
        )

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )



    def _should_log_request(
            self,
            path: str,
            method: str
    ) -> bool:
        return path.rstrip("/") == "/notifications" and method == "POST"

    async def _read_json_body(
            self,
            request: Request,
    ) -> dict[str, Any]:
        body = await request.body()

        if not body:
            return {}

        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}

    def _parse_json_bytes(
            self,
            response_body: bytes,
    ) -> dict[str, Any]:
        if not response_body:
            return {}

        try:
            return json.loads(response_body.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _extract_error_message(
            self,
            response_data: dict[str, Any],
    ) -> Any:
        if response_data.get("error_msg"):
            return response_data.get("error_msg")

        if response_data.get("detail"):
            return response_data.get("detail")

        return None

    def _log_notification_request(
            self,
            request: Request,
            response: Response,
            request_body: dict[str, Any],
            response_data: dict[str, Any],
            duration_ms: float,
    ) -> None:
        client_ip = request.client.host if request.client else None

        error_msg = self._extract_error_message(response_data = response_data)

        logger.info(
            "Notification request completed | "
            "method=%s / path=%s / status_code=%s / duration_ms=%s / client_ip=%s "
            "source_service=%s / channel=%s / notification_type=%s / recipient=%s "
            "notification_id=%s / final_status=%s / error_msg=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            client_ip,
            request_body.get("source_service"),
            request_body.get("channel"),
            request_body.get("notification_type"),
            request_body.get("recipient"),
            response_data.get("id"),
            response_data.get("status"),
            error_msg,
        )