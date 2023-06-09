from typing import List

from flask import abort
from flask import request
from werkzeug.routing import Map

from src.lib.controller_factory import ControllerFactory
from src.lib.inject import inject


class RouteMeta:
    def __init__(self, route, handler, controller, action):
        self.route = route
        self.handler = handler
        self.controller = controller
        self.action = action


@inject
class Router:
    def __init__(self, controller_factory: ControllerFactory):
        self.controller_factory = controller_factory
        self.controller_route_map: List[RouteMeta] = []

    def map_route(self, route, handler, controller, action):
        self.controller_route_map.append(RouteMeta(route, handler, controller, action))

    def dispatch_request(self):
        # Get the request's path and method.
        path = request.path
        # trim trailing slash if any
        path = path.rstrip('/')
        # trim first slash if any
        path = path.lstrip('/')

        method = request.method

        # Go through all routes in the map.
        for route_meta in self.controller_route_map:
            # Check if the route can handle the request.
            if route_meta.route == path:
                for entry in self.controller_factory.controllers:
                    if entry.controller.__name__ == route_meta.controller:
                        controller  = entry.controller()
                        return getattr(controller, route_meta.action)()

        # If no route can handle the request, return a 404 error.
        abort(404)
