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
│   ├── database_manager.py        # Database operations layer (PostgreSQL)
│   ├── Backend/
│   │   ├── app.py                 # Flask server (main API endpoints)
│   │   ├── service.py             # Audio generation service (ElevenLabs)
│   │   └── databridge.py          # Database connection bridge
│   └── Frontend/
│       ├── templates/
│       │   └── index.html         # Main UI (Bootstrap 5)
│       └── static/
│           ├── assets/            # CSS, JS, images, vendor libraries
│           └── uploads/           # Uploaded CSV files
├── database/
│   ├── 00_setup_database.sql      # Database initialization
│   ├── 01_create_driver_table.sql # Session tracking table
│   ├── 02_create_single_table.sql # Individual name requests
│   ├── 03_create_csv_upload_table.sql # CSV upload tracking
│   ├── create_all_tables.sql      # Combined table creation
│   ├── drop_all_tables.sql        # Database reset
│   ├── README.md                  # Database documentation
│   └── SCHEMA_DIAGRAM.md          # ER diagram and schema details
├── .env                           # Environment configuration (create this)
└── requirements.txt               # Python dependencies
```
