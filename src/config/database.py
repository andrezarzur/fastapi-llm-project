from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.setting import Settings


engine = create_engine(Settings().DATABASE_URL, isolation_level=None)
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()
