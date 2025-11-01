-- Create Driver table. This table tracks driver operations (individual text pronunciations)

DROP TABLE IF EXISTS Driver CASCADE;

CREATE TABLE Driver (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    feature VARCHAR(255) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create index for better query performance
CREATE INDEX idx_driver_datetime ON Driver(datetime);
CREATE INDEX idx_driver_feature ON Driver(feature);