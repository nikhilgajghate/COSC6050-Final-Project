# Database Setup Guide

This directory contains SQL scripts to set up the PostgreSQL database for the Name Pronunciation CLI application.

### 1. Driver Table (Parent)
- **Purpose**: Tracks all operations (both single text and CSV uploads)
- **Columns**:
  - `id` (UUID): Primary key, auto-generated
  - `feature` (VARCHAR): Type of operation ('single_text' or 'csv_upload')
  - `datetime` (TIMESTAMP): When the operation occurred

### 2. Single Table (Child)
- **Purpose**: Stores detailed data for single text input operations
- **Columns**:
  - `id` (UUID): Primary key, **foreign key to Driver.id**
  - `input` (VARCHAR): User-provided text input for pronunciation
  - `datetime` (TIMESTAMP): When the operation occurred
- **Relationship**: Each record must have a corresponding Driver record with the same ID

### 3. CSV_Upload Table (Child)
- **Purpose**: Stores detailed data for CSV file upload operations
- **Columns**:
  - `id` (UUID): Primary key, **foreign key to Driver.id**
  - `filename` (VARCHAR): Name of the uploaded CSV file
  - `contents` (JSONB): JSON representation of CSV file contents
  - `datetime` (TIMESTAMP): When the upload occurred
- **Relationship**: Each record must have a corresponding Driver record with the same ID

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install PostgreSQL
Make sure PostgreSQL is installed. 

You can do so by navigating to your command line interface and entering `psql` and entering your password at the User level. 

### 3. Create Database
I'd recommend creating the database using the DBeaver user interface for ease. 

### 4. Run Setup Scripts
After you create the database, navigate to your IDE to run the scripts to create the tables in two ways:

#### Option A: Run Master Script (Recommended)
```bash
cd database/
psql -U postgres -d name_pronunciation -f create_all_tables.sql
```

#### Option B: Run Individual Scripts in Order
```bash
cd database/
psql -U postgres -d name_pronunciation -f 00_setup_database.sql
psql -U postgres -d name_pronunciation -f 01_create_driver_table.sql
psql -U postgres -d name_pronunciation -f 02_create_single_table.sql
psql -U postgres -d name_pronunciation -f 03_create_csv_upload_table.sql
```

### 4. Configure Environment Variables

Create a `.env` file in the **project root** directory with the following:

```env
# ElevenLabs API (Required for pronunciation)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Database Configuration (Required for database logging)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=name_pronunciation
DB_USER=postgres
DB_PASSWORD=<this should be the password you entered when installing Postgres>
```

**Important Notes:**
- Never commit `.env` file to version control
- The Flask backend will work **without** database configured (it will just skip logging)
- Database is optional but recommended for tracking usage

## 🏃 Running the Application

### With Database (Recommended)

```bash
# 1. Set up database
Follow the above steps to set up the database

# 2. Start Flask backend
cd src/Backend
python app.py

# 3. Open browser to http://localhost:5000
```

### SQL Scripts
- `00_setup_database.sql` - Initial database setup and extensions
- `01_create_driver_table.sql` - Creates the Driver table (parent)
- `02_create_single_table.sql` - Creates the Single table (child) with FK to Driver
- `03_create_csv_upload_table.sql` - Creates the CSV_Upload table (child) with FK to Driver
- `create_all_tables.sql` - Master script that runs all setup scripts in order
- `drop_all_tables.sql` - Drops all tables (useful for starting fresh)
- `README.md` - This documentation file

## 🧪 Testing the Setup

After running the setup scripts, you can test in multiple ways:

### 1. Direct Python Test
```bash
python src/database_manager.py
```

### 2. Flask API Health Check
```bash
# Start Flask app
cd src/Backend && python app.py

# In another terminal
curl http://localhost:5000/api/health
```

Expected output:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 3. Use the Application
1. Start Flask: `python src/Backend/app.py`
2. Open browser: http://localhost:5000
3. Pronounce a name or upload CSV
4. Check database logs in console
