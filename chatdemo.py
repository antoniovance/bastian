# -*- coding:utf-8 -*-

from dotenv import load_dotenv
from tornado import ioloop
from tornado import web
from tornado.options import define
from tornado.options import options
from pathlib import Path
import os
import redis

from handlers import MainHandler, ChatSocketHandler, MapHandler

# get configurations from dot env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

define('port', default=8888, help="this is given port, bitch", type=int)
define('redis_host', default=os.getenv('REDIS_HOST'), help='this is redis host', type=str)
define('redis_port', default=int(os.getenv('REDIS_PORT')), help='this is redis port', type=int)
define('redis_db', default=int(os.getenv('REDIS_DB')), help='this is redis db', type=int)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
            (r"/map", MapHandler),
        ]

        settings = dict(
            cookie_secret="YOU CANT GUESS MY SECRET",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True
        )

        cache = redis.Redis(host='localhost', port=6379, db=0)

        super(Application, self).__init__(handlers=handlers, **settings)


def main():
    options.parse_command_line()
    app = Application()
    app.listen(options.port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
