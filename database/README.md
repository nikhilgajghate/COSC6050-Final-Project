# Database Setup Guide

This directory contains SQL scripts to set up the PostgreSQL database for the Name Pronunciation CLI application.

## Database Schema

The application uses three main tables with a **parent-child relationship**:

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

Edit the `.env` file with your PostgreSQL connection details:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=name_pronunciation
DB_USER=postgres
DB_PASSWORD=<this should be the password you entered when installing Postgres>
```

## File Descriptions

- `00_setup_database.sql`: Initial database setup and extensions
- `01_create_driver_table.sql`: Creates the Driver table (parent)
- `02_create_single_table.sql`: Creates the Single table (child) with FK to Driver
- `03_create_csv_upload_table.sql`: Creates the CSV_Upload table (child) with FK to Driver
- `create_all_tables.sql`: Master script that runs all setup scripts in order
- `drop_all_tables.sql`: Drops all tables (useful for starting fresh)
- `README.md`: This documentation file

## How the Relationship Works

When a user performs an operation:

1. **Single Text Operation** (Option 1):
   - Create Driver record with `feature='single_text'` → Get ID (e.g., `123`)
   - Create Single record with same ID `123` and the user's input text
   - Both records share the same UUID

2. **CSV Upload Operation** (Option 2):
   - Create Driver record with `feature='csv_upload'` → Get ID (e.g., `456`)
   - Create CSV_Upload record with same ID `456` and file details
   - Both records share the same UUID

This design allows you to:
- Query Driver table to see all operations
- Join with Single or CSV_Upload tables to get operation-specific details
- Use the `feature` column to know which child table to join

## Testing the Setup

After running the setup scripts, you can test the database connection using the Python DatabaseManager:

```bash
python src/database_manager.py
```

## Security Notes

- Never commit your `.env` file with real credentials

