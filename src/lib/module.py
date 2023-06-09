from abc import abstractmethod

from src.lib.container_builder import ContainerBuilder


class Module:
    @abstractmethod
    def load(self, builder: ContainerBuilder):
        pass
