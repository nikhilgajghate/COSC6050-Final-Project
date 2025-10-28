# Database Setup Guide

This directory contains SQL scripts to set up the PostgreSQL database for the Name Pronunciation CLI application.

## Database Schema

The application uses three main tables:

### 1. Driver Table
- **Purpose**: Tracks individual text pronunciation operations
- **Columns**:
  - `id` (UUID): Unique identifier, auto-generated
  - `feature` (VARCHAR): Text that was converted to speech
  - `datetime` (TIMESTAMP): When the operation occurred

### 2. Single Table
- **Purpose**: Tracks single text input operations from users
- **Columns**:
  - `id` (UUID): Unique identifier, auto-generated
  - `input` (VARCHAR): User-provided text input for pronunciation
  - `datetime` (TIMESTAMP): When the operation occurred

### 3. CSV_Upload Table
- **Purpose**: Tracks CSV file upload operations with stored contents
- **Columns**:
  - `id` (UUID): Unique identifier, auto-generated
  - `filename` (VARCHAR): Name of the uploaded CSV file
  - `contents` (JSONB): JSON representation of CSV file contents
  - `datetime` (TIMESTAMP): When the upload occurred

## Setup Instructions

### 1. Install PostgreSQL
Make sure PostgreSQL is installed. You can do so by navigating to your command line interface and entering `psql` and entering your password at the User level. 

### 2. Create Database
I'd recommend creating the database using the DBeaver user interface for ease. 

### 3. Run Setup Scripts
You can run the scripts in two ways:

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
Copy `.env.template` to `.env` and update the database connection details:

```bash
cp .env.template .env
```

Edit the `.env` file with your PostgreSQL connection details:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=name_pronunciation
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## File Descriptions

- `00_setup_database.sql`: Initial database setup and extensions
- `01_create_driver_table.sql`: Creates the Driver table
- `02_create_single_table.sql`: Creates the Single table  
- `03_create_csv_upload_table.sql`: Creates the CSV_Upload table
- `create_all_tables.sql`: Master script that runs all setup scripts
- `README.md`: This documentation file

## Testing the Setup

After running the setup scripts, you can test the database connection using the Python DatabaseManager:

```python
from src.database_manager import DatabaseManager

# Test connection
db = DatabaseManager()
if db.test_connection():
    print("Database setup successful!")
    
    # View table info
    info = db.get_all_tables_info()
    print(info['summary'])
else:
    print("Database connection failed. Check your configuration.")
```

## Indexes

The tables include several indexes for optimal performance:
- Datetime indexes for time-based queries
- Text indexes for searching features/inputs
- GIN index on JSONB column for JSON queries

## Security Notes

- Never commit your `.env` file with real credentials
- Consider using connection pooling for production environments
- Use strong passwords for database users
- Regularly backup your database
