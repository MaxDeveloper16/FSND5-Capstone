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



if __name__ == "__main__":
    unittest.main()