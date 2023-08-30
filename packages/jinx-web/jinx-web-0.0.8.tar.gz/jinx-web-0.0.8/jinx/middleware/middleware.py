from typing import Callable
from ..request import Request
from ..response import Response


class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ: dict, start_response: Callable):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, req: Request):
        pass

    def process_response(self, req: Request, resp: Response):
        pass

    def handle_request(self, request: Request) -> Response:
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
