from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db = SQLAlchemy()
app_globals = {}

mail = Mail()

def get_app():
    if app_globals.get('app', False):
        app= app_globals['app']
    else :
        app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)

    mail.init_app(app)


    from app.login.routes import routes
    app.register_blueprint(routes, url_prefix='/auth')

    from app.pq.routes import routes
    app.register_blueprint(routes, url_prefix='/pq')
    from app.routesindex import routes
    app.register_blueprint(routes, url_prefix='/')

    app_globals['app'] = app
    return app


if __name__ == '__main__':
    get_app().run(host= '192.168.10.159', debug=True)
