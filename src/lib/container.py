import inspect
from typing import List
from typing import Type
from typing import TypeVar

from src.lib.container_entry import ContainerEntry
from src.lib.scope import Scope

T = TypeVar('T')


class Container():
    _builder: object

    def __init__(self, registry: List[ContainerEntry], builder):
        self.builder = builder
        self._registry = registry

    def resolve(self, member_type: Type[T]) -> T:
        for entry in self._registry:
            if entry.cls is member_type or isinstance(entry.cls, member_type) or isinstance(entry.instance,
                                                                                            member_type):
                if entry.scope == Scope.SINGLETON:
                    if not entry.instance:
                        entry.instance = self._create_instance(entry.cls)
                        return entry.instance
                    if entry.instance:
                        return entry.instance
                if entry.scope == Scope.REQUEST:
                    if not entry.instance:
                        entry.instance = self._create_instance(entry.cls)
                        return entry.instance
                    return entry.instance
                else:  # Scope.TRANSIENT
                    return self._create_instance(entry.cls)
        raise ValueError(f"No member of type {member_type} registered")

    def depend(self, member_type: str) -> T:
        if isinstance(member_type, str):
            # member_type is a string because of search in the registry
            for entry in self._registry:
                if entry.cls.__name__ == member_type:
                    return self.resolve(entry.cls)

    def _create_instance(self, component: type) -> object:
        params = inspect.signature(component).parameters
        if not params:
            return component()
        dependencies = {
            name: self.resolve(param.annotation)
            for name, param in params.items()
            if param.annotation != inspect.Parameter.empty
        }
        return component(**dependencies)

    @staticmethod
    def instance(self):
        return self.builder
