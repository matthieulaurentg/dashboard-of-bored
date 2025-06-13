#!/usr/bin/env python3
"""
Build script for Three Card Roulette
Creates distributable packages and handles versioning
"""
import os
import sys
import subprocess
import shutil
from datetime import datetime

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def increment_version():
    """Increment version number"""
    version_file = 'version.txt'
    try:
        with open(version_file, 'r') as f:
            current_version = f.read().strip()
        
        parts = current_version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        new_version = '.'.join(parts)
        
        with open(version_file, 'w') as f:
            f.write(new_version)
        
        print(f"📈 Version updated: {current_version} → {new_version}")
        return new_version
    except Exception as e:
        print(f"❌ Version update failed: {e}")
        return None

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning build directories...")
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        try:
            if '*' in dir_pattern:
                import glob
                for path in glob.glob(dir_pattern):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
            else:
                if os.path.exists(dir_pattern):
                    shutil.rmtree(dir_pattern)
        except Exception as e:
            print(f"Warning: Could not clean {dir_pattern}: {e}")

def build_package():
    """Build the package"""
    print("📦 Building package...")
    
    # Clean previous builds
    clean_build()
    
    # Build source and wheel distributions
    commands = [
        ("python setup.py sdist bdist_wheel", "Building distributions"),
        ("python -m twine check dist/*", "Checking distributions"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    print("✅ Package built successfully!")
    print("📁 Distribution files created in 'dist/' directory")
    return True

def install_locally():
    """Install package locally for testing"""
    return run_command("pip install -e .", "Installing locally")

def create_release():
    """Create a git release"""
    # Read current version
    try:
        with open('version.txt', 'r') as f:
            version = f.read().strip()
    except:
        print("❌ Could not read version")
        return False
    
    # Git commands
    commands = [
        ("git add .", "Adding files to git"),
        (f'git commit -m "Release version {version}"', "Committing changes"),
        (f'git tag -a v{version} -m "Version {version}"', "Creating git tag"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    print(f"🏷️ Release v{version} created!")
    print("💡 To publish: git push origin main --tags")
    return True

def main():
    """Main build process"""
    print("🚀 Three Card Roulette Build Script")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        print("Available commands:")
        print("  build     - Build package only")
        print("  release   - Increment version, build, and create git release")
        print("  install   - Install locally for testing")
        print("  clean     - Clean build artifacts")
        command = input("Enter command: ").lower()
    
    if command == "clean":
        clean_build()
    elif command == "build":
        build_package()
    elif command == "install":
        if build_package():
            install_locally()
    elif command == "release":
        new_version = increment_version()
        if new_version and build_package():
            create_release()
            print(f"🎉 Release {new_version} is ready!")
    else:
        print("❌ Unknown command")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())