from flask import Blueprint

from container_builder import ContainerBuilder


def route(rule, **options):
    def decorator(f):
        container = ContainerBuilder.instance()
        endpoint = options.pop("endpoint", None)
        if endpoint is None:
            endpoint = f.__name__
        bp = container.resolve(Blueprint)
        bp.add_url_rule(rule, endpoint, f, **options)
        return f

    return decorator
