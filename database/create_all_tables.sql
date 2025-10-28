-- Master script to create all tables in the correct order
-- Run this script to set up the entire database schema

-- First, run the setup script
\i 00_setup_database.sql

-- Then create all tables in order
\i 01_create_driver_table.sql
\i 02_create_single_table.sql  
\i 03_create_csv_upload_table.sql

