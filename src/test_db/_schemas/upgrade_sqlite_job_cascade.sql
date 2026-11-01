-- SQLite migration script: cascade job deletes from person and organization
--
-- job.person_id and job.organization_id had no ON DELETE action, so deleting a
-- person or organization that still has jobs failed. Deleting either now also
-- deletes its jobs. SQLite cannot alter a foreign key, so the table is rebuilt.

-- Disable foreign key constraints temporarily to prevent issues during the table swap
PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

-- 1. Create the new table with ON DELETE CASCADE on both foreign keys
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

-- 2. Copy the data from the old table into the new table
INSERT INTO job_new (
    id, g_id, description, employee_id, location, pay_group, position,
    organization_id, person_id, created_at, updated_at
)
SELECT
    id, g_id, description, employee_id, location, pay_group, position,
    organization_id, person_id, created_at, updated_at
FROM job;

-- 3. Drop the old table
DROP TABLE job;

-- 4. Rename the new table to the original table name
ALTER TABLE job_new RENAME TO job;

-- 5. Add the unique index back on the employee_id and organization_id columns
CREATE UNIQUE INDEX job_employeeIDOrganizationIndex ON job (employee_id, organization_id);

-- 6. Report any foreign key violations in the copied data
-- (rows returned here mean the data was already inconsistent; this does not abort)
PRAGMA foreign_key_check(job);

COMMIT;

-- Re-enable foreign key constraints
PRAGMA foreign_keys=on;
