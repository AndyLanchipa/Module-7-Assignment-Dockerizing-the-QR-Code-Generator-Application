#!/usr/bin/env python3
"""
Demonstration script for QR Code Generator
Creates several example QR codes with different configurations
"""

import subprocess
import sys
from pathlib import Path

def create_demo_qr_codes():
    """Create demonstration QR codes"""
    
    print("🎨 QR Code Generator - Demo Script")
    print("==================================")
    
    # Ensure output directory exists
    demo_dir = Path("demo_qr_codes")
    demo_dir.mkdir(exist_ok=True)
    
    # Demo URLs and configurations
    demos = [
        {
            "url": "https://github.com/kaw393939",
            "output": "github_kaw393939.png",
            "description": "Default GitHub Profile"
        },
        {
            "url": "https://www.njit.edu",
            "output": "njit_website.png", 
            "description": "NJIT Official Website"
        },
        {
            "url": "https://github.com/AndyLanchipa/Module-7-Assignment-Dockerizing-the-QR-Code-Generator-Application",
            "output": "project_repository.png",
            "description": "This Project's Repository"
        },
        {
            "url": "https://hub.docker.com",
            "output": "dockerhub.png",
            "description": "Docker Hub"
        },
        {
            "url": "https://www.python.org",
            "output": "python_org.png",
            "description": "Python Official Website"
        }
    ]
    
    success_count = 0
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. Creating QR code for: {demo['description']}")
        print(f"   URL: {demo['url']}")
        
        try:
            result = subprocess.run([
                sys.executable, "main.py",
                "--url", demo["url"],
                "--dir", str(demo_dir),
                "--output", demo["output"]
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"   ✅ Created: {demo_dir / demo['output']}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {result.stderr.strip()}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Timeout creating QR code")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Demo completed!")
    print(f"   Successfully created {success_count}/{len(demos)} QR codes")
    print(f"   Check the '{demo_dir}' directory for generated QR codes")
    
    # List created files
    qr_files = list(demo_dir.glob("*.png"))
    if qr_files:
        print(f"\n📁 Generated files:")
        for qr_file in sorted(qr_files):
            size_kb = qr_file.stat().st_size / 1024
            print(f"   - {qr_file.name} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    try:
        create_demo_qr_codes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        sys.exit(1)
