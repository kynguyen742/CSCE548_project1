# Security Vulnerability Database

**CSCE 548 – Project 4**
Ky Nguyen

## Project Overview

This project implements a **Security Vulnerability Database** using an **n-tier architecture**. The application allows users to retrieve, insert, and update vulnerability records through a web client that communicates with a backend REST API. The backend service interacts with a MySQL database through business and data access layers.

The purpose of this project is to demonstrate the design and implementation of a full-stack application using generative AI assistance, following the architecture developed in Projects 1–3.

---

## System Architecture

The application follows a **four-layer n-tier architecture**:

Client Layer → Service Layer → Business Layer → Data Layer → Database

**Client Layer**

* Web interface used by the user to interact with the system

**Service Layer**

* REST API built with Python and Flask
* Handles HTTP requests and responses

**Business Layer**

* Contains application logic
* Validates and processes requests before interacting with the database

**Data Layer**

* Data Access Object (DAO) components
* Responsible for executing SQL queries and returning results

**Database**

* MySQL database storing vulnerability records and related data

---

## Technologies Used

* Python 3
* Flask
* MySQL
* MySQL Workbench
* HTML / CSS / JavaScript
* GitHub
* REST API architecture

---

## Repository Structure

```
.
├── business/                # Business logic layer
├── clients/                 # Client-side web interface
├── services/                # Service/API layer
├── db.py                    # Database connection configuration
├── models.py                # Data models used across the system
├── vuln_dao.py              # Data access object for vulnerabilities
├── 01_schema.sql            # Database schema creation script
├── 02_seed.sql              # Sample database seed data
├── 03_show_schema.sql       # Script to view database structure
├── requirements.txt         # Python dependencies
├── Project4_Deployment_and_System_Test.pdf
└── README.md
```

---

## Features

The application supports the following operations:

* Retrieve all vulnerabilities
* Retrieve a vulnerability by ID
* Insert a new vulnerability record
* Update an existing vulnerability
* (Optional) Delete vulnerability records

These operations are accessible through the REST API and the client interface.

---

## Setup Instructions

### 1. Download the Repository

Clone the repository or download the ZIP file from GitHub.

```
git clone <repository-url>
```

or

Download ZIP → Extract to a local folder.

---

### 2. Database Setup

Open **MySQL Workbench** and create the database using the provided scripts.

Run the following scripts in order:

1. `01_schema.sql`
   Creates the database tables.

2. `02_seed.sql`
   Inserts sample data.

3. `03_show_schema.sql` (optional)
   Displays the database structure.

Verify that tables and records were successfully created.

---

### 3. Install Python Dependencies

Create and activate a virtual environment (recommended).

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Install required packages:

```
pip install -r requirements.txt
```

---

### 4. Configure Database Connection

Open `db.py` and update the database connection settings if necessary.

Example configuration:

```
host = "localhost"
user = "root"
password = "your_password"
database = "vulnerability_db"
```

---

### 5. Start the Backend Service

Run the service layer to start the API server.

```
python app.py
```

The server should start locally at:

```
http://127.0.0.1:5000
Since it is a Flask so it is commonly run on port 5000
```

---

### 6. Launch the Client

Open the client interface located in the `clients/` folder.

You can either:

* open the HTML file directly in a browser, or
* run a simple local web server.

Example:

```
python -m http.server 8000
port for http client server
```

Then open:

```
http://127.0.0.1:8000
```

---

## Verifying Successful Setup

The system is working correctly if:

* The API server starts without errors
* The client interface loads in a browser
* Vulnerability records are displayed
* New records can be inserted
* Existing records can be updated
* Database queries reflect these changes

---

## Full System Testing

Full system testing demonstrates end-to-end functionality across all layers of the application. The following operations were tested:

* Retrieve all vulnerabilities
* Retrieve a vulnerability by ID
* Insert a new vulnerability record
* Update an existing vulnerability
* (Optional) Delete a vulnerability record

Screenshots and detailed testing procedures are included in:

**Project4_Deployment_and_System_Test.pdf**

located in the root of this repository.

---

## Author

Ky Nguyen
University of South Carolina
CSCE 548 – Software Engineering / Database Systems
