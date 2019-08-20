# -*- coding:utf-8 -*-

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base

# using the query string is equivalent
engine = create_engine("postgresql://user:pass@host/dbname?client_encoding=utf8")

base = declarative_base()


class User(base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(Enum('s', 'l', 'g', 'b', 't', 'q', 'i', name='gender'))
    sex = Column(Enum('f', 'm', name='sex'))


class ChatRoom(base):
    __tablename__ = 'chat_room'

    id = Column(Integer, primary_key=True)
    administer = Column(ForeignKey('User.id'))
    members = Column()
    created = Column(DateTime, default=datetime.now())

class ChatRoomMessage(base):
    __table__ = "chat_room_message"

    user_id = Column(ForeignKey('User.id'))
    chat_room_id = Column(ForeignKey('ChatRoom.id'))
    text = Column(Text, nullable=True)
    created = Column(DateTime, default=datetime.now())

