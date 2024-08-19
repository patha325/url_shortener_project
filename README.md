# URL Shortener

This is a simple Django-based URL shortener application where users can create their own shortened URLs and track the number of clicks.

## Features
- User authentication (login, logout (buggy))
- Create and manage your own shortened URLs
- Track the number of clicks for each URL

## Setup

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone this repository:
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
2. Build the Docker containers:
docker-compose build
3. Run the containers:
docker-compose up
4. Apply the migrations:
   docker-compose exec web python manage.py migrate
5. Create a superuser:
   docker-compose exec web python manage.py createsuperuser
6. Access the application:
   Visit http://localhost:8000 in your browser.
7. Had some issues with the database?
docker-compose exec web python manage.py makemigrations url_shortener
docker-compose exec web python manage.py migrate

### Test
docker-compose exec web python manage.py test

### Technologies used
Django
PostgreSQL
Docker
Docker Compose
