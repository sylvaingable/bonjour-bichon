FROM python:3.12-slim

WORKDIR /app

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment in a volume-mounted location
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first for better layer caching
COPY requirements.txt .

# Create venv and install dependencies
RUN python -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY src/ ./src/

# Change ownership to app user
RUN chown -R app:app /app

USER app

# Set entrypoint so the container can be run without specifying the command
ENTRYPOINT ["python", "-m", "src.main"]