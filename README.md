# python-low_code
## Pre-Commit Set up for Developers
### This document provides step-by-step instructions for installing and configuring pre-commit on a Windows machine. These steps ensure that code is properly linted, formatted etc. before being committed to a remote branch.
# 1. Open Command Prompt
### •	Start by opening the Command Prompt (CMD) on your VDI machine
# 2. Install Python
### •	Install python on your machine.
# 3. Navigate to Your Repository
### •	Use the dir command to navigate to the directory where your repository is cloned.
# 4. Set Up a Virtual Environment
### •	Install the virtual environment package by running
#### pip install virtualenv
### •	Create a new virtual environment in a directory named .venv:
#### python -m virtualenv .venv
# 5. Activate the Virtual Environment
#### •	Activate the virtual environment with the following command:
#### .venv/Scripts/activate OR .\.venv\Scripts\activate
# 6. Install Pre-Commit
#### •	Install pre-commit in your virtual environment:
pip install pre-commit
7. Verify the Virtual Environment
•	From your current directory, run dir to confirm that the .venv folder exists. This directory contains the virtual environment.
•	Change to the .venv directory:
cd .venv
•	From this location, run dir to check for the Scripts folder. This folder contains executables for the virtual environment.
•	Change to the Scripts directory:
cd Scripts
•	Inside the Scripts folder, you should find the pre-commit.exe binary file
8. Install Pre-Commit Hooks
•	While inside the Scripts directory, install the pre-commit hooks by running:
pre-commit.exe install
9. Run Pre-Commit Checks
•	To run pre-commit on all files in the repository, use:
pre-commit run --all-files
The initial run might take longer, but subsequent runs will be faster. After setup, pre-commit will automatically run every time you execute a git commit.
10. Add Pre-Commit Configuration
•	Use the below pre-commit-config.yaml in your project root directory before installing pre-commit hooks.
 
It should also be noted that in the CI process, linting/pre-commit is also added as Job. This ensures that the codes cannot be merged to higher branches through PR incase the users do not perform pre-commit locally.
