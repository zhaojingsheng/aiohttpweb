from aioweb.aiohttpdemo_polls.views import index,poll
from aiohttp import web
import pathlib
import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent
# print(PROJECT_ROOT / "static")
def setup_routes(app):
    app.router.add_get("/",index)
    app.router.add_get("/poll/{question_id}",poll)  #使用url变量参数传递
    setup_static_routes(app)

def setup_static_routes(app):
    app.router.add_static("/static/",path=PROJECT_ROOT / "static",name="static")