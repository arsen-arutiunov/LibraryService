
# LibraryService API

LibraryService is a Django-based API for managing a library system. It provides various services such as user management, book borrowing, payments, notifications, and more, with features like JWT authentication, role-based permissions, and integration with third-party services like Stripe and Telegram.

## Features

- **User Management**: CRUD functionality for user profiles with authentication via JWT.
- **Book Management**: Create, read, update, and delete books in the library, with access restricted to admin users.
- **Borrowings**: Manage borrowings, including borrowing date, expected return date, and payment processing.
- **Payments**: Integration with Stripe for processing payments related to book borrowing.
- **Notifications**: Integration with the Telegram API to send notifications about borrowing events, including overdue books and successful payments.
- **Overdue Borrowing Check**: Scheduled task for checking overdue borrowings.
- **Docker Support**: Full support for running the service in Docker containers with PostgreSQL database.

## Installation

### Prerequisites

- Python 3.11+
- Docker (for running the app with PostgreSQL)
- Stripe API key (for payment integration)
- Telegram API key (for notifications)

### Setup

1. Clone the repository:
    ```bash
    git clone git@github.com:arsen-arutiunov/LibraryService.git
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    - Create a `.env` file in the root of the project.
    - Add the following environment variables:

    ```
    STRIPE_API_KEY=your_stripe_api_key
    TELEGRAM_API_KEY=your_telegram_api_key
    DJANGO_SECRET_KEY=your_django_secret_key
    DEBUG=True  # Set to False in production
    ```

5. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser for accessing the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the application:
    ```bash
    python manage.py runserver
    ```

    The app should now be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication

- **POST /api/users/**: Create a new user with email, first name, last name, and password.
- **POST /api/users/token/**: Log in and obtain a JWT token.
- **GET /api/users/me/**: Retrieve the authenticated user's profile.

### Book Management

- **GET /api/books/**: List all books.
- **POST /api/books/**: Create a new book (admin only).
- **GET /api/books/{id}/**: Retrieve details of a specific book.
- **PUT /api/books/{id}/**: Update a book (admin only).
- **DELETE /api/books/{id}/**: Delete a book (admin only).

### Borrowing Management

- **POST /api/borrowings/**: Create a new borrowing record (decreases book inventory by 1).
- **GET /api/borrowings/**: List all borrowings (filtered by user or active status).
- **GET /api/borrowings/{id}/**: Retrieve details of a specific borrowing.
- **POST /api/borrowings/{id}/return/**: Mark a borrowing as returned (increases book inventory by 1).

### Payment Management

- **GET /api/payments/**: List my payments (List all payments for admin).
- **POST /api/payments/**: Create payment.
- **GET /api/payments/success/**: Handle successful payment callback from Stripe.
- **GET /api/payments/cancel/**: Handle canceled payment callback from Stripe.

## Development

### Running with Docker

1. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

2. The app will be accessible at `http://127.0.0.1:8000/` within the Docker container.

3. To run migrations inside Docker:
    ```bash
    docker-compose exec <name-your-app-in-docker> python manage.py migrate
    ```

4. To create a superuser inside Docker:
    ```bash
    docker-compose exec <name-your-app-in-docker> python manage.py createsuperuser
    ```

### Scheduled Tasks

LibraryService uses Celery to run scheduled tasks for checking overdue borrowings. To run Celery workers, use the following command:

```bash
docker-compose exec <name-your-app-in-docker> celery -A LibraryService worker --loglevel=info
```

### Running Tests

To run tests in the project:

```bash
python manage.py test
```
