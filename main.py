import tornado.ioloop
import tornado.web
import mongoengine

from settings import *
from urls import urls


def main():
    mongoengine.connect(mongo_db_name)

    app = tornado.web.Application(urls, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
