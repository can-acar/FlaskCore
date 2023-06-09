from typing import List, TypeVar

T = TypeVar('T')


class Singleton(type[T]):
    _instances: List[T] = []

    def __call__(cls, *args, **kwargs) -> T:
        if not cls._instances:
            cls._instances.append(super().__call__(*args, **kwargs))
        return cls._instances[0]

    # def __call__(cls, *args, **kwargs):
    #     if cls not in cls._instances:
    #         cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    #     return cls._instances[cls]
