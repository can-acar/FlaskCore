import functools

from src.lib.container_builder import ContainerBuilder
from src.lib.router import Router


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
                    if '[controller]' in api_route_template or '[action]' in api_route_template:
                        route_template = api_route_template.replace('[controller]', cls.__name__.lower())
                        action_name = attr_name.lower()

                        if hasattr(handler, 'route'):
                            route_template = route_template.replace('[action]', handler.route)
                        else:
                            route_template = route_template.replace('[action]', action_name)
                    else:
                        route_template = api_route_template
                        if hasattr(handler, 'route'):
                            route_template = route_template + '/' + handler.route
                        else:
                            route_template = route_template + '/' + attr_name.lower()

                    methods = []

                    # get http method decoratored methods
                    if hasattr(handler, 'methods'):
                        for method in handler.methods:
                            if method not in methods:
                                methods.append(method)

                    router.map_route(route_template, handler, cls_name, attr_name, methods)

        return cls

    return class_decorator
