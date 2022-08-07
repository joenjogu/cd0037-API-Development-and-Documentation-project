from math import ceil
import sys
import traceback
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app, resources={r'/api/*' : {'origins' : '*'}})

    """
    @DONE: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
             'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
             'GET, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def sample_endpoint():
        return jsonify({'message': 'Hello World'})

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        if not categories:
            abort(404)

        formatted_categories = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and
    pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        max_page = ceil(len(formatted_questions) / QUESTIONS_PER_PAGE)
        if page > max_page:
            abort(404)

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': categories[questions[start].category].type
        })

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/delete_question/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id
                ).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })

        except:
            abort(422)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions/submit', methods=['POST'])
    def post_question():

        try:

            if request.method == 'POST':
                if not request.json:
                    abort(422)
                question = request.json['question'].strip()
                answer = request.json['answer'].strip()
                difficulty = request.json['difficulty']
                category = request.json['category']

                total_categories = len(Category.query.all())
                max_difficulty = 5

                if not (question and answer and difficulty and category):
                    abort(404)

                if category > total_categories:
                    return jsonify({
                        'success': False,
                        'message': 'category does not exist'
                    })

                if difficulty > max_difficulty:
                    return jsonify({
                        'success': False,
                        'message': f'maximum difficulty is {max_difficulty}'
                    })

                question: Question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty
                )

                question.insert()

                return jsonify({
                    'success': True,
                    'question': question.format()
                })
            else:
                abort(405)

        except:
            traceback.print_exc()
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/search', methods=['GET', 'POST'])
    def search_by_term():
        search_term = None
        print(f' search term{search_term}', file=sys.stdout)

        try:
            if request.method == 'POST':
                if not request.json:
                    abort(422)

                search_term = request.json['searchTerm']
                print(f'POST search term{search_term}', file=sys.stdout)
                if search_term:
                    search_results = Question.query.filter(
                        Question.question.ilike(f'%{search_term}%')
                        ).all()
                    print(f'search results {search_results}', file=sys.stdout)
                else:
                    abort(422)

                if search_results:
                    formatted_questions = [question.format() for question in search_results]
                    question_category_id = search_results[0].category
                    current_category = Category.query.filter(
                        Category.id == question_category_id
                        ).first().type

                    return jsonify({
                        'success': True,
                        'questions': formatted_questions,
                        'total_questions': len(formatted_questions),
                        'current_category': current_category
                    })

                else:
                    abort(404)

            else:
                abort(405)

        except:
            abort(404)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        try:
            if not category_id:
                abort(422)
            questions = Question.query.filter(Question.category == category_id).all()

            formatted_questions = [question.format() for question in questions]

            if len(questions) == 0:
                abort(404)

            categories = Category.query.all()

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': categories[category_id].type
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.route('/quiz', methods=['POST'])
    def get_random_quiz():

        try:
            if request.method == 'POST':
                if not request.json:
                    abort(400)

                category_id = request.json['quiz_category']
                previous_questions = request.json['previous_questions']

                if not (category_id or previous_questions):
                    questions = Question.query.all()
                    formatted_questions = [question.format() for question in questions]
                    print(f'category id {category_id}', file=sys.stdout)
                    return jsonify({
                        'success': True,
                        'question': random.choice(formatted_questions)
                    })

                if (not category_id) and previous_questions:
                    previous_questions_ids = []
                    [previous_questions_ids.append(question['id']) for question in previous_questions]

                    db_questions = Question.query.filter(
                        ~Question.id.in_(previous_questions_ids)
                        ).all()
                    print(f'filtered db Qs {db_questions}', file=sys.stdout)

                    formatted_questions = [question.format() for question in db_questions]

                    return jsonify({
                        'success': True,
                        'question': random.choice(formatted_questions)
                    })

                if (not previous_questions) and category_id:
                    db_questions = Question.query.filter(
                        Question.category == category_id
                        ).all()
                    print(f'filtered db Qs {db_questions}', file=sys.stdout)
                    formatted_questions = [question.format() for question in db_questions]

                    return jsonify({
                        'success': True,
                        'question': random.choice(formatted_questions)
                    })

                if category_id and previous_questions:
                    previous_questions_ids = []
                    [previous_questions_ids.append(question['id']) for question in previous_questions]
                    db_questions = Question.query.filter(
                        ~Question.id.in_(previous_questions_ids)
                        & (Question.category == category_id)
                        ).all()
                    print(f'filtered db Qs {db_questions}', file=sys.stdout)

                    formatted_questions = [question.format() for question in db_questions]

                    return jsonify({
                        'success': True,
                        'question': random.choice(formatted_questions)
                    })

            else:
                abort(405)

        except:
            traceback.print_exc()
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def unallowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        })

    return app
