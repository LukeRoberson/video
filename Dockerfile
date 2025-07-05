# Use the official Python image from the Docker Hub
# 3.12 is required for now to support Alpine's uwsgi-python3 package
# This tag is the latest Alpine with the latest Python 3.12
# https://pkgs.alpinelinux.org/package/edge/main/x86/uwsgi-python3

FROM python:3.12-alpine
LABEL org.opencontainers.image.base.name="python:3.12-alpine"

# Create non-root user with no password
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory in the container
WORKDIR /app

# Switch to the non-root user
USER appuser

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the application using uWSGI
CMD python3 -m app.main

# Build and upload with:
# docker build -t yourusername/1320:latest .
# docker push yourusername/1320:latest
