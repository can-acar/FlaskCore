import functools

from src.lib.container_builder import ContainerBuilder
from src.lib.router import Router


def ApiRoute(template='api/[controller]/[action]'):
    api_route_template = template

    def class_decorator(cls):

        container = ContainerBuilder.instance()
        router = container.resolve(Router)
        cls.is_api_route = True
        cls.api_route_template = api_route_template
        cls.route_data = router.controller_route_map
        cls_name = cls.__name__
        cls_name_without_suffix = cls_name.lower()  # Remove "controller" suffix
        if cls_name_without_suffix.endswith("controller"):
            cls_name_without_suffix = cls_name_without_suffix[:-10]  # Remove "controller" suffix
        # TODO: add route template to controller
        for attr_name, handler in cls.__dict__.items():
            if not attr_name.startswith("__"):
                if callable(handler):
                    route_template = api_route_template.replace('[controller]', cls.__name__.lower())
                    action_name = attr_name.lower()
                    # has route property in handler

                    if hasattr(handler, 'route'):
                        action_name = handler.route.split('/')[-1]
                        route_template = route_template.replace('[action]', action_name)
                    else:
                        route_template = route_template.replace('[action]', action_name)

                    # if not define [action] in route template, use method name as action name
                    if '[action]' not in route_template:
                        route_template = route_template + '/' + action_name

                    methods = []

                    # get http method decoratored methods
                    if hasattr(handler, 'methods'):
                        for method in handler.methods:
                            if method not in methods:
                                methods.append(method)

                    router.map_route(route_template, handler, cls_name, attr_name, methods)

        return cls

    return class_decorator
