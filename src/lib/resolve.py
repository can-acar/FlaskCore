import functools
import inspect

from lib.container_builder import ContainerBuilder


def resolve(*deps):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            container = ContainerBuilder.instance()
            params = inspect.signature(func).parameters
            func_deps = {name: param.annotation for name, param in params.items() if param.annotation in deps}

            resolved = {name: container.resolve(dep) for name, dep in func_deps.items()}
            return func(*args, **resolved, **kwargs)

        return wrapper

    return decorator

# def resolve(types: Union[type, List[type]]) -> Callable:
#     if not isinstance(types, list):
#         types = [types]
#
#     def decorator(func):
#         sig = inspect.signature(func)
#
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             container = ContainerBuilder.instance()
#             for type_ in types:
#                 if type_.__name__ in sig.parameters and type_.__name__ not in kwargs:
#                     kwargs[type_.__name__] = container.resolve(type_)
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator

# def resolve(types: Union[type, List[type]]) -> Callable:
#     if not isinstance(types, list):
#         types = [types]
#
#     def decorator(func):
#         if not inspect.isfunction(func):
#             raise TypeError("The @resolve decorator can only be used with functions")
#
#         sig = inspect.signature(func)
#
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             container = ContainerBuilder.instance()
#             for name, param in sig.parameters.items():
#                 if name not in kwargs and param.annotation in types:
#                     kwargs[name] = container.resolve(param.annotation)
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator

# def resolve(cls: Any) -> Callable:
#     """
#     Decorator to resolve a single dependency for a function or method.
#     """
#
#     def decorator(func: Callable) -> Callable:
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             container = ContainerBuilder.instance()
#
#             sig = inspect.signature(func)
#             for name, param in sig.parameters.items():
#                 if name not in kwargs and param.annotation == cls:
#                     kwargs[name] = container.resolve(cls)
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator

# class resolve:
#     def __init__(self, types: Union[type, List[type]]):
#         types = [types]  # if not isinstance(types, list) else types
#         self.types = types
#
#     def __call__(self, func):
#         sig = inspect.signature(func)
#         types_dict = dict(zip(sig.parameters, self.types))
#
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             container = ContainerBuilder.instance()
#             for name, param in sig.parameters.items():
#                 if name not in kwargs and param.annotation in types_dict:
#                     kwargs[name] = container.resolve(param.annotation)
#             return func(*args, **kwargs)
#
#         return wrapper

# def resolve(*deps):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             container = ContainerBuilder.instance()
#             params = inspect.signature(func).parameters
#             func_deps = {name: param.annotation for name, param in params.items() if param.annotation in deps}
#
#             resolved = {name: container.resolve(dep) for name, dep in func_deps.items()}
#             return func(*args, **resolved, **kwargs)
#
#         return wrapper
#
#     return decorator
