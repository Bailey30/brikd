FROM python:3.13

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Set work directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock before copying the whole project
COPY Pipfile Pipfile.lock /app/

# Install dependencies via pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the code
COPY . /app/

# Run future commands within the Pipenv environment
# Use `pipenv run` to run Django or other commands

