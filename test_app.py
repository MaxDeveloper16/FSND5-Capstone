import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Performance, db_drop_and_create_all
from config import bearer_tokens, database_config
from sqlalchemy import desc
from datetime import date

# Create dict with Authorization key and Bearer token as values. 
# Later used by test classes as Header

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}

#----------------------------------------------------------------------------#
# Setup of Unittest
#----------------------------------------------------------------------------#

class TestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = app
        self.client = self.app.test_client
        self.database_path = database_config["SQLALCHEMY_DATABASE_URI"]
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

# Test driven development (TDD): Create testcases first, then add endpoints to pass tests

#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#

    def test_get_actors_by_assistant(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)
    
    def test_get_actors_by_director(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_get_actors_by_producer(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)



    def test_error401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#
    def test_get_movies_by_assistant(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)
    
    def test_get_movies_by_director(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies_by_producer(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /actors POST
#----------------------------------------------------------------------------#
    def test_add_actor_by_director(self):
        """Test POST add actor."""

        new_actor = {
            'name' : 'David',
            'gender' : 'Male',
            'age' : 25
        } 

        res = self.client().post('/actors', json = new_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)

    def test_add_actor_by_producer(self):
        """Test POST add actor."""

        new_actor = {
            'name' : 'Lucy',
            'gender' : 'Female',
            'age' : 22
        } 

        res = self.client().post('/actors', json = new_actor, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)

    def test_error401_add_actor_by_assistant(self):
        """Test POST add actor."""

        new_actor = {
            'name' : 'Leo',
            'gender' : 'Male',
            'age' : 22
        } 
        res = self.client().post('/actors', json = new_actor, headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#      
    def test_add_movie_by_producer(self):
        """Test POST add movie."""

        new_movie = {
            'title' : 'Panda',
            'release_date' : '2018-10-01'
        } 

        res = self.client().post('/movies', json = new_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)

    def test_error401_add_movie_by_assistant(self):
        """Test POST add movie."""

        new_movie = {
            'title' : 'Nemo',
            'release_date' : '2010-01-01'
        } 

        res = self.client().post('/movies', json = new_movie, headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /actors/<int:actor_id> PATCH
#----------------------------------------------------------------------------#
    def test_update_actor(self):
        """Test PATCH existing actors"""
        update_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/1', json = update_actor_with_new_age, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error401_update_actor_by_assistant(self):
        """Test PATCH existing actors"""
        update_actor_with_new_age = {
            'age' : 30
        } 

        res = self.client().patch('/actors/1', json = update_actor_with_new_age, headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies/<int:movie_id> PATCH
#----------------------------------------------------------------------------#
    def test_update_movie(self):
        """Test PATCH existing movies"""
        update_actor_with_new_release_date = {
            'release_date' : '2020-10-01'
        } 

        res = self.client().patch('/movies/1', json = update_actor_with_new_release_date, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


    def test_error401_update_movie_by_assistant(self):
        """Test PATCH existing movies"""
        update_actor_with_new_release_date = {
            'release_date' : '2020-10-01'
        } 

        res = self.client().patch('/movies/1', json = update_actor_with_new_release_date, headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /actors/<int:actor_id> DELETE
#----------------------------------------------------------------------------#
    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        res = self.client().delete('/movie/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

#----------------------------------------------------------------------------#
# Tests for /movies/<int:movie_id> DELETE
#----------------------------------------------------------------------------#


if __name__ == "__main__":
    unittest.main()