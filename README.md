# SimRacing Hub

A web application for sim racing enthusiasts to organize and participate in racing events, share experiences, and connect with other racers.

## Features

### Events
- Create and manage racing events
- Subscribe to events
- View upcoming events dashboard
- Detailed event information including dates and race times

### Social Features
- User profiles with avatars
- Create and share posts about racing experiences
- Comment on posts
- Like posts
- Follow other racers' activities

### User Management
- User registration and authentication
- Profile customization
- Personal dashboard
- View subscribed events

## Getting Started

1. Clone the repository:
```
git clone [repository-url]
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file with your settings:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

Note: For the SECRET_KEY, you can generate a secure key using Python:
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. Run migrations:
```
python manage.py migrate
```

6. Create a superuser:
```
python manage.py createsuperuser
```

7. Run the development server:
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Technologies Used
- Django
- Bootstrap
- SQLite (development) / PostgreSQL (production)
- Crispy Forms
- Font Awesome
