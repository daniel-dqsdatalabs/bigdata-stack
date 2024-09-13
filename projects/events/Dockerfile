# Pull the official base image
FROM python:3.12-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /app

# Install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev \
    && apt-get install -y libpq-dev \
    && apt-get clean

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/