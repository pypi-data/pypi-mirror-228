import os
import inspect
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Tuple

from jinja2 import Environment
from jinja2 import FileSystemLoader
from parse import parse
from requests import Session as RequestsSesssion
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from .middleware.middleware import Middleware
from .request import Request
from .response import Response


HTTP_METHODS = ["get", "post", "put", "patch", "delete", "options"]


class Jinx:
    def __init__(
        self,
        *,
        templates_dir="jinx/templates",
        static_dir="jinx/static",
        static_root="/static",
    ) -> None:
        self.routes = {}

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

        self.exception_handler = None

        self.whitenoise = WhiteNoise(self._wsgi_app, root=static_dir)
        self.static_root = static_root

        self.middleware = Middleware(self)

    def __call__(self, environ: dict, start_response: Callable):
        path_info = environ["PATH_INFO"]

        if path_info.startswith(self.static_root):
            environ["PATH_INFO"] = path_info[len(self.static_root) :]
            return self.whitenoise(environ, start_response)
        return self.middleware(environ, start_response)

    def _wsgi_app(self, environ: dict, start_response: Callable) -> Iterable:
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def add_route(
        self, path: str, handler: Callable, *, allowed_methods: list[str] = None
    ):
        if path in self.routes:
            raise AssertionError(f"Duplicate route: {path}")
        if allowed_methods is None:
            allowed_methods = HTTP_METHODS
        self.routes[path] = {
            "handler": handler,
            "allowed_methods": set(allowed_methods),
        }

    def route(self, path: str, *, allowed_methods: list[str] = None):
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods=allowed_methods)
            return handler

        return wrapper

    def not_found(self, request, response):
        response.body = self.template("404.html")
        response.status_code = 404
        return response

    def find_handler(self, request_path: str) -> Tuple[dict, dict]:
        for path, handler_data in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler_data, parse_result.named
        return {"handler": self.not_found, "allowed_methods": set(HTTP_METHODS)}, {}

    def handle_request(self, request: Request) -> Response:
        response = Response()

        handler_data, kwargs = self.find_handler(request_path=request.path)
        handler = handler_data["handler"]
        allowed_methods = handler_data["allowed_methods"]
        try:
            if inspect.isclass(handler):
                method = request.method.lower()
                handler = getattr(handler(), method, None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)
            elif request.method.lower() not in allowed_methods:
                raise AttributeError("Method not allowed", request.method)
            handler(request, response, **kwargs)
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

        return response

    def template(self, template_name: str, context: Optional[dict] = None) -> str:
        if not context:
            context = {}
        return self.templates_env.get_template(template_name).render(**context)

    def test_session(self, base_url="http://testserver"):
        session = RequestsSesssion()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def add_exception_handler(self, exception_handler: Callable):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
