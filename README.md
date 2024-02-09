# Project Title

Brief description of the project.

## Prerequisites

- Docker installed on your machine.

## Getting Started

1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.

## Running the Application


### If you want you can update your .env File OR you can use exist

Open the existing `mkv_second_test/.env` file in the root directory of the project.

Add or update the following environment variables in the `mkv_second_test/.env` file:

```dotenv
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```

Save the .env file after making changes.

To run the Django application in a Docker container, use the following command:

You need super-user permissions:

Linux/MacOS:
```bash
sudo docker-compose up --build
```

Windows:
open a command prompt with administrator privileges
```bash
docker-compose up --build
```


