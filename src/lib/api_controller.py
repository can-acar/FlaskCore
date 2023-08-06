import functools
import inspect

from src.lib.container_builder import ContainerBuilder
from src.lib.controller_factory import ControllerFactory
from src.lib.controller_meta import ControllerMeta
from src.lib.inject_dependencies import inject_dependencies
from src.lib.router import Router


def ApiController(cls):
    container = ContainerBuilder.instance()
    orig_init = cls.__init__
    cls.is_controller = True
    cls.is_api_controller = True
    cls.controller_factory = None

    def get_controller_factory(self):
        if self.controller_factory is None:
            self.controller_factory = container.resolve(ControllerFactory)
            self.controller_factory.add_controller(ControllerMeta(cls, cls.__name__))
        return self.controller_factory

    # @functools.wraps(cls.__init__)
    # def __init__(self, *args, **kwargs):
    #     params = inspect.signature(orig_init).parameters
    #     for name, param in params.items():
    #         if param.annotation is not param.empty:
    #             instance = container.resolve(param.annotation)
    #             kwargs.setdefault(name, instance)
    #     orig_init(self, *args, **kwargs)
    #
    # cls.__init__ = __init__
    return get_controller_factory(cls)
