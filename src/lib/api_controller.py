import functools
import inspect

from src.lib.container_builder import ContainerBuilder


def ApiController(cls):
    orig_init = cls.__init__
    cls.is_api_controller = True
    cls.controller_name = cls.__name__.lower()

    @functools.wraps(cls.__init__)
    def __init__(self, *args, **kwargs):
        container = ContainerBuilder.instance()
        params = inspect.signature(orig_init).parameters
        for name, param in params.items():
            if param.annotation is not param.empty:
                instance = container.resolve(param.annotation)
                kwargs.setdefault(name, instance)
        orig_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls
