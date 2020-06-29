from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db

# database_name = "casting"
# database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', database_name)



database_path = 'postgres://yqgtcgyqeopzwh:6c0bf32519debf3f20cbcf9d29017316f6d8fadbde58721a0b462b2b9f629925@ec2-34-206-31-217.compute-1.amazonaws.com:5432/d77bn7d6q8g0le'


app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
