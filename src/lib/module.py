from abc import abstractmethod

from container_builder import ContainerBuilder


class Module:
    @abstractmethod
    def load(self, builder: ContainerBuilder):
        pass
