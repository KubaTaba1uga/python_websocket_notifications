from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .env import get_env_var

username = get_env_var("POSTGRES_USER")
password = get_env_var("POSTGRES_PASSWORD")
db = get_env_var("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@database/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
