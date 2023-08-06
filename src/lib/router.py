import json
import re
from typing import List
from flask import request
from flask import Response

from src.lib.controller_base import ControllerBase
from src.lib.controller_factory import ControllerFactory

from src.lib.controller_meta import ControllerMeta
from src.lib.inject import inject
from src.lib.router_meta import RouteMeta


@inject
class Router:
    def __init__(self, controller_factory: ControllerFactory):
        self.controller_factory = controller_factory
        self.controller_route_map: List[RouteMeta] = []

    def map_route(self, route, handler, controller, action):

        self.controller_route_map.append(RouteMeta(controller, action, handler, route))  # RouteMeta(route, handler, controller, action))

    def dispatch_request(self):
        # Get the request's path and method.
        path = request.path
        # trim trailing slash if any
        path = path.rstrip('/')
        # trim first slash if any
        path = path.lstrip('/')

        method = request.method

        is_matched = False

        controller: ControllerBase = None
        controller_meta: ControllerMeta = None
        router_meta: RouteMeta = None
        # Go through all routes in the map.
        for route_meta in self.controller_route_map:
            # Match the 'api/v1/test/(?P<test_key>[^/]+)-(?P<test_value>[^/]+)' == 'api/v1/test/1-2'
            if re.match(route_meta.route, path):
                for entry in self.controller_factory.controllers:
                    if entry.name == route_meta.controller:
                        is_matched = True
                        controller = entry.controller
                        # controller.request = request
                        # controller.response = Response
                        controller_meta = entry
                        router_meta = route_meta
                        break
                        # return route_meta.handler(controller)

        if is_matched:
            # If the method is not allowed, return a 405 error.
            # if method not in meta.handler.methods:
            #     header = {'Content-Type': 'application/json'}
            #     return Response(json.dumps({'message': 'Method not allowed.', 'status': False}), status=405, headers=header)
            return router_meta.handler(controller)

            # controller_meta.handler(,controller, route_meta.action)
            # header = {'Content-Type': 'application/json'}
            # result = meta.handler(controller)
            # return Response(json.dumps(result), status=200, headers=header)
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
