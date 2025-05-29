import importlib.util
import subprocess
import sys

def install_package(package_name):
    """Install a Python package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def check_and_install():
    """Check if 'colorama' is installed and install it if missing."""
    package_name = "colorama"
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"{package_name} not found. Installing...")
        install_package(package_name)
        print(f"{package_name} installed successfully.")
    else:
        print(f"{package_name} is already installed.")

if __name__ == "__main__":
    check_and_install()