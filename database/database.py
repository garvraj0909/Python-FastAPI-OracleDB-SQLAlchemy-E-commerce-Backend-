'''
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from the project's .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE_NAME = os.getenv("DB_SERVICE_NAME", "FREEPDB1")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_USER or not DB_PASSWORD:
    raise ValueError("DB_USER and DB_PASSWORD must be set in .env")

DATABASE_URL = (
    f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.exec_driver_sql("SELECT 1 FROM DUAL")
            print("Oracle database connection successful!")
            print("Test query result:", result.scalar())
    except Exception as e:
        print("Oracle database connection failed!")
        print(f"{type(e).__name__}: {e}")
'''



import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DIALECT = os.getenv("DIALECT", "").strip().lower()


def get_required_env(name):
    value = os.getenv(name)
    if not value or not value.strip():
        raise ValueError(f"Missing environment variable: {name}")
    return value.strip()


DB_HOST = get_required_env("DB_HOST")
DB_PORT = get_required_env("DB_PORT")
DB_USER = get_required_env("DB_USER")
DB_PASSWORD = get_required_env("DB_PASSWORD")

if DIALECT == "oracle":
    DB_SERVICE_NAME = get_required_env("DB_SERVICE_NAME")

    DATABASE_URL = (
        f"oracle+oracledb://{quote_plus(DB_USER)}:"
        f"{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/"
        f"?service_name={DB_SERVICE_NAME}"
    )

elif DIALECT == "postgres":
    DB_NAME = get_required_env("DB_NAME")

    DATABASE_URL = (
        f"postgresql+psycopg://{quote_plus(DB_USER)}:"
        f"{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

else:
    raise ValueError(
        "Invalid DIALECT. Set DIALECT=oracle or DIALECT=postgres."
    )


engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            query = (
                "SELECT 1 FROM DUAL"
                if DIALECT == "oracle"
                else "SELECT 1"
            )
            result = connection.execute(text(query))
            print(f"{DIALECT.upper()} connection successful!")
            print(f"Test query result: {result.scalar()}")

    except Exception as error:
        print(f"{DIALECT.upper()} connection failed!")
        print(f"{type(error).__name__}: {error}")

    finally:
        engine.dispose()
