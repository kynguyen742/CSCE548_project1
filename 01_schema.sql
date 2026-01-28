DROP DATABASE IF EXISTS vuln_db;
CREATE DATABASE vuln_db;
USE vuln_db;

-- 1) vendors
CREATE TABLE vendors (
  vendor_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  website VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2) products
CREATE TABLE products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  vendor_id INT NOT NULL,
  name VARCHAR(120) NOT NULL,
  version VARCHAR(60),
  platform VARCHAR(60),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_products_vendor
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
    ON DELETE RESTRICT
);

-- 3) vulnerabilities
CREATE TABLE vulnerabilities (
  vuln_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  cve_id VARCHAR(20) UNIQUE,                 -- e.g., CVE-2026-12345
  title VARCHAR(200) NOT NULL,
  description TEXT,
  severity ENUM('LOW','MEDIUM','HIGH','CRITICAL') NOT NULL,
  cvss DECIMAL(3,1),                         -- e.g., 9.8
  published_date DATE,
  status ENUM('OPEN','PATCHED','MITIGATED') DEFAULT 'OPEN',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_vuln_product
    FOREIGN KEY (product_id) REFERENCES products(product_id)
    ON DELETE RESTRICT
);

-- 4) references (urls/articles/advisories per vulnerability)
CREATE TABLE vuln_references (
  ref_id INT AUTO_INCREMENT PRIMARY KEY,
  vuln_id INT NOT NULL,
  ref_type ENUM('ADVISORY','BLOG','POC','VENDOR','NEWS') NOT NULL,
  url VARCHAR(500) NOT NULL,
  note VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_refs_vuln
    FOREIGN KEY (vuln_id) REFERENCES vulnerabilities(vuln_id)
    ON DELETE CASCADE
);

-- 5) tags + join table (many-to-many)
CREATE TABLE tags (
  tag_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE vulnerability_tags (
  vuln_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (vuln_id, tag_id),
  CONSTRAINT fk_vt_vuln FOREIGN KEY (vuln_id) REFERENCES vulnerabilities(vuln_id) ON DELETE CASCADE,
  CONSTRAINT fk_vt_tag  FOREIGN KEY (tag_id)  REFERENCES tags(tag_id) ON DELETE CASCADE
);

-- Helpful indexes
CREATE INDEX idx_vuln_severity ON vulnerabilities(severity);
CREATE INDEX idx_vuln_published ON vulnerabilities(published_date);
CREATE INDEX idx_products_vendor ON products(vendor_id);
