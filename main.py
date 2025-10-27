#!/usr/bin/env python3
"""
QR Code Generator Application
Generates QR codes for URLs with configurable options
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"qr_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def create_qr_code(url, output_dir="qr_codes", filename=None):
    """
    Generate a QR code for the given URL
    
    Args:
        url (str): The URL to encode in the QR code
        output_dir (str): Directory to save the QR code image
        filename (str): Custom filename for the QR code image
    
    Returns:
        str: Path to the generated QR code image
    """
    logger = logging.getLogger(__name__)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_code_{timestamp}.png"
    
    # Ensure filename has .png extension
    if not filename.endswith('.png'):
        filename += '.png'
    
    full_path = output_path / filename
    
    try:
        # Create QR code instance with configuration
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR Code
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to the QR code
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create an image with styled appearance
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="black",
            back_color="white"
        )
        
        # Save the image
        img.save(full_path)
        
        logger.info(f"QR code generated successfully: {full_path}")
        logger.info(f"Encoded URL: {url}")
        
        return str(full_path)
        
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        raise


def main():
    """Main function to handle command line arguments and generate QR code"""
    parser = argparse.ArgumentParser(
        description="Generate QR codes for URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url https://github.com/kaw393939
  python main.py --url https://www.njit.edu --output custom_qr.png
  python main.py --url https://example.com --dir /custom/path
        """
    )
    
    parser.add_argument(
        "--url",
        required=True,
        help="URL to encode in the QR code"
    )
    
    parser.add_argument(
        "--output",
        help="Output filename for the QR code image"
    )
    
    parser.add_argument(
        "--dir",
        default="qr_codes",
        help="Output directory for QR code images (default: qr_codes)"
    )
    
    # Parse environment variables as well
    url_from_env = os.getenv('QR_URL')
    output_dir_from_env = os.getenv('QR_OUTPUT_DIR', 'qr_codes')
    
    args = parser.parse_args()
    
    # Use environment variable if URL not provided via command line
    if not args.url and url_from_env:
        args.url = url_from_env
    
    if not args.url:
        parser.error("URL is required either via --url argument or QR_URL environment variable")
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting QR Code Generator")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Arguments: {vars(args)}")
    
    try:
        # Generate QR code
        output_path = create_qr_code(
            url=args.url,
            output_dir=args.dir or output_dir_from_env,
            filename=args.output
        )
        
        print(f"QR code generated successfully: {output_path}")
        logger.info("QR Code Generator completed successfully")
        
    except Exception as e:
        logger.error(f"Application failed: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
