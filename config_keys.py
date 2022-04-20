import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


user_token = os.getenv("USER_TOKEN")
bots_token = os.getenv("BOTS_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
BASE = declarative_base()
