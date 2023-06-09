from typing import List
from typing import TypeVar

from container_entry import ContainerEntry
from lib.container import Container
from lib.scope import Scope
from singleton import Singleton

T = TypeVar('T')


class ContainerBuilder(metaclass=Singleton):
    _container = None

    def __init__(self):
        self._registry: List[ContainerEntry] = []

    def build(self) -> Container:
        container = Container(self._registry)
        ContainerBuilder._container = container
        self.register_instance(self, Scope.SINGLETON)
        self.register_instance(container, Scope.SINGLETON)

        return ContainerBuilder._container

    def register(self, component=None, scope=Scope.TRANSIENT) -> 'ContainerBuilder':
        self._registry.append(ContainerEntry(component, scope))
        return self

    def register_type(self, member_types, component=None, scope=Scope.TRANSIENT) -> 'ContainerBuilder':
        if not issubclass(component, member_types):
            raise TypeError(f"The provided component is not of the expected type: {member_types}")

        self._registry.append(ContainerEntry(component, scope))
        return self

    def register_instance(self, instance, scope=Scope.SINGLETON) -> 'ContainerBuilder':
        self._registry.append(ContainerEntry(instance, scope, instance=instance))
        return self

    def register_module(self, module) -> 'ContainerBuilder':
        module.load(self)
        return self

    @staticmethod
    def instance() -> Container:
        if ContainerBuilder._container is None:
            ContainerBuilder._container = ContainerBuilder()._container
        return ContainerBuilder._container
