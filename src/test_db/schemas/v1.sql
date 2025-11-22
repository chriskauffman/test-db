CREATE TABLE address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    street TEXT,
    locality TEXT,
    region TEXT,
    postal_code TEXT,
    country TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE address_entity (
address_id INT NOT NULL,
entity_id INT NOT NULL
);
CREATE TABLE bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    routing_number TEXT,
    account_number TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE bank_account_entity (
bank_account_id INT NOT NULL,
entity_id INT NOT NULL
);
CREATE TABLE debit_card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    attributes TEXT,
    name TEXT,
    card_number VARCHAR(16),
    cvv VARCHAR(3),
    expiration_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE debit_card_entity (
debit_card_id INT NOT NULL,
entity_id INT NOT NULL
);
CREATE TABLE entity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attributes TEXT,
    description TEXT,
    phone_number TEXT,
    child_name VARCHAR(255)
);
CREATE TABLE job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    attributes TEXT,
    description TEXT,
    employee_id TEXT,
    location TEXT,
    pay_group TEXT,
    organization_id INT CONSTRAINT organization_id_exists REFERENCES organization(id) ,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE organization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    employer_identification_number TEXT NOT NULL UNIQUE,
    external_id TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    child_name VARCHAR(255)
);
CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    social_security_number VARCHAR(9) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    child_name VARCHAR(255)
);
CREATE TABLE personal_key_value_secure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    person_id INT NOT NULL CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX personal_key_value_secure_keyPersonIndex ON personal_key_value_secure (key, person_id);
