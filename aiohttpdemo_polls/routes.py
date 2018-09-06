from aioweb.aiohttpdemo_polls.views import index,poll
from aiohttp import web
import pathlib
import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent
# print(PROJECT_ROOT / "static")
def setup_routes(app):
    app.router.add_get("/",index)
def pool_routes(app):
    app.router.add_get("/pool",poll)
def setup_static_routes(app):
    app.router.add_static("/static/",path=PROJECT_ROOT / "static",name="static")