-- Database setup script for Name Pronunciation CLI
-- This script sets up the initial database configuration

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create a schema for the application (optional, but good practice)
-- CREATE SCHEMA IF NOT EXISTS name_pronunciation;
-- SET search_path TO name_pronunciation, public;

-- You may want to create a dedicated user for the application
-- CREATE USER name_pronunciation_user WITH PASSWORD 'your_password_here';
-- GRANT ALL PRIVILEGES ON DATABASE your_database_name TO name_pronunciation_user;

-- Comments
COMMENT ON EXTENSION pgcrypto IS 'Provides cryptographic functions including UUID generation';
