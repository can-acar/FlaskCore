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


def HttpGet(template=None):
    if callable(template):
        route_regex = ''
        fn = template
    else:
        route_regex = create_regex(template)

        def decorator(fn):
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
                    raise ValueError("Invalid request method. Expected GET.")

            if template:
                wrapper.is_http_get = True
                wrapper.route = route_regex
                wrapper.endpoint = fn.__name__
                wrapper.methods = ['GET']
                wrapper.is_route = True
            else:
                wrapper.is_route = False
            return wrapper

        return decorator
    # Decorator is used as @HttpGet
    fn.is_http_get = True
    fn.route = fn.__name__
    fn.endpoint = fn.__name__
    fn.methods = ['GET']
    fn.is_route = False
    return fn
