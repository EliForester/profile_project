# Profile Project
Project to create/use user profile

## Getting Started

Clone the repository

Run the following:

```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
```

### Prerequisites

Created on Python 3 w Django 2

requirements.txt
```
Django==2.2.24
Pillow==8.2.0
pytz==2018.3
sqlparse==0.4.1

```

### Notes

DEBUG is set to True because setting it false will also validate ALLOWED_HOSTS

PW validation uses UserAttributeSimilarityValidator max_similarity = 0.3
