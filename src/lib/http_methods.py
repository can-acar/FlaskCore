import re
import asyncio
from functools import wraps
from flask import request
from src.lib.create_regex import create_regex


def HttpGet(route=None):
    def wrapper(fn):
        fn.is_route = True
        fn.route = route
        fn.endpoint = fn.__name__
        fn.methods = [].append(fn.methods) if hasattr(fn, 'methods') else ['GET']
        fn.handler = fn
        if callable(route):
            route_regex = create_regex(route.__name__)
        else:
            route_regex = create_regex(route) if route else ''

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            if request.method == 'GET':
                # define api route template
                if hasattr(fn, 'api_route_template'):
                    api_route_template = fn.api_route_template
                    if not api_route_template.startswith('/'):
                        api_route_template = '/' + api_route_template

                    # /api/[controller]/[action] => replace [controller] and [action] with controller name and action name
                    full_path = api_route_template.replace('[controller]', fn.__class__.__name__.lower()).replace('[action]', route_regex)

                    # if not api_route_template.endswith('/'):
                    #     api_route_template += '/'
                    # full_path = api_route_template + route_regex
                    match = re.match(full_path, request.path)
                    if match:
                        kwargs.update(match.groupdict())
                        return fn(*args, **kwargs)

                else:
                    raise ValueError(f"Invalid request method. Expected GET.")


            else:
                raise ValueError(f"Invalid request method. Expected GET.")

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
                raise ValueError(f"Invalid request method. Expected GET.")

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        else:
            return sync_wrapper

    wrapper.methods = ['GET']
    return wrapper


def HttpPost(route=None):
    def wrapper(fn):
        fn.is_route = True
        fn.route = route
        fn.endpoint = fn.__name__
        fn.methods = [].append(fn.methods) if hasattr(fn, 'methods') else ['POST']
        if callable(route):
            route_regex = create_regex(route.__name__)
        else:
            route_regex = create_regex(route) if route else ''

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            if request.method == 'POST':
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
                raise ValueError(f"Invalid request method. Expected POST.")

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
                raise ValueError(f"Invalid request method. Expected POST.")

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        else:
            return sync_wrapper

    wrapper.methods = ['POST']

    return wrapper
