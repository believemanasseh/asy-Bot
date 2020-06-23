from rq import Queue
from worker import conn
from views import ChatterBotApiView

q = Queue(connection=conn)

result = q.enqueue(ChatterBotApiView, 'http://heroku.com')