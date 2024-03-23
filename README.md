# admin-portal

This project is a flask API application running inside a docker container.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Docker is installed on your machine. If you don't have Docker installed, follow the instructions on the [Docker website](https://docs.docker.com/get-docker/)

## Project Setup
1. Clone the Repository
First, clone the repository containing the Flask application to your local machine:

git clone https://github.com/Maxtone9/admin-portal.git
cd admin-portal


2. Build the Docker Image
Run the following command to build the Docker image:
docker build -t flask-app .


3. Run the Docker Container
Once the image is built, you can run the Docker container using the following command:

docker run -p 60000:60000 flask-app

This command will start the Flask application inside a Docker container, and it will be accessible at http://localhost:60000.


