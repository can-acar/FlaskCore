import asyncio

from flask import Flask

from modules.api_module import ApiModule
from src.lib.container_builder import ContainerBuilder
from src.lib.flask_core import FlaskCore


async def start_flask_app(port):
    builder = ContainerBuilder()
    app = Flask(__name__)
    flask_core = FlaskCore(app, builder)
    builder.register_module(ApiModule())
    flask_core.useCoreService()

    flask_core.useApp(lambda builder: builder)

    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == '__main__':
    asyncio.run(start_flask_app(8082))
