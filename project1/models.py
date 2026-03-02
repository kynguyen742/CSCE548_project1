from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Vendor:
    vendor_id: Optional[int]
    name: str
    website: str | None = None


@dataclass
class Product:
    product_id: Optional[int]
    vendor_id: int
    name: str
    version: str | None = None
    platform: str | None = None

@dataclass
class Vulnerability:
    vuln_id: Optional[int]
    product_id: int
    cve_id: str
    title: str
    description: str
    severity: str
    cvss: float
    published_date: date
    status: str

@dataclass
class VulnerabilityReference:
    ref_id: Optional[int]
    vuln_id: int
    ref_type: str
    url: str
    note: str | None = None


@dataclass
class Tag:
    tag_id: Optional[int]
    name: str


@dataclass
class VulnerabilityTag:
    vuln_id: int
    tag_id: int