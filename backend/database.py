import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("USER")
POSTGRES_PASSWORD = os.getenv("PASSWORD")
POSTGRES_HOST = os.getenv("HOST")
POSTGRES_PORT = os.getenv("PORT")
POSTGRES_DB = os.getenv("DB")

# PostgreSQL URL
postgres_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# SQLAlchemy engine
engine = create_engine(postgres_url)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
