import os
import sys
import subprocess

def check_dependency(command, install_instruction):
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print(f"Missing dependency. Please install it using: {install_instruction}")
        return False

# Check for dependencies
if not check_dependency(["git", "--version"], "Install Git from https://git-scm.com/"):
    sys.exit(1)
if not check_dependency(["virtualenv", "--version"], "Install virtualenv using: pip install virtualenv"):
    sys.exit(1)

# Check for correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python setup_project.py <project_name>")
    sys.exit(1)

project_name = sys.argv[1]

# Create a new directory for the project
os.mkdir(project_name)
os.chdir(project_name)
print(f"Created project directory {project_name}")

# Initialize a virtual environment using virtualenv
subprocess.run(["virtualenv", "venv"])
print("Initialized virtual environment")

# Set up a Git repository within the project directory
subprocess.run(["git", "init"])
print("Initialized Git repository")

# Create necessary files
with open("README.md", "w") as f:
    f.write(f"# {project_name}\n")
print("Created README.md file")

with open(".gitignore", "w") as f:
    f.write("venv\n__pycache__\n")
print("Created .gitignore file")

with open("requirements.txt", "w") as f:
    f.write("# Add your requirements here\n")
print("Created requirements.txt file")

print("Project setup completed successfully!")
