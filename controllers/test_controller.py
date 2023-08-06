from services.test_service import TestService
from src.lib.api_controller import ApiController
from src.lib.api_route import ApiRoute
from src.lib.controller_base import ControllerBase
from src.lib.http_methods import HttpGet
from src.lib.http_methods import HttpPost
from flask import Response


@ApiController
@ApiRoute('api/v1/test/[action]')
class TestController(ControllerBase):

    def __init__(self):
        pass

    @HttpGet('test')  # /{test_key:alpha}-{test_value:min(3)?}
    def with_route(self):  # test_key: str, test_value: str
        return self.Ok({'test': 'test-action'})

    @HttpGet
    def without_route(self):
        return self.Ok({'test': 'test-action'})

    # @HttpGet('test/{test_key:alpha}-{test_value:min(3)?}')
    # def test(self, test_key: str, test_value: str):
    #     return {test_key: test_value}
    #
    # @HttpGet('test2/{test_key}-{test_value?}')
    # def test2(self, test_key, test_value):
    #     return {test_key: test_value}

    # 'test3/{test_key}-{test_value:between(3, 5)?}'
