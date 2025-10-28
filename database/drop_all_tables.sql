-- Script to drop all tables (useful for starting fresh)
-- Run this if you need to recreate the database from scratch

-- Drop in reverse order due to foreign key constraints
DROP TABLE IF EXISTS CSV_Upload CASCADE;
DROP TABLE IF EXISTS Single CASCADE;
DROP TABLE IF EXISTS Driver CASCADE;


SELECT 'All tables dropped successfully!' as status;
