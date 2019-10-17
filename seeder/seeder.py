from sqlalchemy import create_engine, Column, Sequence, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO
from flask import Flask
import time
import datetime
import os

conf = Config()
database_string = f'postgresql://{os.environ.get("DATABASE_USER")}:{os.environ.get("DATABASE_PASS")}@{os.environ.get("HOST")}:5432/{os.environ.get("DATABASE")}'
db = create_engine(database_string)
base = declarative_base()

app = Flask(__name__)
socketio = SocketIO(app)


def connect():
    try:
        session = sessionmaker(bind=db)
        ses = session()
        base.metadata.create_all(db)
        return ses
    except Exception as e:
        print(e)


class Ticks(base):
    __tablename__ = 'ticks'

    id_entry = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, createad_at):
        self.created_at = createad_at


def insert_to_table():
    now = datetime.datetime.utcnow()
    entry = Ticks(createad_at=now.strftime('%Y-%m-%d %H:%M:%S'))
    session = connect()
    session.add(entry)
    session.commit()
    session.close()


sched = BackgroundScheduler(daemon=True)
sched.add_job(insert_to_table, trigger='cron', second='*')
sched.start()


# def scheduler():
#     job = sched.add_job(insert_to_table, trigger='cron', second='*')
#     while True:
#         time.sleep(1)
#     # schedule.every(1).seconds.do(insert_to_table)
#     # while True:
#     #     schedule.run_pending()
#     #     time.sleep(1)


if __name__ == '__main__':
    socketio.run(app, debug=True)


