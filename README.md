# Request ID Middleware

**Request ID Middleware** is a Python library that provides middleware for Django
and FastAPI applications to generate and propagate request IDs across
incoming requests, enabling easier tracking in logs, Sentry,
and other observability tools.

## Features
- Request ID Propagation: Automatically generate or extract X-Request-ID headers and make them available throughout your application.
- Django and FastAPI Support: Middleware that works out-of-the-box with Django and FastAPI.
- Sentry Integration: Track request IDs in Sentry to trace issues by request.
- Logging Support: Inject request IDs into logs for better traceability across services.

## Installation

 ```bash
pip install x-request-id-middleware
 ```

## Usage

### Django Setup

1. Add the RequestIDMiddleware to your Django MIDDLEWARE settings:
    ```python
    MIDDLEWARE = [
        ...,
        'x_request_id_middleware.django_middleware.XRequestIDMiddleware',
        ...
    ]
    ```

2. Access the request ID in your views or any part of your application:
    ```python
    from x_request_id_middleware.common import get_request_id
    
    def some_view(request):
        request_id = get_request_id()
        print(f"The request ID is: {request_id}")
    ```

### FastAPI Setup

3. Add the FastAPIXRequestIDMiddleware to your FastAPI app:
    ```python
    from fastapi import FastAPI
    from x_request_id_middleware.fastapi_middleware import FastAPIXRequestIDMiddleware
    
    app = FastAPI()
    app.add_middleware(FastAPIXRequestIDMiddleware)
    ```

2. Access the request ID in your FastAPI routes:
    ```python
    from x_request_id_middleware.common import get_request_id
    
    @app.get("/")
    async def root():
        request_id = get_request_id()
        return {"request_id": request_id}
    ```

### Logging Integration

To include request IDs in your log messages, 
use the `XRequestIDConfigLogging` class from the 
`x_request_id_middleware.logging_config` module.

The XRequestIDConfigLogging class allows you to configure 
logging and add request IDs to your log messages.

Setting Up `XRequestIDConfigLogging`

1. #### Import and Initialize

    Import the XRequestIDConfigLogging class and create an instance of it.
    You can optionally provide a custom log format string when initializing 
    the instance. If no format is provided, the default format will be used.
    ```python
    from x_request_id_middleware.logging_config import XRequestIDConfigLogging
    
    # Optionally, provide a custom log format
    custom_format = "%(asctime)s %(levelname)s [%(request_id)s] %(message)s"
    
    # Initialize with a custom format
    x_request_id = XRequestIDConfigLogging(str_format=custom_format)
    
    # Or initialize with default format
    x_request_id = XRequestIDConfigLogging()
    ```
2. #### Configure Logging

    Once you have created an instance of `XRequestIDConfigLogging`, 
    it will automatically set up the root logger and apply the formatter
    and filter to it.

    If you create new loggers using `logging.getLogger(__name__)` or similar,
    you need to add them to the configuration by calling the `configure_logging`
    method on your `XRequestIDConfigLogging` instance.
    ```python
    import logging
   
   from settings import x_request_id

    # Example of configuring a new logger
    logger = logging.getLogger(__name__)
    x_request_id.configure_logging(logger)
    ```
   
    The configure_logging method adds the formatter and filter to the
    specified logger, ensuring that request IDs are included
    in the log messages.

#### Example Usage

Here’s an example of how you might set up and use 
`XRequestIDConfigLogging` in your application:

```python
import logging

from x_request_id_middleware.logging_config import XRequestIDConfigLogging

# Initialize XRequestIDConfigLogging with a custom format
x_request_id = XRequestIDConfigLogging(
    str_format="%(asctime)s %(levelname)s [%(request_id)s] %(message)s"
)

# Create a new logger
logger = logging.getLogger(__name__)

# Configure the new logger to include request ID in log messages
x_request_id.configure_logging(logger)

# Use the logger in your application
logger.error("This is an error message with request ID.")

```

### Sentry Integration

If you're using Sentry for error tracking, this library can
automatically add the request ID to your Sentry logs:

1. Initialize Sentry in your project.

2. The request ID will automatically be attached to Sentry events as a `request_id` tag.
    ```python
    from x_request_id_middleware.common import set_request_id
    
    def some_error_prone_function():
        set_request_id("my-request-id")
        raise Exception("An error occurred")
    ```
   
## NGINX Integration

To ensure that request IDs are properly propagated through your system,
you need to configure NGINX to include the X-Request-ID header
in the request it passes to your application.

### NGINX Configuration

1. Update NGINX Configuration
Open your NGINX configuration file
(typically located at /etc/nginx/nginx.conf or
/etc/nginx/sites-available/default) and modify it to add the
X-Request-ID header. You can use the $request_id variable,
which NGINX generates for each request.

Example NGINX configuration:

```
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
    }
}
```
In this example, the X-Request-ID header is set to the value of the
$request_id variable, which NGINX will include in requests forwarded
to your application.

2. Restart NGINX

After updating the configuration, restart NGINX to apply the changes:

```bash
sudo systemctl restart nginx
```

### Verifying Request ID Propagation

1. Send a Request

    Send a request to your server and verify that the X-Request-ID header
    is included in the response.

2. Check Application Logs

    Verify that your application logs include the request ID, 
    which will help you trace requests through your system.

---

### Contributing

If you want to contribute to the project, please open an issue or
submit a pull request. All contributions, bug reports,
and feature requests are welcome.

---

### License

This project is licensed under the MIT License.

---


