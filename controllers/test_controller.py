from models.test_request import TestRequest
from services.test_service import TestService
from src.lib.api_controller import ApiController
from src.lib.api_route import ApiRoute
from src.lib.controller_base import ControllerBase
from src.lib.http_methods import HttpGet
from src.lib.validate import validate


@ApiController
@ApiRoute('api/[controller]/[action]')
class TestController(ControllerBase):

    def __init__(self, test_service: TestService):
        self._test_service = test_service

    @HttpGet('/test/{test_key}-{test_value}')
    @validate(TestRequest, to="test")
    def test(self, test: TestRequest):
        return self._test_service.test(test)

    @HttpGet('/test2/{test_key}-{test_value}')
    @validate(TestRequest, to="test")
    def test2(self, test: TestRequest):
        return self._test_service.test(test)
