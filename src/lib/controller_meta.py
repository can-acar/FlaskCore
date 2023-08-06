class ControllerMeta:
    def __init__(self, controller, name: str, base_controller=None):  # route: str,
        self.controller = controller
        self.name = name
        # self.route = route
        self.base_controller = base_controller

    # callback handler for the route
    def handler(self, controller):
        return self.controller(controller)

    # def handler(self, controller, action):
    #     return getattr(controller, action)()
