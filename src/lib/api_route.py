from flask import Request
from flask import Response

from src.lib.container_builder import ContainerBuilder
from src.lib.router import Router


def ApiRoute(template='api/[controller]/[action]'):
    api_route_template = template

    def class_decorator(cls):
        container = ContainerBuilder.instance()
        router = container.resolve(Router)
        cls.api_route_template = api_route_template
        cls.route = router
        # cls.request = Request
        # cls.response = Response
        cls_name = cls.__name__
        cls_name_without_suffix = cls_name.lower()  # Remove "controller" suffix
        if cls_name_without_suffix.endswith("controller"):
            cls_name_without_suffix = cls_name_without_suffix[:-10]  # Remove "controller" suffix

        for attr_name, handler in cls.__dict__.items():
            if not attr_name.startswith("__"):
                if callable(handler):
                    route_template = template.replace('[controller]', cls.__name__.lower())
                    action_name = attr_name.lower()
                    route_template = route_template.replace('[action]', action_name)
                    # add slash to end of route template
                    if not route_template.endswith('/'):
                        route_template += '/'

                    # Eğer handler'in bir route özelliği varsa (HttpGet veya HttpPost tarafından eklenmiş olabilir),
                    # bu route özelliğini genel route şablonuna ekleyin.
                    if hasattr(handler, 'route'):
                        route_template += handler.route

                    # actual_route = create_regex(route_template)

                    router.map_route(route_template, handler, cls_name, attr_name)

        return cls

    return class_decorator

    # get http method decoratored methods
