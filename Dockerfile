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

# Install uWSGI and other dependencies, then clean up in the same layer
RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install --upgrade pip uwsgi && \
    apk del gcc musl-dev linux-headers

# Install Git, to check for updates
RUN apk add --no-cache git

# Set permsissions while still running as root
RUN chown -R appuser:appgroup /app
RUN chmod -R 755 /app

# Switch to the non-root user
USER appuser

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .


# Start the application using uWSGI
CMD ["uwsgi", \
    "--http", "0.0.0.0:5000", \
    "--module", "app.main:app", \
    "--master", \
    "--processes", "4", \
    "--threads", "2"]

# Build and upload with:
# docker build -t yourusername/1320:latest .
# docker push yourusername/1320:latest
