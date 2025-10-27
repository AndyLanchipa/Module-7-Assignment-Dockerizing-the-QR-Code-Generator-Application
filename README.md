# QR Code Generator

A containerized Python application that generates QR codes for URLs with Docker support.

## Features

- QR Code generation for any URL
- Docker containerization with security best practices
- Command-line interface with flexible options
- Automated testing and CI/CD pipeline
- Volume mounting for persistent output

## Prerequisites

- Python 3.12+ (for local development)
- Docker (for containerized usage)
- Git

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/AndyLanchipa/Module-7-Assignment-Dockerizing-the-QR-Code-Generator-Application.git
cd Module-7-Assignment-Dockerizing-the-QR-Code-Generator-Application
```

2. Create virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Docker Installation

Install Docker by running the setup script:
```bash
./setup-docker.sh
```

## Usage

### Using Docker (Recommended)

```bash
# Build the image
docker build -t qr-code-generator-app .

# Run with default URL
docker run --rm -v $(pwd)/qr_codes:/app/qr_codes qr-code-generator-app

# Run with custom URL
docker run --rm -v $(pwd)/qr_codes:/app/qr_codes \
  qr-code-generator-app --url https://www.njit.edu

# Run with custom output filename
docker run --rm -v $(pwd)/qr_codes:/app/qr_codes \
  qr-code-generator-app --url https://example.com --output my_qr.png
```

### Using Python Locally

```bash
# Basic usage
python main.py --url https://github.com/kaw393939

# With custom output
python main.py --url https://www.example.com --output my_qr.png

# With custom directory
python main.py --url https://example.com --dir /custom/path
```

## Command Line Options

```bash
python main.py --url <URL> [--output <filename>] [--dir <directory>]
```

- `--url`: URL to encode in the QR code (required)
- `--output`: Custom output filename (optional)
- `--dir`: Output directory (default: qr_codes)

## Docker Management

```bash
# Check container logs
docker logs <container_name>

# Stop and remove container
docker stop <container_name>
docker rm <container_name>

# Push to DockerHub
docker tag qr-code-generator-app username/qr-code-generator-app:latest
docker push username/qr-code-generator-app:latest
```

## Testing

Run the test suite:
```bash
python test_qr_generator.py
```

Run demo script:
```bash
python demo.py
```

## Output

- QR codes are saved as PNG images in the `qr_codes/` directory
- Execution logs are saved in the `logs/` directory
- Files are named with timestamps unless custom name is provided

## Project Structure

```
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── setup-docker.sh       # Docker installation script
├── demo.py               # Demo script
├── test_qr_generator.py  # Test suite
├── DOCKER.md            # Docker documentation
├── REFLECTION.md        # Assignment reflection
└── .github/workflows/   # CI/CD pipeline
```

## Security Features

- Container runs as non-root user for security
- Uses minimal Python slim base image
- Input validation and error handling
- No hardcoded sensitive information

## Documentation

- [DOCKER.md](./DOCKER.md) - Detailed Docker usage guide
- [REFLECTION.md](./REFLECTION.md) - Assignment reflection document

