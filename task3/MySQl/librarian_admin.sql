GRANT USAGE ON *.* TO `librarian_admin`@`localhost` IDENTIFIED BY PASSWORD '*CC67043C7BCFF5EEA5566BD9B1F3C74FD9A5CF5D';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER ON `library\_users`.* TO `librarian_admin`@`localhost` WITH GRANT OPTION;