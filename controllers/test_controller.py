import json

from flask import Response

from models.test_request import TestRequest
from services.test_service import TestService
from src.lib.api_controller import ApiController
from src.lib.api_route import ApiRoute
from src.lib.controller_base import ControllerBase
from src.lib.http_methods import HttpGet
from src.lib.validate import validate


# def Ok(data=None) -> Response:
#     header = {'Content-Type': 'application/json'}
#     return Response(json.dumps(data), status=200, headers=header)


@ApiController
@ApiRoute('api/v1')
class TestController(ControllerBase):

    def __init__(self, test_service: TestService) -> ControllerBase:
        self._test_service = test_service

    @HttpGet('test/{test_key:alpha}-{test_value:alpha}')
    def test(self, test_key: str, test_value: str):
        return Ok(self, data={test_key: test_value})

        # return Ok(data={test_key: test_value})

        @HttpGet('test2/{test_key}-{test_value}')
        @validate(TestRequest, to="test")
        def test2(self, test: TestRequest):
            return self._test_service.test(test)
