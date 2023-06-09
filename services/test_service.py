class TestService:

    def __init__(self):
        pass

    def test(self, test):
        return {'message': 'Ok!',
                'data': {
                    'test_key': test.test_key,
                    'test_value': test.test_value

                }}
