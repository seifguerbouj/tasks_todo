# FastAPI ToDo List

This FastAPI application serves as a simple ToDo List REST API, allowing users to sign up, log in, and manage their tasks.

## Features
- User authentication (sign up, log in) using JWT tokens.
- CRUD operations for managing tasks (create, read, update, delete).
- PostgreSQL database integration for data persistence.
- Secure password hashing using bcrypt.

## How to Run

### Prerequisites
- Docker installed on your machine.

### Running the Application
1. Clone this repository to your local machine.
2. Navigate to the root directory of the cloned repository.
3. Execute the following command to start the application:
   ```bash
   docker-compose up

Once the containers are up and running, you can access the FastAPI application at [http://localhost:3000](http://localhost:3000).

You can interact with the API endpoints using tools like cURL, Postman, or you can use Swagger at [http://localhost:3000/docs](http://localhost:3000/docs).

## Endpoints

### Sign Up
- **URL:** `/signup/`
- **Method:** `POST`
- **Description:** Create a new user account.

### Log In
- **URL:** `/token`
- **Method:** `POST`
- **Description:** Generate an access token by logging in.

### Create Task
- **URL:** `/tasks/`
- **Method:** `POST`
- **Description:** Create a new task.

### Read Tasks
- **URL:** `/tasks/`
- **Method:** `GET`
- **Description:** Retrieve all tasks for the logged-in user.

### Read Task
- **URL:** `/tasks/{task_id}`
- **Method:** `GET`
- **Description:** Retrieve details of a specific task.

### Update Task
- **URL:** `/tasks/{task_id}`
- **Method:** `PUT`
- **Description:** Update details of a specific task.

### Delete Task
- **URL:** `/tasks/{task_id}`
- **Method:** `DELETE`
- **Description:** Delete a specific task.

### Delete All Tasks
- **URL:** `/tasks/`
- **Method:** `DELETE`
- **Description:** Delete all tasks associated with the logged-in user.

### Get All Completed Tasks
- **URL:** `/done/`
- **Method:** `GET`
- **Description:** Get all completed tasks for the logged in user.