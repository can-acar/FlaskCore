from services.test_service import TestService
from src.lib.container_builder import ContainerBuilder
from src.lib.module import Module
from src.lib.scope import Scope


class ApiModule(Module):
    def load(self, builder: ContainerBuilder):
        builder.register(TestService, scope=Scope.TRANSIENT)
