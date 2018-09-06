from aiohttp import web
import aiomysql
from aioweb.aiohttpdemo_polls import routes
from aioweb.aiohttpdemo_polls.settings import config
import aiohttp_jinja2
import jinja2
from aioweb.aiohttpdemo_polls.db import init_mysql,close_mysql
from aioweb.aiohttpdemo_polls.middlewares import setup_middlewares
import pathlib
import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent
app=web.Application()
routes.setup_routes(app)
app["config"]=config
setup_middlewares(app)
routes.pool_routes(app)
aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader( r".\templates"))
app.on_startup.append(init_mysql)
app.on_cleanup.append(close_mysql)
web.run_app(app)