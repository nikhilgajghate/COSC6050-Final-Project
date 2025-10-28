-- Create Single table
-- This table tracks single text input operations
-- The id is a foreign key to Driver table

DROP TABLE IF EXISTS Single CASCADE;

CREATE TABLE Single (
    id UUID PRIMARY KEY,
    input VARCHAR(1000) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_single_driver FOREIGN KEY (id) REFERENCES Driver(id) ON DELETE CASCADE
);

-- Create index for better query performance
CREATE INDEX idx_single_datetime ON Single(datetime);
CREATE INDEX idx_single_input ON Single(input);

-- Add comments for documentation
COMMENT ON TABLE Single IS 'Tracks single text input operations from users (linked to Driver table)';
COMMENT ON COLUMN Single.id IS 'Foreign key reference to Driver.id';
COMMENT ON COLUMN Single.input IS 'User-provided text input for pronunciation';
COMMENT ON COLUMN Single.datetime IS 'Timestamp when the operation occurred';
