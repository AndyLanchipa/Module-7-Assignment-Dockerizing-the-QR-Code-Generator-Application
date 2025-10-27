# Use the official Python image from DockerHub as the base image
FROM python:3.12-slim-bullseye as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for logs and QR codes
RUN mkdir logs qr_codes

# Copy the rest of the application's source code
COPY . .

# Default command for development
CMD ["python", "main.py", "--url", "https://github.com/development"]

# Production stage
FROM base as production

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN useradd -m -u 1001 myuser && \
    mkdir logs qr_codes && \
    chown myuser:myuser logs qr_codes

# Copy the rest of the application's source code into the container, setting ownership to 'myuser'
COPY --chown=myuser:myuser . .

# Switch to the non-root user for security
USER myuser

# Use ENTRYPOINT and CMD to allow flexibility when running the container
ENTRYPOINT ["python", "main.py"]
CMD ["--url", "http://github.com/kaw393939"]
