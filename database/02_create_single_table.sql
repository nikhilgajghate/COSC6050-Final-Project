-- Create Single table: This table tracks single text input operations.

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
