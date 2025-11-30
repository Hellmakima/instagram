# this doesn't work as mongodb is not in docker

# Use lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system deps (for building some Python packages)
# Using pip for now muight chage this to use uv instead
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
# removed some pips for now
COPY devdocs/requirements.txt ./requirements.txt

# Install dependencies with pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code but skip the tests
COPY auth-server/app ./app

# Expose backend port
EXPOSE 5001

# Set working directory to backend
WORKDIR /app

# Run uvicorn when container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
