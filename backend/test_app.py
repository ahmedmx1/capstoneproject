import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors

class CapstonProjectTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting"
        self.database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = Actors(
            name="new actor",
            age="15",
            gender="male"
        )

        self.new_movie = Movies(
            title="new movie",
            release_date="1-1-2020"
        )
    
    def tearDown(self):
        # Executed after reach test
        pass
    
    def test_getting_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_getting_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_add_new_actor(self):
        newActor = {
            "name":"new actor",
            "age":"15",
            "gender":"male"
        }
        res = self.client().post('/actors', json=newActor)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    
    def test_add_new_movie(self):
        newMovie = {
            "title": "new movie",
            "release_date": "1-1-2020"
        }
        res = self.client().post('/movies', json=newMovie)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    
    def test_add_new_actor_422(self):
        newActor = {
            "name":"new actor",
            "gender":"male"
        }
        res = self.client().post('/actors', json=newActor)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)
    
    def test_add_new_movie_422(self):
        newMovie = {
            "title": "new movie"
        }
        res = self.client().post('/movies', json=newMovie)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)
    
    def test_delete_actor():
        newActor = Actors(name="new actor", age="15", gender="male")
        newActor.insert()
        actor_id = newActor.id

        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success', True])
        self.assertEqual(data['actor'], actor_id)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie():
        newMovie = Movies(title="new movie", release_date="1-1-2020")
        newMovie.insert()
        movie_id = newMovie.id

        res = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success', True])
        self.assertEqual(data['movie'], movie_id)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
