CREATE TABLE app_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE employer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT NOT NULL UNIQUE,
    alternate_id TEXT
);
CREATE TABLE job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    employee_id TEXT,
    location TEXT,
    pay_group TEXT,
    employer_id INT CONSTRAINT employer_id_exists REFERENCES employer(id) ON DELETE CASCADE,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
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
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    street TEXT,
    locality TEXT,
    region VARCHAR(2),
    postal_code VARCHAR(5),
    country VARCHAR(2),
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_address_name_person_index ON personal_address (name, person_id);
CREATE TABLE personal_app_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_app_settings_name_person_index ON personal_app_settings (name, person_id);
CREATE TABLE personal_bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    routing_number TEXT,
    account_number TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_bank_account_name_person_index ON personal_bank_account (name, person_id);
CREATE TABLE personal_debit_card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    card_number VARCHAR(16),
    cvv VARCHAR(3),
    expiration_month VARCHAR(2),
    expiration_year VARCHAR(4),
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_debit_card_name_person_index ON personal_debit_card (name, person_id);
CREATE TABLE personal_o_auth2_token (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    gid TEXT NOT NULL UNIQUE,
    attributes TEXT,
    client_id TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    encrypted_token TEXT
);
CREATE UNIQUE INDEX personal_o_auth2_token_client_id_person_index ON personal_o_auth2_token (client_id, person_id);
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT NOT NULL UNIQUE,
    value TEXT
);
