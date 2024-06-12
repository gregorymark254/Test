from flask import Flask
from flask_migrate import Migrate

import manage
from api.views import blueprint
from extensions import db

app = Flask(__name__)
app.register_blueprint(blueprint=blueprint)
app.config.from_object('config')
app.cli.add_command(manage.user_cli)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
