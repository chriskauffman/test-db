CREATE TABLE address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    street TEXT,
    locality TEXT,
    region VARCHAR(2),
    postal_code VARCHAR(5),
    country VARCHAR(2)
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE address_organization (
address_id INT NOT NULL,
organization_id INT NOT NULL
);
CREATE TABLE address_person (
address_id INT NOT NULL,
person_id INT NOT NULL
);
CREATE TABLE bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    routing_number TEXT,
    account_number TEXT
);
CREATE TABLE bank_account_organization (
bank_account_id INT NOT NULL,
organization_id INT NOT NULL
);
CREATE TABLE bank_account_person (
bank_account_id INT NOT NULL,
person_id INT NOT NULL
);
CREATE TABLE debit_card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    card_number VARCHAR(16),
    cvv VARCHAR(3),
    expiration_date DATE
);
CREATE TABLE debit_card_organization (
debit_card_id INT NOT NULL,
organization_id INT NOT NULL
);
CREATE TABLE debit_card_person (
debit_card_id INT NOT NULL,
person_id INT NOT NULL
);
CREATE TABLE job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    employee_id TEXT,
    location TEXT,
    pay_group TEXT,
    employer_id INT CONSTRAINT employer_id_exists REFERENCES organization(id) ON DELETE CASCADE,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE TABLE key_json (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT NOT NULL UNIQUE,
    value TEXT
);
CREATE TABLE key_value_secure (
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
CREATE TABLE organization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    name TEXT NOT NULL UNIQUE,
    alternate_id TEXT NOT NULL UNIQUE
);
CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    g_id TEXT NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    social_security_number VARCHAR(9) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT NOT NULL UNIQUE
);
CREATE TABLE personal_key_json (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT,
    value TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_key_json_keyPersonIndex ON personal_key_json (key, person_id);
CREATE TABLE personal_key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT,
    value TEXT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX personal_key_value_keyPersonIndex ON personal_key_value (key, person_id);
CREATE TABLE personal_key_value_secure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    key TEXT,
    person_id INT NOT NULL CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    value TEXT
);
CREATE UNIQUE INDEX personal_key_value_secure_keyPersonIndex ON personal_key_value_secure (key, person_id);
