from src.lib.model import Model


class TestRequest(Model):
    test_key: str
    test_value: str
    _properties = {
        "test_key": {
            "type": str,
            "error": "test_key must be a string"
        },
        "test_value": {
            "type": str,
            "error": "test_value must be a string"
        }
    }
