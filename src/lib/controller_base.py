import json
from abc import ABC, abstractmethod
from typing import List

from flask import Flask
from flask import Request
from flask import Response


class ControllerBase(ABC):
    app: Flask = None
    request: Request = None
    response: Response = None
    route_data: List = []
    api_route_template: str = None

    @abstractmethod
    def __init__(self, app: Flask, request: Request, response: Response):
        self.app = app
        self.request = request
        self.response = response
        self.route_data: List = []
        self.api_route_template = ''

    def Ok(self, data=None):
        return self.Json(data)

    def Json(self, data):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(data)
        return self.response(data, 200, mimetype='application/json', headers=headers)

    def BadRequest(self, data):
        headers = {'Content-Type': 'application/json'}
        return self.response(data, 400, mimetype='application/json', headers=headers)

    def Unauthorized(self, data):
        headers = {'Content-Type': 'application/json'}
        return self.response(data, 401, mimetype='application/json', headers=headers)

    def NotFound(self, data):
        headers = {'Content-Type': 'application/json'}
        return self.response(data, 404, mimetype='application/json', headers=headers)

    def ContentType(self, data, content_type):
        headers = {'Content-Type': content_type}
        return self.response(data, 200, mimetype=content_type, headers=headers)

    def File(self, file_path):
        return self.app.send_static_file(file_path)

    # get request file list
    def GetFileList(self):
        return self.request.files
