# Django Schedule Planner

Basic schedule planner to assist event coordinators with planning with entertainers and event crew over a given period of time. Admin users will have access to CRUD functionality while mid management will have access to the schedules. 

## Table of contents
- 1. Features
- 2. Installation 
- 3. ENV Variables
- 4. App operation
- 5. Images
- 6. Deployment
- 7. License

## 1. Features

- Django 5.2.1
- Collection of custom extensions with [django-extensions](http://django-extensions.readthedocs.org).
- HTTPS and other security related settings on Staging and Production.
- Procfile for running gunicorn with Render. 
- PostgreSQL database in production mode and SQLite in development mode. 
- Crispy Forms and Bootstrap for styling
- PostgreSQL database support with psycopg2.
- Whitenoise for managing static transfers

## 2. How to install

### 🚀 Getting Started

Follow these steps to set up and run the project locally.

#### Prerequisites

* Python 3.x
* pip (Python package installer)

#### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/neilbenjamin/your-repo-name.git](https://github.com/neilbenjamin/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**

    It's highly recommended to use a virtual environment to manage project dependencies isolation.

    ```bash
    # Create the virtual environment (named '.venv' in this example)
    python3 -m venv .venv

    # Activate the virtual environment:
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows (Command Prompt):
    # .venv\Scripts\activate.bat
    # On Windows (PowerShell):
    # .venv\Scripts\Activate.ps1
    ```
    *Note: If you use a virtual environment manager like `virtualenvwrapper` or `pyenv-virtualenv`, you can use its equivalent commands (e.g., `mkvirtualenv your-project-name` and `workon your-project-name`) instead of the `venv` commands above.*

3.  **Install project dependencies:**
    With your virtual environment activated:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application should now be accessible at `http://127.0.0.1:8000/`.

```bash
$ django-admin.py startproject \
  --template=https://github.com/jpadilla/django-project-template/archive/master.zip \
  --name=Procfile \
  --extension=py,md,env \
  project_name
$ mv example.env .env
$ pipenv install --dev
```

## 3. Environment variables

```
SECRET_KEY='django-insecure-&tlrs71*5ho#q+aw3#-c^e$uf!nv66ri'
DJANGO_DEBUG='yes'
```

## 4. Use 
- Create an account
- Log in 
- View schedule
- add, update or delete
- Contact Admin

## 5 Images


## 6. Deployment

You can deploy to your choice of deployment options and based on those, you 
may need to reconfigure your settings to match the host deployment reqeuirements.

## 7. License

Copyright (c) 2025 Neil Benjamin

Permission is restricted for any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software.
