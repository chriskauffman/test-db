/*
Reset MySQL/MariaDB database and user for testing environment

Example usage:
mariadb -u root -h nas02 -p < reset_mysql.sql

*/

DROP DATABASE IF EXISTS test_db;
-- DROP USER IF EXISTS test_db;
-- CREATE USER test_db;
CREATE DATABASE test_db;
GRANT ALL PRIVILEGES ON test_db.* TO test_db;
FLUSH PRIVILEGES;
