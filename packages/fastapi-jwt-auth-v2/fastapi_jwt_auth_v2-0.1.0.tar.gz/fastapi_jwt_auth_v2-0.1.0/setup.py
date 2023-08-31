from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "FastAPI extension that provides JWT Auth support"
with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="fastapi_jwt_auth_v2",
    version=VERSION,
    author="Daniel Chico",
    author_email="daniel.chico0109@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    requires=["fastapi", "pyjwt"],
    keywords=["python", "fastapi", "jwt", "authentication"],
    url="https://github.com/DanielChico/fastapi-jwt-auth-v2",
)
