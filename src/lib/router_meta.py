class RouteMeta:
    def __init__(self, controller, action, handler, route):
        self.route = route
        self.handler = handler
        self.controller = controller
        self.action = action
