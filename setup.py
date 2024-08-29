from setuptools import setup
from setuptools import find_packages


setup(
    name="x-request-id-middleware",
    version="0.2.1",
    description="Library to handle request ID propagation for Django and FastAPI",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "sentry-sdk>=1.16.0",
    ],
    extras_require={
        "django": ["django>=4.2"],
        "fastapi": [
            "fastapi>=0.103",
            "starlette>=0.27",
            "anyio>=3.6.2",
            "httpx>=0.27.0"
        ],
    },
    python_requires=">=3.8",
)
