import os
import subprocess
import sys


def check_dependency(command, install_instruction):
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print(f"Missing dependency. Please install it using: {install_instruction}")
        return False


# Create GitHub Actions Workflow YAML
def create_github_actions_workflow(folder):
    github_folder = os.path.join(folder, ".github", "workflows")
    os.makedirs(github_folder, exist_ok=True)
    with open(os.path.join(github_folder, "python_linting.yml"), "w") as f:
        f.write(
            """name: Python Linting

on:
  pull_request:
    paths:
      - '**.py'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install isort black

    - name: Run isort
      run: isort . --check

    - name: Run Black
      run: black . --check
"""
        )
    print("Created GitHub Actions Workflow")


# Create isort.cfg
def create_isort_cfg(folder):
    with open(os.path.join(folder, "isort.cfg"), "w") as f:
        f.write(
            """[settings]
profile = black
"""
        )
    print("Created isort.cfg file")


# Check for dependencies
if not check_dependency(["git", "--version"], "Install Git from https://git-scm.com/"):
    sys.exit(1)
if not check_dependency(
    ["virtualenv", "--version"], "Install virtualenv using: pip install virtualenv"
):
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

# Create GitHub Actions Workflow and isort.cfg
create_github_actions_workflow(os.getcwd())
create_isort_cfg(os.getcwd())

print("Project setup completed successfully!")
