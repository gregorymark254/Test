import click
from flask.cli import with_appcontext, AppGroup
from extensions import db
from models.users import User

user_cli = AppGroup('user', help='Manage users')


@user_cli.command('create')
@click.argument("name")
@click.argument("email")
@click.argument("age")
@with_appcontext
def create_user(name: str, email: str, age: int):
    user = User(name=name, email=email, age=age)
    db.session.add(user)
    db.session.commit()
    click.echo(f'User {name} created')
