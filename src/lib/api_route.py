import functools

from src.lib.container_builder import ContainerBuilder
from src.lib.router import Router


def create_endpoint(handler, cls_name, action_name):
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        return cls_name + '.' + action_name

    return wrapper


def ApiRoute(template='api/[controller]/[action]'):
    api_route_template = template

    def class_decorator(cls):

        container = ContainerBuilder.instance()
        router = container.resolve(Router)
        cls.is_api_route = True
        cls.api_route_template = template
        cls.route_data = router.controller_route_map
        cls_name = cls.__name__
        cls_name_without_suffix = cls_name.lower()  # Remove "controller" suffix
        if cls_name_without_suffix.endswith("controller"):
            cls_name_without_suffix = cls_name_without_suffix[:-10]  # Remove "controller" suffix
        # TODO: add route template to controller
        for attr_name, handler in cls.__dict__.items():
            if not attr_name.startswith("__"):
                if callable(handler):
                    route_template = api_route_template
                    action_name = attr_name.lower()
                    endpoint = f"{cls_name}.{action_name}"
                    handler.api_route_template = api_route_template

                    if hasattr(handler, 'route'):
                        route_template = handler.route
                        action_name = handler.route
                        handler.route_template = route_template
                        handler.endpoint = endpoint
                    else:
                        route_template = api_route_template  # .replace("[controller]", cls_name).replace("[action]", action_name)
                        handler.route_template = route_template
                        action_name = attr_name.lower()
                        # Create to strint to function
                        handler.endpoint = endpoint

                    methods = []

                    # get http method decoratored methods
                    if hasattr(handler, 'methods'):
                        for method in handler.methods:
                            if method not in methods:
                                methods.append(method)

                    router.map_route(route_template, handler, cls_name, action_name, methods)

        return cls

    return class_decorator
