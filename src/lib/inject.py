import functools
import inspect

from src.lib.container_builder import ContainerBuilder


def inject(original_class):
    orig_init = original_class.__init__

    @functools.wraps(original_class.__init__)
    def __init__(self, *args, **kwargs):
        container = ContainerBuilder.instance()
        params = inspect.signature(orig_init).parameters
        for name, param in params.items():
            if param.annotation is not param.empty:
                instance = container.resolve(param.annotation)
                kwargs.setdefault(name, instance)
        orig_init(self, *args, **kwargs)

    original_class.__init__ = __init__
    return original_class
