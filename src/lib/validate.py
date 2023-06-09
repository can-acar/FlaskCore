import inspect
from functools import wraps

from flask import jsonify
from flask import request


# allow async functions to be used as routes


def validate(model, to=None):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            data = request.get_json()
            model_instance = model(**data)
            if not model_instance.is_valid():
                return {"errors": model_instance.errors}, 400
            if to:
                kwargs[to] = model_instance
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            data = request.get_json()
            model_instance = model(**data)
            if not model_instance.is_valid():
                return {"errors": model_instance.errors}, 400
            if to:
                kwargs[to] = model_instance
            return func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

# def validate(model, to=None):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             data = request.get_json()
#             model_instance = model(**data)
#             if not model_instance.is_valid():
#                 return jsonify(model_instance.errors), 400
#             return func(*args, **kwargs, model=model_instance)
#
#         return wrapper
#
#     return decorator
