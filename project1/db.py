# # src/db.py
# import os
# import mysql.connector

# def get_connection():
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST", "localhost"),
#         user=os.getenv("DB_USER", "root"),
#         password=os.getenv("DB_PASSWORD", ""),
#         database=os.getenv("DB_NAME", "vuln_db"),
#         port=int(os.getenv("DB_PORT", "3306")),
#     )
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="KNThresh@742",
        database="vuln_db"
    )