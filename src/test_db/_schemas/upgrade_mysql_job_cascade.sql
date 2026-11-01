-- MySQL / MariaDB migration script: cascade job deletes from person and organization
--
-- job.person_id and job.organization_id had no ON DELETE action, so deleting a
-- person or organization that still has jobs failed. Deleting either now also
-- deletes its jobs.
--
-- MySQL commits DDL implicitly, so this cannot be wrapped in a transaction.
-- Tested on MariaDB 13.0 only.

ALTER TABLE job DROP FOREIGN KEY job_organization_id_exists;
ALTER TABLE job DROP FOREIGN KEY job_person_id_exists;

ALTER TABLE job ADD CONSTRAINT job_organization_id_exists
    FOREIGN KEY (organization_id) REFERENCES organization (id) ON DELETE CASCADE;
ALTER TABLE job ADD CONSTRAINT job_person_id_exists
    FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE;
