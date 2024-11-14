# Trails API

The **Trails API** is a Flask-based RESTful service designed to manage trails, locations, user accounts, and access logs. The API supports CRUD operations for each entity and uses authentication to ensure secure access. This project features structured code with modular components, database configuration through environment variables, and interactive API documentation via Swagger.

![Trails API](/static/images/image.png)

## Features

- **CRUD Operations**: Manage trails, locations, and user access logs.
- **Authentication**: Basic auth-based protection with customizable authentication URL.
- **Database**: Automatically creates tables in SQL Server if they do not exist.
- **Swagger Documentation**: Interactive API documentation available at `/apidocs`.
- **Modular Code**: Configurations, database interactions, and decorators are split for better maintainability.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [License](#license)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/SaadAlsuabie/Trails_application.git
   cd Trails_application
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (see [Configuration](#configuration) below).

4. Run the API:
   ```bash
   python app.py
   ```

## Project Structure

```plaintext
trails-api/
│
├── app.py               # Main application file with API routes and setup
├── db.py                # Database operations and table management
├── config.py            # Configuration settings using environment variables
├── decorators.py        # Authentication decorators
├── swagger.json         # Swagger documentation
├── requirements.txt     # Python dependencies
└── static/
    └── swagger.json     # Swagger UI static files
```

## Endpoints

| Endpoint                   | Method | Description              |
|----------------------------|--------|--------------------------|
| `/trails`                  | GET    | Retrieve all trails      |
| `/trails`                  | POST   | Create a new trail       |
| `/trails/{trail_id}`       | GET    | Retrieve a trail by ID   |
| `/trails/{trail_id}`       | PUT    | Update a trail by ID     |
| `/trails/{trail_id}`       | DELETE | Delete a trail by ID     |

Access the interactive Swagger documentation at [http://localhost:5000/apidocs](http://localhost:5000/apidocs) for a complete list of endpoints.

## Authentication

The API uses basic authentication, with the following decorator in `decorators.py` to verify user credentials:

```python
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate_user(auth.username, auth.password):
            return make_response({'Error':'Authentication failed'}, 401)
        return f(*args, **kwargs)
    return decorated_function
```

Set up the authentication URL in `.env` file for user verification.

## Configuration

The `config.py` file loads environment variables to configure database settings and the authentication URL. Example `.env` file:

```plaintext
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_NAME=trailsdb
DB_USER=yourusername
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=1433
AUTH_URL=https://your-auth-url.com/verify
```

Environment variables are accessed as follows:

```python
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.dbdriver = os.getenv('DB_DRIVER')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.auth_url = os.getenv('AUTH_URL')
```

## Deployment

Deploy the Trails API on a server and ensure the following:

1. Set up SQL Server with correct permissions.
2. Configure the environment variables in production.
3. Ensure `AUTH_URL` points to a valid authentication endpoint.

## Screenshots

### Swagger API Documentation
![Swagger UI](https://via.placeholder.com/800x400.png?text=Swagger+UI+Documentation)

### Authentication Prompt
![Authentication](https://via.placeholder.com/800x400.png?text=Authentication+Prompt)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

---

The Trails API is designed to be secure, scalable, and easy to integrate with client applications. For more information on usage or development, please contact [support@example.com](mailto:support@example.com).