import os
from flask import Flask, session
from web_app.db import init_app
import web_app.auth as auth_module
import web_app.blog as blog_module
import web_app.other as other_module


"""
    web_app-1.0.0-py3-none-any.whl
    You can install this project using pip command like this:
    pip install web_app-1.0.0-py3-none-any.whl
    but before this set virtual environment so our package can download dependencies like flask, etc
"""
# Application Factory Pattern
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'web_app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def default_page():
        return 'Hello, This project is working!'




    """
    Flask Signals
    """

    from flask.signals import got_request_exception
    from werkzeug.exceptions import HTTPException
    @app.before_request
    def print_error():
        print("Signal for before request")
    
    # Todo: check why below codes is not working
    def print_exception_error(sender, exception):
        print("Sending error notification to dev team")
    got_request_exception.connect(print_exception_error, app)

    """
    Register Error Handling
    We can render html error page for the specific error or exceptions
    """
    from flask import render_template

    # @app.errorhandler(500)
    # def page_not_found(e):
    #     # note that we set the 404 status explici
    #     return render_template('error.html'), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        if isinstance(e, HTTPException):
            return e
        return render_template('error.html'), 500
    


    init_app(app)

    # register the blueprints
    app.register_blueprint(auth_module.bp)
    app.register_blueprint(blog_module.bp)
    app.register_blueprint(other_module.bp)

    return app