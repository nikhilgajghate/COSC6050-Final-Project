# G2I - Quick Start Guide for Developers

This guide will get you up and running with the G2I Name Pronunciation application in under 5 minutes.

## Prerequisites

- Python 3.7+
- PostgreSQL 12+ (optional, but recommended)
- ElevenLabs API key (required for pronunciation)

## Setup Steps

### 1. Clone and Install Dependencies

```bash
# Clone the repository (if not already done)
cd COSC6050-Final-Project

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
DB_PASSWORD=your_password_here
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

**Note:** If you skip this step, the Flask backend will still work but won't log operations to the database.

### 4. Run the Flask Backend

```bash
cd src/Backend
python app.py
```

You should see:
```
✅ Database connection established
 * Running on http://127.0.0.1:5000
```

### 5. Test the Application

Open your browser to: http://localhost:5000

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
