import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

database_name = "casting"
database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', database_name)
# postgres://cpkiytpbuggisp:a8f2fcdd4388380ae7a6d6b2cf7f8dd4450218f5c9d50ae349f784a2c8d00c88@ec2-54-234-28-165.compute-1.amazonaws.com:5432/d8s7jscd01cvvq
# database_path = "postgres://cpkiytpbuggisp:a8f2fcdd4388380ae7a6d6b2cf7f8dd4450218f5c9d50ae349f784a2c8d00c88@ec2-54-234-28-165.compute-1.amazonaws.com:5432/d8s7jscd01cvvq"

# database_path = os.environ['DATABASE_URL']


db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

class Movies(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(String(80), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
        }
    
    def __repr__(self):
        return json.dumps(self)


class Actors(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(80), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }
    
    def __repr__(self):
        return f'<Actors {self.id} {self.name}>'

