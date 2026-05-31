"""Simple DB connectivity check for the project.
Run from repository root with the backend venv activated.
Usage:
    python backend/scripts/db_check.py
"""
import os
import sys

from urllib.parse import urlparse

try:
    from app.config import DATABASE_URL
except Exception:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not set. Set it in backend/.env or environment.")
    sys.exit(2)

print("Using DATABASE_URL:", DATABASE_URL)

try:
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT 1')
    print('Database connection OK')
    cur.close()
    conn.close()
    sys.exit(0)
except Exception as e:
    print('Database connection failed:')
    print(e)
    sys.exit(1)
