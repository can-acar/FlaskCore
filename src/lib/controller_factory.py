import importlib
import inspect
import os
from typing import List

from typing import TypeVar

from flask import Flask

from src.lib.container import Container
from src.lib.controller_base import ControllerBase
from src.lib.controller_meta import ControllerMeta
from src.lib.inject import inject
from src.lib.inject_dependencies import inject_dependencies

T = TypeVar('T')


@inject
class ControllerFactory:
    def __init__(self, app: Flask, container: Container):
        self.app = app
        self.controllers: List[ControllerMeta] = []
        self.container = container  # type: Container

    def use_controller(self):
        self._gather_controllers()

    def _gather_controllers(self):
        controller_info = {}
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
                                # inspect all classes in the file and find all controllers
                                for name, obj in inspect.getmembers(module):
                                    if inspect.isclass(obj) and issubclass(obj, ControllerBase):
                                        if hasattr(obj, 'is_api_controller') and obj.is_api_controller:
                                            if hasattr(obj, 'api_route_template') and obj.api_route_template:
                                                controller = inject_dependencies(obj.__init__, self.container)

                                                self.controllers.append(
                                                    ControllerMeta(controller, name, obj.api_route_template))
                                                break
