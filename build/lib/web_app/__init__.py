import os
from flask import Flask
from web_app.db import init_app
import web_app.auth as auth_module
import web_app.blog as blog_module
import web_app.swagger as swagger_module

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

    init_app(app)

    # register the blueprints
    app.register_blueprint(auth_module.bp)
    app.register_blueprint(blog_module.bp)
    # app.register_blueprint(swagger_module.swaggerui_blueprint)
    # app.add_url_rule('/blog/', endpoint='index')

    return app