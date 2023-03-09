from flask.views import View, MethodView
from flask import Blueprint, session

bp = Blueprint('other', __name__, url_prefix='/other')

"""
Class based View
"""
class Hello(View):
    init_every_request = False

    def dispatch_request(self, name):
        return f"Hello, {name}!"

bp.add_url_rule(
    "/hello/<name>", view_func=Hello.as_view("hello")
)

from werkzeug.exceptions import BadRequest

class CounterView(MethodView):
    def get(self):
        session['counter'] = session.get('counter', 0) + 1
        return {"count": session.get('counter', 0)}
    
    def post(self):
        session['counter'] = 0
        return {"count": session.get('counter', 0)}
    
bp.add_url_rule(
    "/counter", view_func=CounterView.as_view("counter")
)