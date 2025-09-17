CREATE TABLE employer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT NOT NULL UNIQUE,
    alternate_id TEXT NOT NULL UNIQUE
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    employee_id TEXT,
    location TEXT,
    pay_group TEXT,
    employer_id INT CONSTRAINT employer_id_exists REFERENCES employer(id) ON DELETE CASCADE,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE TABLE key_json (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT NOT NULL UNIQUE,
    value TEXT
);
CREATE TABLE key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT NOT NULL UNIQUE,
    value TEXT
);
CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    social_security_number VARCHAR(9) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT NOT NULL UNIQUE
);
CREATE TABLE personal_address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    street TEXT,
    locality TEXT,
    region VARCHAR(2),
    postal_code VARCHAR(5),
    country VARCHAR(2),
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_address_namePersonIndex ON personal_address (name, person_id);
CREATE TABLE personal_bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    routing_number TEXT,
    account_number TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_bank_account_namePersonIndex ON personal_bank_account (name, person_id);
CREATE TABLE personal_debit_card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    card_number VARCHAR(16),
    cvv VARCHAR(3),
    expiration_date DATE,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_debit_card_namePersonIndex ON personal_debit_card (name, person_id);
CREATE TABLE personal_key_json (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT NOT NULL UNIQUE,
    value TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_key_json_keyPersonIndex ON personal_key_json (key, person_id);
CREATE TABLE personal_key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT NOT NULL UNIQUE,
    value TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_key_value_keyPersonIndex ON personal_key_value (key, person_id);
CREATE TABLE personal_o_auth2_token (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    client_id TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    encrypted_token TEXT
);
CREATE UNIQUE INDEX personal_o_auth2_token_clientIDPersonIndex ON personal_o_auth2_token (client_id, person_id);
