import functools
import inspect

from lib.container_builder import ContainerBuilder


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

# def inject(cls: Union[Any, List[Any]]) -> Callable:
#     if not isinstance(cls, list):
#         cls = [cls]
#
#     def decorator(original_class):
#         orig_init = original_class.__init__
#
#         @functools.wraps(original_class.__init__)
#         def __init__(self, *args, **kwargs):
#             container = ContainerBuilder.instance()
#             for dependency in cls:
#                 instance = container.resolve(dependency)
#                 kwargs[dependency.__name__.lower()] = instance
#             orig_init(self, *args, **kwargs)
#
#         original_class.__init__ = __init__
#         return original_class
#
#     return decorator

# ****  bu çalıştı
# def inject(cls: Union[Any, List[Any]]) -> Callable:
#     if not isinstance(cls, list):
#         cls = [cls]
#
#     def decorator(target):
#         if not inspect.isclass(target) and not inspect.ismethod(target):
#             raise TypeError("The @inject decorator can only be used with classes and class methods")
#
#         sig = inspect.signature(target)
#
#         @functools.wraps(target)
#         def wrapper(*args, **kwargs):
#             container = ContainerBuilder.instance()
#             for name, param in sig.parameters.items():
#                 if name not in kwargs and param.annotation in cls:
#                     kwargs[name] = container.resolve(param.annotation)
#             return target(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
# ****

# def inject(cls):
#     @functools.wraps(cls)
#     def wrapper(*args, **kwargs):
#         constructor = cls.__init__
#         params = inspect.signature(constructor).parameters
#         deps = {name: param.annotation for name, param in params.items() if param.annotation != param.empty}
#         container = ContainerBuilder.instance()
#         resolved = {name: container.resolve(dep) for name, dep in deps.items()}
#         return cls(*args, **resolved, **kwargs)
#
#     return wrapper
