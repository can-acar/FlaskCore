import importlib
import inspect
import os
from typing import List

from typing import TypeVar

from flask import Flask

from src.lib.container import Container
from src.lib.controller_base import ControllerBase
from src.lib.inject import inject
from src.lib.inject_dependencies import inject_dependencies

T = TypeVar('T')


class ControllerEntry:
    def __init__(self, controller, name: str):
        self.controller = controller
        self.name = name


@inject
class ControllerFactory:
    def __init__(self, app: Flask, container: Container):
        self.app = app
        self.controllers: List[ControllerEntry] = []
        self.container = container  # type: Container

    def use_controller(self):

        self._gather_controllers()

        # for name, controller in self.controllers.items():
        # controller = self.container.resolve(controller)
        # self.app.add_url_rule(controller.route, view_func=controller.dispatch_request, methods=controller.methods)

    def _gather_controllers(self):

        dir_path = self.app.root_path
        # get all 'controllers' folders in the project
        for root, dirs, files in os.walk(dir_path):
            for dir in dirs:
                if dir == 'controllers':
                    # get all files in the controllers folder
                    for root, dirs, files in os.walk(os.path.join(root, dir)):
                        for file in files:
                            if file.endswith('.py') and file != '__init__.py':
                                module_name = file[:-3]  # Strip the .py at the end
                                # import the file
                                module = importlib.import_module(f'controllers.{module_name}')

                                # module = __import__(f'{root}.{file[:-3]}', fromlist=[f'{file[:-3]}'])
                                # inspect all classes in the file and find all controllers
                                for name, obj in inspect.getmembers(module):
                                    # if object has @ApiRoute decorator

                                    if inspect.isclass(obj) and issubclass(obj, ControllerBase):
                                        if hasattr(obj, 'is_api_controller') and obj.is_api_controller:
                                            # create an instance of the controller and inject dependencies

                                            obj.__init__ = inject_dependencies(obj.__init__, self.container)
                                            self.controllers.append(ControllerEntry(obj, name))
