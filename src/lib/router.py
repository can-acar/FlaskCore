from flask import request

from container import Container
from inject import inject


@inject
class Router:
    def __init__(self, container: Container):
        self.container = container
        self.controller_route_map = {}

    def dispatch_request(self):
        controller_name, method_name, route_params = self.parse_route(request.path)
        controller = self.container.depend(controller_name)
        method = getattr(controller, method_name)

        if not callable(method):
            raise Exception(f"No callable method {method_name} in {controller_name}")

        # route_params (dinamik URL parametreleri) yönteme iletilir.
        return method(**route_params)

    def parse_route(self, path):
        # URL'yi parçalara ayırır ve kontrolörün adını ve yöntemin adını bulur.
        # "/user/<user_id>" -> ("UserController", "<user_id>")
        path_parts = path.strip("/").split("/")
        controller_name = f"{path_parts[0].capitalize()}Controller"
        method_name = path_parts[1]

        # Dinamik URL parametrelerini alır.
        route_params = request.view_args or {}

        return controller_name, method_name, route_params
