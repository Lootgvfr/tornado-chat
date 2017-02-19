from tornado.web import url

from handlers import HomeHandler, RegistrationHandler, LoginHandler,\
    LogoutHandler, ChatHandler

urls = [
    url(r'/$', HomeHandler, name='home'),
    url(r'/login$', LoginHandler, name='login'),
    url(r'/logout$', LogoutHandler, name='logout'),
    url(r'/registration$', RegistrationHandler, name='registration'),
    url(r'/chat$', ChatHandler, name='chat'),
]
