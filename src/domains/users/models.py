from sqlalchemy import Column, String, Integer
from src.config.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    fantasy_name = Column("fantasy_name", String, nullable=False)
    cnpj = Column("cnpj", String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)

    def __init__(self, fantasy_name, cnpj, email, password):
        self.fantasy_name = fantasy_name
        self.cnpj = cnpj
        self.email = email
        self.password = password


Base.metadata.create_all(bind=engine)
