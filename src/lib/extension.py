# def extension(cls):
#     def decorator(extension_cls):
#         for name, value in vars(extension_cls).items():
#             if name.startswith("__") or not callable(value):
#                 continue
#             setattr(cls, name, value)
#         return cls
#
#     return decorator

def extension(cls):
    def decorator(extension_cls):
        for name, value in vars(extension_cls).items():
            if name.startswith("__"):
                continue
            setattr(cls, name, staticmethod(value) if callable(value) else value)
        return cls

    if callable(cls):
        return decorator(cls)
    return decorator

# def extension(cls):
#     def decorator(fn):
#         setattr(cls, fn.__name__, fn)
#         return fn
#
#     return decorator