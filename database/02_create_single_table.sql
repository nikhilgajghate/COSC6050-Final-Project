-- Create Single table
-- This table tracks single text input operations

DROP TABLE IF EXISTS Single CASCADE;

CREATE TABLE Single (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    input VARCHAR(1000) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create index for better query performance
CREATE INDEX idx_single_datetime ON Single(datetime);
CREATE INDEX idx_single_input ON Single(input);

-- Add comments for documentation
COMMENT ON TABLE Single IS 'Tracks single text input operations from users';
COMMENT ON COLUMN Single.id IS 'Unique identifier for each single operation';
COMMENT ON COLUMN Single.input IS 'User-provided text input for pronunciation';
COMMENT ON COLUMN Single.datetime IS 'Timestamp when the operation occurred';
