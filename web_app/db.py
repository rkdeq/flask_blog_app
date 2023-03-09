import sqlite3
from flask import g, current_app
import click

# g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request.
def get_db():
    """
    Creates a database connection if there is none yet for the
    current application context.
    needs to be set it to g as g always get cleaned up after request and response cycle.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db
        
def close_db(e=None):
    """
    Closes the database connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # below action will be failed because during testing schema.sql file cant be accessible.
    # we created temporary file for testing database
    with current_app.open_resource('schema.sql') as sql_file:
        encoded_sql_query = sql_file.read()
        sql_query = encoded_sql_query.decode('utf8')
        db.executescript(sql_query)
    

@click.command('init_db')
def init_db_from_command_line():
    """
    Initializes the database from the command line
    The Command would be something like this: flask init_db
    """
    init_db()
    click.echo('Initialized database!')


def init_app(app):
    """
    On app startup, this function will be called closed the connection and add new commands to command line line
    """
    app.teardown_appcontext(close_db) # Close db after returning response
    app.cli.add_command(init_db_from_command_line) # Add new command and can be called with flask command line





