FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=schedule_planner.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Change work directory to where manage.py is
WORKDIR /app/schedule_planner

# Collect static files
# Note: We skip 'migrate' here because the database is usually not available during the build.
# You should run migrations as a "Release Command" on Render or manually in the shell.
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "schedule_planner.wsgi:application"]
