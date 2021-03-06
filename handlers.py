import tornado.web
import tornado.websocket

from models import User, Message
from helpers import encode_password, check_password
from settings import host
from chat import chat_obj


class CurrentUserMixin:
    def get_current_user(self):
        cookie = self.get_secure_cookie('auth')
        try:
            username = str(cookie, 'utf-8')
            return User.objects(username=username)[0]
        except (IndexError, TypeError) as e:
            return None


class BaseHandler(CurrentUserMixin, tornado.web.RequestHandler):
    pass


class BaseWebsocketHandler(CurrentUserMixin, tornado.websocket.WebSocketHandler):
    pass


class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html',
                    socket_url='ws://{0}{1}'.format(host, self.reverse_url('chat')))


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('auth', '')
        self.redirect(self.reverse_url('home'))


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        try:
            user = User.objects(username=username)[0]
            if not check_password(user, password):
                raise ValueError()
            self.set_secure_cookie('auth', username)

            result = {
                'type': 'redirect',
                'redirect_url': self.reverse_url('home')
            }

        except Exception as e:
            result = {
                'type': 'error',
                'message': 'Invalid credentials'
            }
        self.write(result)


class RegistrationHandler(BaseHandler):
    def get(self):
        self.render('registration.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        repeat_password = self.get_argument('repeat-password')
        try:
            if not password == repeat_password:
                raise ValueError('Passwords do not match')

            if User.objects(username=username) or User.objects(email=email):
                raise ValueError('User with given username or email already exists')

            p = encode_password(password)
            User(username=username, email=email, password=p).save()
            self.set_secure_cookie('auth', username)

            result = {
                'type': 'redirect',
                'redirect_url': self.reverse_url('login')
            }

        except Exception as e:
            result = {
                'type': 'error',
                'message': str(e)
            }
        self.write(result)


class ChatHandler(BaseWebsocketHandler):
    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        self.id = None

    def open(self):
        if self.current_user:
            print(self.current_user.username + ' connected')
        self.id = chat_obj.add_handler(self)
        messages = Message.objects.order_by('-dt_sent')[:10]
        html_messages = [
            str(self.render_string('message.html', message=msg), 'utf-8') for msg in messages
        ]
        result = {
            'type': 'open',
            'content': ''.join(html_messages)
        }
        self.write_message(result)

    def on_message(self, message):
        if self.current_user:
            if not 1 <= len(message) <= 500:
                self.write_message({'type': 'error', 'message': 'Message must be 1 to 500 characters long'})
            else:
                self.write_message({'type': 'response'})
                chat_obj.process_message(message, self.current_user)

    def on_close(self):
        if self.current_user:
            print('rip ' + self.current_user.username)
        chat_obj.remove_handler(self.id)
