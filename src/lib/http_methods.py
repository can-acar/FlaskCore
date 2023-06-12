import re
from functools import wraps
from flask import request
from src.lib.create_regex import create_regex


def HttpGet(template=None):
    if callable(template):
        route_regex = ''
        fn = template
    else:
        route_regex = create_regex(template)

        def decorator(fn):
            @wraps(fn)
            def sync_wrapper(*args, **kwargs):
                if request.method == 'GET':
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
                    raise ValueError("Invalid request method. Expected GET.")

            if template:
                sync_wrapper.is_http_get = True
                sync_wrapper.route = route_regex
                sync_wrapper.endpoint = fn.__name__
                sync_wrapper.methods = ['GET']
                sync_wrapper.is_route = True
            else:
                sync_wrapper.is_route = False

            @wraps(fn)
            async def async_wrapper(*args, **kwargs):
                if request.method == 'GET':
                    api_route_template = args[0].api_route_template
                    if not api_route_template.startswith('/'):
                        api_route_template = '/' + api_route_template
                    if not api_route_template.endswith('/'):
                        api_route_template += '/'
                    full_path = api_route_template + route_regex
                    match = re.match(full_path, request.path)
                    if match:
                        kwargs.update(match.groupdict())
                        return await fn(*args, **kwargs)
                else:
                    raise ValueError("Invalid request method. Expected GET.")

            if template:
                async_wrapper.is_http_get = True
                async_wrapper.route = route_regex
                async_wrapper.endpoint = fn.__name__
                async_wrapper.methods = ['GET']
                async_wrapper.is_route = True
            else:
                async_wrapper.is_route = False

            if request.is_async:
                return async_wrapper
            else:
                return sync_wrapper

        return decorator

    fn.is_http_get = True
    fn.route = fn.__name__
    fn.endpoint = fn.__name__
    fn.methods = ['GET']
    fn.is_route = False
    return fn
