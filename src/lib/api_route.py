from src.lib.container_builder import ContainerBuilder
from src.lib.router import Router


def ApiRoute(template='api/[controller]/[action]'):
    def class_decorator(cls):
        container = ContainerBuilder.instance()
        router = container.resolve(Router)
        cls._api_route_template = template
        cls_name = cls.__name__
        cls_name_without_suffix = cls_name.lower()  # Remove "controller" suffix
        if cls_name_without_suffix.endswith("controller"):
            cls_name_without_suffix = cls_name_without_suffix[:-10]  # Remove "controller" suffix

            # ignore __init__ arguments to the constructor

        for attr_name, handler in cls.__dict__.items():
            if not attr_name.startswith("__"):
                if callable(handler):
                    # This is a method
                    action_name = attr_name.lower() if not attr_name.startswith("__") else ''
                    # Replace placeholders with actual values
                    route_template = template.replace('[controller]', cls_name_without_suffix).replace('[action]',
                                                                                                       action_name)
                    # Remove double slashes (if any)
                    actual_route = route_template.replace('//', '/')
                    # Remove trailing slash (if any)
                    actual_route = actual_route.rstrip('/')
                    # Here you can store the actual route in some way. For example:
                    handler.route = actual_route
                    handler.endpoint = action_name

                    router.map_route(actual_route, handler, cls_name, attr_name)

        return cls

    return class_decorator

    # get http method decoratored methods
