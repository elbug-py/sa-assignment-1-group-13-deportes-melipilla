# SA: Assignment 1

This project is a web application developed with Django and MongoDB (mongoengine), ready to run with Docker.

## Requirements

- Python 3.13
- MongoDB
- Django
- Docker and docker-compose
- Apache Mesos (no need to install anything, as it is automatically started with Zookeeper via Docker containers)

## Running with Docker

1. Clone the repository:

   ```sh
   git clone <repo-url>
   cd sa-assignment-1-group-13-deportes-melipilla
   ```

2. Start the services (The processes of populating the database and starting Mesos are automated):

   ```sh
   cd docker
   docker-compose up --build
   ```

3. Access the Web project

   url: http://localhost:8000/

---

**Author:** Group 13 - Deportes Melipilla
