# Movies project

## Table of Contents
- Project Description
- Requirements
- Installation
- Usage
- Endpoints

____
## Project Description
The Movies Project is a web application that allows users to view a list of movies and their details. The application includes a script to transfer data from a SQLite database to PostgreSQL. It uses Django for the backend framework, PostgreSQL as the database, employs Docker for containerization and Nginx for managing static files. The Movies Project provides two endpoints: accessing information about a specific movie and  viewing a paginated list of movies.

## Requirements

- Python 3.8+
- Docker

## Installing

1. Clone the repository
```
git clone git@github.com:AnnaKatunina/movies_project.git
```
2. Create .env file in root directory with variables: SECRET_KEY, DEBUG, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

3. Build a docker container
```
docker-compose up --build
```

4. Migrate all migrations to postgres database
```
docker exec -it app_movies python app/manage.py migrate
```

5. Create superuser to access the admin panel
```
docker exec -it app_movies python app/manage.py createsuperuser
```

6. Move data from sqlite database to postgres
```
docker exec -it app_movies python from_sqlite_to_postgres/load_data.py
```
## Usage
To start the project, run the following command:

```
docker-compose up
```
Then, navigate to http://localhost/api/v1/ to view the web application.

## Endpoints
The following endpoints are available:

- api/v1/movies/<uuid:pk>/: URL for viewing details of a single movie
- api/v1/movies/: URL for paginated list of movies
