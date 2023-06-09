from flask import abort
from flask import request
from werkzeug.routing import Map

from src.lib.controller_factory import ControllerFactory
from src.lib.inject import inject


@inject
class Router:
    def __init__(self, controller_factory: ControllerFactory):
        self.controller_factory = controller_factory
        self.controller_route_map = {}

    def map_route(self, route, handler):
        self.controller_route_map[route] = handler

    def dispatch_request(self):
        # Get the request's path and method.
        path = request.path
        method = request.method

        # Go through all controllers.
        for controller in self.controller_factory.controllers:
            # Check if the controller can handle the request.
            try:
                if controller.can_handle_request(path, method):
                    return controller.handle_request()
            except AttributeError:
                print(f"Error: controller is a {type(controller)}, not a Controller object. Value: {controller}")

        # If no controller can handle the request, return a 404 error.
        abort(404)

    # def dispatch_request(self):
    #     controller_name, method_name, route_params = self.parse_route(request.path)
    #     controller = self.container.depend(controller_name)
    #     method = getattr(controller, method_name)
    #
    #     if not callable(method):
    #         raise Exception(f"No callable method {method_name} in {controller_name}")
    #
    #     # route_params (dinamik URL parametreleri) yönteme iletilir.
    #     return method(**route_params)
    #
    # def parse_route(self, path):
    #     # URL'yi parçalara ayırır ve kontrolörün adını ve yöntemin adını bulur.
    #     # "/user/<user_id>" -> ("UserController", "<user_id>")
    #     path_parts = path.strip("/").split("/")
    #     controller_name = f"{path_parts[0].capitalize()}Controller"
    #     method_name = path_parts[1]
    #
    #     # Dinamik URL parametrelerini alır.
    #     route_params = request.view_args or {}
    #
    #     return controller_name, method_name, route_params
