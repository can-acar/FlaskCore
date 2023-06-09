from src.lib import router


def ApiRoute(template='api/[controller]/[action]'):
    def class_decorator(cls):
        cls._api_route_template = template
        cls_name = cls.__name__.lower()
        if cls_name.endswith("controller"):
            cls_name = cls_name[:-10]  # Remove "controller" suffix

        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):
                # This is a method
                action_name = attr_name.lower()
                # Replace placeholders with actual values
                actual_route = template.replace('[controller]', cls_name).replace('[action]', action_name)
                # Here you can store the actual route in some way. For example:
                attr_value._actual_route = actual_route

                # I want to callback to Route decorator to add the route to the Flask app
                # I don't know how to do it, so I'll just store the route in a list
                # and then I'll add it to the Flask app in the main.py file
                router.Router.map_route(actual_route, attr_value)

        return cls

    return class_decorator
