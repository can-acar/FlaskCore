from src.lib.container import Container
from src.lib.container_builder import ContainerBuilder
from src.lib.controller_base import ControllerBase
from src.lib.controller_factory import ControllerFactory
from src.lib.router import Router
from src.lib.scope import Scope


class FlaskCore:
    def __init__(self, app: object, builder: ContainerBuilder):
        self.builder = builder
        self.app = app

    def useCoreService(self):
        self.builder.register_instance(self.app, scope=Scope.SINGLETON)
        self.builder.register(ControllerBase, scope=Scope.TRANSIENT)
        self.builder.register(ControllerFactory, scope=Scope.SINGLETON)
        self.builder.register(Router, scope=Scope.SINGLETON)

    def useApp(self, call_back):
        container = call_back(self.builder.build())

        controller_factory = container.resolve(ControllerFactory)

        controller_factory.use_controller()

        router = container.resolve(Router)

        self.app.dispatch_request = router.dispatch_request

        call_back(container)
