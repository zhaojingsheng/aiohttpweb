from aioweb.aiohttpdemo_polls.views import index
from aiohttp import web
import pathlib
import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent
# print(PROJECT_ROOT / "static")
def setup_routes(app):
    app.router.add_get("/",index)
    setup_static_routes(app)

def setup_static_routes(app):
    app.router.add_static("/static/",path=PROJECT_ROOT / "static",name="static")