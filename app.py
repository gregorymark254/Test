from flask import Flask

import manage
from api.views import blueprint
from auth.views import auth_blueprint
from extensions import db, migrate, cors, jwt, cache

app = Flask(__name__)
app.register_blueprint(blueprint=blueprint)
app.register_blueprint(blueprint=auth_blueprint)
app.config.from_object('config')
app.cli.add_command(manage.user_cli)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
cache.init_app(app)
cors.init_app(app, resources={r"/api/*": {
    "origins": ["http://127.0.0.1:5000"]
}})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
