from datetime import date
from vuln_dao import VulnerabilityDAO
from models import Vulnerability

dao = VulnerabilityDAO()

def print_vulns(vulns):
    for v in vulns:
        print(f"[{v.vuln_id}] {v.cve_id} | {v.severity} | CVSS {v.cvss} | {v.status} | {v.title} ({v.published_date})")

def main():
    while True:
        print("\n=== Vulnerability DB Console ===")
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
            vulns = dao.list_all(limit)
            print_vulns(vulns)

        elif choice == "2":
            vid = int(input("Vuln ID: "))
            v = dao.get_by_id(vid)
            if not v:
                print("Not found.")
            else:
                print(v)

        elif choice == "3":
            sev = input("Severity (LOW/MEDIUM/HIGH/CRITICAL): ").strip().upper()
            limit = int(input("Limit: "))
            vulns = dao.search_by_severity(sev, limit)
            print_vulns(vulns)

        elif choice == "4":
            product_id = int(input("Product ID (1-7 from seed): "))
            cve_id = input("CVE ID (e.g., CVE-2026-99999): ").strip()
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            severity = input("Severity (LOW/MEDIUM/HIGH/CRITICAL): ").strip().upper()
            cvss = float(input("CVSS (e.g., 7.5): "))
            published = input("Published date (YYYY-MM-DD): ").strip()
            status = input("Status (OPEN/PATCHED/MITIGATED): ").strip().upper()

            v = Vulnerability(
                vuln_id=None,
                product_id=product_id,
                cve_id=cve_id,
                title=title,
                description=desc,
                severity=severity,
                cvss=cvss,
                published_date=date.fromisoformat(published),
                status=status
            )
            new_id = dao.create(v)
            print(f"Created vulnerability with ID {new_id}")

        elif choice == "5":
            vid = int(input("Vuln ID: "))
            new_status = input("New Status (OPEN/PATCHED/MITIGATED): ").strip().upper()
            ok = dao.update_status(vid, new_status)
            print("Updated." if ok else "Not found / no change.")

        elif choice == "6":
            vid = int(input("Vuln ID: "))
            ok = dao.delete(vid)
            print("Deleted." if ok else "Not found.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
