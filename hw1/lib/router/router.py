import json
import re
from typing import Callable, Dict, List, Tuple, Any
import uvicorn


class SimpleAPI:
    def __init__(self):
        self.routes: List[Tuple[re.Pattern, str, Callable]] = []

    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        assert scope['type'] == 'http'
        path = scope['path']
        method = scope['method'].upper()
        # Нормализация пути
        if path != '/' and path.endswith('/'):
            path = path.rstrip('/')
        for pattern, route_method, handler in self.routes:
            match = pattern.match(path)
            if match and method == route_method:
                scope['path_params'] = match.groupdict()
                await handler(scope, receive, send)
                return
        await self.send_404(send)

    def route(self, path: str, methods: List[str] = ['GET']):
        path_regex = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)
        pattern = re.compile(f'^{path_regex}/?$')

        def decorator(handler: Callable):
            for method in methods:
                self.routes.append((pattern, method.upper(), handler))
            return handler

        return decorator

    async def send_json(self, send, data, status=200):
        response = json.dumps(data).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [(b"content-type", b"application/json")],
        })
        await send({
            "type": "http.response.body",
            "body": response,
        })

    async def send_400(self, send):
        await self.send_json(send, {"error": "Bad Request"}, status=400)

    async def send_422(self, send):
        await self.send_json(send, {"error": "Unprocessable Entity"}, status=422)

    async def send_404(self, send):
        await self.send_json(send, {"error": "Not Found"}, status=404)

    async def get_request_body(self, receive):
        body = b''
        while True:
            message = await receive()
            body += message.get('body', b'')
            if not message.get('more_body', False):
                break
        return body

    def run(self, host: str = '127.0.0.1', port: int = 8000, **kwargs):
        uvicorn.run(self, host=host, port=port, **kwargs)
