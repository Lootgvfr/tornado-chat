import tornado.ioloop
import tornado.web

from settings import settings
from urls import urls


def main():
    app = tornado.web.Application(urls, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
