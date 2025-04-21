# Hacker News Pipeline

This project provides a FastAPI-based REST API that retrieves and stores the top stories from Hacker News. The API supports JWT authentication and various filters, including pagination, author search, and score filtering. The project is Dockerized and includes Celery for background tasks.

## Features

- **GET /stories**: Paginated list of stories with optional filtering by:
  - Author (`author`)
  - Minimum score (`min_score`)
  - Title search (`search`)
  - Pagination (`page`, `limit`)

- **GET /stories/{story_id}**: Get detailed information for a specific story by its ID.

- **GET /stats/top-authors**: Provides the top 5 authors based on the total score of their stories.

- **JWT Authentication**: Secure API endpoints with JWT tokens.

- **Background Task Processing**: Uses Celery to fetch and store Hacker News stories asynchronously.

## Requirements

- Python 3.9+
- Docker (for running the app in a container)
- Redis (for Celery task queue)
- PostgreSQL (for data storage)

## Installation

Clone this repository:

```bash
git clone https://github.com/ezgiee/hackernews_pipeline.git
cd hackernews_pipeline
```

Create a .env file based on .env.example:
```bash
cp .env.example .env
```

Update the .env file with your specific configuration.

## Running the Application

```bash
docker-compose up --build
```

This will build the Docker images and start the containers for:

- Web app (FastAPI)

- Celery workers

- Celery beat

- Redis

- PostgreSQL

Once the app is running, you can access the API at http://0.0.0.0:8000


## JWT Authentication

To authenticate, you can obtain a JWT token by sending a POST request (form-data) to /token with the following payload:

{
  "username": "admin",
  "password": "admin"
}

You will receive an access_token in the response. This token should be included in the Authorization header of subsequent requests as a Bearer token.

## Endpoints

**GET /stories**

Fetch a paginated list of stories with optional filters:
Query Parameters:

    author (optional): Filter stories by author name.

    min_score (optional): Filter stories by minimum score.

    search (optional): Search for stories by title.

    page (optional): Page number for pagination (default: 1).

    limit (optional): Number of stories per page (default: 20, max: 100).

**GET /stories/{story_id}**

Fetch detailed information about a specific story by its ID.

**GET /stats/top-authors**

Fetch the top 5 authors by the total score of their stories.
Background Task Processing

The project uses Celery to fetch and store Hacker News stories asynchronously. The task is scheduled to run periodically to keep the database up to date. 

## Logging

The application uses Python's built-in logging library to log important events and errors. 
