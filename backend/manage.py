from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db

database_name = "casting"
database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', database_name)


app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()