import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fras.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def migrate_db():
    """Add missing columns to existing tables (SQLite + PostgreSQL compatible)."""
    insp = inspect(engine)
    tables = insp.get_table_names()

    # SQLite accepts integer 0/1 for boolean; PostgreSQL requires TRUE/FALSE literal
    is_sqlite = DATABASE_URL.startswith("sqlite")
    bool_false = "DEFAULT 0" if is_sqlite else "DEFAULT FALSE"

    migrations = {
        "users": {
            "facility_code": "VARCHAR(20)",
            "province": "VARCHAR(100)",
            "ward": "VARCHAR(100)",
            "latitude": "FLOAT",
            "longitude": "FLOAT",
            "facility_types": "VARCHAR(500)",
        },
        "assessments": {
            "latitude": "FLOAT",
            "longitude": "FLOAT",
            "is_demo": f"BOOLEAN {bool_false}",
        },
    }

    with engine.connect() as conn:
        for table_name, columns in migrations.items():
            if table_name not in tables:
                continue
            existing_cols = {c["name"] for c in insp.get_columns(table_name)}
            for col_name, col_type in columns.items():
                if col_name not in existing_cols:
                    try:
                        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                        print(f"[migrate] Added column {table_name}.{col_name}")
                    except Exception as e:
                        print(f"[migrate] WARN: Could not add {table_name}.{col_name}: {e}")
                        conn.rollback()
