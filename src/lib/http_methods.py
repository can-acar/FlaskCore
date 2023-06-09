from functools import wraps

from flask import request


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
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == 'GET':
                if route:
                    fn.is_http_get = True
                    fn.route = route
                    fn.endpoint = fn.__name__
                    fn.methods = ['GET']
                    fn.is_route = True
                else:
                    fn.is_route = False

                return fn(*args, **kwargs)
            else:
                fn.is_http_get = False
                raise ValueError("Invalid request method. Expected GET.")

        return wrapper

    return decorator