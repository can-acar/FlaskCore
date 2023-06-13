from services.test_service import TestService
from src.lib.api_controller import ApiController
from src.lib.api_route import ApiRoute
from src.lib.controller_base import ControllerBase
from src.lib.http_methods import HttpGet
from src.lib.http_methods import HttpPost


@ApiController
@ApiRoute('api/v1/[action]')
class TestController(ControllerBase):

    def __init__(self, test_service: TestService):
        self._test_service = test_service

    # @HttpGet('test/{test_key:alpha}-{test_value:min(3)?}')
    # def test(self, test_key: str, test_value: str):
    #     return {test_key: test_value}
    #
    # @HttpGet('test2/{test_key}-{test_value?}')
    # def test2(self, test_key, test_value):
    #     return {test_key: test_value}

    # 'test3/{test_key}-{test_value:between(3, 5)?}'

    @HttpGet('test')
    def test_action(self):
        return {'test': 'test-action'}

    @HttpGet
    def test3(self):
        return {'test': 'test'}
