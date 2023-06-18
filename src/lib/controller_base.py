from abc import abstractmethod
from typing import List

from flask import Flask
from flask import Request
from flask import Response


class ControllerBase:
    app: Flask = None
    request = None
    response = None
    route_data: List = []
    api_route_template: str = None

    @abstractmethod
    def __init__(self, app: Flask):
        self.app = app
        self.request = Request
        self.response = Response
        self.route_data: List = []
        self.api_route_template = ''

    def Ok(self, data):
        return self.response(data, 200)

    def Json(self, data):
        return self.response(data, 200, mimetype='application/json')

    def BadRequest(self, data):
        return self.response(data, 400)

    def Unauthorized(self, data):
        return self.response(data, 401)

    def NotFound(self, data):
        return self.response(data, 404)

    def ContentType(self, data, content_type):
        return self.response(data, 200, mimetype=content_type)

    def File(self, file_path):
        return self.app.send_static_file(file_path)

    # get request file list
    def GetFileList(self):
        return self.request.files
