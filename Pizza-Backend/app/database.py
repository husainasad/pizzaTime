from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# print(config.sections())

# with open('../config.ini', 'r') as f:
#     print(f.read())

db_config = config['localDB']
database_name = db_config['database_name']
username = db_config['username']
password = db_config['password']
host = db_config['url']
port = db_config['port']

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
