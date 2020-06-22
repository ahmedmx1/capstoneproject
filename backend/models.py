import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

database_name = "casting"
database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', database_name)


db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movies(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(80))
    release_date = Column(String(80))

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
    name = db.Column(db.String(80))
    age = db.Column(db.String(80))
    gender = db.Column(db.String(80))

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



# class Movies(db.Model):
#     # Autoincrementing, unique primary key
#     id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
#     # String Title
#     title = Column(String(80), unique=True)
#     # the ingredients blob - this stores a lazy json blob
#     # the required datatype is [{'color': string, 'name':string, 'parts':number}]
#     release_date =  Column(String(180), nullable=False)

#     '''
#     insert()
#         inserts a new model into a database
#         the model must have a unique name
#         the model must have a unique id or null id
#         EXAMPLE
#             drink = Drink(title=req_title, recipe=req_recipe)
#             drink.insert()
#     '''
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     '''
#     delete()
#         deletes a new model into a database
#         the model must exist in the database
#         EXAMPLE
#             drink = Drink(title=req_title, recipe=req_recipe)
#             drink.delete()
#     '''
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     '''
#     update()
#         updates a new model into a database
#         the model must exist in the database
#         EXAMPLE
#             drink = Drink.query.filter(Drink.id == id).one_or_none()
#             drink.title = 'Black Coffee'
#             drink.update()
#     '''
#     def update(self):
#         db.session.commit()

#     def __repr__(self):
#         return json.dumps(self.short())

# class Actors(db.Model):
#     # Autoincrementing, unique primary key
#     id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
#     # String Title
#     name = Column(String(80), unique=True)
#     # the ingredients blob - this stores a lazy json blob
#     # the required datatype is [{'color': string, 'name':string, 'parts':number}]
#     age =  Column(String(180), nullable=False)

#     '''
#     insert()
#         inserts a new model into a database
#         the model must have a unique name
#         the model must have a unique id or null id
#         EXAMPLE
#             drink = Drink(title=req_title, recipe=req_recipe)
#             drink.insert()
#     '''
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     '''
#     delete()
#         deletes a new model into a database
#         the model must exist in the database
#         EXAMPLE
#             drink = Drink(title=req_title, recipe=req_recipe)
#             drink.delete()
#     '''
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     '''
#     update()
#         updates a new model into a database
#         the model must exist in the database
#         EXAMPLE
#             drink = Drink.query.filter(Drink.id == id).one_or_none()
#             drink.title = 'Black Coffee'
#             drink.update()
#     '''
#     def update(self):
#         db.session.commit()

#     def __repr__(self):
#         return json.dumps(self.short())