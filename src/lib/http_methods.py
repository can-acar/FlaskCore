import re
from functools import wraps
from flask import request

from src.lib.create_regex import create_regex


def HttpPost(route=None):
    def decorator(fn):
        fn.is_http_post = True

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == 'POST':
                return fn(*args, **kwargs)
            else:
                raise ValueError("Invalid request method. Expected POST.")

        if route:
            fn.route = route
            fn.endpoint = fn.__name__
            fn.methods = ['POST']
            fn.is_route = True
        else:
            fn.is_route = False
        return wrapper

    return decorator


def HttpGet(route=None):
    if route:
        route_regex = create_regex(route)

    def decorator(fn):
        # get the _api_route_template from ApiRoute

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == 'GET':
                # a
                api_route_template = args[0].api_route_template
                if not api_route_template.startswith('/'):
                    api_route_template = '/' + api_route_template

                if not api_route_template.endswith('/'):
                    api_route_template += '/'
                full_path = api_route_template + route_regex
                match = re.match(full_path, request.path)
                if match:
                    kwargs.update(match.groupdict())
                    return fn(*args, **kwargs)
            else:
                fn.is_http_get = False
                return {'message': 'Method not allowed.', 'status': False}  # Response("Invalid request method. Expected GET.", status=400)
                # raise ValueError("Invalid request method. Expected GET.")

        if route:
            wrapper.is_http_get = True
            wrapper.route = route_regex
            wrapper.endpoint = fn.__name__
            wrapper.methods = ['GET']
            wrapper.is_route = True
        else:
            wrapper.is_route = False
        return wrapper

    return decorator
