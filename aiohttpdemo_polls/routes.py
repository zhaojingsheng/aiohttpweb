from aiohttpdemo_polls.views import index,poll,results,vote
from aiohttp import web
import pathlib
import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent
# print(PROJECT_ROOT / "static")
def setup_routes(app):
    app.router.add_get("/",index)
    app.router.add_get("/poll/{question_id}",poll,name="poll")  #使用url变量参数传递
    app.router.add_get("/poll/{question_id}/results", results, name="results")
    app.router.add_get("/poll/{question_id}/vote", vote,name="vote")
    setup_static_routes(app)

def setup_static_routes(app):
    app.router.add_static("/static/",path=PROJECT_ROOT / "static",name="static")