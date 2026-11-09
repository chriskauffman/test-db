-- SQLite migration script for test-db databases created before issue #153.
--
-- person_secure_key_value stores encrypted values that the current release
-- cannot read. Dropping it is intentionally destructive to those values.

PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

CREATE TABLE job_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    g_id VARCHAR(90) NOT NULL UNIQUE,
    description TEXT,
    employee_id TEXT,
    location TEXT,
    pay_group TEXT,
    position TEXT,
    organization_id INT CONSTRAINT organization_id_exists REFERENCES organization(id) ON DELETE CASCADE,
    person_id INT CONSTRAINT person_id_exists REFERENCES person(id) ON DELETE CASCADE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

INSERT INTO job_new (
    id, g_id, description, employee_id, location, pay_group, position,
    organization_id, person_id, created_at, updated_at
)
SELECT
    id, g_id, description, employee_id, location, pay_group, position,
    organization_id, person_id, created_at, updated_at
FROM job;

DROP TABLE job;
ALTER TABLE job_new RENAME TO job;
CREATE UNIQUE INDEX job_employeeIDOrganizationIndex ON job (employee_id, organization_id);

DROP TABLE IF EXISTS person_secure_key_value;

DELETE FROM key_value
WHERE key_name IN (
    'TestDB_EncryptedPickleColSalt',
    'TestDB_EncryptedPickleColIterations',
    'TestDB_EncryptedPickleColCheck'
);

UPDATE key_value
SET value = '2'
WHERE key_name = 'TestDB_ApplicationSchemaVersion';

COMMIT;

PRAGMA foreign_keys=on;
