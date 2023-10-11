class ControllerMeta:
    def __init__(self, controller, name: str, route):
        self.controller = controller
        self.name = name
        self.route = route
        self.handler = self.controller

    # callback handler for the route
    def handler(self):
        return self.controller
