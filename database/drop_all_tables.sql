-- Script to drop all tables: For local development purposes.

-- Dropping in reverse order to not violate foreign key constraints.
DROP TABLE IF EXISTS CSV_Upload CASCADE;
DROP TABLE IF EXISTS Single CASCADE;
DROP TABLE IF EXISTS Driver CASCADE;


SELECT 'All tables dropped successfully!' as status;
