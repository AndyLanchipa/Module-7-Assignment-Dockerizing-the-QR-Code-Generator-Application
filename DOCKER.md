# Docker Deployment Guide

This guide covers how to build, run, and deploy the QR Code Generator using Docker.

## Prerequisites

- Docker installed on your system
- DockerHub account (for pushing images)

## Building the Docker Image

### Basic Build

```bash
# Build with default tag
docker build -t qr-code-generator-app .

# Build with custom tag
docker build -t your-username/qr-code-generator:v1.0 .
```

### Multi-stage Build Options

```bash
# Build development version
docker build --target development -t qr-code-generator:dev .

# Build production version (default)
docker build --target production -t qr-code-generator:prod .
```

## Running the Container

### Basic Usage

```bash
# Run with default URL
docker run --rm qr-code-generator-app

# Run with custom URL
docker run --rm qr-code-generator-app --url https://www.example.com
```

### With Volume Mounting

```bash
# Mount output directory to save QR codes
docker run --rm \
  -v $(pwd)/qr_codes:/app/qr_codes \
  qr-code-generator-app --url https://www.njit.edu

# Mount both output and logs directories
docker run --rm \
  -v $(pwd)/qr_codes:/app/qr_codes \
  -v $(pwd)/logs:/app/logs \
  qr-code-generator-app --url https://github.com/example
```

### Using Environment Variables

```bash
# Set URL via environment variable
docker run --rm \
  -e QR_URL=https://www.python.org \
  -v $(pwd)/qr_codes:/app/qr_codes \
  qr-code-generator-app

# Set custom output directory
docker run --rm \
  -e QR_OUTPUT_DIR=custom_output \
  -v $(pwd)/custom_output:/app/custom_output \
  qr-code-generator-app --url https://example.com
```

### Background/Daemon Mode

```bash
# Run in background
docker run -d --name qr-generator \
  -v $(pwd)/qr_codes:/app/qr_codes \
  qr-code-generator-app --url https://github.com/user/repo

# Check status and logs
docker ps
docker logs qr-generator

# Stop and remove
docker stop qr-generator
docker rm qr-generator
```

## Using Docker Compose

### Basic Usage

```bash
# Run default service
docker-compose up

# Run custom service
docker-compose --profile custom up

# Run development service
docker-compose --profile development up
```

### Background Mode

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs

# Stop services
docker-compose down
```

## Pushing to DockerHub

### Setup

1. Create account at [DockerHub](https://hub.docker.com)
2. Login from command line:

```bash
docker login
```

### Tag and Push

```bash
# Tag your image
docker tag qr-code-generator-app your-username/qr-code-generator:latest

# Push to DockerHub
docker push your-username/qr-code-generator:latest

# Push with version tag
docker tag qr-code-generator-app your-username/qr-code-generator:v1.0
docker push your-username/qr-code-generator:v1.0
```

### Automated Pushing with GitHub Actions

The repository includes a GitHub Actions workflow that automatically:

1. Tests the application
2. Builds the Docker image
3. Pushes to DockerHub on main branch updates

#### Setup Required Secrets

In your GitHub repository settings, add these secrets:

- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: Your DockerHub access token

## Security Considerations

### Non-Root User

The Docker image runs as a non-root user (`myuser`) for enhanced security:

```dockerfile
# Creates non-root user
RUN useradd -m -u 1001 myuser

# Switches to non-root user
USER myuser
```

### Minimal Base Image

Using `python:3.12-slim-bullseye` reduces attack surface:

- Smaller image size
- Fewer installed packages
- Reduced security vulnerabilities

### File Permissions

Output directories have proper ownership:

```bash
# Directories owned by myuser
RUN mkdir logs qr_codes && chown myuser:myuser logs qr_codes
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure volume mount paths exist and have proper permissions
2. **Command Not Found**: Verify Docker is installed and running
3. **Build Failures**: Check network connectivity and Docker daemon status

### Debug Mode

```bash
# Run interactively for debugging
docker run -it --rm qr-code-generator-app /bin/bash

# Check container filesystem
docker run --rm qr-code-generator-app ls -la /app
```

### Container Inspection

```bash
# Inspect running container
docker exec -it container_name /bin/bash

# View container details
docker inspect qr-code-generator-app

# Check resource usage
docker stats container_name
```

## Performance Optimization

### Build Optimization

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t qr-code-generator-app .

# Multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 -t qr-code-generator-app .
```

### Runtime Optimization

```bash
# Limit memory usage
docker run --memory=512m qr-code-generator-app

# Set CPU limits
docker run --cpus=1.0 qr-code-generator-app
```

## Production Deployment

### Health Checks

Add health check to Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import main; print('healthy')" || exit 1
```

### Environment-Specific Configs

```bash
# Production
docker run -e ENVIRONMENT=production qr-code-generator-app

# Staging
docker run -e ENVIRONMENT=staging qr-code-generator-app
```

## Next Steps

1. Set up CI/CD pipeline with GitHub Actions
2. Deploy to cloud platforms (AWS, GCP, Azure)
3. Implement container orchestration (Kubernetes)
4. Add monitoring and logging solutions
