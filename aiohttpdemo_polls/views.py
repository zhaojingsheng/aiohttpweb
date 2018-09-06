from aiohttp import web
import aiohttp_jinja2
from aioweb.aiohttpdemo_polls import db
async def index(request):
    return web.Response(text="hello world")


@aiohttp_jinja2.template("detail.html")
async def poll(request):
    async with request.app["db"].acquire() as conn:
        question_id=request.match_info["question_id"]
        try:
            question,choices=await db.get_question(conn,question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            "question":question,
            "choices":choices
        }