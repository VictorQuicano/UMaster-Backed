# 🏗️ U-MASTER (Backend)

Proyect maded in python3 and this have many endpoints.

## ✨Features

- RESTful API built with Django and Django REST Framework (DRF)
- User authentication and permissions
- CRUD operations for main resources
- Pagination, filtering, and ordering
- JWT authentication support

## 📋Prerequisites

Ensure you have the following installed:

- Python 3.10.12
- pip
- virtualenv
- PostgreSQL or SQLite

## 🛠️Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VictorQuicano/UMaster-Backed.git
   cd UMaster-Backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (optional but recommended):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the API at `http://127.0.0.1:8000/api/`

## 🔑Authentication

This project uses Django REST Framework authentication. Make sure to include an `Authorization` header with a valid token when making requests to protected endpoints.

## ⚙️Environment Variables

Copy the `.env-example` file in the `.env`.

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/db_name
```

## ✅Deployment

1. Configure a production-ready database (e.g., PostgreSQL)
2. Set `DEBUG=False` in environment variables
3. Use a production-ready WSGI server like Gunicorn
4. Configure static files storage (e.g., AWS S3, WhiteNoise)

## License

This project is licensed under the MIT License. See `LICENSE` for details.
