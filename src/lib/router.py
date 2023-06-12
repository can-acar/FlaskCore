import json
import re
from typing import List

from flask import abort
from flask import request
from flask import Response
from werkzeug.routing import Map

from src.lib.controller_factory import ControllerFactory
from src.lib.inject import inject


class RouteMeta:
    def __init__(self, route, handler, controller, action, methods: []):
        self.route = route
        self.handler = handler
        self.controller = controller
        self.action = action
        self.methods: [] = methods


@inject
class Router:
    def __init__(self, controller_factory: ControllerFactory):
        self.controller_factory = controller_factory
        self.controller_route_map: List[RouteMeta] = []

    def map_route(self, route: object, handler: object, controller: object, action: object, methods: []):
        self.controller_route_map.append(RouteMeta(route, handler, controller, action, methods))

    def dispatch_request(self):
        header = {'Content-Type': 'application/json'}
        # Get the request's path and method.
        path = request.path
        # trim trailing slash if any
        path = path.rstrip('/')
        # trim first slash if any
        path = path.lstrip('/')
        controller = None

        method = request.method  # type:str # 'GET', 'POST', 'PUT', 'DELETE'
        is_matched = False
        # Go through all routes in the map.
        for route_meta in self.controller_route_map:
            # Match the 'api/v1/test/(?P<test_key>[^/]+)-(?P<test_value>[^/]+)' == 'api/v1/test/1-2'

            if re.match(route_meta.route, path):
                if method not in route_meta.methods:
                    return Response(json.dumps({'message': 'Method Not Allowed', 'status': False}),
                                    status=400,
                                    headers=header)

                for entry in self.controller_factory.controllers:
                    if entry.controller.__name__ == route_meta.controller:
                        is_matched = True
                        controller = entry.controller()
                        break

                if controller is not None:
                    return route_meta.handler(controller)

        if not is_matched:
            return Response(json.dumps({'message': 'Not found.', 'status': False}), status=404, headers=header)

        return Response(json.dumps({'message': 'Not found.', 'status': False}), status=404, headers=header)
