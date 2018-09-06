from sqlalchemy import create_engine, MetaData

from aioweb.aiohttpdemo_polls.settings import config
from aioweb.aiohttpdemo_polls.db import question, choice


DSN = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(question.insert(), [
        {"id":0, 'question_text': 'What\'s new?',
         'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.execute(choice.insert(), [
        {"id":1,'choice_text': 'Not much', 'votes': 0, 'question_id':0},
        {"id":2,'choice_text': 'The sky', 'votes': 0, 'question_id': 0},
        {"id":3,'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 0},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    # print(db_url)
    engine = create_engine(db_url)
    #
    create_tables(engine)
    sample_data(engine)