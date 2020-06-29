from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db

# database_name = "casting"
# database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', database_name)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()