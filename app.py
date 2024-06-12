from flask import Flask


import manage
from api.views import blueprint
from extensions import db, migrate, cors

app = Flask(__name__)
app.register_blueprint(blueprint=blueprint)
app.config.from_object('config')
app.cli.add_command(manage.user_cli)

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app, resources={r"/api/*": {
    "origins": ["http://127.0.0.1:5000"]
}})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
