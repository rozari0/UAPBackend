FROM python:3-alpine

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    libjpeg-turbo-dev \
    zlib-dev \
    python3-dev \
    jpeg-dev \
    postgresql-dev \
    musl-dev \
    curl \
    rustup \
    uv

# Set environment variables
ENV PATH="/usr/local/cargo/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY pyproject.toml /app/
RUN uv sync --no-dev

# Copy application files
COPY . /app/
