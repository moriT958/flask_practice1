from flask import Flask

import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'data.sqlite'),
        SECRET_KEY='development'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import todo
    app.register_blueprint(todo.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/hello')
    def hello():
        return "<h1>Hello, World!</h1>"
    
    return app