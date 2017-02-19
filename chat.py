import datetime
import tornado.template

from models import Message


class Chat:
    waiting_handlers = dict()
    inc = 0

    def add_handler(self, handler):
        self.inc += 1
        self.waiting_handlers[self.inc] = handler
        return self.inc

    def remove_handler(self, handler_id):
        if handler_id and self.waiting_handlers.get(handler_id):
            del self.waiting_handlers[handler_id]

    def process_message(self, message, user):
        msg = Message(
            dt_sent=datetime.datetime.now(),
            author=user,
            text=message
        )
        msg.save()
        result = {
            'type': 'new_message',
            'content': str(next(iter(self.waiting_handlers.values()))
                           .render_string('message.html', message=msg), 'utf-8')
        }
        for h_id, handler in self.waiting_handlers.items():
            handler.write_message(result)


chat_obj = Chat()
