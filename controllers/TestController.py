from services.test_service import TestService


@ApiController
@ApiRoute('api/[controller]/[action]')
@inject
class TestController:

    def __init__(self, test_service: TestService):
        self._test_service = test_service

    @HttpGet('/test')
    @validate(TestRequest, to="test")
    def test(self,test:TestRuest):
        return self._test_service.test()
