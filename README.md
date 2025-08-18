# SA: Assignment 1

This project is a web application developed with Django and MongoDB (mongoengine), ready to run with Docker.

## Requirements

- Python 3.10+
- MongoDB (local or Docker)
- Django
- Docker and docker-compose (recommended)

## Running with Docker (recommended)

1. Clone the repository:

   ```sh
   git clone <repo-url>
   cd sa-assignment-1-group-13-deportes-melipilla
   ```

2. Start the services:

   ```sh
   cd docker
   docker-compose up --build
   ```

3. Seed the database:

   ```sh
   docker-compose exec web python manage.py seed
   ```

4. Access the web:
   (Not sure what to put here, ask the frontend team)

Check the internal project documentation for model details and request examples (may not exist yet).

---

**Author:** Group 13 - Deportes Melipilla
