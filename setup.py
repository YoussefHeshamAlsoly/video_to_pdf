import os
import sys
import subprocess

def install_req():
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            required_packages = [line.strip() for line in f if line.strip()]

        installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode().splitlines()
        
        installed_packages_set = {pkg.lower() for pkg in installed_packages}

        packages_to_install = [
            pkg for pkg in required_packages
            if pkg.lower() not in installed_packages_set
        ]

        if packages_to_install:
            try:
                # get the missing packages
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install"] + packages_to_install
                )
                print("Missing libraries installed successfully.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while trying to install libraries: {e}")
                return False
        else:
            print("All required libraries are already installed.")
            return True
    else:
        print("requirements.txt file not found.")
        return False

