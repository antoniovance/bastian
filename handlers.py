# -*- coding:utf-8 -*-
from datetime import datetime
from tornado import escape
from tornado import web
from tornado import websocket
import json
import redis
import uuid
import logging


class ChatRoom(object):
    chat_room_key = 'CHATROOM'

    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, db=0)

    def get_chat_room_messages(self):
        if self.cache.exists(self.chat_room_key) != 0:
            return [json.loads(str(x, encoding='utf-8')) for x in self.cache.lrange(name=self.chat_room_key, start=0, end=300)]
        return []

    def update_chat_room_messages(self, chat):
        self.cache.lpush(self.chat_room_key, json.dumps(chat))

        if self.cache.llen(self.chat_room_key) > 300:
            self.cache.ltrim(self.chat_room_key, start=0, end=299)


class MainHandler(web.RequestHandler):

    def get(self):
        self.render(
            "index.html",
            messages=ChatRoom().get_chat_room_messages(),
            username='游客%d' % ChatSocketHandler.client_id)


class ChatSocketHandler(websocket.WebSocketHandler):
    waiters = set()     #保存所有在线Websocket连接
    client_id = 1

    def open(self, *args: str, **kwargs: str):
        self.client_id = ChatSocketHandler.client_id
        ChatSocketHandler.client_id = ChatSocketHandler.client_id + 1
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = escape.json_decode(message)
        chat = {
            'id': str(uuid.uuid4()),
            'body': parsed.get('body', ''),
            'type': "message",

            "client_id": self.client_id,
            "username": parsed['username'],
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        chat['html'] = escape.to_basestring(
            self.render_string("message.html", message=chat)
        )
        ChatRoom().update_chat_room_messages(chat=chat)
        ChatSocketHandler.send_updates(chat=chat)

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except Exception as e:
                logging.error("Error sending message", exec_info=True)

class MapHandler(web.RequestHandler):
    def get(self):

        header = {
            'Homepage': {},
            'Activity': {
                'subs': {
                    'eating': {},
                    'walking': {},
                    'party': {}
                }
            },
            'AboutUs': {},
        }

        self.render(
            "map.html",
            header=header
        )
