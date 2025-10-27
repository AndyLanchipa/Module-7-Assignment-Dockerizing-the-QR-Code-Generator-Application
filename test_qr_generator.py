#!/usr/bin/env python3
"""
Test script for QR Code Generator
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def test_local_execution():
    """Test the application runs locally"""
    print("🧪 Testing local execution...")
    
    try:
        # Create a temporary directory for test output
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, "main.py",
                "--url", "https://github.com/test",
                "--dir", temp_dir,
                "--output", "test_qr.png"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Check if QR code was created
                qr_file = Path(temp_dir) / "test_qr.png"
                if qr_file.exists():
                    print("✅ Local execution test passed")
                    print(f"   QR code created: {qr_file}")
                    return True
                else:
                    print("❌ QR code file not created")
                    return False
            else:
                print(f"❌ Local execution failed: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        print("❌ Local execution timed out")
        return False
    except Exception as e:
        print(f"❌ Local execution error: {e}")
        return False

def test_docker_build():
    """Test Docker image builds successfully"""
    print("🐳 Testing Docker build...")
    
    try:
        result = subprocess.run([
            "docker", "build", "-t", "qr-code-generator-test", "."
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Docker build test passed")
            return True
        else:
            print(f"❌ Docker build failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Docker build timed out")
        return False
    except FileNotFoundError:
        print("⚠️  Docker not found - skipping Docker tests")
        return None
    except Exception as e:
        print(f"❌ Docker build error: {e}")
        return False

def test_docker_run():
    """Test Docker container runs successfully"""
    print("🏃 Testing Docker container execution...")
    
    try:
        # Run container and capture output
        result = subprocess.run([
            "docker", "run", "--rm", 
            "qr-code-generator-test",
            "--url", "https://github.com/docker-test"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Docker container test passed")
            print(f"   Container output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Docker container failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Docker container timed out")
        return False
    except FileNotFoundError:
        print("⚠️  Docker not found - skipping Docker tests")
        return None
    except Exception as e:
        print(f"❌ Docker container error: {e}")
        return False

def cleanup_test_images():
    """Clean up test Docker images"""
    try:
        subprocess.run([
            "docker", "rmi", "qr-code-generator-test"
        ], capture_output=True, text=True)
        print("🧹 Cleaned up test Docker image")
    except:
        pass  # Ignore cleanup errors

def main():
    """Run all tests"""
    print("🚀 QR Code Generator - Test Suite")
    print("=================================")
    
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    tests_passed = 0
    tests_total = 0
    
    # Test local execution
    tests_total += 1
    if test_local_execution():
        tests_passed += 1
    
    print()
    
    # Test Docker build
    tests_total += 1
    docker_build_result = test_docker_build()
    if docker_build_result is True:
        tests_passed += 1
    elif docker_build_result is None:
        tests_total -= 1  # Don't count skipped tests
    
    print()
    
    # Test Docker run (only if build succeeded)
    if docker_build_result is True:
        tests_total += 1
        docker_run_result = test_docker_run()
        if docker_run_result is True:
            tests_passed += 1
        elif docker_run_result is None:
            tests_total -= 1
    
    # Cleanup
    cleanup_test_images()
    
    print()
    print("=" * 40)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
