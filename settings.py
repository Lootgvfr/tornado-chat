import os
import uuid

settings = {
    'debug': True,
    'login_url': '/login',
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'xsrf_cookies': True,
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': 'whatever'
}

mongo_db_name = 'tornado-chat'
