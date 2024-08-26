import subprocess
import toml

# Load the Pipfile
pipfile = toml.load('Pipfile')

# Get the packages
packages = pipfile['packages'].keys()

# List to hold packages that failed to install
failed_packages = []

# Install packages one by one
for package in packages:
    print(f"Installing {package}...")
    process = subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        print(line.decode().strip())
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        failed_packages.append(package)

# Print the packages that failed to install
if failed_packages:
    print("Failed to install the following packages:")
    for package in failed_packages:
        print(package)
else:
    print("All packages installed successfully.")