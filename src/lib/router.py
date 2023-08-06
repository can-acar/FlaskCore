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
            # Match the 'api/v1/test/(?P<test_key>[^/]+)-(?P<test_value>[^/]+)' == 'api/v1/test/1-2'
            if re.match(route_meta.route, path):
                for entry in self.controller_factory.controllers:
                    if entry.name == route_meta.controller:
                        controller = entry.controller()

                        return route_meta.handler(controller)
            else:
                header = {'Content-Type': 'application/json'}
                return Response(json.dumps({'message': 'Not found.', 'status': False}), status=404, headers=header)

        # If no route can handle the request, return a 404 error.
        header = {'Content-Type': 'application/json'}
        return Response(json.dumps({'message': 'Not found.', 'status': False}), status=404, headers=header)

        # , route_meta.action
        ##return getattr(controller, route_meta.action)()
        # call the handler function
        # return route_meta.handler(controller, route_meta.action)
        # if route_meta.route == path:
        #     for entry in self.controller_factory.controllers:
        #         if entry.controller.__name__ == route_meta.controller:
        #             controller  = entry.controller()
        #             return getattr(controller, route_meta.action)()

        # If no route can handle the request, return a 404 error.
        # and decorate
        # the
        # response
        # with the handler's response
        # return getattr(controller, route_meta.action)()
        # # return route_meta.handler(getattr(controller, route_meta.action)())
