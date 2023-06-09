class Model:
    _properties = {}

    def __init__(self, **kwargs):
        self._errors = {}
        for prop, attr in self._properties.items():
            value = kwargs.get(prop)
            if not isinstance(value, attr["type"]):
                self._errors[prop] = attr["error"]
            else:
                setattr(self, prop, value)

    def is_valid(self):
        return len(self._errors) == 0

    @property
    def errors(self):
        return self._errors
