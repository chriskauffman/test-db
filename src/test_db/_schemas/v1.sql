CREATE TABLE key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT NOT NULL UNIQUE,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE organization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    employer_identification_number TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE organization_address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INT CONSTRAINT organization_id_exists REFERENCES organization(id) ON DELETE CASCADE,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    street TEXT,
    locality TEXT,
    region TEXT,
    postal_code TEXT,
    country TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE organization_bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INT CONSTRAINT organization_id_exists REFERENCES organization(id) ON DELETE CASCADE,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    routing_number TEXT,
    account_number TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX organization_bank_account_organizationRoutingNumberAccountNumberIndex ON organization_bank_account (organization_id, routing_number, account_number);
CREATE TABLE organization_key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INT NOT NULL CONSTRAINT organization_id_exists REFERENCES organization(id) ON DELETE CASCADE,
    key_name TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX organization_key_value_organizationKeyIndex ON organization_key_value (organization_id, key_name);
CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    description TEXT,
    date_of_birth DATE,
    social_security_number TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE person_address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    street TEXT,
    locality TEXT,
    region TEXT,
    postal_code TEXT,
    country TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE person_bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    routing_number TEXT,
    account_number TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX person_bank_account_personRoutingNumberAccountNumberIndex ON person_bank_account (person_id, routing_number, account_number);
CREATE TABLE person_debit_card (
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
CREATE UNIQUE INDEX person_debit_card_personCardNumberIndex ON person_debit_card (person_id, card_number);
CREATE TABLE person_key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INT NOT NULL CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    key_name TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX person_key_value_personKeyIndex ON person_key_value (person_id, key_name);
CREATE TABLE person_secure_key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INT NOT NULL CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    key_name TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX person_secure_key_value_personKeyIndex ON person_secure_key_value (person_id, key_name);
CREATE TABLE job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    employee_id TEXT,
    location TEXT,
    pay_group TEXT,
    position TEXT,
    organization_id INT CONSTRAINT organization_id_exists REFERENCES organization(id) ,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX job_employeeIDOrganizationIndex ON job (employee_id, organization_id);
CREATE TABLE job_key_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INT NOT NULL CONSTRAINT job_id_exists REFERENCES job(id) ON DELETE CASCADE,
    key_name TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE UNIQUE INDEX job_key_value_jobKeyIndex ON job_key_value (job_id, key_name);
