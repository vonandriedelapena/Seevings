# Django Collaboration Setup Guide

Welcome to the project! Follow these steps to set up your local development environment.

---

## Prerequisites
Ensure you have the following installed on your system:
- **Python 3** (version 3.10 or higher recommended)  
- **Git**  
- **MySQL Server** (and MySQL Workbench or CLI access)  

---

## 1. Clone the Repository
If you haven't already, clone the project from GitHub and navigate into the root directory:

```bash
git clone https://github.com/3WokRide/Seevings.git
cd Seevings
```

---

## 2. Create and Activate the Virtual Environment
We use a virtual environment named `.venv` to isolate all project dependencies.

### A. Create Environment
Run this command from the project root:

```bash
python -m venv .venv
```

### B. Activate Environment (CRITICAL)
You must activate the environment for every new terminal session you start.

| Operating System | Command |
|------------------|----------|
| **Windows (CMD/PowerShell)** | `.\.venv\Scripts\activate` |
| **macOS / Linux** | `source .venv/bin/activate` |

> ✅ You will know it's active when `(.venv)` appears at the start of your terminal prompt.

---

## 3. Install Python Dependencies
With the virtual environment active, install all required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables (`.env`)
Your project uses a secure `.env` file for configuration (database credentials, secret key, etc.). This file is excluded from Git.

1. **Create the file**  
   Copy the provided template to create your local `.env` file:  
   - Windows:  
     ```bash
     copy .env.example .env
     ```  
   - macOS / Linux:  
     ```bash
     cp .env.example .env
     ```  

2. **Edit the file**  
   Open the newly created `.env` file.  

3. **Update credentials**  
Input your local MySQL database credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`)  

---

## 5. Initialize the Database
1. Start your local MySQL server.  
2. Manually create the empty database defined in your `.env` file (e.g., `your_local_django_db`).  

Once the database exists, run migrations to create the required tables:

```bash
python .\seevings\manage.py migrate
```

> ⚠️ If this step fails, double-check that your MySQL server is running and your `.env` credentials are correct.

---

## 6. Run the Development Server
You are ready to go! Start the server using the project's `manage.py`:

```bash
python .\seevings\manage.py runserver
```

You can now access the application at:  
👉 http://127.0.0.1:8000/

---

## 🔧 Useful Commands
- **Create Superuser (Admin Account):**
  ```bash
  python .\seevings\manage.py createsuperuser
  ```
- **Deactivate Virtual Environment:**
  ```bash
  deactivate
  ```
