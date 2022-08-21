import os
import sys
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

    def test_get_questions(self):
        """Test GET request for fetching all questions"""
        response = self.client().get('/questions?page=1')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        # self.assertTrue(data['current_category'])

    # def test_delete_question(self):
    #     """Test DELETE request for question with id"""
    #     response = self.client().delete('/delete_question/12')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])

    def test_404_when_delete_question_id_nonexistent(self):
        """Test DELETE request for question with non-existent id"""
        response = self.client().delete('/delete_question/50000000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_submit_question(self):
        """Test POST request to submit a new question"""
        response = self.client().post('/questions/submit', json={
            'question': 'What species are orangutan?',
            'answer': 'Homo Trumpes',
            'difficulty': 2,
            'category': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_405_when_submit_question(self):
        """Test GET request to submit a new question endpoint returns 405"""
        response = self.client().get('/questions/submit', json={
            'question': 'What species are orangutan?',
            'answer': 'Homo Trumpes',
            'difficulty': 2,
            'category': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search(self):
        """Test search by term endpoint"""
        response = self.client().post('/search', json={'searchTerm': 'orangutan'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_for_search_term_not_found(self):
        """Test no results for search term returns 404"""
        response = self.client().post('/search', json={'searchTerm': 'rebbeberb'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self):
        """Test get questions in specific category"""
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_get_random_quiz(self):
        """Test get random quiz POST endpoint"""
        response = self.client().post('/quiz', json= {
            'quiz_category': {'id': ''},
            'previous_questions': [3, 6, 8, 10]
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_random_quiz_with_no_payload_returns_422(self):
        """Test a 422 response for no payload"""
        response = self.client().post('/quiz')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()