#!/bin/bash
#
# Django Project Setup Script (setup.sh)
# Automates the creation of the virtual environment and package installation.
# -------------------------------------------------------------------------

# Define the name of the virtual environment folder
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
ENV_EXAMPLE_FILE=".env.example"
ENV_FILE=".env"

echo "========================================="
echo "🚀 Starting Django Project Setup"
echo "========================================="

# 1. Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 could not be found."
    echo "Please ensure Python 3 is installed and in your PATH."
    exit 1
fi

# 2. Create the Virtual Environment (.venv)
if [ ! -d "$VENV_DIR" ]; then
    echo "1/5: Creating virtual environment in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
else
    echo "1/5: Virtual environment directory '$VENV_DIR' already exists. Skipping creation."
fi

# Determine the path to the Python executable inside the VENV
if [ -f "$VENV_DIR/bin/python" ]; then
    PYTHON_EXEC="$VENV_DIR/bin/python" # Linux/macOS
elif [ -f "$VENV_DIR/Scripts/python.exe" ]; then
    PYTHON_EXEC="$VENV_DIR/Scripts/python.exe" # Windows
else
    echo "Error: Could not find Python executable in the virtual environment."
    exit 1
fi

# 3. Install Python Dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "2/5: Installing dependencies from '$REQUIREMENTS_FILE'..."
    # Ensure pip is up-to-date and then install packages using the VENV's pip
    $PYTHON_EXEC -m pip install --upgrade pip
    $PYTHON_EXEC -m pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Python dependencies. Check requirements.txt."
        exit 1
    fi
else
    echo "Error: '$REQUIREMENTS_FILE' not found. Cannot install dependencies."
    exit 1
fi

# 4. Create .env file from .env.example
if [ -f "$ENV_EXAMPLE_FILE" ]; then
    echo "3/5: Checking for local environment file ($ENV_FILE)..."
    if [ ! -f "$ENV_FILE" ]; then
        cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
        echo "   -> Created local '$ENV_FILE' from '$ENV_EXAMPLE_FILE'."
        echo "   -> IMPORTANT: You MUST edit '$ENV_FILE' with your actual MySQL credentials."
    else
        echo "   -> Local '$ENV_FILE' already exists. Skipping copy."
    fi
else
    echo "Warning: '$ENV_EXAMPLE_FILE' not found. Skipping .env creation."
fi

# 5. Run Initial Django Migrations (Schema Setup)
echo "4/5: Applying initial Django database migrations (Schema setup)..."
# Use the Python executable inside the VENV to run manage.py
$PYTHON_EXEC manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Migrations failed. Have you created the empty MySQL database and updated your '$ENV_FILE'?"
    exit 1
fi

# 6. Final Steps and Instructions
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo "Next Steps:"
echo "1. MANUALLY: Edit the new '$ENV_FILE' with your local MySQL DB Name, User, and Password."
echo "2. ACTIVATE: Start the virtual environment in your terminal (see instructions below)."
echo "3. RUN: Use '$PYTHON_EXEC manage.py runserver' to start the project."
echo "4. OPTIONAL: Run '$PYTHON_EXEC manage.py createsuperuser' if you need an admin account."

echo -e "\nTo activate your environment, use one of the following commands:"
echo "  - Linux/macOS: source .venv/bin/activate"
echo "  - Windows (CMD): .venv\\Scripts\\activate"
echo "  - Windows (PS): .venv\\Scripts\\Activate.ps1"
echo "  - PyCharm users: PyCharm should detect the .venv folder automatically."
