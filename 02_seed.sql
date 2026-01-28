USE vuln_db;

-- Vendors
INSERT INTO vendors (name, website) VALUES
('Microsoft', 'https://www.microsoft.com'),
('Apple', 'https://www.apple.com'),
('Google', 'https://www.google.com'),
('Adobe', 'https://www.adobe.com'),
('Cisco', 'https://www.cisco.com');

-- Products
INSERT INTO products (vendor_id, name, version, platform) VALUES
(1, 'Windows 11', '23H2', 'Windows'),
(1, 'Windows Server', '2022', 'Windows'),
(2, 'iOS', '17.x', 'Mobile'),
(2, 'macOS', '14.x', 'Desktop'),
(3, 'Chrome', 'Latest', 'Cross-platform'),
(4, 'Acrobat Reader', '2024', 'Cross-platform'),
(5, 'IOS XE', '17.x', 'Network');

-- Tags
INSERT INTO tags (name) VALUES
('RCE'), ('Privilege Escalation'), ('XSS'), ('SQLi'), ('Auth Bypass'),
('DoS'), ('Info Disclosure'), ('Supply Chain'), ('Zero-day'), ('Patch Available');

-- 50 vulnerabilities (generated quickly with repetitive but valid test data)
-- Note: CVE IDs here are "mock" format for class; your instructor usually accepts test data.
INSERT INTO vulnerabilities (product_id, cve_id, title, description, severity, cvss, published_date, status)
SELECT
  p.product_id,
  CONCAT('CVE-2026-', LPAD(seq.n, 5, '0')) AS cve_id,
  CONCAT('Test Vulnerability #', seq.n, ' in ', p.name) AS title,
  CONCAT('This is seeded test data for vulnerability #', seq.n, '.'),
  CASE
    WHEN seq.n % 10 = 0 THEN 'CRITICAL'
    WHEN seq.n % 3 = 0 THEN 'HIGH'
    WHEN seq.n % 2 = 0 THEN 'MEDIUM'
    ELSE 'LOW'
  END AS severity,
  CASE
    WHEN seq.n % 10 = 0 THEN 9.8
    WHEN seq.n % 3 = 0 THEN 8.1
    WHEN seq.n % 2 = 0 THEN 5.4
    ELSE 3.1
  END AS cvss,
  DATE_SUB(CURDATE(), INTERVAL (seq.n % 365) DAY) AS published_date,
  CASE
    WHEN seq.n % 4 = 0 THEN 'PATCHED'
    WHEN seq.n % 7 = 0 THEN 'MITIGATED'
    ELSE 'OPEN'
  END AS status
FROM
  (SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
   UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
   UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
   UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
   UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25
   UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
   UNION SELECT 31 UNION SELECT 32 UNION SELECT 33 UNION SELECT 34 UNION SELECT 35
   UNION SELECT 36 UNION SELECT 37 UNION SELECT 38 UNION SELECT 39 UNION SELECT 40
   UNION SELECT 41 UNION SELECT 42 UNION SELECT 43 UNION SELECT 44 UNION SELECT 45
   UNION SELECT 46 UNION SELECT 47 UNION SELECT 48 UNION SELECT 49 UNION SELECT 50
  ) AS seq
JOIN products p
  ON p.product_id = ((seq.n - 1) % 7) + 1;

-- Add 1 reference per vulnerability (50 rows)
INSERT INTO vuln_references (vuln_id, ref_type, url, note)
SELECT
  v.vuln_id,
  'NEWS',
  CONCAT('https://example.com/news/', v.cve_id),
  'Seeded reference link'
FROM vulnerabilities v;

-- Tag each vulnerability with 2 tags (100 rows in join table)
INSERT INTO vulnerability_tags (vuln_id, tag_id)
SELECT v.vuln_id,
       CASE WHEN v.vuln_id % 2 = 0 THEN 1 ELSE 2 END AS tag_id
FROM vulnerabilities v;

INSERT INTO vulnerability_tags (vuln_id, tag_id)
SELECT v.vuln_id,
       CASE WHEN v.vuln_id % 3 = 0 THEN 10 ELSE 6 END AS tag_id
FROM vulnerabilities v;
