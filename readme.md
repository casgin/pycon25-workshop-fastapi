# Message Application

A FastAPI-based RESTful API for managing messages with image upload capabilities.

## Features

- CRUD operations for messages
- Image upload functionality
- SQLAlchemy ORM for database operations
- Alembic for database migrations
- FastAPI automatic documentation (Swagger UI and ReDoc)

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd message-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/api/v1/docs
- ReDoc Documentation: http://localhost:8000/api/v1/redoc

## API Endpoints

### Root Endpoint

#### GET /
- Description: Check if the application is running
- Response:
```json
{
    "application": "Is running"
}
```

### Messages

#### GET /messages
- Description: Retrieve all non-deleted messages
- Response: List of messages
```json
[
    {
        "id": 1,
        "title": "Message Title",
        "category": "Category",
        "text": "Message content",
        "image": "optional/image/path.jpg",
        "created_at": "2024-03-21T10:00:00",
        "updated_at": "2024-03-21T10:00:00",
        "deleted_at": null
    }
]
```

#### POST /messages
- Description: Create a new message
- Request Body:
```json
{
    "title": "Message Title",
    "category": "Category",
    "text": "Message content"
}
```
- Response: Created message object

#### PUT /message/{message_id}
- Description: Update an existing message
- Parameters:
  - message_id: Integer
- Request Body:
```json
{
    "title": "Updated Title",
    "category": "Updated Category",
    "text": "Updated content"
}
```
- Response: Updated message object

#### DELETE /message/{message_id}
- Description: Soft-delete a message
- Parameters:
  - message_id: Integer
- Response Status: 204 No Content

#### POST /message/upload/{message_id}
- Description: Upload an image for a specific message
- Parameters:
  - message_id: Integer
- Request Body:
  - file: Image file (multipart/form-data)
- Response: Updated message object with image path

## Data Models

### Message
- id: Integer (Primary Key)
- title: String
- category: String
- text: String
- image: String (Optional)
- created_at: DateTime
- updated_at: DateTime
- deleted_at: DateTime (Optional)

## Error Handling

The API uses standard HTTP status codes:
- 200: Successful operation
- 201: Resource created
- 204: No content (successful deletion)
- 400: Bad request
- 404: Resource not found
- 500: Internal server error

## Development

The project uses:
- FastAPI for the web framework
- SQLAlchemy for ORM
- Alembic for database migrations
- Pydantic for data validation

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Launch project

```bash
 uvicorn main:app --host=127.0.0.1 --port=8090 --reload
```