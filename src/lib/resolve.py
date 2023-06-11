import functools
import inspect

from src.lib.container_builder import ContainerBuilder


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
