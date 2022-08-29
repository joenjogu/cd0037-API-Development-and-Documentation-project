# TRIVIA API

This API The application supports endpoints to:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Setup

The API can be run on localhost using Flask and Postgres database

## API Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Fetches a paginated array of questions with a maximum of 10 questions per page. The whole dictionary contains an array of categories as well.
- Query Parameters: `page` which can be used to navigate to a specific page of the paginated questions. 
- Returns: an object with keys: `categories` containing an array of `category ids`, `questions` containing an array of question dictionaries, `total_questions` with value as an integer of the total number of questions

```json
{
  "categories": [
    1, 
    2, 
    3, 
    4, 
    5, 
    6
  ], 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true, 
  "total_questions": 16
}
```




