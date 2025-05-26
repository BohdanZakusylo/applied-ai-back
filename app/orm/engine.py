from sqlalchemy import create_engine
from .base import Base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv();

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}");

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
