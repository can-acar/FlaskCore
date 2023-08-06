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

    def add_controller(self, meta: ControllerMeta):
        self.controllers.append(meta)

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

                                controller = None
                                base_controller = None
                                is_controller = False
                                for name, obj in inspect.getmembers(module):
                                    # if object has @ApiRoute decorator

                                    # is not a subclass of ControllerBase

                                    if inspect.isclass(obj) and issubclass(obj, ControllerBase) and obj == ControllerBase:
                                        # is subclass of ControllerBase get subclass instance
                                        base_controller = inject_dependencies(obj.__init__, self.container)

                                    if inspect.isclass(obj) and issubclass(obj, ControllerBase) and obj != ControllerBase and not inspect.isabstract(obj):
                                        controller = inject_dependencies(obj, self.container)
                                        controller.base_controller = base_controller
                                        controller.api_route_template = obj.api_route_template
                                        controller.name = name
                                        is_controller = True
                                        break

                                if is_controller:
                                    self.controllers.append(ControllerMeta(controller, controller.name, controller.route, controller.api_route_template, base_controller))
