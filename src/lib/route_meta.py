class RouteMeta:
    def __init__(self, route, handler, controller, action, methods: []):
        self.route = route
        self.handler = handler
        self.controller = controller
        self.action = action
        self.methods: [] = methods
