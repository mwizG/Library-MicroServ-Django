Library Microservice System
Welcome to the Library Microservice System! This project is designed to manage a library system using microservices architecture implemented in Python and Django. The system includes user authentication, book management, loan management, and an API gateway.

Table of Contents
Overview
Microservices
Technologies Used
Installation
Usage
Endpoints
Testing
Contributing
License
Overview
The Library Microservice System is a distributed system that separates the functionalities of user management, book management, and loan processing into distinct microservices. Each microservice has its own database and communicates with others through REST APIs. An API gateway serves as the entry point for all client requests, routing them to the appropriate microservice.

Microservices
User Microservice

Manages user registration, authentication, and profile management.
Handles token generation for authenticated sessions.
Books Microservice

Manages book catalog, including adding, updating, viewing, and deleting books.
Provides endpoints for searching and retrieving book details.
Loans Microservice

Manages borrowing and returning of books.
Tracks loan status and history.
API Gateway

Serves as the entry point for all client requests.
Routes requests to the appropriate microservice based on the endpoint.
Handles authentication and token validation.
Technologies Used
Python
Django & Django REST Framework
PostgreSQL
Docker
Nginx
JWT (JSON Web Tokens) for authentication
Gunicorn as WSGI HTTP Server
Installation
Prerequisites
Python 3.8+
Docker & Docker Compose
Steps
Clone the Repository

bash
Copy code
git clone https://github.com/your-username/library-microservice-system.git
cd library-microservice-system
Environment Setup

Create a .env file in the root directory and add the necessary environment variables:
bash
Copy code
DEBUG=True
SECRET_KEY=your_secret_key
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
Build and Run with Docker

bash
Copy code
docker-compose up --build
Apply Migrations

bash
Copy code
docker-compose exec usersms python manage.py migrate
docker-compose exec booksmicroservice python manage.py migrate
docker-compose exec loansmicroservice python manage.py migrate
Usage
Accessing the Services
API Gateway: http://localhost:8000
User Microservice: http://localhost:8001
Books Microservice: http://localhost:8002
Loans Microservice: http://localhost:8003
Example Requests
Register a new user:

http
Copy code
POST /api/users/register/
{
  "username": "exampleuser",
  "password": "password123",
  "email": "user@example.com"
}
Login:

http
Copy code
POST /api/users/login/
{
  "username": "exampleuser",
  "password": "password123"
}
Add a new book:

http
Copy code
POST /api/books/
{
  "title": "Example Book",
  "author": "John Doe",
  "isbn": "1234567890123"
}
Borrow a book:

http
Copy code
POST /api/loans/borrow/
{
  "user_id": 1,
  "book_id": 2,
  "borrow_date": "2024-07-01",
  "return_date": "2024-07-15"
}
Endpoints
User Microservice
POST /api/users/register/
POST /api/users/login/
GET /api/users/profile/
Books Microservice
GET /api/books/
POST /api/books/
GET /api/books/<id>/
PUT /api/books/<id>/
DELETE /api/books/<id>/
Loans Microservice
POST /api/loans/borrow/
POST /api/loans/return/
GET /api/loans/
Testing
Run tests for each microservice:

bash
Copy code
docker-compose exec usersms python manage.py test
docker-compose exec booksmicroservice python manage.py test
docker-compose exec loansmicroservice python manage.py test
Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Commit your changes (git commit -am 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Create a new Pull Request.
