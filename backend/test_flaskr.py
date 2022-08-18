import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('postgres:bugatti430','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_sample_endpoint(self):
        """Test the sample endpoint returns a 200 for a GET request"""
        response = self.client().get('/')

        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        """Test GET request for fetching all categories"""
        response = self.client().get('/categories')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_405_for_POST_to_get_categories(self):
        """Test GET request for fetching all categories"""
        response = self.client().post('/categories')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # def test_get_questions(self):
    #     """Test GET request for fetching all questions"""
    #     response = self.client().get('/questions')

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    #     self.assertTrue(data['current_category'])


    def test_delete_question(self):
        """Test DELETE request for question with id"""
        response = self.client().delete('/delete_question/8')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_404_when_delete_question_id_nonexistent(self):
        """Test DELETE request for question with non-existent id"""
        response = self.client().delete('/delete_question/50000000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        # self.assertTrue(data['deleted'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()