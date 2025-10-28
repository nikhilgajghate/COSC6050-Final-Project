-- Create CSV_Upload table
-- This table tracks CSV file upload operations and stores the contents as JSON

DROP TABLE IF EXISTS CSV_Upload CASCADE;

CREATE TABLE CSV_Upload (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    contents JSONB NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create index for better query performance
CREATE INDEX idx_csv_upload_datetime ON CSV_Upload(datetime);
CREATE INDEX idx_csv_upload_filename ON CSV_Upload(filename);
CREATE INDEX idx_csv_upload_contents_gin ON CSV_Upload USING gin(contents);

-- Add comments for documentation
COMMENT ON TABLE CSV_Upload IS 'Tracks CSV file upload operations with stored contents';
COMMENT ON COLUMN CSV_Upload.id IS 'Unique identifier for each CSV upload operation';
COMMENT ON COLUMN CSV_Upload.filename IS 'Name of the uploaded CSV file';
COMMENT ON COLUMN CSV_Upload.contents IS 'JSON representation of CSV file contents';
COMMENT ON COLUMN CSV_Upload.datetime IS 'Timestamp when the upload occurred';
