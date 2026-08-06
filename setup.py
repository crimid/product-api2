from setuptools import setup, find_packages

setup(
    name="product-api2",
    version="1.0.0",
    description="Product API with testing and CI/CD",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn>=0.30.0",
        "sqlmodel>=0.0.24",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
        "bcrypt>=4.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.6",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=5.0.0",
            "httpx>=0.27.0",
            "pytest-asyncio>=0.23.0",
            "pytest-benchmark>=4.0.0",
            "ruff>=0.4.0",
            "black>=24.0.0",
        ],
    },
    python_requires=">=3.11",
)
