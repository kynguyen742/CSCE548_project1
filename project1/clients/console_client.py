# src/client/console_client.py
from __future__ import annotations

from datetime import date
import requests

BASE_URL = "http://127.0.0.1:5000"


def print_vulns(vulns):
    for v in vulns:
        print(f"[{v['vuln_id']}] {v['cve_id']} | {v['severity']} | CVSS {v['cvss']} | {v['status']} | {v['title']} ({v['published_date']})")


def main():
    while True:
        print("\n=== Vulnerability Service Client ===")
        print("1) List latest vulnerabilities")
        print("2) Get vulnerability by ID")
        print("3) Search by severity")
        print("4) Add vulnerability")
        print("5) Update vulnerability status")
        print("6) Delete vulnerability")
        print("0) Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            limit = int(input("Limit (e.g., 10): "))
            r = requests.get(f"{BASE_URL}/vulnerabilities", params={"limit": limit}, timeout=10)
            r.raise_for_status()
            print_vulns(r.json())

        elif choice == "2":
            vid = int(input("Vuln ID: "))
            r = requests.get(f"{BASE_URL}/vulnerabilities/{vid}", timeout=10)
            if r.status_code == 404:
                print("Not found.")
            else:
                r.raise_for_status()
                print(r.json())

        elif choice == "3":
            sev = input("Severity (LOW/MEDIUM/HIGH/CRITICAL): ").strip().upper()
            limit = int(input("Limit: "))
            r = requests.get(f"{BASE_URL}/vulnerabilities/search", params={"severity": sev, "limit": limit}, timeout=10)
            if r.status_code == 400:
                print("Error:", r.json().get("error"))
            else:
                r.raise_for_status()
                print_vulns(r.json())

        elif choice == "4":
            product_id = int(input("Product ID: "))
            cve_id = input("CVE ID (e.g., CVE-2026-99999): ").strip()
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            severity = input("Severity (LOW/MEDIUM/HIGH/CRITICAL): ").strip().upper()
            cvss = float(input("CVSS (e.g., 7.5): "))
            published = input("Published date (YYYY-MM-DD): ").strip()
            status = input("Status (OPEN/PATCHED/MITIGATED): ").strip().upper()

            payload = {
                "product_id": product_id,
                "cve_id": cve_id,
                "title": title,
                "description": desc,
                "severity": severity,
                "cvss": cvss,
                "published_date": published,
                "status": status,
            }

            r = requests.post(f"{BASE_URL}/vulnerabilities", json=payload, timeout=10)
            if r.status_code >= 400:
                print("Error:", r.json().get("error"))
            else:
                print("Created:", r.json())

        elif choice == "5":
            vid = int(input("Vuln ID: "))
            new_status = input("New Status (OPEN/PATCHED/MITIGATED): ").strip().upper()
            r = requests.patch(f"{BASE_URL}/vulnerabilities/{vid}/status", json={"status": new_status}, timeout=10)
            if r.status_code >= 400:
                try:
                    print("Error:", r.json().get("error"))
                except Exception:
                    print("Error:", r.text)
            else:
                print("Updated.")

        elif choice == "6":
            vid = int(input("Vuln ID: "))
            r = requests.delete(f"{BASE_URL}/vulnerabilities/{vid}", timeout=10)
            if r.status_code == 404:
                print("Not found.")
            else:
                r.raise_for_status()
                print("Deleted.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()