from sqlalchemy import create_engine
from .base import Base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv();

PGURL = os.getenv("PGURL")

engine = create_engine(PGURL);

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
