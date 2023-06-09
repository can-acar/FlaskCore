import inspect

from src.lib.container import Container


def inject_dependencies(original_class, container: Container):
    # Get the __init__ method of the class
    orig_init = original_class.__init__

    # Redefine the __init__ method
    def new_init(self, *args, **kwargs):
        # Get the parameters of the original __init__ method
        params = inspect.signature(orig_init).parameters

        # Go through the parameters and if a parameter is a class,
        # replace it with an instance of that class
        for name, param in params.items():
            if param.annotation is not param.empty and \
                    inspect.isclass(param.annotation):
                instance = container.resolve(param.annotation)
                kwargs.setdefault(name, instance)
                # kwargs[name] = container.resolve(param.annotation)

        # Call the original __init__ method with the new parameters
        orig_init(self, *args, **kwargs)

    # Replace the original __init__ method with the new one
    original_class.__init__ = new_init

    return original_class
