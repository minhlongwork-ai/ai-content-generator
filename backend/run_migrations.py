import sqlite3
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ai_content_generator.db"
MIGRATIONS_DIR = BASE_DIR / "migrations"

def run_sql_file(conn, file_path):
    print(f"Running migration: {file_path.name}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # SQLite doesn't support some Postgres-specific syntax like 'SERIAL' or 'ARRAY',
    # or 'JSONB'. I need to translate them for local SQLite testing.
    sql = sql.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
    sql = sql.replace('TIMESTAMP DEFAULT NOW()', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    sql = sql.replace('DECIMAL(10,2)', 'REAL')
    sql = sql.replace('JSONB', 'JSON')
    sql = sql.replace('JSON', 'TEXT')
    sql = sql.replace('TEXT[]', 'TEXT')
    sql = sql.replace('ARRAY(Text)', 'TEXT')
    sql = sql.replace('ON DELETE CASCADE', '') # Simplify for SQLite
    sql = sql.replace('::jsonb', '')
    sql = sql.replace('E\'', '\'') # Remove Postgres escape char
    
    # Remove Postgres-specific functions/triggers if they cause errors in SQLite
    if "CREATE OR REPLACE FUNCTION" in sql:
        print(f"  Note: Skipping Postgres triggers/functions in SQLite for {file_path.name}")
        # Split by ';' and skip lines with triggers
        parts = sql.split(';')
        sql = ';'.join([p for p in parts if "FUNCTION" not in p and "TRIGGER" not in p])

    try:
        conn.executescript(sql)
        conn.commit()
        print(f"✓ {file_path.name} completed.")
    except Exception as e:
        print(f"❌ Error in {file_path.name}: {e}")

def main():
    if DB_PATH.exists():
        print(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    
    # Run migration 001
    run_sql_file(conn, MIGRATIONS_DIR / "001_add_skill_system_tables.sql")
    
    # Run migration 002
    run_sql_file(conn, MIGRATIONS_DIR / "002_add_marketplace_tables.sql")
    
    conn.close()
    print("\n✓ Migration complete! Local SQLite database ready.")

if __name__ == "__main__":
    main()
