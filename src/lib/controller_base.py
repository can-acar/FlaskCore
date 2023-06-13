from abc import abstractmethod
from typing import List

from flask import Flask
from flask import Request
from flask import Response


class ControllerBase:
    app: Flask = None
    request: Request = None
    response: Response = None
    route_data: List = []
    api_route_template: str = ''

    @abstractmethod
    def __init__(self, app: Flask):
        self.app = app
        self.request = Request
        self.response = Response
        self.route_data: List = []
        self.api_route_template = ''
