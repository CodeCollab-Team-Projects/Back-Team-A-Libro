from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


MYSQL_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/python_db"

engine = create_engine(MYSQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()