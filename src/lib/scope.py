from enum import Enum


class Scope(Enum):
    SINGLETON = 1
    TRANSIENT = 2
    REQUEST = 3
