from aioweb.aiohttpdemo_polls.settings import  config
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)
from aiomysql.sa import create_engine
import asyncio

meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default="0", nullable=False),

    Column('question_id',
           Integer,
           ForeignKey('question.id', ondelete='CASCADE'))
)

class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_mysql(app):
    conf=app["config"]["postgres"]
    engine=await create_engine(host=conf['host'],
                            port=conf['port'],
                           user=conf["user"],password=conf["password"],
                           db=conf["database"],
                            minsize=conf["minsize"],
                            maxsize=conf["maxsize"])
    app["db"]=engine  #将连接池添加进共享数据

async def close_mysql(app):
    app["db"].close()
    await app["db"].wait_closed()

async def get_question(conn, question_id):
    result = await conn.execute(
        question.select()
        .where(question.c.id == question_id))
    question_record = await result.first()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await conn.execute(
        choice.select()
        .where(choice.c.question_id == question_id)
        .order_by(choice.c.id))
    choice_records = await result.fetchall()
    return question_record, choice_records


async def vote(conn, question_id, choice_id):
    result = await conn.execute(
        choice.update()
        .returning(*choice.c)
        .where(choice.c.question_id == question_id)
        .where(choice.c.id == choice_id)
        .values(votes=choice.c.votes+1))
    record = await result.fetchone()
    if not record:
        msg = "Question with id: {} or choice id: {} does not exists"
        raise RecordNotFound(msg.format(question_id, choice_id))

if __name__=="__main__":
    async def go():
        conf=config["postgres"]
        # print(conf)
        engine = await create_engine(host=conf['host'],
                                     port=conf['port'],
                                     user=conf["user"], password=conf["password"],
                                     db=conf["database"],
                                     minsize=conf["minsize"],
                                     maxsize=conf["maxsize"])
        async with engine.acquire() as conn:
            result = await conn.execute(
                question.select()
                    .where(question.c.id == 0))
            print(await result.first())
    loop=asyncio.get_event_loop()
    # task=asyncio.ensure_future(go())
    loop.run_until_complete(go())

    loop.close()