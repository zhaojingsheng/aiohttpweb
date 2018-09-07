from aiohttp import web
import aiohttp_jinja2
from aioweb.aiohttpdemo_polls import db
@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app["db"].acquire() as conn:
        cursor=await conn.execute(db.question.select())
        records=await cursor.fetchall()
        questions=[dict(q) for q in records]
        return {"questions":questions}


@aiohttp_jinja2.template("detail.html")
async def poll(request):
    async with request.app["db"].acquire() as conn:
        question_id=request.match_info["question_id"] #获取url中的变量参数
        try:
            question,choices=await db.get_question(conn,question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        # print(question,choices)
        return {"question":question,
                "choices":choices}