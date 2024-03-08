import sqlite3

from flask import g, current_app

import click


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', default=None)
    if db is not None:
        db.close()


@click.command('init-db')
def init_db():
    with current_app.app_context():
        con = get_db()
        cur = con.cursor()
        query = current_app.open_resource('schema.sql').read().decode('utf8')
        cur.executescript(query)
    click.echo('Initialized the Database!')

def init_app(app):
    app.cli.add_command(init_db)
    app.teardown_appcontext(close_db)