# QR Code Generator

A Python application that generates QR codes for URLs with configurable options and Docker support.

## Features

- Generate QR codes for any URL
- Configurable output directory and filename
- Styled QR codes with rounded corners
- Comprehensive logging
- Environment variable support
- Docker containerization

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd qr-code-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Basic usage
python main.py --url https://github.com/kaw393939

# Custom output filename
python main.py --url https://www.njit.edu --output custom_qr.png

# Custom output directory
python main.py --url https://example.com --dir /custom/path
```

### Environment Variables

- `QR_URL`: Default URL to encode (can be overridden by --url)
- `QR_OUTPUT_DIR`: Default output directory (default: qr_codes)

### Docker Usage

```bash
# Build the image
docker build -t qr-code-generator-app .

# Run with default URL
docker run -d --name qr-generator qr-code-generator-app

# Run with custom URL
docker run -d --name qr-generator \
  -v $(pwd)/qr_codes:/app/qr_codes \
  qr-code-generator-app --url https://www.njit.edu

# Check logs
docker logs qr-generator
```

## Output

- QR code images are saved as PNG files
- Logs are saved in the `logs/` directory
- Default output directory is `qr_codes/`

## License

MIT License
