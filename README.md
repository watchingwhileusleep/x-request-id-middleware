# Request ID Middleware

**Request ID Middleware** is a Python library that provides middleware for Django
and FastAPI applications to generate and propagate request IDs across
incoming requests, enabling easier tracking in logs, Sentry,
and other observability tools.

## Features
- **Request ID Propagation**: Automatically generate or extract X-Request-ID headers and make them available throughout your application.
- **Django and FastAPI Support**: Middleware that works out-of-the-box with Django and FastAPI.
- **Sentry Integration**: Track request IDs in Sentry to trace issues by request.
- **Logging Support**: Inject request IDs into logs for better traceability across services.

## Installation

### Basic Installation (Core)

To install the core package without any framework dependencies:

```bash
pip install x-request-id-middleware
```

Or using **Poetry**:

```bash
poetry add x-request-id-middleware
```

### Django Installation

For Django support, install the package with the `django` extras:

```bash
pip install "x-request-id-middleware[django]"
```

Or using **Poetry**:

```bash
poetry add x-request-id-middleware -E django
```

### FastAPI Installation

For FastAPI support, install the package with the `fastapi` extras:

```bash
pip install "x-request-id-middleware[fastapi]"
```

Or using **Poetry**:

```bash
poetry add x-request-id-middleware -E fastapi
```

## Usage

### Django Setup

1. Add the `XRequestIDMiddleware` to your Django `MIDDLEWARE` settings:
    ```python
    MIDDLEWARE = [
        ...,
        'x_request_id_middleware.django_middleware.XRequestIDMiddleware',
        ...
    ]
    ```

2. Accessing the Request ID:

    While you can access the request ID in your views or other parts of
   your application, please note that this is typically not necessary in a
   real-world application. The middleware automatically handles the
   propagation of the `X-Request-ID` header for you.

    ```python
    from x_request_id_middleware.common import get_x_request_id
    
    def some_view(request):
        x_request_id = get_x_request_id()
        print(f"The request ID is: {x_request_id}")
    ```

    In a real-world scenario, you usually do not need to manually access
   the `X-Request-ID` as the middleware manages this automatically.

### FastAPI Setup

1. Add the `FastAPIXRequestIDMiddleware` to your FastAPI app:
    ```python
    from fastapi import FastAPI
    from x_request_id_middleware.fastapi_middleware import FastAPIXRequestIDMiddleware
    
    app = FastAPI()
    app.add_middleware(FastAPIXRequestIDMiddleware)
    ```

2. Accessing the Request ID:

    Similarly, while you can access the request ID in your FastAPI routes,
    this is generally not required in production. The middleware automatically
    handles the `X-Request-ID` header for you.

    ```python
    from x_request_id_middleware.common import get_x_request_id
    
    @app.get("/")
    async def root():
        x_request_id = get_x_request_id()
        return {"x_request_id": x_request_id}
    ```

    In practice, the middleware ensures the `X-Request-ID` is propagated
    properly without needing manual handling.

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
    custom_format = "%(asctime)s %(levelname)s [%(x_request_id)s] %(message)s"
    
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
    str_format="%(asctime)s %(levelname)s [%(x_request_id)s] %(message)s"
)

# Create a new logger
logger = logging.getLogger(__name__)

# Configure the new logger to include request ID in log messages
x_request_id.configure_logging(logger)

# Use the logger in your application
logger.error("This is an error message with request ID.")

```

### Sentry Integration

If you're using Sentry for error tracking, this library automatically
adds the request ID to your Sentry logs. You don't need to manually set
the request ID for Sentry. Here’s how it works:

1. **Initialize Sentry in your project**:

    Ensure that Sentry is initialized in your application as usual. For example:
    
    ```python
    import sentry_sdk

    sentry_sdk.init(
        dsn="your_sentry_dsn_here",
        # Other Sentry configuration
    )
    ```

2. **Automatic Request ID Tagging**:

    Once Sentry is initialized, the request ID will be automatically
    attached to Sentry events as a `x_request_id` tag. This means you don't
    need to call `set_request_id` manually. The middleware will handle
    setting the request ID in the context for both Django and FastAPI,
    and it will be picked up by Sentry.

    Here’s how you would typically use the middleware in your applications:

    - **For Django**:
   
        ```python
        # In your Django settings.py
        MIDDLEWARE = [
            ...,
            'x_request_id_middleware.django_middleware.XRequestIDMiddleware',
            ...
        ]
        ```

    - **For FastAPI**:

        ```python
        from fastapi import FastAPI
        from x_request_id_middleware.fastapi_middleware import FastAPIXRequestIDMiddleware
        
        app = FastAPI()
        app.add_middleware(FastAPIXRequestIDMiddleware)
        ```

    You can now rely on Sentry to automatically handle request IDs for you.
   
## NGINX Integration

To ensure that request IDs are properly propagated through your system,
you need to configure NGINX to include the X-Request-ID header
in the request it passes to your application.

### NGINX Configuration

1. Update NGINX Configuration
Open your NGINX configuration file
(typically located at /etc/nginx/nginx.conf or
/etc/nginx/sites-available/default) and modify it to add the
X-Request-ID header. You can use the $x_request_id variable,
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
        proxy_set_header X-Request-ID $x_request_id;
    }
}
```
In this example, the X-Request-ID header is set to the value of the
$x_request_id variable, which NGINX will include in requests forwarded
to your application.

2. Restart NGINX

After updating the configuration, restart NGINX to apply the changes:

```bash
sudo systemctl restart nginx
```

### Verifying X-Request-ID Propagation

1. Send a Request

    Send a request to your server and verify that the X-Request-ID header
    is included in the response.

2. Check Application Logs

    Verify that your application logs include the X-request-ID, 
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


