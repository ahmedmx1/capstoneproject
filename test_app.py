import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors


# assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFYeVB6cHFtOTRXNEFkZE1CVUpodyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3AyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWU1M2JjZTkyMmQxMzAwMTkxNjVjYTYiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNTkzMTc1MTI1LCJleHAiOjE1OTMyNjE1MjUsImF6cCI6IjNPUVpuM0JIUHFOTm9IU0ZNc3pRUzFXN3h3TzVSWWRkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Q7f6LhVpFgRKtax382T-b3jezgn1QsajCira-Ohrm0bvwJa68SAqVHtXCoXYSVWY-nCm-bcKJQDbborGQQ7f4nw2p3XwhZ5QJc4xmuRdOWgEp4Q2Kz1Uin0RkGjuodk0f2hLZ2fbhkTmdbUZLt2x8as89Xhe0wA-vzLVuJO5C91bu4HhL4T3cNoKLJHzmb-ptxx8so7WtQHjVCB6_-JvvobMMp23K1EPvQhB_S8xiXQEZ0g-rXDKsvjkGwWYiQMbTjgNwMfDhX5AS8gn61qrLF9cP_4erQVVDQR_9dQLGvqweim97WsKuFFrMYZxxr-e7U65MvbR2OT3Z9CuExgSyw'
# director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFYeVB6cHFtOTRXNEFkZE1CVUpodyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3AyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWU1M2M1ZjkyMmQxMzAwMTkxNjVkNmMiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNTkzMTc1MzM1LCJleHAiOjE1OTMyNjE3MzUsImF6cCI6IjNPUVpuM0JIUHFOTm9IU0ZNc3pRUzFXN3h3TzVSWWRkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.XJ7KTqXzkIEjeYSyzbHPGc9HkMhTxkvPP2xGuY1wifDVzQCzkjPHz1Cct5n6OKbt1SfTFBwaDsinVyvSm0S5Ha7rx5X369Wx0DM8tkgWGTWrrSFFSx6fkIVBKgVBtZj6Q-Z34G4OdIuivgF2pBpsNGlgVUup7hyo7tjuZSNgQWokJaVJa6APU62BWZ7ORBTzx86NmRZF-gccnUP9pp1HeUS1M8C053h5D_wcaFXEmXobUAELB1V92jrdNFRGUohluDbXAKJNGdnuyDIbi6Pd_mk3sZqjIJC2ikxObBf8N_crdfdWDez9zGxz4OstiikDug-_eRBae26-yQAq4X1V8g'
# producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFYeVB6cHFtOTRXNEFkZE1CVUpodyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3AyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWYzZTk0NjZlOGZiYjAwMTM1NWIxNGQiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNTkzMTc1Mzk2LCJleHAiOjE1OTMyNjE3OTYsImF6cCI6IjNPUVpuM0JIUHFOTm9IU0ZNc3pRUzFXN3h3TzVSWWRkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.JpovTtvki7hHeVt7wv0IXHMyp1fNoFDY4Wo13jToB0FKerPNFLM2LPfQq3iW3w4JTL00tC1S7_NrBRHTfgJ677IxYDhm6lUj4vQ0zVzYhu2s0TlL3rchzpjM4dmmIuOzTauABieeyUnZmTT2Rmxp137OCxWOw0pY0aRh_6wsBj-VXNTIkpxMH3ULKdpJytDvxiPuWGQ25hob4cL2Q4ZmVtSd1Qpv4SQPA1hkgwlvzfNpqZdnytZR8_FgxnEg4o_mAVu7B8-9xpLElxaevhcXL2qXz9eu8_6WogkXunKj1Cbwv-H97JT_t8plp6N6sN0z1GnhpGaIo00VNsj_AQU7qw'


# assistant_token = os.environ['assistant_token']
# director_token = os.environ['director_token']
# producer_token = os.environ['producer_token']

class CapstonProjectTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.assistant_token = os.environ['assistant_token']
        self.director_token = os.environ['director_token']
        self.producer_token = os.environ['producer_token']
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
            age=15,
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
        res = self.client().get('/actors', headers={"Authorization": "bearer " + self.assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_getting_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "bearer " + self.assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_getting_actors_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_getting_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_add_new_actor(self):
        newActor = {
            "name": "new actor",
            "age": 15,
            "gender": "male"
        }
        res = self.client().post('/actors', json=newActor, headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_new_movie(self):
        newMovie = {
            "title": "new movie",
            "release_date": "1-1-2020"
        }
        res = self.client().post('/movies', json=newMovie, headers={"Authorization": "bearer " + self.producer_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_new_actor_422(self):
        newActor = {
            "name": "new actor",
            "gender": "male"
        }
        res = self.client().post('/actors', json=newActor, headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)

    def test_add_new_movie_422(self):
        newMovie = {
            "title": "new movie"
        }
        res = self.client().post('/movies', json=newMovie, headers={"Authorization": "bearer " + self.producer_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)

    def test_delete_actor(self):
        newActor = Actors(name="new actor", age=15, gender="male")
        newActor.insert()
        actor_id = newActor.id

        res = self.client().delete(f'/actors/{actor_id}', headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor_id)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie(self):
        newMovie = Movies(title="new movie", release_date="1-1-2020")
        newMovie.insert()
        movie_id = newMovie.id

        res = self.client().delete(f'/movies/{movie_id}', headers={"Authorization": "bearer " + self.producer_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], movie_id)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_404(self):
        res = self.client().delete('/actors/id', headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/id', headers={"Authorization": "bearer " + self.producer_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_update_actor(self):
        newActor = Actors(name="new actor", age=15, gender="male")
        newActor.insert()
        actor_id = newActor.id

        actor_patch = {
            "name": "updated name"
        }

        res = self.client().patch(f'/actors/{actor_id}', json=actor_patch, headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['name'], actor_patch['name'])

    def test_update_movie(self):
        newMovie = Movies(title="new title", release_date="1-1-2020")
        newMovie.insert()
        movie_id = newMovie.id

        movie_patch = {
            "title": "updated title"
        }

        res = self.client().patch(f'/movies/{movie_id}', json=movie_patch, headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], movie_patch['title'])

    def test_update_actor_404(self):
        actor_patch = {
            "name": "updated name"
        }

        res = self.client().patch('/actors/id', json=actor_patch, headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_update_movie_404(self):
        movie_patch = {
            "title": "updated title"
        }

        res = self.client().patch('/movies/id', json=movie_patch, headers={"Authorization": "bearer " + self.director_token})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
