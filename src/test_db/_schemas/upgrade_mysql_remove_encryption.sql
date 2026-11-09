-- MySQL / MariaDB migration script for test-db databases created before issue #153.
--
-- person_secure_key_value stores encrypted values that the current release
-- cannot read. Dropping it is intentionally destructive to those values.
-- MySQL commits DDL implicitly, so this script is not wrapped in a transaction.

ALTER TABLE job DROP FOREIGN KEY job_organization_id_exists;
ALTER TABLE job DROP FOREIGN KEY job_person_id_exists;

ALTER TABLE job ADD CONSTRAINT job_organization_id_exists
    FOREIGN KEY (organization_id) REFERENCES organization (id) ON DELETE CASCADE;
ALTER TABLE job ADD CONSTRAINT job_person_id_exists
    FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE;

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
