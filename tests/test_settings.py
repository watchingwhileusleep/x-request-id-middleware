INSTALLED_APPS = [
    "django.contrib.contenttypes",
]
MIDDLEWARE = [
    "request_id_middleware.django.XRequestIdMiddleware",
]
SENTRY_DSN = "http://example.com/123"
