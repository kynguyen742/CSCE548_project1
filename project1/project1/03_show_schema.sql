-- Make sure we're using the correct database
USE vuln_db;

-- 1) Show all tables created by 01_schema.sql
SHOW TABLES;

-- 2) Show table structure (columns, types, keys)
DESCRIBE vendors;
DESCRIBE products;
DESCRIBE vulnerabilities;
DESCRIBE vuln_references;
DESCRIBE tags;
DESCRIBE vulnerability_tags;

-- 3) Show foreign key relationships (proof of relational design)
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'vuln_db'
  AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;
