# Use the official Alpine Python image from the Docker Hub
# Using Python 3.13 to match the development

FROM python:3.13.9-alpine
LABEL org.opencontainers.image.base.name="python:3.13.7-alpine"

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user with no password
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory in the container, set permissions
WORKDIR /app
RUN chown -R appuser:appgroup /app
RUN chmod -R 755 /app

# Install uWSGI and other dependencies, then clean up in the same layer
RUN apk add --no-cache gcc musl-dev linux-headers nodejs npm && \
    pip install --upgrade pip uwsgi && \
    apk del gcc musl-dev linux-headers

# Update packages
RUN apk update && \
    apk upgrade && \
    apk add --no-cache sqlite && \
    rm -rf /var/cache/apk/*

# Switch to the non-root user
USER appuser

# Copy the requirements file and install dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install .

# Install frontend dependencies and build TypeScript
COPY package.json ./
COPY package-lock.json ./
RUN npm install && npm run build

# Copy files (not all at once to minimize layer size)
COPY robots.txt .
COPY static/icons/ ./static/icons/
COPY static/img/ ./static/img/
COPY static/css/ ./static/css/
COPY static/js/ ./static/js/
COPY templates/ ./templates/
COPY static/vtt/ ./static/vtt/
COPY static/subtitles/ ./static/subtitles/
COPY static/themes/ ./static/themes/
COPY app/ ./app/
COPY search/ ./search/
COPY changelog.yaml .
COPY videos.db .

# Expose the application port
EXPOSE 5000

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
