from abc import abstractmethod

from flask import Flask


class ControllerBase:
    @abstractmethod
    def __init__(self, app: Flask) -> object:
        self.app = app
