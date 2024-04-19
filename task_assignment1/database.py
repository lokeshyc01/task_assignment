from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
encoded_password = urllib.parse.quote("root@123")

SQL_URL = f"mysql+mysqlconnector://root:"+encoded_password+"@localhost:3306/iacsd0923"
engine = create_engine(SQL_URL)
SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()