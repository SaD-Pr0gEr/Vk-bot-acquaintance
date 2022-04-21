import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

USER_TOKEN = os.getenv("USER_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_ID = os.getenv("APP_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
BASE = declarative_base()
Session = sessionmaker(bind=engine)
BASE_DIR = Path(__file__).resolve().parent
