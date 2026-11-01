-- PostgreSQL migration script: cascade job deletes from person and organization
--
-- job.person_id and job.organization_id had no ON DELETE action, so deleting a
-- person or organization that still has jobs failed. Deleting either now also
-- deletes its jobs.

BEGIN;

ALTER TABLE job DROP CONSTRAINT IF EXISTS organization_id_exists;
ALTER TABLE job DROP CONSTRAINT IF EXISTS person_id_exists;

ALTER TABLE job ADD CONSTRAINT organization_id_exists
    FOREIGN KEY (organization_id) REFERENCES organization (id) ON DELETE CASCADE;
ALTER TABLE job ADD CONSTRAINT person_id_exists
    FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE;

COMMIT;
