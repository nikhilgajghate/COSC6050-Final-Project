# G2I - Quick Start Guide for Developers

This guide will get you up and running with the G2I Name Pronunciation application.

## Prerequisites

- Python
- PostgreSQL
- ElevenLabs API key (required for pronunciation)
- Behind the Names (required for origins)


## Setup Steps

### 1. Clone and Install Dependencies

```bash
# Clone the repository (if not already done)
cd COSC6050-Final-Project

# Create a Python virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Required: ElevenLabs API key for pronunciation
ELEVENLABS_API_KEY=your_api_key_here

# Optional: Database configuration (app works without this)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=name_pronunciation
DB_USER=postgres
DB_PASSWORD=your_password_here (same as password set during Postgres installations)
```

### 3. Set Up Database (Optional but Recommended)

```bash
python database/setup_database.py
```

This script will:
- Create the database if it doesn't exist
- Create all necessary tables
- Verify the setup
- Test the connection

**Note:** This is a required step in order to make the application run. If you skip this step, the application will not run.

### 4. Run the Flask Backend

```bash
python src/Backend/app.py
```

You should see:
```
Running on http://127.0.0.1:5050 (click whichever one is displayed)
```

### 5. Test the Application

Open your browser to http://127.0.0.1:5050 

Try:
1. Type a name and click "Pronounce"
2. Upload a CSV file with names

## Architecture Overview

```
COSC6050-Final-Project/
├── src/
│   ├── main.py                    # CLI version
│   ├── database_manager.py        # Database operations layer
│   ├── Backend/
│   │   ├── app.py                # Flask server (with DB integration)
│   │   └── iteration1.py         # Audio generation
│   └── Frontend/
│       ├── templates/
│       │   └── index.html        # Main UI
│       └── static/               # Assets, CSS, JS
├── database/
│   ├── setup_database.py         # Automated setup script
│   ├── reset_database.py         # Reset script
│   └── *.sql                     # SQL schema files
└── .env                          # Configuration (create this)
```
