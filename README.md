# Solorence v0.1

**Solorence** is a web application built with Django (backend) and Nuxt.js (frontend). It serves as a consultative note-taking system, designed to streamline communication and documentation between professionals.

## Project Structure

- **Backend**: Located in the `core` folder, built with Django.
- **Frontend**: Located in the `front` folder, built with Nuxt.js.
- **Containerization**: Uses Docker and Docker Compose to simplify setup and deployment.

## Prerequisites

Make sure you have these tools installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/farzad-mohebi/Solorence
   cd Solorence
   ```

2. Start the project with Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This command will build and start the containers for both the backend (Django) and the frontend (Nuxt.js).

3. Access the application:
   - **Frontend**: `http://localhost:3000`
   - **Backend API**: `http://localhost:8000`

## Project Structure

```
noteup/
├── core/            # Django backend
└── front/           # Nuxt.js frontend
└── docker-compose.yml
```

## Available Commands

- **Run**: `docker-compose up`
- **Stop**: `docker-compose down`
- **Rebuild**: `docker-compose up --build`

## Environment Variables

Ensure you create and configure environment variables in both `core/.env` and `front/.env` for sensitive information (e.g., database credentials, API keys).

## License

This project is licensed under the LGP License.
