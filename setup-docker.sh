#!/bin/bash

# Docker Installation and Setup Script for QR Code Generator
# This script helps install Docker and set up the development environment

set -e

echo "🐳 QR Code Generator - Docker Setup Script"
echo "==========================================="

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "Windows"
    else
        echo "Unknown"
    fi
}

# Function to check if Docker is installed
check_docker() {
    if command -v docker >/dev/null 2>&1; then
        echo "✅ Docker is already installed"
        docker --version
        return 0
    else
        echo "❌ Docker is not installed"
        return 1
    fi
}

# Function to install Docker on macOS
install_docker_macos() {
    echo "📦 Installing Docker on macOS..."
    echo "Please download and install Docker Desktop from:"
    echo "https://desktop.docker.com/mac/main/amd64/Docker.dmg"
    echo ""
    echo "After installation:"
    echo "1. Open Docker Desktop"
    echo "2. Follow the setup wizard"
    echo "3. Wait for Docker to start"
    echo "4. Run this script again to continue"
}

# Function to install Docker on Linux
install_docker_linux() {
    echo "📦 Installing Docker on Linux..."
    
    # Update package index
    sudo apt-get update
    
    # Install prerequisites
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo \
        "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    echo "✅ Docker installed successfully!"
    echo "Please log out and log back in for group changes to take effect"
}

# Function to install Docker on Windows
install_docker_windows() {
    echo "📦 Installing Docker on Windows..."
    echo "Please download and install Docker Desktop from:"
    echo "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    echo ""
    echo "Requirements:"
    echo "- Windows 10 64-bit: Pro, Enterprise, or Education"
    echo "- WSL 2 feature enabled"
    echo "- Virtualization enabled in BIOS"
}

# Function to build and test the application
build_and_test() {
    echo "🔨 Building Docker image..."
    docker build -t qr-code-generator-app .
    
    echo "🧪 Testing Docker container..."
    docker run --rm -v $(pwd)/test-output:/app/qr_codes qr-code-generator-app --url https://github.com/test
    
    echo "✅ Docker build and test completed successfully!"
    echo "📁 Test QR code saved in ./test-output/"
}

# Function to show usage instructions
show_usage() {
    echo ""
    echo "🚀 Next Steps:"
    echo "=============="
    echo "1. Build the image:    docker build -t qr-code-generator-app ."
    echo "2. Run the container:  docker run --rm qr-code-generator-app"
    echo "3. Custom URL:         docker run --rm -v \$(pwd)/qr_codes:/app/qr_codes qr-code-generator-app --url https://example.com"
    echo "4. Check logs:         docker logs <container_name>"
    echo ""
    echo "📚 Documentation: See README.md for more examples"
}

# Main execution
main() {
    OS=$(detect_os)
    echo "🖥️  Detected OS: $OS"
    echo ""
    
    if check_docker; then
        echo ""
        read -p "🚀 Docker is installed. Build and test the application? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            build_and_test
        fi
        show_usage
    else
        echo ""
        case $OS in
            "macOS")
                install_docker_macos
                ;;
            "Linux")
                read -p "Install Docker automatically? (y/n): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    install_docker_linux
                fi
                ;;
            "Windows")
                install_docker_windows
                ;;
            *)
                echo "❌ Unsupported operating system: $OS"
                echo "Please install Docker manually from: https://docs.docker.com/get-docker/"
                ;;
        esac
    fi
}

# Run main function
main "$@"
