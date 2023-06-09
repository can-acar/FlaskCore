def ApiRoute(template='api/[controller]/[action]'):
    def decorator(cls):
        cls._api_route_template = template
        return cls

    return decorator
