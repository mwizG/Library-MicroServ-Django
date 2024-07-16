## Library Microservice System
## Overview
The Library Management System is a microservices-based application designed to practice creating and deploying a scalable microservice architecture utilizing RESTful APIs. This project is built with Python and the Django framework, deployed on AWS EC2 servers, and incorporates Version Control( Git and Github) practices for smooth integration and deployment. Each microservice is containerized using Docker, enabling consistency across different environments. The system allows users to manage books, loans, and authentication within a library.

## Microservices

### 1. **API Gateway**
- **Port:** 8001
- **Description:** Serves as the entry point to the system, routing requests to the appropriate microservices.

### 2. **Books Service**
- **Port:** 8000
- **Description:** Manages the books in the library, including creating, retrieving, updating, and deleting book records.

### 3. **Loans Service**
- **Port:** 8003
- **Description:** Manages the borrowing and returning of books.

### 4. **Users Service**
- **Port:** 8002
- **Description:** Handles user authentication and user management.

## Features

- **CRUD Operations for Books:** Users can create, read, update, and delete book records.
- **Loan Management:** Users can borrow and return books, with the system tracking loan dates and statuses.
- **User Authentication:** Secure login and registration system for users.
- **API Gateway:** Routes requests and handles communication between microservices.

## Technologies Used
Backend Framework: Django
Microservices Architecture: Separate services for books, loans, and user authentication
API Gateway: Centralized gateway for routing requests to appropriate microservices
Database: SQLite
Containerization: Docker
Web Server: HTTPD (Apache)
Deployment: AWS EC2
CI/CD: not yet done
GIT and GITHUB: used for version control
## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.x and pip.

### Steps

1. **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd library-management-system
    ```

2. **Set Up Environment Variables:**
   Create a `.env` file in the project root and add the following environment variables:
    ```env
    SERVER_IP=<your-server-ip>
    ```

3. **Build and Run Docker Containers:**
    ```bash
    docker-compose up --build
    ```

4. **Apply Migrations:**
    ```bash
    docker-compose exec apigateway python manage.py migrate
    docker-compose exec bookms python manage.py migrate
    docker-compose exec loansms python manage.py migrate
    docker-compose exec usersms python manage.py migrate
    ```

5. **Create a Superuser (for admin access):**
    ```bash
    docker-compose exec usersms python manage.py createsuperuser
    ```

## Usage

### Access the API Gateway

- **Home Page:**
  ```http
  http://<your-server-ip>:8001/gateway/home/
  ```

### API Endpoints

- **Books Service:**
  - Create a New Book: `POST /new/`
  - Retrieve Book Details: `GET /books/<book_id>/`
  - Update Book Details: `PUT /books/<book_id>/`
  - Delete a Book: `DELETE /books/<book_id>/`

- **Loans Service:**
  - Borrow a Book: `POST /loans/borrow/`
  - Return a Book: `POST /loans/return/`
  - View Loan Status: `GET /loans/status/<loan_id>/`

- **Users Service:**
  - Register: `POST /users/register/`
  - Login: `POST /users/login/`
  - User Details: `GET /users/<user_id>/`

## Customization

### Styling

- Custom CSS files (`mybooks.css` and `borrow.css`) are used to style HTML elements for different functionalities.

### Date Fields

- Forms are customized to include specific field types like date pickers for date fields.

## Troubleshooting

- **Session Issues:** Ensure that session management is correctly configured and that the `django_session` table is properly set up.
- **Server IP Changes:** Use environment variables to manage dynamic IP addresses for your server.

## Contributing

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
