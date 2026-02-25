-- Disable foreign key constraints temporarily to prevent issues during the table swap
PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

-- 1. Create the new table with the updated schema (card_number is just TEXT)
CREATE TABLE person_debit_card_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    card_number TEXT,
    cvv TEXT,
    expiration_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 2. Copy the data from the old table into the new table
INSERT INTO person_debit_card_new (
    id, person_id, g_id, description, card_number, cvv, expiration_date, created_at, updated_at
)
SELECT 
    id, person_id, g_id, description, card_number, cvv, expiration_date, created_at, updated_at
FROM person_debit_card;

-- 3. Drop the old table
DROP TABLE person_debit_card;

-- 4. Rename the new table to the original table name
ALTER TABLE person_debit_card_new RENAME TO person_debit_card;

COMMIT;

-- Re-enable foreign key constraints
PRAGMA foreign_keys=on;
