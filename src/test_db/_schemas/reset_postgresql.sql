/*
Reset PostgreSQL database and user for testing environment

Example usage:
psql -h nas02 -U postgres -f reset_postgresql.sql

*/

DROP DATABASE IF EXISTS test_db;
-- DROP USER IF EXISTS test_db;
-- CREATE USER test_db;
CREATE DATABASE test_db OWNER test_db;
GRANT ALL PRIVILEGES ON DATABASE test_db TO test_db;
GRANT ALL ON SCHEMA public TO test_db;
