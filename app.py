import asyncio

from flask import Flask

from modules.api_module import ApiModule
from src.lib.container_builder import ContainerBuilder
from src.lib.controller_base import ControllerBase
from src.lib.controller_factory import ControllerFactory
from src.lib.router import Router
from src.lib.scope import Scope



async def start_flask_app(port):
    builder = ContainerBuilder()
    app = Flask(__name__)
    builder.register_instance(app, scope=Scope.SINGLETON)
    builder.register(ControllerBase, scope=Scope.TRANSIENT)
    builder.register(ControllerFactory, scope=Scope.SINGLETON)
    builder.register(Router, scope=Scope.SINGLETON)
    builder.register_module(ApiModule())

    container = builder.build()

    controller_factory = container.resolve(ControllerFactory)

    controller_factory.use_controller()

    router = container.resolve(Router)

    app.dispatch_request = router.dispatch_request

    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == '__main__':
    asyncio.run(start_flask_app(8082))
