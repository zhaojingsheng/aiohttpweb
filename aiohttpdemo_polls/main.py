from aiohttp import web
import aiomysql

import aiohttp_jinja2
import jinja2
import pathlib
import yaml
import os

from aiohttpdemo_polls import routes
from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.db import init_mysql,close_mysql
from aiohttpdemo_polls.middlewares import setup_middlewares

tmp_path=os.path.split(__file__)[0]+"/templates"


app=web.Application()
routes.setup_routes(app)
app["config"]=config  #将配置添加进共享数据
# setup_middlewares(app)
aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader(tmp_path))
app.on_startup.append(init_mysql)
app.on_cleanup.append(close_mysql)
web.run_app(app)